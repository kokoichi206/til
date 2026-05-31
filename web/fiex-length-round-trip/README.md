# Fixed-Length Round Trip Planner

目標距離の「周回路（出発点に戻るループ）」を生成し、地図上に描画する Next.js アプリ。

論文 **Rhyd Lewis & Padraig Corcoran, _Fast Algorithms for Computing Fixed-Length
Round Trips in Real-World Street Networks_, SN Computer Science 5:868 (2024)**
（[doi:10.1007/s42979-024-03223-3](https://doi.org/10.1007/s42979-024-03223-3),
オープンアクセス）のアルゴリズムを TypeScript で実装している。

## できること

- 緯度経度（地図クリック / 現在地 / 入力）と目標距離を指定（ランニング想定で徒歩道ベース。API は自転車プロファイルも受付）
- OpenStreetMap の道路網を基に、目標距離に近く・往復の少ない周回路を複数生成
- パレートフロント（最適解）＋方位の異なる代替ループを地図に描画

## 必要なキー: なし

- **道路データ**: OpenStreetMap Overpass API（キー不要）
- **地図描画**: MapLibre GL JS + OSM ラスタータイル（キー不要）

Google Maps を使わない理由（依頼の 2 観点に基づく判断）:

1. **計算へのデータ利用**: Google Maps Platform ToS（3.2.3）は、Google のデータから
   独自の経路グラフ/データセットを作る・キャッシュすることを禁止している。よって
   カスタム経路アルゴリズムの計算データ源にはできない。OSM は ODbL で計算・保存が自由。
2. **複雑経路の描画**: Google でも描画自体は可能だが、課金アカウント（クレジットカード）と
   API キーが必須（$200 無料枠は 2025/3 廃止）。OSM 系なら無料・キー不要。

> 見た目を Google Maps にしたい場合は `src/client/lib/map-style.ts` の差し替えと
> Maps JavaScript API キー（要課金アカウント）の発行のみで対応可能。描画層は抽象化済み。

## アルゴリズム（論文の KRT 問題）

開始点 s・目標長 k に対し、閉じた歩行で次の 2 目的を同時最小化する（多目的最適化）:

- `f1 = |k − L(S)|` 距離誤差
- `f2 = 既踏破区間の再通過割合(%)` 往復の重複

実装は 2 段構成:

1. **Stage 1 — 等時線多角形法** (`round-trip.ts`)
   - `k/2` 到達圏を Dijkstra で算出（論文の isochrone に相当）
   - 多方位・多アスペクトの楕円多角形ウェイポイントを生成（始点を頂点0に固定し周長を k に正規化）
   - 各レッグを Dijkstra で接続。既使用エッジに ×5 ペナルティを与え重複を抑制
   - out-and-back（U ターンの行き止まり）を除去し `(f1, f2)` を評価
2. **Stage 2 — パレート局所探索** (`pareto-local-search.ts`, 論文 Algorithm 3 & 4)
   - 残余グラフ＋ダミー頂点＋BFS 木による近傍操作（区間置換／サブサイクル付加）
   - 非支配解アーカイブを反復改善

## ディレクトリ構成

`ads-report-pro` のレイヤリング（`app`/`client`/`server`/`shared`/`types`, `@/*` エイリアス,
Zod による env/入力検証）に準拠。

```
src/
  app/                 ルート + API
    api/round-trip/route.ts   POST: 計算エンドポイント
    page.tsx / layout.tsx
  client/              UI（'use client'）
    components/MapView.tsx           MapLibre（命令的・SSR安全）
    components/RoundTripPlanner.tsx  フォーム + 結果 + 地図
    hooks/useRoundTrip.ts
    lib/map-style.ts
  server/
    osm/               Overpass 取得・グラフ構築
    routing/           geo / graph / dijkstra / isochrone / round-trip / walk / pareto-local-search
    usecases/compute-round-trips.ts  全体オーケストレーション
  shared/
    env/server-env.ts  任意設定（Overpass エンドポイント等）
    types/round-trip.ts 共有型 + Zod スキーマ
```

## 開発

```bash
pnpm install
pnpm dev            # http://localhost:3077
pnpm type-check     # 型チェック
pnpm test           # 単体テスト（合成グリッドで Dijkstra / 評価 / E2E を検証）
pnpm build          # 本番ビルド

# 起動中サーバへの実データ（Overpass）スモーク
pnpm rt:smoke
LAT=34.985 LNG=135.758 KM=5 PROFILE=bike pnpm rt:smoke
```

### 任意の環境変数

| 変数 | 用途 |
|---|---|
| `OVERPASS_ENDPOINT` | 公開 Overpass を避けて自前インスタンスを使う場合 |
| `OVERPASS_USER_AGENT` | OSM 利用エチケット用の User-Agent |

## 注意 / 既知の制約

- 公開 Overpass はフェアユース（~1万クエリ/日, ~1GB/日, User-Agent 必須）。多用時は自前インスタンス推奨。
- 目標距離は 200m〜25km。大きいほど取得・計算が重くなる（東京中心で 2.5km ≈ 8〜10 秒, うち Overpass 1.5〜3 秒）。
- OSM タイルは開発用途。本番は OSM タイル利用ポリシーに従い独自/商用タイルへ。

データ出典: © OpenStreetMap contributors (ODbL)
