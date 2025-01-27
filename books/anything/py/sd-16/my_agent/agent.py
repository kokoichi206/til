from functools import lru_cache
from typing import Annotated, ClassVar, Literal, Sequence, Union
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langgraph.graph import add_messages, StateGraph, END, START
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode


class AgentState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], add_messages]


class GraphConfig(BaseModel):
    ANTHROPIC: ClassVar[str] = "anthropic"
    OPENAI: ClassVar[str] = "openai"

    model_name: Literal[ANTHROPIC, OPENAI]


@lru_cache(maxsize=2)
def _get_model(model_name: str) -> ChatOpenAI | ChatAnthropic:
    if model_name == GraphConfig.OPENAI:
        model = ChatOpenAI(temperature=0, model_name="gpt-4o")
    elif model_name == GraphConfig.ANTHROPIC:
        model = ChatAnthropic(temperature=0, model_name="claude-3.5-sonnet-20241022")
    else:
        raise ValueError(f"Unknown model name: {model_name}")

    model = model.bind_tools(tools)
    return model


tools = [TavilySearchResults(max_results=1)]
tool_node = ToolNode(tools)


# define whether the agent should continue or end
def should_continue(state: AgentState) -> Literal["end", "continue"]:
    last_message = state.messages[-1]
    return "continue" if last_message.tool_calls else "end"


# execute the model
def call_model(state: AgentState, config: GraphConfig) -> dict:
    messages = state.messages
    messages = [{"role": "system", "content": "u are a helpful assistant."}] + messages
    model_name = config.get("configurable", {}).get("model_name", "anthropic")
    model = _get_model(model_name)
    response = model.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(AgentState, config_schema=GraphConfig)

workflow.add_node("call_model", call_model)
workflow.add_node("tool_node", tool_node)

workflow.add_edge(START, "call_model")
workflow.add_conditional_edges(
    "call_model",
    should_continue,
    {
        "continue": "tool_node",
        "end": END,
    },
)
workflow.add_edge("tool_node", "call_model")

graph = workflow.compile()
