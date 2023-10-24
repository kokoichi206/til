## なんでも

- [Bun](https://github.com/oven-sh/bun)
  - js, ts の高速ランタイム
  - nodejs の代わりを目指す
  - nodejs などの従来の js ランタイムの課題
    - ツールチェーンの複雑さによるパフォーマンスや開発効率の低下
    - バンドルの問題
      - js や css をアプリにバンドルするために webpack などが必要
    - トランスパイルの問題
      - ts や tsx を使用するには Babel などが必要
    - タスクランナーパッケージマネージャーの問題
  - 特徴
    - Bun のランタイム部分は Zig で実装されてる
    - ts と jsx を直接実行することが可能（？）
  - js, ts の統合インフラになることを長期の目標にしている
- チームビルディング
  - 自分が得意なことは何か
  - どうやってチームの成果に貢献するつもりか
  - 自分が大切に思う価値観は何か
  - チームメンバーは自分にどんな成果を期待してると思うか
- 生産性を向上
  - マイクロブレイク
    - 有効なケース
      - ルーティングタスク
      - 創造的なタスク
    - 有効ではなかったケース
      - 認知的要求の高いタスク
        - プログラミングなど
- 個人開発
  - 同じことを考える人はたくさんいるので、気にしない
    - **Google は１８番目の検索エンジン**
- vim
  - design-not
- サービスメッシュと [Istio](https://istio.io/)
  - サイドカー
  - コントロールプレーン

## コンテナイメージ

### 基礎知識

- コンテナ
  - 現在絵は Docker コンテナを指すのが一般的
- コンテナイメージ
  - ベースイメージから変更が加えられるごとにレイヤが作成され、複数のレイヤを透過的に重ね合わせることで1つのファイルシステムを実現
    - **イメージレイヤ**
  - イメージレイヤ
    - 読み取り専用
- Dockerfile
  - テキスト形式でバージョン管理システムと相性がいい
  - **命令ごとにレイヤが作成される**
- 理想的なコンテナに必要なこと
  - 再現性
    - バージョンの固定
  - セキュリティ
    - **コンテナブレイクアウト**
    - **コンテナエスケープ**
    - 不要なファイルを含めない
    - distroless にする
      - Go, Rust などのビルドしたアビアンリが1つあれば動くアプリケーションであれば、distroless にするのも選択肢
      - シェル、linux ディストリビューションとしてのプログラムは含まれない
    - 頻繁にビルドしなおす
      - セキュリティパッチの適応が可能性あるので
      - `--no-cache` オプションが推奨されている
  - 可搬性
    - 環境依存をなくす
    - コンテナイメージを軽量に保つ
- 書き方
  - パースディレクティブ
    - syntax
    - escape
  - 記述で気をつけるべきところ
    - ベースイメージの選択
    - イメージサイズ、レイヤ数
    - キャッシュ、ビルドの速度

``` dockerfile
FROM node:20-slim
WORKDIR /src
# レイヤーを刻むことで package ファイル以外の更新について、npm install の部分のキャッシュを効かせる！
COPY package.json package-lock.json
RUN npm install
COPY . .
ENTRYPOINT ["node", "app.js"]
```

### ベストプラクティス

- イメージレイヤの概念
- イメージサイズ
- イメージの過去レイヤに残った機密情報の漏洩
- ビルドコンテキスト
  - ビルドコンテキストとして指定されたパス以下に含まれるディレクトリやファイルを、**全て docker engine デーモンのメモリ上に取り込む！！**
    - 無駄なファイルではあるが、メモリの浪費につながる
- `.dockerignore`
  - コンテキストとして使いたくないファイルやディレクトリを無視できる
- 不要なパッケージを入れない
  - debian 環境での apt-get
    - `--no-install-recommends` をつける

``` dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.20-alpine AS build

RUN apk add --no-cache git

...

FROM scrach
COPY --from=build /bin/project /bin/project
ENTRYPOINT ["/bin/project"]
CMD ["--help"]
```

### ベーシイメージ

- distroless
  - google が提供している軽量なコネtなイメージ群の名称
  - ubuntu のコンテナ
    - フル機能の os が含まれる、いわば軽量な仮想マシンのような側面も持っていた
  - **シェルが含まれてないため、コンテナに入ってのデバッグがしにくい**
    - **debug タグのついたイメージには BusyBox が含まれる！**

### そのほか

[trivy](https://github.com/aquasecurity/trivy)

``` sh
brew install trivy

trivy image python:3.4-alpine -f json -q
```

[dive](https://github.com/wagoodman/dive)

``` sh
brew install dive

dive python:3.4-alpine
```

[hadolint](https://github.com/hadolint/hadolint)

``` sh
brew install hadolint

hadolint <Dockerfile>
```

### セキュリテイ

- イメージ作成時には脆弱性がなくても、時間の経過とともにセキュリティパッチの適応されてない脆弱なものになるかもしれない
  - イメージを際ビルドしてデプロイすることが必要
- イメージの脆弱性スキャン
  - 悪用可能な脆弱性をコンテナ実行環境から除外したり検知したりできることが目的！
- イメージスキャンのタイミング
  - 以下の二段構えが理想的
    - CI
    - 実行基盤
- SBOM
  - ソフトウェアコンポーネントやそれらの依存関係の情報を機械的に処理可能なリストのこと
  - コンテナイメージの SBOM を作成するツールには Trivy や Syft


## LLM アプリケーション開発

- ハルシネーション（幻覚）
  - でっちあげのような情報を応答するような LLM の振る舞い
- RAG: Retrieval-augmented Generation
  - 検索により強化した生成
    - 外部から取得した情報をもとに回答を作成する手法のこと
  - 正確な情報を得るための仕組み
- ベクトルデータベース
- 埋め込み
  - 高次元のデータから、低次元のデータに変換すること
- text-embedding-ada-002
  - 埋め込みベクトルを作成するためのモデル

## Go


