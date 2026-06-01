from openai import OpenAI

from src.config import (
    BASE_URL,
    API_KEY,
    TEMPERATURE,
    MAX_TOKENS,
    MAX_HISTORY_MESSAGES,
    SUMMARY_TRIGGER_MESSAGES,
)

# --------------------------------------------------
# Client
# --------------------------------------------------

client = OpenAI(
    base_url=BASE_URL or "http://127.0.0.1:1234/v1",
    api_key=API_KEY or "lm-studio",
)

# --------------------------------------------------
# Available Models
# --------------------------------------------------


def get_available_models():
    try:
        models = client.models.list()

        model_names = []

        for model in models.data:
            model_name = model.id.lower()

            if "embedding" in model_name:
                continue

            model_names.append(model.id)

        model_names.sort()
        return model_names

    except Exception as e:
        print(f"Error loading models: {e}")
        return []


# --------------------------------------------------
# Message Cleanup
# --------------------------------------------------


def normalize_messages(messages):
    """
    Clean message history before sending to LM Studio.

    Rules:
    - keep only user/assistant roles
    - drop empty messages
    - merge consecutive messages with the same role
    - drop any leading assistant messages so the sequence starts with user
    """
    cleaned = []

    for message in messages:
        role = message.get("role")

        if role not in ("user", "assistant"):
            continue

        content = str(message.get("content", "")).strip()
        if not content:
            continue

        if not cleaned:
            cleaned.append(
                {
                    "role": role,
                    "content": content,
                }
            )
            continue

        previous_role = cleaned[-1]["role"]

        if previous_role == role:
            cleaned[-1]["content"] += "\n\n" + content
        else:
            cleaned.append(
                {
                    "role": role,
                    "content": content,
                }
            )

    # LM Studio prompt templates can fail if the first non-system message
    # is assistant. Drop any leading assistant messages defensively.
    while cleaned and cleaned[0]["role"] == "assistant":
        cleaned.pop(0)

    return cleaned


def _messages_to_transcript(messages):
    cleaned_messages = normalize_messages(messages)

    lines = []
    for index, message in enumerate(cleaned_messages, start=1):
        role = message.get("role", "unknown").title()
        content = message.get("content", "").strip()
        if content:
            lines.append(f"{index}. {role}: {content}")

    return "\n".join(lines)


# --------------------------------------------------
# Normal Response
# --------------------------------------------------


def ask_llm(messages, model_name):
    messages = normalize_messages(messages)

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    return response.choices[0].message.content


# --------------------------------------------------
# Streaming Response
# --------------------------------------------------


def stream_llm(messages, model_name):
    messages = normalize_messages(messages)

    stream = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        stream=True,
    )

    finish_reason = None

    for chunk in stream:
        if not chunk.choices:
            continue

        choice = chunk.choices[0]

        if choice.finish_reason:
            finish_reason = choice.finish_reason

        delta = choice.delta.content

        if delta:
            yield {
                "type": "token",
                "content": delta,
            }

    yield {
        "type": "finish",
        "reason": finish_reason,
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
- Do not add commentary.
- Return only the summary text.
""".strip()

SUMMARY_UPDATE_SYSTEM_PROMPT = """
You are updating an existing memory summary for a chatbot conversation.

Preserve:
- important facts
- names
- preferences
- decisions
- constraints
- open tasks
- unresolved questions

Rules:
- Merge the old summary with the new conversation.
- Remove repetition.
- Keep it concise.
- Do not invent facts.
- Return only the updated summary text.
""".strip()


def generate_summary(messages, model_name, previous_summary=""):
    transcript = _messages_to_transcript(messages)

    if previous_summary.strip():
        summary_messages = [
            {
                "role": "system",
                "content": SUMMARY_UPDATE_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""Previous summary:

{previous_summary.strip()}

New conversation messages:

{transcript}

Return only the updated summary text.
""",
            },
        ]
    else:
        summary_messages = [
            {
                "role": "system",
                "content": SUMMARY_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""Conversation messages:

{transcript}

Return only the summary text.
""",
            },
        ]

    response = client.chat.completions.create(
        model=model_name,
        messages=summary_messages,
        temperature=0,
        max_tokens=300,
    )

    return response.choices[0].message.content


# --------------------------------------------------
# Build Context
# --------------------------------------------------


def build_context_for_llm(chat):
    messages = normalize_messages(chat["messages"])

    context = [
        {
            "role": "system",
            "content": chat["system_prompt"],
        }
    ]

    if len(messages) < SUMMARY_TRIGGER_MESSAGES:
        context.extend(messages)
        return context

    summary = chat.get("summary", "").strip()
    if summary:
        context.append(
            {
                "role": "system",
                "content": f"""
Conversation Summary

{summary}
""".strip(),
            }
        )

    if MAX_HISTORY_MESSAGES > 0:
        context.extend(messages[-MAX_HISTORY_MESSAGES:])
    else:
        context.extend(messages)

    return context


# --------------------------------------------------
# Auto Summary Update
# --------------------------------------------------


def update_summary_if_needed(chat, model_name):
    message_count = len(chat.get("messages", []))
    last_summary_count = chat.get("last_summary_count", 0)

    if message_count < SUMMARY_TRIGGER_MESSAGES:
        return chat

    if (message_count - last_summary_count) < SUMMARY_TRIGGER_MESSAGES:
        return chat

    try:
        previous_summary = chat.get("summary", "").strip()
        source_messages = chat["messages"][last_summary_count:] if last_summary_count > 0 else chat["messages"]

        summary = generate_summary(
            source_messages,
            model_name,
            previous_summary=previous_summary,
        )

        chat["summary"] = summary
        chat["last_summary_count"] = message_count

    except Exception as e:
        print(f"Summary generation failed: {e}")

    return chat


# --------------------------------------------------
# Continue Function
# --------------------------------------------------


def continue_response(messages, model_name):
    continuation_messages = normalize_messages(messages)

    continuation_messages.append(
        {
            "role": "user",
            "content": """
Continue exactly where the previous assistant response stopped.

Rules:
- Continue from the exact point where the answer stopped.
- Do not restart.
- Do not repeat.
- Do not summarize.
- Do not explain what you are doing.
- Do not write things like:
  "Continuing..."
  "Certainly"
  "Let's continue"
  "Here is the next part"

Output only the continuation text.
""".strip(),
        }
    )

    return stream_llm(
        continuation_messages,
        model_name,
    )


# --------------------------------------------------
# get_model_details
# --------------------------------------------------


def get_model_details(model_name):
    try:
        models = client.models.list()

        for model in models.data:
            if model.id == model_name:
                return {
                    "name": model.id,
                    "owned_by": getattr(model, "owned_by", "Unknown"),
                }

        return {}

    except Exception:
        return {}