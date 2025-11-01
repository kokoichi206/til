from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_tavily import TavilySearch
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    AIMessage,
    ToolMessage,
    ToolCall,
)
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages


load_dotenv(override=True)

web_search = TavilySearch(max_results=2, topic="general")

working_directory = "report"

file_toolkit = FileManagementToolkit(
    root_dire=str(working_directory),
    selected_tools=["write_file"],
)
write_file = file_toolkit.get_tools()[0]

tools = [web_search, write_file]
tools_by_name = {tool.name: tool for tool in tools}

# LLM の初期化。
llm_with_tools = init_chat_model(
    model="claude-sonnet-4-5-20250929",
    timeout=300,
).bind_tools(tools)

system_prompt = """
あなたの責務はユーザからのリクエストを調査し、調査結果をファイル出力することです。
- ユーザーのリクエスト調査にWeb検索が必要であれば、Web検索ツールを使ってください。
- 必要な情報が集まったと判断したら検索は終了して下さい。
- 検索は最大2回までとしてください。
- ファイル出力はHTML形式(.html)に変換して保存してください。
  * Web検索が拒否された場合、Web検索を中止してレポート作成してください。
  * レポート保存を拒否された場合、レポート作成を中止し、内容をユーザーに直接伝えて下さい。
"""


@task
def invoke_llm(messages: list[BaseMessage]) -> AIMessage:
    response = llm_with_tools.invoke([SystemMessage(content=system_prompt)] + messages)
    return response


@task
def use_tool(tool_call):
    tool = tools_by_name[tool_call["name"]]
    observation = tool.invoke(tool_call["args"])
    return ToolMessage(content=observation, tool_call_id=tool_call["id"])


def ask_human(tool_call: ToolCall):
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    tool_data = {"name": tool_name}
    if tool_name == web_search.name:
        args = "* ツール名\n"
        args += f"  * {tool_name}\n"
        args += "* 引数一覧\n"
        for k, v in tool_args.items():
            args += f"  * {k}\n"
            args += f"   * {v}\n"
        tool_data["args"] = args
    elif tool_name == write_file.name:
        args = "* ツール名\n"
        args += f"  * {tool_name}\n"
        args += "* 保存ファイル名\n"
        args += f"  * {tool_args['file_path']}\n"
        tool_data["html"] = tool_args["text"]
    tool_data["args"] = args

    feedback = interrupt(tool_data)

    if feedback == "APPROVE":
        return tool_call

    return ToolMessage(
        content=f"ユーザーからツール使用が拒否されました: {tool_name}",
        name=tool_name,
        tool_call_id=tool_call["id"],
    )


checkpointer = MemorySaver()


@entrypoint(checkpointer)
def agent(messages):
    llm_response = invoke_llm(messages).result()

    while True:
        if not llm_response.tool_calls:
            break

        approved_tools = []
        tool_results = []

        for tool_call in llm_response.tool_calls:
            feedback = ask_human(tool_call)
            if isinstance(feedback, ToolMessage):
                tool_results.append(feedback)
            else:
                approved_tools.append(feedback)

        tool_futures = []
        for tool_call in approved_tools:
            future = use_tool(tool_call)
            tool_futures.append(future)

        # Future が完了するのを待ち、結果を回収する。
        tool_use_results = []
        for f in tool_futures:
            result = f.result()
            tool_use_results.append(result)

        messages = add_messages(
            messages,
            [llm_response, *tool_use_results, *tool_results],
        )

        llm_response = invoke_llm(messages).result()

    return llm_response
