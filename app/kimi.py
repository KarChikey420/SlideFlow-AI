from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

KIMI_API_KEY = os.getenv("API_KEY")
if not KIMI_API_KEY:
    raise ValueError("KIMI_API_KEY is missing! Add it to your .env file.")

BASE_URL = "https://openrouter.ai/api/v1"

def get_kimi_model(
    model_name: str = "moonshotai/kimi-k2-thinking",
    temperature: float = 0.7,
    max_tokens: int | None = None,
):
    """
    Create a customized Kimi LLM instance.
    Use this if you need multiple variations of Kimi.
    """
    return ChatOpenAI(
        api_key=KIMI_API_KEY,
        base_url=BASE_URL,
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
    )

kimi_llm = get_kimi_model(max_tokens=1000)

