import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load env from root
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("❌ API key is missing!")

# Connect to OpenRouter instead of OpenAI
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

def get_learning_plan(prompt):
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",  # ✅ open-access model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
