from groq import Groq

from src.config import (
    GROQ_API_KEY,
    DEFAULT_MODEL,
    MAX_HISTORY_MESSAGES,
    SUMMARY_TRIGGER_MESSAGES,
)

client = Groq(
    api_key=GROQ_API_KEY
)


def get_available_models():
    return [DEFAULT_MODEL]


def normalize_messages(messages):

    cleaned = []

    for message in messages:

        role = message.get("role")

        if role not in (
            "user",
            "assistant",
        ):
            continue

        content = str(
            message.get(
                "content",
                ""
            )
        ).strip()

        if not content:
            continue

        cleaned.append(
            {
                "role": role,
                "content": content,
            }
        )

    return cleaned


def ask_llm(
    messages,
    model_name,
):

    response = client.chat.completions.create(
        model=model_name,
        messages=normalize_messages(
            messages
        ),
    )

    return (
        response
        .choices[0]
        .message.content
    )


def stream_llm(
    messages,
    model_name,
):

    stream = client.chat.completions.create(
        model=model_name,
        messages=normalize_messages(
            messages
        ),
        stream=True,
    )

    for chunk in stream:

        content = (
            chunk
            .choices[0]
            .delta.content
        )

        if content:

            yield {
                "type": "token",
                "content": content,
            }

    yield {
        "type": "finish",
        "reason": "stop",
    }


SUMMARY_SYSTEM_PROMPT = """
Summarize the conversation.
Keep:
- facts
- preferences
- decisions
- tasks
- constraints
Return only the summary.
"""


def generate_summary(
    messages,
    model_name,
    previous_summary="",
):

    transcript = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in messages
        ]
    )

    prompt = f"""
Previous Summary:

{previous_summary}

Conversation:

{transcript}

Generate an updated summary.
"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return (
        response
        .choices[0]
        .message.content
    )


def build_context_for_llm(chat):

    messages = normalize_messages(
        chat["messages"]
    )

    context = []

    if len(messages) < SUMMARY_TRIGGER_MESSAGES:
        return messages

    summary = chat.get(
        "summary",
        ""
    )

    if summary:

        context.append(
            {
                "role": "system",
                "content":
                f"Conversation Summary:\n{summary}"
            }
        )

    context.extend(
        messages[
            -MAX_HISTORY_MESSAGES:
        ]
    )

    return context


def update_summary_if_needed(
    chat,
    model_name,
):

    return chat


def continue_response(
    messages,
    model_name,
):
    return stream_llm(
        messages,
        model_name,
    )


def get_model_details(
    model_name,
):

    return {
        "name": model_name,
        "owned_by": "Groq",
    }