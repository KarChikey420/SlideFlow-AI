from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_KEY")
if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_KEY in .env")

llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",  
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    temperature=0.7,
    max_tokens=800,
)
