from openai import OpenAI

from src.config import (
    MODEL_NAME,
    BASE_URL,
    API_KEY,
    TEMPERATURE,
    MAX_TOKENS
)


client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


def ask_llm(messages):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    return response.choices[0].message.content