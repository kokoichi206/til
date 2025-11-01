import asyncio
import boto3
import operator
import os

from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel
from typing import Annotated, Dict

from dotenv import load_dotenv

load_dotenv()

web_search = TavilySearch(max_results=2)


@tool
def send_aws_sns(text: str):
    """テキストを AWS SNS のトピックに Publish するツール"""
    topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")
    sns_client.publish(TopicArn=topic_arn, Message=text)


tools = [web_search, send_aws_sns]

llm_with_tools = init_chat_model(
    # # supported models:
    # # https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/models-supported.html
    # # us. をつけると全リージョンから取得されるため rate limit を受けづらくなる。
    # model="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    # model_provider="bedrock_converse",
    #
    # bedrock が支払いでこけたため anthropic から直接使う。
    model="claude-sonnet-4-5-20250929",
).bind_tools(tools)


class AgentState(BaseModel):
    messages: Annotated[list[AnyMessage], operator.add]


builder = StateGraph(AgentState)

system_prompt = """
あなたの責務はユーザーからの質問を調査し、結果を要約して AWS SNS に送ることです。
検索は１回のみとしてください。
"""


async def agent(state: AgentState) -> Dict[str, list[AIMessage]]:
    response = await llm_with_tools.ainvoke(
        [SystemMessage(system_prompt)] + state.messages,
    )
    return {"messages": [response]}


builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))


def route_node(state: AgentState) -> str:
    last_message = state.messages[-1]
    if not last_message.tool_calls:
        return END
    return "tools"


builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", route_node)
builder.add_edge("tools", "agent")

graph = builder.compile()


async def main():
    question = "LangGraph の基本をやさしく解説して！"
    response = await graph.ainvoke({"messages": [HumanMessage(question)]})
    return response


response = asyncio.run(main())
print(response)
