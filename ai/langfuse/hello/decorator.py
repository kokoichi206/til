import os
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from tavily import TavilyClient


from dotenv import load_dotenv
from langfuse import observe


load_dotenv()

llm = init_chat_model(
    model="claude-sonnet-4-5-20250929",
)


@observe(name="paooonn")
def create_query(query: str):
    system_prompt = """ユーザーからの問い合わせ内容を Web 検索してレポートを作成します。
Web 検索用のクエリを 1 つ作成してください。検索単語以外は回答しないでください。"""

    prompt = f"ユーザーの質問: {query}"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ]

    response = llm.invoke(messages)
    return response.content


tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

@observe
def web_search(query: str):
    search_result = tavily_client.search(query=query, num_results=3)
    return [doc["content"] for doc in search_result["results"]]

@observe
def create_repost(query: str, contents: list[str]):
    system_prompt = """以下の Web 検索結果をもとに、ユーザーの問い合わせ内容に対するレポートを作成してください。
レポートは日本語で作成してください。"""
    prompt = f"ユーザーの質問: {query}\n\nWeb 検索結果:\n" + "\n".join(contents)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ]

    response = llm.invoke(messages)
    return response.content


@observe
def workflow(query: str):
    search_query = create_query(query)
    contents = web_search(search_query)
    report = create_repost(query, contents)
    return report


query = "LangChain と LangGraph のユースケースの違いについて教えてください。"

report = workflow(query)
print("=== Report ===")
print(report)
