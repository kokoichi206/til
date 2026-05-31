"use client";

import dynamic from "next/dynamic";
import { useEffect, useMemo, useState } from "react";

import { useRoundTrip } from "@/client/hooks/useRoundTrip";
import type { LngLat } from "@/shared/types/round-trip";

const MapView = dynamic(() => import("@/client/components/MapView"), {
  ssr: false,
  loading: () => (
    <div className="flex h-full w-full items-center justify-center bg-slate-100 text-slate-500">
      地図を読み込み中…
    </div>
  ),
});

interface Preset {
  label: string;
  lat: number;
  lng: number;
}

const PRESETS: Preset[] = [
  { label: "東京駅", lat: 35.681, lng: 139.767 },
  { label: "京都駅", lat: 34.985, lng: 135.758 },
  { label: "セントラルパーク(NY)", lat: 40.7829, lng: -73.9654 },
  { label: "カーディフ(英)", lat: 51.4816, lng: -3.1791 },
];

const HOME_KEY = "flrt:home";

interface HomeLocation {
  lat: number;
  lng: number;
}

// 経路の「形を決める点」を最大 k 個選ぶ（Ramer–Douglas–Peucker の貪欲版）。
// 等間隔サンプルより曲がり角を残せるため、Google の再探索でも本来の道を辿りやすい。
function simplifyToK(path: LngLat[], k: number): LngLat[] {
  const n = path.length;
  if (n <= k) return path;
  // 緯度経度を近似的に平面化（perpendicular 距離計算用）。
  const latRef = (path[0]![1] * Math.PI) / 180;
  const proj = ([lng, lat]: LngLat): [number, number] => [
    lng * Math.cos(latRef) * 111_320,
    lat * 111_320,
  ];
  const pts = path.map(proj);
  const perp = (i: number, a: number, b: number): number => {
    const [px, py] = pts[i]!;
    const [ax, ay] = pts[a]!;
    const [bx, by] = pts[b]!;
    const dx = bx - ax;
    const dy = by - ay;
    const len2 = dx * dx + dy * dy;
    if (len2 === 0) return Math.hypot(px - ax, py - ay);
    const t = ((px - ax) * dx + (py - ay) * dy) / len2;
    const cx = ax + t * dx;
    const cy = ay + t * dy;
    return Math.hypot(px - cx, py - cy);
  };
  const keep = new Set<number>([0, n - 1]);
  while (keep.size < k) {
    const sorted = [...keep].sort((a, b) => a - b);
    let bestIdx = -1;
    let bestDist = -1;
    for (let s = 0; s + 1 < sorted.length; s++) {
      const a = sorted[s]!;
      const b = sorted[s + 1]!;
      for (let i = a + 1; i < b; i++) {
        const d = perp(i, a, b);
        if (d > bestDist) {
          bestDist = d;
          bestIdx = i;
        }
      }
    }
    if (bestIdx < 0) break;
    keep.add(bestIdx);
  }
  return [...keep].sort((a, b) => a - b).map((i) => path[i]!);
}

/**
 * 計算した周回路を Google マップ（経路モード・徒歩）で開く URL を作る。
 * Maps URLs はキー不要だが waypoint は実用上 ~9 個まで。
 * 「曲がり角」を優先選択(simplifyToK)して渡すことで再探索の精度を上げる。
 * それでも Google が点間を自前データで補うため「近似」になる（完全一致は GPX で）。
 */
function googleMapsDirUrl(start: LngLat, path: LngLat[], maxWaypoints = 9): string {
  const ll = ([lngV, latV]: LngLat) => `${latV.toFixed(6)},${lngV.toFixed(6)}`;
  const origin = ll(start);
  // 始点・終点(=start)を含めて簡約し、中間の形状点だけ waypoint にする。
  const shape = simplifyToK(path, maxWaypoints + 2);
  const picks = shape.slice(1, -1);
  const waypoints = picks.map(ll).join("|");
  const params = new URLSearchParams({
    api: "1",
    origin,
    destination: origin, // 周回路なので始点に戻る
    travelmode: "walking",
  });
  // waypoints は URLSearchParams だと | が %7C になる。Google はどちらも解釈する。
  const wp = waypoints ? `&waypoints=${encodeURIComponent(waypoints)}` : "";
  return `https://www.google.com/maps/dir/?${params.toString()}${wp}`;
}

const escapeXml = (s: string): string =>
  s.replace(/[<>&'"]/g, (c) =>
    ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", "'": "&apos;", '"': "&quot;" })[c]!,
  );

/** 経路を GPX(トラック) 文字列にする。全点をそのまま出力＝正確な経路。 */
function toGpx(path: LngLat[], name: string): string {
  const pts = path
    .map(([lng, lat]) => `<trkpt lat="${lat.toFixed(6)}" lon="${lng.toFixed(6)}"/>`)
    .join("");
  return (
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<gpx version="1.1" creator="Running Planner" xmlns="http://www.topografix.com/GPX/1/1">` +
    `<trk><name>${escapeXml(name)}</name><trkseg>${pts}</trkseg></trk></gpx>`
  );
}

/** GPX をダウンロードさせる。 */
function downloadGpx(path: LngLat[], name: string): void {
  const blob = new Blob([toGpx(path, name)], { type: "application/gpx+xml" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${name}.gpx`;
  a.click();
  URL.revokeObjectURL(url);
}

/**
 * GPX をスマホの共有シートに出す（Web Share API）。OsmAnd/Komoot/AirDrop 等へ直接渡せる。
 * 共有が使えない環境（多くの PC）ではダウンロードにフォールバック。
 */
async function shareGpx(path: LngLat[], name: string): Promise<void> {
  const file = new File([toGpx(path, name)], `${name}.gpx`, {
    type: "application/gpx+xml",
  });
  if (typeof navigator.canShare === "function" && navigator.canShare({ files: [file] })) {
    try {
      await navigator.share({ files: [file], title: name, text: "ランニングコース(GPX)" });
      return;
    } catch (err) {
      // ユーザーがキャンセルした場合は何もしない。それ以外は保存にフォールバック。
      if (err instanceof DOMException && err.name === "AbortError") return;
    }
  }
  downloadGpx(path, name);
}

export function RoundTripPlanner(): React.JSX.Element {
  const [lat, setLat] = useState(35.681);
  const [lng, setLng] = useState(139.767);
  const [targetKm, setTargetKm] = useState(3);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [locating, setLocating] = useState(false);
  const [geoError, setGeoError] = useState<string | null>(null);
  const [geoNote, setGeoNote] = useState<string | null>(null);
  const [home, setHome] = useState<HomeLocation | null>(null);
  const [homeNote, setHomeNote] = useState<string | null>(null);

  const { state, run } = useRoundTrip();

  useEffect(() => {
    if (state.status === "success") setSelectedId(state.result.recommendedId);
  }, [state]);

  // 保存済みの自宅を localStorage から読み込む（クライアントのみ）。
  useEffect(() => {
    try {
      const raw = localStorage.getItem(HOME_KEY);
      if (!raw) return;
      const parsed: unknown = JSON.parse(raw);
      if (
        typeof parsed === "object" &&
        parsed !== null &&
        typeof (parsed as HomeLocation).lat === "number" &&
        typeof (parsed as HomeLocation).lng === "number"
      ) {
        setHome({
          lat: (parsed as HomeLocation).lat,
          lng: (parsed as HomeLocation).lng,
        });
      }
    } catch {
      // localStorage 不可（プライベートモード等）。自宅機能は無効になるが他は動作継続。
    }
  }, []);

  const saveHome = () => {
    const h: HomeLocation = { lat, lng };
    try {
      localStorage.setItem(HOME_KEY, JSON.stringify(h));
      setHome(h);
      setHomeNote(`自宅を登録しました（${lat.toFixed(5)}, ${lng.toFixed(5)}）。`);
    } catch {
      setHomeNote("自宅を保存できませんでした（ブラウザの保存機能が無効です）。");
    }
  };

  const useHome = () => {
    if (!home) return;
    setLat(home.lat);
    setLng(home.lng);
    setGeoError(null);
    setGeoNote(null);
  };

  const clearHome = () => {
    try {
      localStorage.removeItem(HOME_KEY);
    } catch {
      // 解除はベストエフォート。状態だけは確実にクリアする。
    }
    setHome(null);
    setHomeNote("自宅の登録を解除しました。");
  };

  const result = state.status === "success" ? state.result : null;

  const mapStart: LngLat | null = useMemo(() => {
    if (result) return result.start;
    return [lng, lat];
  }, [result, lat, lng]);

  const candidates = result?.candidates ?? [];

  const onSubmit = () => {
    // ランニング用途のため徒歩(walk)固定。
    void run({ lat, lng, targetMeters: Math.round(targetKm * 1000), profile: "walk" });
  };

  const getPosition = (options: PositionOptions) =>
    new Promise<GeolocationPosition>((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject, options);
    });

  // IP ベースの概算現在地（サーバー経由）。ブラウザ測位が使えない環境の代替。
  const locateByIp = async (): Promise<boolean> => {
    try {
      const res = await fetch("/api/geo-ip");
      const j = await res.json();
      if (!res.ok) {
        setGeoError(j?.error ?? "IP からの現在地取得に失敗しました。");
        return false;
      }
      setLat(Number(Number(j.lat).toFixed(6)));
      setLng(Number(Number(j.lng).toFixed(6)));
      setGeoNote(
        `概算現在地(IP${j.city ? ` / ${j.city}` : ""})を使用しました。精度は都市レベルです。地図クリックで微調整できます。`,
      );
      return true;
    } catch (err) {
      setGeoError(
        err instanceof Error
          ? `IP からの現在地取得に失敗: ${err.message}`
          : "IP からの現在地取得に失敗しました。",
      );
      return false;
    }
  };

  const useCurrentLocation = async () => {
    setLocating(true);
    setGeoError(null);
    setGeoNote(null);
    try {
      // まずブラウザ測位を 1 回だけ試す（始点は道路へスナップするため低精度で十分）。
      if ("geolocation" in navigator) {
        try {
          const pos = await getPosition({
            enableHighAccuracy: false,
            timeout: 7000,
            maximumAge: 600_000,
          });
          setLat(Number(pos.coords.latitude.toFixed(6)));
          setLng(Number(pos.coords.longitude.toFixed(6)));
          return;
        } catch (err) {
          const e = err as GeolocationPositionError;
          // 許可拒否はユーザー操作が必要なので IP に進まず明示する。
          if (e.code === e.PERMISSION_DENIED) {
            setGeoError(
              "位置情報の利用が拒否されました。ブラウザ/OS の許可設定を確認してください。",
            );
            return;
          }
          // 取得不能・タイムアウト（macOS の kCLErrorLocationUnknown 等）→ IP 概算へ。
        }
      }
      await locateByIp();
    } finally {
      setLocating(false);
    }
  };

  return (
    <div className="flex h-[calc(100dvh-3rem)] w-full flex-col md:flex-row">
      <aside className="flex w-full flex-col gap-4 overflow-y-auto border-b border-slate-200 bg-white p-4 md:w-[380px] md:border-r md:border-b-0">
        <header>
          <h1 className="text-lg font-bold text-slate-900">
            Fixed-Length Round Trip
          </h1>
          <p className="mt-1 text-xs leading-relaxed text-slate-500">
            目標距離の周回路を生成します（Lewis &amp; Corcoran 2024 の等時線多角形法
            + パレート局所探索 / OpenStreetMap データ）。
          </p>
        </header>

        <section className="flex flex-col gap-3">
          <div>
            <label className="text-xs font-semibold text-slate-700">プリセット</label>
            <div className="mt-1 flex flex-wrap gap-1.5">
              {home && (
                <button
                  type="button"
                  onClick={useHome}
                  className="rounded border border-emerald-400 bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-700 hover:bg-emerald-100"
                >
                  🏠 自宅
                </button>
              )}
              {PRESETS.map((p) => (
                <button
                  key={p.label}
                  type="button"
                  onClick={() => {
                    setLat(p.lat);
                    setLng(p.lng);
                  }}
                  className="rounded border border-slate-300 px-2 py-1 text-xs text-slate-700 hover:bg-slate-100"
                >
                  {p.label}
                </button>
              ))}
            </div>
          </div>

          <div>
            <button
              type="button"
              onClick={() => void useCurrentLocation()}
              disabled={locating}
              className="flex w-full items-center justify-center gap-1.5 rounded border border-blue-300 bg-blue-50 px-2 py-1.5 text-sm font-semibold text-blue-700 hover:bg-blue-100 disabled:opacity-50"
            >
              {locating ? "現在地を取得中…" : "📍 現在地を始点にする"}
            </button>
            {geoNote && (
              <p className="mt-1 text-[11px] text-blue-600">{geoNote}</p>
            )}
            {geoError && (
              <p className="mt-1 text-[11px] text-red-600">{geoError}</p>
            )}
            <div className="mt-2 flex items-center justify-between gap-2">
              <button
                type="button"
                onClick={saveHome}
                className="flex-1 rounded border border-slate-300 px-2 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-100"
              >
                🏠 この地点を自宅に登録
              </button>
              {home && (
                <button
                  type="button"
                  onClick={clearHome}
                  className="text-[11px] text-slate-400 underline hover:text-slate-600"
                >
                  解除
                </button>
              )}
            </div>
            {homeNote && (
              <p className="mt-1 text-[11px] text-emerald-600" aria-live="polite">
                {homeNote}
              </p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-2">
            <label className="flex flex-col text-xs font-semibold text-slate-700">
              緯度 (lat)
              <input
                type="number"
                step="0.0001"
                value={lat}
                onChange={(e) => setLat(Number(e.target.value))}
                className="mt-1 rounded border border-slate-300 px-2 py-1 text-sm"
              />
            </label>
            <label className="flex flex-col text-xs font-semibold text-slate-700">
              経度 (lng)
              <input
                type="number"
                step="0.0001"
                value={lng}
                onChange={(e) => setLng(Number(e.target.value))}
                className="mt-1 rounded border border-slate-300 px-2 py-1 text-sm"
              />
            </label>
          </div>
          <p className="-mt-1 text-[11px] text-slate-400">
            地図をクリックして始点を指定することもできます。
          </p>

          <label className="flex flex-col text-xs font-semibold text-slate-700">
            目標距離: <span className="text-blue-700">{targetKm.toFixed(1)} km</span>
            <input
              type="range"
              min={0.5}
              max={20}
              step={0.5}
              value={targetKm}
              onChange={(e) => setTargetKm(Number(e.target.value))}
              className="mt-1"
            />
          </label>

          <button
            type="button"
            onClick={onSubmit}
            disabled={state.status === "loading"}
            className="rounded bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {state.status === "loading" ? "計算中…（数秒）" : "周回路を計算"}
          </button>
        </section>

        {state.status === "error" && (
          <p className="rounded bg-red-50 p-2 text-xs text-red-700">{state.message}</p>
        )}

        {result && (
          <section className="flex flex-col gap-2">
            <div className="text-[11px] text-slate-500">
              候補 {result.candidates.length} 件 / ノード {result.stats.graphNodes}・
              エッジ {result.stats.graphEdges} / 計算 {result.stats.computeMs}ms
              （Overpass {result.stats.overpassMs}ms）
            </div>
            <ul className="flex flex-col gap-1.5">
              {candidates.map((c, i) => {
                const isSel = c.id === selectedId;
                return (
                  <li key={c.id}>
                    <button
                      type="button"
                      onClick={() => setSelectedId(c.id)}
                      className={`w-full rounded border px-3 py-2 text-left text-sm ${
                        isSel
                          ? "border-blue-600 bg-blue-50"
                          : "border-slate-200 hover:bg-slate-50"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-slate-800">
                          #{i + 1}{" "}
                          {c.id === result.recommendedId && (
                            <span className="ml-1 rounded bg-emerald-100 px-1 text-[10px] text-emerald-700">
                              推奨
                            </span>
                          )}
                        </span>
                        <span className="text-slate-700">
                          {(c.lengthMeters / 1000).toFixed(2)} km
                        </span>
                      </div>
                      <div className="mt-0.5 flex justify-between text-[11px] text-slate-500">
                        <span>誤差 ±{(c.lengthError / 1000).toFixed(2)}km</span>
                        <span>重複 {c.overlapPercent}%</span>
                        <span
                          className={
                            c.onParetoFront ? "text-blue-500" : "text-slate-400"
                          }
                          title={`手法: ${c.source}`}
                        >
                          {c.onParetoFront ? "フロント" : "別方向"}
                        </span>
                      </div>
                    </button>
                  </li>
                );
              })}
            </ul>
            {(() => {
              const sel = candidates.find((c) => c.id === selectedId) ?? candidates[0];
              if (!sel) return null;
              return (
                <>
                  <button
                    type="button"
                    onClick={() =>
                      void shareGpx(
                        sel.path,
                        `round-trip-${(sel.lengthMeters / 1000).toFixed(1)}km`,
                      )
                    }
                    className="rounded border border-emerald-600 bg-emerald-600 px-3 py-2 text-center text-sm font-semibold text-white hover:bg-emerald-700"
                  >
                    GPX をスマホに送る / 保存
                  </button>
                  <p className="text-[10px] text-slate-500">
                    スマホでこのボタン → 共有シートから <b>OsmAnd / Komoot / Garmin Connect</b> に渡すと、
                    走りながら音声＋ライン表示で正確にナビできます（PC では GPX が保存されます）。
                  </p>
                  <a
                    href={googleMapsDirUrl(result.start, sel.path)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="rounded border border-slate-300 px-3 py-1.5 text-center text-xs text-slate-600 hover:bg-slate-100"
                  >
                    Google マップで開く（近似・参考）
                  </a>
                  <p className="text-[10px] text-slate-400">
                    ※ Google マップは経由地点(最大約9点)を再探索するため近似です。正確な経路は上の GPX を使ってください。
                  </p>
                </>
              );
            })()}
            <p className="text-[10px] text-slate-400">{result.attribution}</p>
          </section>
        )}
      </aside>

      <main className="relative min-h-[50vh] flex-1">
        <MapView
          start={mapStart}
          candidates={candidates}
          selectedId={selectedId}
          onPick={(pLng, pLat) => {
            setLng(Number(pLng.toFixed(6)));
            setLat(Number(pLat.toFixed(6)));
          }}
        />
      </main>
    </div>
  );
}
