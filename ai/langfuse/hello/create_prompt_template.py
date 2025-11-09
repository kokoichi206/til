from dotenv import load_dotenv
from httpx import get
from langfuse import get_client


load_dotenv()

lf = get_client()

lf.create_prompt(
    name="ai-agent",
    type="chat",
    prompt=[
        {
            "role": "user",
            "content": "{{city}}の人口は？",
        }
    ],
    config={
        "model": "claude-sonnet-4-5-20250929",
        "temperature": 0.7,
    }
)
