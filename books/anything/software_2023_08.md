## なんでも

- Emonet
  - MaaS: Malware as a Service
  - RaaS: Ransomware as a Service
- MLOps
- three.js
  - https://github.com/watab0shi/software-design-threejs-3d-programming-samples/tree/main/chapter-06
- Go 言語
  - 型階層 type hierarchy を取り入れなかった！
  - 埋め込みフィールド: embedded
    - 委譲を実現: delegation
  - オブジェクト指向型言語との違いで重要な点
    - クラスとは異なり、Go ではデータと振る舞いを別に扱うこと！
  - メソッドとメソッドセットは別の概念
    - 埋め込みしても、その型のメソッドになるわけではない
      - メソッドセットには入る
    - フィールドを埋め込んでも、メソッドは増えない
      - 継承で発生する弱いカプセル化問題を回避
    - フィールドを埋め込むとメソッドセットは増える
      - 代入可能なインタフェースの幅を広げ、抽象化を柔軟に

## アジャイル

- XP
  - 価値
  - 原則
  - プラクティス
- MVP
  - Minimum Viable Product

### スクラムを回す

- スクラムの３本柱
  - 透明性、検査、適応
- 5つの価値基準
  - 確約、集中、公開、尊敬、結城
- デイリースクラム
  - 主役は開発者
  - スクラムマスターの顔色を窺わない
- スプリントレビュー
  - ワーキングセッション
  - 議論する場

### アジャイルな設計・開発

- 必要な時に、必要なだけ、設計する
  - Enough design up front: ENUF
- 設計のポイント
  - ドメイン知識
  - 先人たちの見つけたアーキテクチャ
- Easier To Change
- アジャイルにおけるテスト
- 技術的負債の付き合い方
  - ４象限
    - 設計の際の考慮の度合い
      - 無鉄砲か身長か
    - 負債になることに気づいていたかどうか
      - 意図的か不注意か
  - 無鉄砲かつ不注意
    - 十分亜知識がない時など
    - 気づかれないため、後になって深刻な問題になることも
  - 無鉄砲かつ意図的
    - 時間や実装コストの問題などで、負債になることがわかっている
    - 後で直すつもり、とか
  - 慎重かつ意図的
    - 選択肢について考慮した上で、その部分が後になって深刻になる可能性が十分低いとチームで考えた場合
    - 踏み倒すことができる部分
  - 慎重かつ不注意
- 技術的負債を減らすには
  - リファクタリング
  - 依存ライブラリの更新

### 大規模

- 大規模アジャイルフレームワーク
  - Nexus
  - LeSS
    - Large-Scale Scrum

## TiDB

### NewSQL

- ACID 特性
  - トランザクションにおける4つの重要な特性
  - Atomicity, Consistency, Isolation, Durability
- CAP 定理
  - Consistency, Availability, Partition-tolerance
- 拡張性
  - スケールアップ、スケールアウト
- RDBMS
  - メリット
    - ACID 属性
    - 一貫性と可用性に強い
  - デメリット
    - 非構造化データによわい
    - データが大容量になたっときの拡張性に弱い
    - スキーマ変更に対する柔軟性が低い
- NoSQL
  - 複数のサーバーによって DB を構成することで、高い可用性、拡張性、処理性能を実現
  - 一貫性を一部犠牲
  - 弱いところ
    - 型チェックが弱い
    - 完全な ACID 特性は保証しない
- NewSQL
  - RDBMS と NoSQL の両方の特徴を有する
  - 分散性を持った RDB ライクなデータベース
  - 一貫性と分断耐性に強く、可用性も（ある程度）強い！
  - デメリット
    - スケール可能な RDBMS という位置付けのため、非構造化データを扱いにくい
  - 導入や運用のコストは高いかも

### TiDB の仕組み

タイデービー: Ti = チタン

- 両方をサポート = ハイブリッドトランザクション
  - Online Transaction Processing: OLTP
  - Online Analytical Processing: OLAP
- 特徴
  - マスターの冗長化が容易
  - シャーディングが不要
  - 効率の良いスケール
  - タイムトラベルクエリができる
    - 過去の状態のデータを参照可能
    - デフォルトだと10分前まで
- TiDB Cloud

### TiDB で遊ぶ

- tiup を用いて TiDB を構築するためには、構築対象のサーバーに ssh でログインする必要がある。
  - そのため Kubernetes に TiDB を構築するには tiup には対応できひん
- 

### Links

- https://docs.pingcap.com/
- playground: https://play.tidbcloud.com/scalability?utm_source=docs&utm_medium=menu

## 位置情報

- 位置情報
  - スマートフォンなどの GNSS で測位した現在地
    - Global Navigation Satellite System
