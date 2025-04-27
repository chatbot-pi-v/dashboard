import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
HEADERS = {"Authorization": f"Bearer {os.getenv('API_TOKEN')}"}

# AUDIO_DIR = "../audio"
# OUTPUT_DIR = "../output"

# os.makedirs(OUTPUT_DIR, exist_ok=True)
