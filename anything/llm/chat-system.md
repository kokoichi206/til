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
