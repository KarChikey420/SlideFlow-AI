from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("API_KEY")

kimi_llm = ChatOpenAI(
    api_key=OPENROUTER_API_KEY,  
    base_url="https://openrouter.ai/api/v1",
    model="moonshotai/kimi-k2-thinking",
    temperature=0.7,
    max_tokens=1500
)
