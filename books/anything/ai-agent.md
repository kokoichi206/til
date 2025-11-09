https://github.com/minorun365/agent-book

## LLM

- AI エージェント
  - プロファイリング
    - 役割や個性の定義が可能
  - 長期記憶
    - 以前の文脈を記憶
  - **計画と振り返り**
    - タスク分割して段階的に実行
    - 実行結果を観察し、必要に応じた計画の修正
  - **ツール実行**
- 計画と振り返り
  - Chain-of-Thought
    - 内部の知識のみで思考せざるを得ない
    - 1つの連鎖ステップで間違えると、以降は間違いが増幅する
  - ReAct: Reasoning and Acting
    - 行動計画を立てて細かなタスクを実行
    - その結果を都度観測し、計画を見直す
    - このサイクルを繰り返す
- ツール実行

### AI エージェントの技術

- Function Calling (Tool Use)
- MCP
  - MCP ホスト
  - MCP クライアント
  - MCP サーバー
  - ツール
- メモリ
- ガードレール
  - LLM の入出力の前後で動作する制御プログラム
  - 悪意のある指示文をエージェント到達前でブロック
- RAG
  - チャンキング
  - ベクトルデータベース

### めも

- Agentic AI
  - AI エージェントに比べて自立性が高まったもの
  - あらかじめタスクを想定してない

## LLM

- 拡張思考 Extended Thinking
  - Reasoning モデル
  - 推論
    - Inference
      - モデルにプロンプトを入力して出力を得るプロセス
    - Reasoning
      - Inference を使って、まるで思考するかのように論理的に結論を導き出す手法
- マルチモーダル入力
- プロンプトキャッシュ

## フレームワーク

- LLM アプリ
  - LangChain
  - LlamaIndex
    - RAG につよい
    - データを活かす
  - Semantic Kernel
  - AI SDK
    - Vercel
- AI エージェント開発
  - LangGraph
    - LangChain 社が開発
    - LangChain を組み合わせて使う
  - CrewAI
  - Mastra
    - Gatsby の開発メンバー
    - LLM 呼び出しには AI SDK を使ってる
  - VoltAgent
    - VoltOps
      - LLM 可観測性プラットフォーム
      - **他のフレームワークの動作も可視化できるぽい？**
  - AutoGen
    - MS,
    - OpenAI Agents SDK
  - ASgent Development Kit (ADK)
  - Strands Agents
    - AWS
    - Amazon Q Developer でも利用されている
- プラットフォーム
  - Amazon Bedrock AgentCore
    - AI エージェントのコアとなる機能群がビルディングブロックとして提供されている
  - Amazon Bedrock Agents
  - Dify
    - エージェント
    - ワークフロー
    - チャットフロー
- UI 開発
  - Streamlit
    - Python での Web アプリ開発
  - Amplify Gen2
  - Vercel

## エージェント開発

- Agentic Workflow
  - LLM に行動選択を任せる部分とプログラムでワークフローを事前定義する部分の組み合わせ
- Multi Agent Sysmtem: MAS
  - 複数の AI エージェントでチームを構成するアプローチ
- https://github.com/humanlayer/12-factor-agents/
  - BAML: https://boundaryml.com/
    - The First Language for Building Agents
- Agent2Agent: A2A
  - AI エージェント同士のコミュニケーションを標準化する規格
  - JSON-RPC というプロトコル
- アンビエント・エージェント
  - ユーザーからの支持を受けて動作するチャットボット型の場合、人からの支持出しが作業のオーバーヘッドとなる
  - AI エージェントが周囲の環境を自ら察知し、シグナルを検知して自動で仕事する
  - **Human-in-the-Loop で品質を保つ**
    - 人間が**いつ**介入するか
      - 通知
      - 質問
      - レビュー
    - 人間が**どのように**介入するか
      - Agent Inbox
      - https://github.com/langchain-ai/agent-inbox

## LLMOps

- 開発フェーズ
  - LLM 選択
  - プロンプトエンジニアリング
    - ドメインエキスパートからのフィードバック
  - 実験管理
    - トレースとその可視化
  - オフライン評価
    - **事前に準備したテストデータセット**で LLM アプリケーションの性能評価をする
    - LLM-as-a-Judge
      - **自然言語の意味も事前学習してるので、人と近い感覚で評価可能**
  - データセット管理
    - LLM アプリケーション評価に利用するデータセットの管理プロセス
- 運用フェーズ

ツール

- LangSmith
  - LangChain 社が開発
- **Langfuse**
  - OSS
  - https://github.com/langfuse/langfuse
- **Ragas**
  - https://github.com/explodinggradients/ragas
- DeepEval

プロンプト管理

- LLM への指示テキストであるプロンプトを体系的に管理するプロセスのこと
- **プロンプトを実装コードから分離して、バージョン管理をすることが必要となる**
  - プロンプト変更時の改善サイクルを効率化できる
  - エンジニア以外のユーザーがプロンプトを用意に変更できる
  - プロンプトの変更履歴を管理できる
  - プロンプトの流用性が高まる
