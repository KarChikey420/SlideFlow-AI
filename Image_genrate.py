import os
import replicate
from dotenv import load_dotenv

load_dotenv()
os.environ["REPLICATE_API_TOKEN"] = os.getenv("IMAGE_API_KEY")

try:
    print("Using token:", os.getenv("IMAGE_API_KEY")[:10] + "********")

    image_prompt = "A futuristic AI robot working in a hospital, ultra modern, digital art"

    image_url = replicate.run(
        "black-forest-labs/flux-schnell",  # 🎯 Free & accessible
        input={
            "prompt": image_prompt
        }
    )

    print("\n🖼️ Image Generated Successfully!")
    print("📎 Image URL:", image_url[0])

except Exception as e:
    print("❌ Error generating image:", e)
