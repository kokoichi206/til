from langchain.chat_models import init_chat_model
from langfuse.langchain import CallbackHandler

from dotenv import load_dotenv


load_dotenv()

llm = init_chat_model(
    model="claude-sonnet-4-5-20250929",
)

langfuse_handler = CallbackHandler()
config = {"callbacks": [langfuse_handler]}

response = llm.invoke("こんちわ！", config=config)
print(response)
