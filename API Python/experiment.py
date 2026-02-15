import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    print("Error: Could not find the API key. Check your filename!")
else:
    print("Key loaded successfully!")