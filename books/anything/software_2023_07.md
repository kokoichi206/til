## なんでも




## gRPC

- 利用箇所
  - マイクロサービス間の通信
  - モバイルアプリとバックエンドサーバーの通信
- 特徴
  - Protocol Buffers
  - HTTP/2 による双方向ストリーミングの利用
    - HTTP/2 のストリームは、Web ブラウザの JS からは直接扱えない
    - → Web ブラウザとバクエンドサーバー間の通信では使えない
    - gRPC-Web なるものもある
- RPC
  - Remote Procedure Call
  - 手元のプログラムから、遠隔地に存在するプログラムの処理の呼び出しを行う手順
- gRPC
  - google 開発
  - Protocol Buffers を IDL: Interface Description Language とする
    - メッセージのバイナリ形式を持っており、各プログラミング言語のデータ構造と対応する形でSiriアライズ・でSiriアライズできる
- HTTP/2 では1つのコネクションでストリームを多重化できる
- Google APIs 標準メソッド
  - https://cloud.google.com/apis/design/standard_methods?hl=ja
- REST
  - 操作の種類が HTTP メソッドから読み取れるあtめ、CDN を通じたコンテンツのキャッシュなどが機械的に行われる！
    - gRPC では独自の工夫が必要
- GraphQL
  - スキーマ駆動開発の文脈
- gRPC-Web
  - Envoy Proxy を通じ、HTTP/1.1 を含む HTTP プロトコルをサポートする
- gPRC-Gateway
  - gRPC のメッセージを JSON に変換する

### Getting started

- HTTP/2
  - cf: 1.1
    - 通信効率向上
      - コネクションはりっぱ
    - ネットワークリソースの効率化
      - バイナリがベース
- スキーマ駆動開発
- デメリット
  - インフラ難易度が高い
    - クライアントからサーバまでを HTTP/2 で通信できる必要がある
  - デバッグ難易度が高い
- タグNo.
  - API の運用中にフィールドを削除する場合には、**一度使ったタグナンバーは、再利用せずに廃番にする！**

### API 設計ポイント

- .proto にコメントを書くことはできる
  - エラーが起きる条件等
- protoc-gen-doc
  - Markdown, HTML とかでドキュメントを出力可能


## Svelte

JavaScript フレームワークの中で、勢いのあるものらしい

- よくあるフレームワークのデメリットを解決したい
- 仮想 DOM を持たない js フレームワーク
  - フレームワークのオーバーヘッドが最小限に抑えられる
    - 高速なパフォーマンスと軽量なバンドルサイズ
- Svelte: コンパイラフレームワーク
- Truly reactive
  - js そのものがリアクティブ
  - 状態管理という概念も不要
- 全てのコードにはバグが存在する可能性があります（All code is buggy）。
  - したがって、書かなければならないコードが多いほど、アプリがバグだらけになるのは理にかなっている
- 比較
  - binding
    - react
      - 単方向データバインディング
      - View に反映するのは自動
      - View から更新するには、イベントハンドラに登録
    - vue.js
      - 双方向データバインディング
      - 自動的に反映されるが故の、パフォーマンス面での注意点が多い
    - svelte
      - トップダウンの単方向データバインディング
      - 親 → 子
      - bind:value で子から親に渡せる
  - 学習コスト
    - react
      - 高いと言われがち
      - JSX 記法の習得
      - 単方向データフローゆえのアーキテクチャ
    - Vue.js
      - HTML, style, logic を１ファイル内に書くことができる
        - SFC: Single-File Component
      - 見通しが良い
    - Svelte
      - SFC のコンポーネント

``` sh
npm create svelte@latest myapp
```

## SNS

分散型 SNS を考える

- comparison of software and protocols for distributed social networking
  - ActivityPub
    - Mastodon
    - Misskey
    - Pleroma
  - AT Protocol
    - 2022/5
  - Nostr: Notes and Other Stuff Transmitted by Relays
    - ノスター、ノストラ
    - 検閲に強い分散型 SNS を構築できる
      - 公開鍵と秘密鍵の鍵ペア
    - クライアントとリレーの2つの要素が、全て ws を通して行われる
    - 無法地帯とも呼ばれている

