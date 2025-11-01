import asyncio
import operator
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel
from typing import Annotated, Dict

from dotenv import load_dotenv


load_dotenv()


mcp_client = None
tools = None
llm_with_tools = None

async def initialize_llm():
    """MCP クライアントとツールを初期化する"""
    global mcp_client, tools, llm_with_tools

    # 現在のパスをフルパスで取得。
    dir = os.path.dirname(os.path.abspath(__file__))

    mcp_client = MultiServerMCPClient(
        {
            # FileSystem MCP.
            "file-system": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    dir,
                ],
                "transport": "stdio",
            },
            # AWS Knowledge MCP.
            "aws-knowledge-mcp-server": {
                "url": "https://knowledge-mcp.global.api.aws",
                "transport": "streamable_http",
            },
        },
    )
    tools = await mcp_client.get_tools()
    
    # LLM の初期化。
    llm_with_tools = init_chat_model(
        model="claude-sonnet-4-5-20250929",
    ).bind_tools(tools)


class AgentState(BaseModel):
    messages: Annotated[list[AnyMessage], operator.add]

system_prompt = """
あなたの責務は AWS ドキュメントを検索し Markdown 形式としてファイル出力することです。
- 検索後 Markdown 形式に変換すること
- 検索は最大 2 回までとし、その時点での情報を出力すること
"""
async def agent(state: AgentState) -> Dict[str, list[AIMessage]]:
    response = await llm_with_tools.ainvoke(
        [SystemMessage(system_prompt)] + state.messages,
    )
    return {"messages": [response]}

# ルーティング関数:
# tools node か end node に遷移する。
def route_node(state: AgentState) -> str:
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError("Last message must be an AIMessage")
    if not last_message.tool_calls:
        return END
    return "tools"

async def main():
    await initialize_llm()

    builder = StateGraph(AgentState)
    builder.add_node("agent", agent)
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", route_node)
    builder.add_edge("tools", "agent")
    
    graph = builder.compile(name="ReAct Agent")
    
    question = "Bedrock で利用可能なモデルプロバイダーって何？"
    response = await graph.ainvoke(
        {"messages": [HumanMessage(question)]}
    )
    print(response)
    return response

asyncio.run(main())
