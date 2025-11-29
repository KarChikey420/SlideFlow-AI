from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

kimi_llm = ChatOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="moonshotai/kimi-k2-thinking",
    temperature=0.7
)
