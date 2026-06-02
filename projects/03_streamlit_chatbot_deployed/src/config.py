import os

import streamlit as st

from dotenv import load_dotenv

load_dotenv()


def get_secret(key, default=None):
    """
    Try .env first.
    If not found, use Streamlit secrets.
    """

    value = os.getenv(key)

    if value:
        return value

    try:
        return st.secrets.get(key, default)
    except Exception:
        return default


GROQ_API_KEY = get_secret(
    "GROQ_API_KEY"
)

DEFAULT_MODEL = get_secret(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

TEMPERATURE = float(
    get_secret(
        "TEMPERATURE",
        0.7
    )
)

MAX_TOKENS = int(
    get_secret(
        "MAX_TOKENS",
        1000
    )
)

MAX_HISTORY_MESSAGES = int(
    get_secret(
        "MAX_HISTORY_MESSAGES",
        10
    )
)

SUMMARY_TRIGGER_MESSAGES = int(
    get_secret(
        "SUMMARY_TRIGGER_MESSAGES",
        20
    )
)

MODEL_INFO = {
    DEFAULT_MODEL: {
        "parameters": "70B",
        "family": "Llama",
        "type": "Groq Cloud",
        "speed": "Very Fast"
    }
}