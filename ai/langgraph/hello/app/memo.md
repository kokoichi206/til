## LangGraph

- AI エージェントなどの複雑な LLM アプリケーション開発を支援するフレームワーク
- API
  - Graph API
    - グラフ構造でワークフローを管理
  - Functional API
    - 通常の Python ぽいやつ、if, for, etc.
- グラフ構造
  - ノード
  - エッジ
    - 有向グラフ
- グラフの node
  - agent node
  - tools node

## tavily

- https://app.tavily.com/home

## memo

``` sh
uv init

uv python install 3.13
uv venv --python 3.13

source .venv/bin/activate

uv add pydantic
uv add langgraph

uv add boto3
uv add 'boto3-stubs[sns]'

uv sync
```

langgraph studio はどうやって使う？
