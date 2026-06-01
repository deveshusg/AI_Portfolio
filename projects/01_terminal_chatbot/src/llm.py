print("llm.py loaded")
from openai import OpenAI

from src.config import (
    MODEL_NAME,
    BASE_URL,
    API_KEY,
    TEMPERATURE,
    MAX_TOKENS
)

from src.prompts import SYSTEM_PROMPT


client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


def ask_llm(user_question):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_question
            }
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    return response.choices[0].message.content