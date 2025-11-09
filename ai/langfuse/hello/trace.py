from logging import config
from mimetypes import init
import os
from pydoc_data import topics
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
# from langchain.agents import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langfuse.langchain import CallbackHandler


from dotenv import load_dotenv
from langfuse import observe

from decorator import web_search


load_dotenv()

web_search = TavilySearch(
    max_results=2,
    topic="general",
)

tools = [web_search]
llm = init_chat_model(
    model="claude-sonnet-4-5-20250929",
)

# ReAct agent の構築。
agent = create_react_agent(llm, tools)

langfuse_handler = CallbackHandler()

messages = agent.invoke(
    {
        "messages": [
            ("human", "AI エージェントの最新動向を教えてください。検索は1度のみで良いです。")
        ]
    },
    # callback func に langfuse を渡す。
    # これだけで langfuse でのトレースがあああああ！！
    config={"callbacks": [langfuse_handler]},
)

for msg in messages["messages"]:
    msg.pretty_print()
