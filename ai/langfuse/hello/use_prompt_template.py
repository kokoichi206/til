from langfuse.langchain import CallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langfuse import get_client


load_dotenv()


def create_agent(model: str, temperature: float):
    llm = init_chat_model(
        model=model,
        temperature=temperature,
    )
    tools = [TavilySearch(max_results=2, topic="general")]
    return create_react_agent(llm, tools)

lf = get_client()

prompt_template = lf.get_prompt(
    "ai-agent",
    type="chat",
    label="latest",
)

model = prompt_template.config["model"]
temperature = prompt_template.config.get("temperature", 0.7)

# Langfuse からの prompt を LangChain 用に変換。
langchain_prompt = ChatPromptTemplate(
    prompt_template.get_langchain_prompt(),
)

messages = langchain_prompt.invoke({"city": "京都"})

agent = create_agent(model=model, temperature=temperature)

langfuse_handler = CallbackHandler()

response = agent.invoke(
    messages,
    config={"callbacks": [langfuse_handler]},
)

response["messages"][-1].pretty_print()
