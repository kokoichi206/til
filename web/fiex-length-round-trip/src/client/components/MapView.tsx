"use client";

import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef } from "react";

import { osmRasterStyle } from "@/client/lib/map-style";
import type { LngLat, RoundTripCandidate } from "@/shared/types/round-trip";

export interface MapViewProps {
  start: LngLat | null;
  candidates: RoundTripCandidate[];
  selectedId: string | null;
  /** 地図クリックで始点を選ぶ。 */
  onPick: (lng: number, lat: number) => void;
}

const DEFAULT_CENTER: [number, number] = [139.767, 35.681]; // 東京駅
const ROUTES_ALL = "routes-all";
const ROUTE_SELECTED = "route-selected";

function lineFeature(path: LngLat[]): GeoJSON.Feature {
  return {
    type: "Feature",
    properties: {},
    geometry: { type: "LineString", coordinates: path },
  };
}

export default function MapView({
  start,
  candidates,
  selectedId,
  onPick,
}: MapViewProps): React.JSX.Element {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const readyRef = useRef(false);
  const startMarkerRef = useRef<maplibregl.Marker | null>(null);

  // 最新の props を ref に保持し、地図再生成を避ける。
  const onPickRef = useRef(onPick);
  onPickRef.current = onPick;
  const stateRef = useRef({ start, candidates, selectedId });
  stateRef.current = { start, candidates, selectedId };

  const render = useRef(() => {});
  render.current = () => {
    const map = mapRef.current;
    if (!map || !readyRef.current) return;
    const { start: s, candidates: cands, selectedId: sel } = stateRef.current;

    const allSrc = map.getSource(ROUTES_ALL) as maplibregl.GeoJSONSource | undefined;
    allSrc?.setData({
      type: "FeatureCollection",
      features: cands.map((c) => lineFeature(c.path)),
    });

    const selected =
      cands.find((c) => c.id === sel) ?? cands[0] ?? null;
    const selSrc = map.getSource(ROUTE_SELECTED) as
      | maplibregl.GeoJSONSource
      | undefined;
    selSrc?.setData(
      selected
        ? lineFeature(selected.path)
        : { type: "FeatureCollection", features: [] },
    );

    // 始点マーカー。
    if (s) {
      if (!startMarkerRef.current) {
        startMarkerRef.current = new maplibregl.Marker({ color: "#dc2626" });
      }
      startMarkerRef.current.setLngLat(s).addTo(map);
    } else {
      startMarkerRef.current?.remove();
    }

    // 選択経路にフィット。
    if (selected && selected.path.length > 1) {
      const bounds = new maplibregl.LngLatBounds();
      for (const p of selected.path) bounds.extend(p);
      map.fitBounds(bounds, { padding: 60, maxZoom: 16, duration: 600 });
    } else if (s) {
      map.easeTo({ center: s, zoom: 14 });
    }
  };

  useEffect(() => {
    if (!containerRef.current) return;
    const map = new maplibregl.Map({
      container: containerRef.current,
      style: osmRasterStyle,
      center: start ?? DEFAULT_CENTER,
      zoom: 14,
      attributionControl: { compact: false },
    });
    mapRef.current = map;
    map.addControl(new maplibregl.NavigationControl({}), "top-right");
    map.on("click", (e) => onPickRef.current(e.lngLat.lng, e.lngLat.lat));
    map.getCanvas().style.cursor = "crosshair";

    map.on("load", () => {
      map.addSource(ROUTES_ALL, {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });
      map.addLayer({
        id: ROUTES_ALL,
        type: "line",
        source: ROUTES_ALL,
        layout: { "line-join": "round", "line-cap": "round" },
        paint: { "line-color": "#60a5fa", "line-width": 2, "line-opacity": 0.45 },
      });

      map.addSource(ROUTE_SELECTED, {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });
      map.addLayer({
        id: ROUTE_SELECTED,
        type: "line",
        source: ROUTE_SELECTED,
        layout: { "line-join": "round", "line-cap": "round" },
        paint: { "line-color": "#1d4ed8", "line-width": 5, "line-opacity": 0.95 },
      });

      readyRef.current = true;
      render.current();
    });

    return () => {
      readyRef.current = false;
      startMarkerRef.current?.remove();
      startMarkerRef.current = null;
      map.remove();
      mapRef.current = null;
    };
    // 初回マウントのみ。
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // props 変化で再描画。
  useEffect(() => {
    render.current();
  }, [start, candidates, selectedId]);

  return <div ref={containerRef} className="h-full w-full" />;
}
