## sec 1

- gpt3.5-turbo
  - 従来の 1/10 のコストで GPT-3.5 を扱える
- プロンプトを工夫することで、**専用に学習したわけではない様々なタスクに対応できる**場合がある
- AI エージェント
  - 自律的に動作する
- 活用事例
  - CYDAS PEOPLE Copilot Chat
    - 問い合わせの効率化
  - PingCAP Chat2Query
    - GPT を用いて自然言語から SQL を作成
- 気をつけること
  - 解答の再現性は期待できない
- 研究一部紹介
  - [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
  - [Precise Zero-Shot Dense Retrieval without Relevance Labels](https://arxiv.org/abs/2212.10496)
  - [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)
    - https://github.com/joonspk-research/generative_agents

## sec 2

- プロンプトエンジニアリング
  - LLM からほしい情報を引き出す
  - [Prompt Engineering Guide](https://www.promptingguide.ai/jp)
  - 構成要素
    - 命令
    - 入力データ
    - 文脈 (context)
    - 出力形式の指定
- でざぱた？
  - Zero-shot プロンプティング
  - Few-shot プロンプティング
    - In-context Learning (ICL)
  - Zero-shot Chain of Thought (Zero-shot CoT)
    - 『ステップバイステップで考えてみましょう』と最後につける。
    - 多くのタスクで効果的！

## sec 3

- gpt-4 は 3.5-turbo の 20-30 倍の料金
- トークン
  - 必ずしも単語と一致するわけではない
  - 経験則として、英語のテキストだと 1 トークンは 4-0.75 単語程度
  - 日本語の方が英語よりも多くなりやすい！
    - 2倍程度になることも

``` sh
pip install python-dotenv

pip install openai

export OPENAI_API_KEY='sk-xxxxxx'
```

- Chat Completions API のパラメータ
  - model
  - messages
  - stream
  - temperature
  - n
  - stop
    - 登場した時点で生成を停止する文字列
  - max_tokens
  - user
- Function calling
  - 利用可能な関数を LLM に伝えておいて、LLM に『関数を使いたい』という判断をさせる機能
  - LLM はどんな関数をどう使いたいかを返してくれるだけ
    - 関数の実行は python などを使って API の利用者側で実行する必要がある

## sec 4

- LangChain
  - LLM を使ったアプリケーションに必要な部品を、抽象化されたモジュールとして提供している
  - 特定ユースケースに特化した機能の提供
- ユースケース
  - ChatGPT のように対話できるチャットぼっと
  - 文章の要約ツール
  - 社内文書や PDF ファイルへの Q and A アプリ
  - AI エージェント
- LangChain 以外のフレームワーク・ライブラリ
  - LlamaIndex
  - Semantic Kernel
  - Guidance
- Modules
  - https://python.langchain.com/docs/get_started/introduction#modules

``` sh
pip install langchain openai
```

- Language models
  - 様々な言語モデルを共通のインタフェースで使用できる
  - LLM を LangChain 流で使えるようにするらっぱあ
- Prompts
  - PromptTemplate
  - 入力に関するモジュール
- Output parsers
  - 出力に関するモジュール
- Chains
  - PromptTemplate の穴埋め → Language models に与える
  - Zero-shot CoT プロンプティング → 要約
  - LLM の出力結果が、サービスのポリシーに違反しないか
  - LLM の結果を元に SQL を実行、データを分析させたい
- 様々な Chains がある
  - LLMChain
    - Prompt Template, Language model, Output Parser を繋ぐ
  - SimpleSequentialChain
    - Chain と Chain を接続する Chain もある
  - SequentialChain
  - LLMRouterChain
  - 既成の Chain とかもある
    - OpenAIModerationChain
      - テキストが OpenAI の利用ポリシーに反していないかチェックする
    - LLMRequestsChain
      - 指定した URL に HTTP リクエストを送信し、レスポンスの内容を踏まえて LLM に回答させる
    - OpenAPIEndpointChain
      - OpenAPI 仕様を元に LLM が API へのリクエストを生成し、その内容で API を呼び出す
    - PALChain (Experimental) Program-aided Language Models
      - LLM がプログラムを生成し、プログラムを実行した結果を返す
    - SQLDatabaseChain (Experimental)
      - LLM が SQL を生成し、データベースに対して実行した上で、最終的な回答を出力させる
- Memory
  - 記憶に関する機能
  - 会話履歴の保存など

## sec 5

### Data Connection

- 外部のデータを接続するための機能
- 背景に RAG: Retrieval Augmented Generation
- ハルシネーション (Hallucination) を避ける
- RAG
  - 文章を OpenAI の Embeddings API などでベクトル化
  - 入力に近い文書を検索して context に含める
- Data Connection では、特に Vector store を使い、文書をベクトル化して保存しておく
- 機能
  - Document loaders
    - データソースからドキュメントを読み込む
  - Document transformers
    - 何らかの変換をかける
  - Text embedding models
    - ドキュメントをベクトル化する
  - Vector Stores
    - ベクトル化したドキュメントの保存先！
  - Retrievers
    - 入力のテキストと関連するドキュメントを検索する
- Document loaders
  - S3
  - BigQuery
  - GoogleDrive
  - NotionDirectory
  - ...
- Vector stores
  - chromadb
    - ローカルで使用可能な Vector store
  - Faiss,
  - ElasticSearch
  - Redis,
  - ...
- Retrievers
- RetrievalQA (Chain)
  - PromptTemplate に context として埋め込んで LLM に回答 (QA) してもらいたいケース！
  - [chain_type](https://python.langchain.com/docs/use_cases/question_answering/vector_db_qa#chain-type)

## 疑問

- デプロイ
