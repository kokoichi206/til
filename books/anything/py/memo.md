``` sh
curl -LsSf https://astral.sh/uv/install.sh | sh

uv python install 3.11

uv init sd-16 --python 3.11


> uv run python --version
Using CPython 3.11.11
Creating virtual environment at: .venv
Python 3.11.11



uv add langchain-core==0.3.19 langchain-anthropic==0.3.0 langchain-openai==0.2.8 langchain-community==0.3.7 langgraph==0.2.50 tavily-python==0.5.0
```

## Links

- [Tavily](https://tavily.com/)
  - AI エージェント専用に構築された検索エンジン
  - リアルタイムで正確かつ事実に基づいた情報を提供
