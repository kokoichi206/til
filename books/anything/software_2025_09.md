## MCP

### 現在地

- 自然言語による情報検索
  - RAG: Retrieval Augmented Generation
    - 検索拡張生成
  - **ベクトル検索に限定されるものではない**
- ディープリサーチ
  - リサーチに特化した LLM アプリケーション
- コーディングエージェント

### MCP

- **LSP みたいな感じ？**
- ローカル MCP
  - stdio で client/server がやりとり
- リモート MCP
  - Streamable HTTP トランスポート
    - **必要に応じて** SSE を利用
- **プリミティブ**
  - サーバー側とクライアント側で別々に定義がある
  - サーバー
    - プロンプト
    - リソース
    - ツール
  - クライアント
    - ルート
    - サンプリング
    - えりしテーション
      - Elicit: 引き出す

``` sh
claude mcp add playwright npx @playwright/mcp@latest
```

- MCP ホスト
  - LangGraph
  - Mastra

### frontend

- AI に情報を伝える
  - コンポーネント情報
  - デザイントークン
  - アイコン詳細

## なんでも

- PSL: Public Suffix List
  - eTLD の判定
  - `example.sakura.ne.jp` の `sakura.ne.jp` が PSL に記載があるので、こちらのドメインが eTLD と判定される
  - ccTLD
    - Country Code Top Level Domain
  - セクション
    -  ICANN DOMAINS
      -  ccTLD とか
    - PRIVATE DOMAINS
      - sakura.ne.jp
  - 全部で 300KB くらいある
    - ブラウザでハードコーディング
- コンテナ
  - カーネルの機能を使ってあたかも別マシンで動いてるように見せた、ホスト上の１プロセス
- 技術選定
  - Flutter
  - Go
    - テストや型によるサポート
    - テストの実行速度
    - AI とのコード補完
  - シナリオを用いた結合テスト
  - gRPC/Connect
    - IDL: インタフェース記述言語
  - TiDB
    - 水平分割できるデータベースソリューション
    - TiCDC
  - TanStack Query
    - Connect との優れた統合性
