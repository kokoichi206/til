``` sh
mkdir my_agent

uv remove langgraph-cli --dev
uv add langgraph-cli==0.1.56 --dev

# LangGraph Server が Docker コンテナとしてビルドされ起動する。
uv run langgraph up
```
