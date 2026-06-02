
import google.generativeai as genai

from src.config import (
    GEMINI_API_KEY,
    DEFAULT_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    MAX_HISTORY_MESSAGES,
    SUMMARY_TRIGGER_MESSAGES,
)

genai.configure(
    api_key=GEMINI_API_KEY
)


# --------------------------------------------------
# Available Models
# --------------------------------------------------

def get_available_models():
    return [DEFAULT_MODEL]


# --------------------------------------------------
# Message Cleanup
# --------------------------------------------------

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
                "",
            )
        ).strip()

        if not content:
            continue

        if (
            cleaned
            and cleaned[-1]["role"] == role
        ):
            cleaned[-1]["content"] += (
                "\n\n" + content
            )
        else:
            cleaned.append(
                {
                    "role": role,
                    "content": content,
                }
            )

    while (
        cleaned
        and cleaned[0]["role"]
        == "assistant"
    ):
        cleaned.pop(0)

    return cleaned


def _messages_to_transcript(messages):

    cleaned_messages = normalize_messages(
        messages
    )

    lines = []

    for index, message in enumerate(
        cleaned_messages,
        start=1,
    ):
        role = (
            message.get(
                "role",
                "unknown",
            ).title()
        )

        content = message.get(
            "content",
            "",
        ).strip()

        if content:
            lines.append(
                f"{index}. {role}: {content}"
            )

    return "\n".join(lines)


# --------------------------------------------------
# Gemini Helpers
# --------------------------------------------------

def _convert_messages(messages):

    converted = []

    for message in messages:

        role = (
            "user"
            if message["role"] == "user"
            else "model"
        )

        converted.append(
            {
                "role": role,
                "parts": [
                    message["content"]
                ],
            }
        )

    return converted


# --------------------------------------------------
# Normal Response
# --------------------------------------------------

def ask_llm(
    messages,
    model_name,
):

    model = genai.GenerativeModel(
        model_name
    )

    response = model.generate_content(
        _convert_messages(
            normalize_messages(
                messages
            )
        )
    )

    return response.text


# --------------------------------------------------
# Streaming Response
# --------------------------------------------------

def stream_llm(
    messages,
    model_name,
):

    model = genai.GenerativeModel(
        model_name
    )

    stream = model.generate_content(
        _convert_messages(
            normalize_messages(
                messages
            )
        ),
        stream=True,
    )

    for chunk in stream:

        if chunk.text:

            yield {
                "type": "token",
                "content": chunk.text,
            }

    yield {
        "type": "finish",
        "reason": "stop",
    }


# --------------------------------------------------
# Generate Summary
# --------------------------------------------------

SUMMARY_SYSTEM_PROMPT = """
You are generating a memory summary for a chatbot conversation.

Preserve:
- important facts
- names
- preferences
- decisions
- constraints
- open tasks
- unresolved questions

Rules:
- Be concise.
- Do not invent facts.
- Return only the summary.
""".strip()


def generate_summary(
    messages,
    model_name,
    previous_summary="",
):

    transcript = (
        _messages_to_transcript(
            messages
        )
    )

    prompt = f"""
Previous Summary:

{previous_summary}

Conversation:

{transcript}

Generate an updated summary.
"""

    model = genai.GenerativeModel(
        model_name
    )

    response = model.generate_content(
        prompt
    )

    return response.text


# --------------------------------------------------
# Build Context
# --------------------------------------------------

def build_context_for_llm(chat):

    messages = normalize_messages(
        chat["messages"]
    )

    context = []

    if len(messages) < SUMMARY_TRIGGER_MESSAGES:

        context.extend(messages)

        return context

    summary = (
        chat.get(
            "summary",
            "",
        )
        .strip()
    )

    if summary:

        context.append(
            {
                "role": "user",
                "content": (
                    f"Conversation Summary:\n\n"
                    f"{summary}"
                ),
            }
        )

    if MAX_HISTORY_MESSAGES > 0:

        context.extend(
            messages[
                -MAX_HISTORY_MESSAGES:
            ]
        )

    else:

        context.extend(messages)

    return context


# --------------------------------------------------
# Auto Summary Update
# --------------------------------------------------

def update_summary_if_needed(
    chat,
    model_name,
):

    message_count = len(
        chat.get(
            "messages",
            [],
        )
    )

    last_summary_count = chat.get(
        "last_summary_count",
        0,
    )

    if (
        message_count
        < SUMMARY_TRIGGER_MESSAGES
    ):
        return chat

    if (
        message_count
        - last_summary_count
    ) < SUMMARY_TRIGGER_MESSAGES:
        return chat

    try:

        previous_summary = (
            chat.get(
                "summary",
                "",
            )
            .strip()
        )

        source_messages = (
            chat["messages"][
                last_summary_count:
            ]
            if last_summary_count > 0
            else chat["messages"]
        )

        summary = generate_summary(
            source_messages,
            model_name,
            previous_summary,
        )

        chat["summary"] = summary

        chat[
            "last_summary_count"
        ] = message_count

    except Exception as e:

        print(
            f"Summary failed: {e}"
        )

    return chat


# --------------------------------------------------
# Continue
# --------------------------------------------------

def continue_response(
    messages,
    model_name,
):
    return stream_llm(
        messages,
        model_name,
    )


# --------------------------------------------------
# Model Details
# --------------------------------------------------

def get_model_details(
    model_name,
):

    return {
        "name": model_name,
        "owned_by": "Google",
    }
