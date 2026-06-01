import os

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")

BASE_URL = os.getenv("BASE_URL")

API_KEY = os.getenv("API_KEY")

TEMPERATURE = float(os.getenv("TEMPERATURE"))

MAX_TOKENS = int(os.getenv("MAX_TOKENS"))