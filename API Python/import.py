import json
import os # This lets us talk to the operating system (Windows/Mac)
from dotenv import load_dotenv # A tool to read your .env file
from openai import OpenAI 

# Load the secret key from the .env file
load_dotenv() 
api_key = os.getenv("OPENAI_API_KEY")