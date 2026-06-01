import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

API_KEY = os.getenv("API_KEY")

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")

TEMPERATURE = float(os.getenv("TEMPERATURE"))

MAX_TOKENS = int(os.getenv("MAX_TOKENS"))

MAX_HISTORY_MESSAGES = int(
    os.getenv("MAX_HISTORY_MESSAGES")
)

SUMMARY_TRIGGER_MESSAGES = int(
    os.getenv("SUMMARY_TRIGGER_MESSAGES")
)

MODEL_INFO = {

    "google/gemma-3-1b": {
        "parameters": "1B",
        "family": "Gemma",
        "type": "General Chat",
        "speed": "Very Fast"
    },

    "deepseek-r1-distill-qwen-14b": {
        "parameters": "14B",
        "family": "DeepSeek",
        "type": "Reasoning",
        "speed": "Slow"
    },

    "phi-3-mini-3.8b-instructiontuned-alpaca": {
        "parameters": "3.8B",
        "family": "Phi",
        "type": "General Chat",
        "speed": "Medium"
    },

    "qwen2.5-1.5b-instruct": {
        "parameters": "1.5B",
        "family": "Qwen",
        "type": "General Chat",
        "speed": "Fast"
    },

    "qwen2.5-coder-1.5b-instruct": {
        "parameters": "1.5B",
        "family": "Qwen",
        "type": "Coding",
        "speed": "Fast"
    }
}