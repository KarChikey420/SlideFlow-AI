import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  
    api_key=os.getenv("API_KEY")              
)

response = client.chat.completions.create(
    model="moonshotai/kimi-k2-thinking",
    messages=[
        {"role": "user", "content": "give me a presentation outline on the topic of artificial intelligence in healthcare."}
    ],
    temperature=0.6,
    max_tokens=1500,  
)


print(response.choices[0].message.content)
