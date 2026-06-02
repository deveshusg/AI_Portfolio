from groq import Groq

from src.config import (
    GROQ_API_KEY,
    DEFAULT_MODEL,
    MAX_HISTORY_MESSAGES,
    SUMMARY_TRIGGER_MESSAGES,
)

from src.model_manager import (
    AVAILABLE_MODELS,
)

# --------------------------------------------------
# Groq Client
# --------------------------------------------------
#
# Purpose:
# - Creates a single reusable connection to Groq.
# - All model requests use this client.
# - Prevents reconnecting on every request.
#
# --------------------------------------------------

client = Groq(
    api_key=GROQ_API_KEY
)

# --------------------------------------------------
# Error Translation
# --------------------------------------------------
#
# Purpose:
# - Convert technical provider errors into
#   user-friendly explanations.
#
# Returned Structure:
#
# {
#     "title": "...",
#     "message": "...",
#     "suggestion": "..."
# }
#
# Used By:
# - Chat generation
# - Future UI error cards
#
# --------------------------------------------------

def get_error_details(
    error_text,
):

    error_text = str(
        error_text
    )

    lower_text = (
        error_text.lower()
    )

    if (
        "429" in lower_text
        or
        "rate_limit" in lower_text
        or
        "tokens per day" in lower_text
        or
        "quota" in lower_text
    ):

        return {

            "title":
            "Model Usage Limit Reached",

            "message":
            (
                "This model has reached "
                "its daily usage limit."
            ),

            "suggestion":
            (
                "Wait for the limit to "
                "reset or choose another "
                "model."
            )
        }

    if (
        "413" in lower_text
        or
        "request_too_large" in lower_text
    ):

        return {

            "title":
            "Request Too Large",

            "message":
            (
                "The conversation became "
                "too large to process."
            ),

            "suggestion":
            (
                "Start a new chat or "
                "generate a summary."
            )
        }

    if (
        "401" in lower_text
        or
        "authentication" in lower_text
        or
        "api key" in lower_text
    ):

        return {

            "title":
            "Authentication Error",

            "message":
            (
                "The API key was rejected."
            ),

            "suggestion":
            (
                "Check your API key "
                "configuration."
            )
        }

    if (
        "timeout" in lower_text
    ):

        return {

            "title":
            "Request Timeout",

            "message":
            (
                "The model did not "
                "respond in time."
            ),

            "suggestion":
            (
                "Try again or use a "
                "different model."
            )
        }

    return {

        "title":
        "Unexpected Error",

        "message":
        (
            "The model returned an "
            "unexpected error."
        ),

        "suggestion":
        (
            "Try again."
        )
    }

# --------------------------------------------------
# Model Limit Detection
# --------------------------------------------------
#
# Purpose:
# - Used for future model exhaustion handling.
# - Currently retained because it is useful
#   and already integrated into the project.
#
# --------------------------------------------------

def is_model_limit_error(
    error_text,
):

    error_text = (
        str(error_text)
        .lower()
    )

    keywords = [

        "rate limit",

        "quota",

        "exceeded",

        "token",

        "too many requests",

        "429",
    ]

    return any(
        keyword in error_text
        for keyword in keywords
    )

# --------------------------------------------------
# Available Models
# --------------------------------------------------
#
# Purpose:
# - Supplies model names to the sidebar.
#
# --------------------------------------------------

def get_available_models():

    return AVAILABLE_MODELS

# --------------------------------------------------
# Message Normalization
# --------------------------------------------------
#
# Purpose:
# - Removes invalid messages.
# - Keeps only user/assistant roles.
# - Prevents malformed requests.
#
# --------------------------------------------------

def normalize_messages(
    messages
):

    cleaned = []

    for message in messages:

        role = message.get(
            "role"
        )

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

# --------------------------------------------------
# Non-Streaming Request
# --------------------------------------------------
#
# Purpose:
# - Generates a full response at once.
# - Currently used by summary generation
#   and utility workflows.
#
# --------------------------------------------------

def ask_llm(
    messages,
    model_name,
):

    try:

        response = (
            client.chat.completions.create(
                model=model_name,
                messages=normalize_messages(
                    messages
                ),
            )
        )

        return (
            response
            .choices[0]
            .message.content
        )

    except Exception as e:

        raise e

# --------------------------------------------------
# Streaming Request
# --------------------------------------------------
#
# Purpose:
# - Streams response tokens to the UI.
# - Produces ChatGPT-style typing.
# - Returns structured error objects instead
#   of crashing the application.
#
# Events Returned:
#
# token
# finish
# model_error
#
# --------------------------------------------------

def stream_llm(
    messages,
    model_name,
):

    try:

        stream = (
            client.chat.completions.create(
                model=model_name,
                messages=normalize_messages(
                    messages
                ),
                stream=True,
            )
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

    except Exception as e:

        yield {
            "type": "model_error",
            "error": str(e),
            "model": model_name,
            "friendly":
            get_error_details(
                str(e)
            )
        }

# --------------------------------------------------
# Summary Prompt
# --------------------------------------------------
#
# Purpose:
# - Defines what information should be
#   preserved inside memory summaries.
#
# --------------------------------------------------

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

# --------------------------------------------------
# Summary Generation
# --------------------------------------------------
#
# Purpose:
# - Compress older conversation history.
# - Prevent prompts from growing forever.
# - Uses only the most recent messages.
#
# Important:
# - Summaries always run on groq/compound.
# - This keeps memory independent from the
#   model selected by the user.
#
# --------------------------------------------------

def generate_summary(
    messages,
    model_name,
    previous_summary="",
):

    recent_messages = (
        messages[-20:]
    )

    transcript = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in recent_messages
        ]
    )

    prompt = f"""
Previous Summary:

{previous_summary}

Conversation:

{transcript}

Generate an updated summary.
"""

    response = (
        client.chat.completions.create(
            model="groq/compound",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
    )

    return (
        response
        .choices[0]
        .message.content
    )

# --------------------------------------------------
# Context Builder
# --------------------------------------------------
#
# Purpose:
# - Builds the final message list sent to
#   the language model.
#
# Strategy:
#
# Small Chats:
#     Send all messages.
#
# Large Chats:
#     Send:
#         Summary
#         +
#         Recent Messages
#
# Benefits:
# - Smaller prompts
# - Faster responses
# - Better scalability
#
# --------------------------------------------------

def build_context_for_llm(
    chat
):

    messages = normalize_messages(
        chat["messages"]
    )

    context = []

    if (
        len(messages)
        <
        SUMMARY_TRIGGER_MESSAGES
    ):

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
                (
                    "Conversation Summary:\n"
                    f"{summary}"
                )
            }
        )

    context.extend(
        messages[
            -MAX_HISTORY_MESSAGES:
        ]
    )

    return context

# --------------------------------------------------
# Automatic Summary Updates
# --------------------------------------------------
#
# Purpose:
# - Periodically refresh memory summaries.
#
# Trigger:
# - When the configured message threshold
#   is crossed.
#
# Safety:
# - Summary failures never stop the chat.
#
# --------------------------------------------------

def update_summary_if_needed(
    chat,
    model_name,
):

    messages = chat.get(
        "messages",
        []
    )

    current_count = len(
        messages
    )

    last_summary_count = chat.get(
        "last_summary_count",
        0
    )

    if (
        current_count
        <
        SUMMARY_TRIGGER_MESSAGES
    ):

        return chat

    if (
        current_count
        <
        last_summary_count
        +
        SUMMARY_TRIGGER_MESSAGES
    ):

        return chat

    try:

        summary = generate_summary(
            messages=messages,
            model_name=model_name,
            previous_summary=chat.get(
                "summary",
                ""
            )
        )

        chat["summary"] = (
            summary
        )

        chat[
            "last_summary_count"
        ] = current_count

    except Exception as e:

        print(
            f"Summary Error: {e}"
        )

    return chat

# --------------------------------------------------
# Continue Generation
# --------------------------------------------------
#
# Purpose:
# - Continue a response after truncation.
# - Reuses the same streaming pipeline.
#
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
# Model Metadata
# --------------------------------------------------
#
# Purpose:
# - Supplies model information to the UI.
# - Can be expanded later with context
#   window, speed, provider, etc.
#
# --------------------------------------------------

def get_model_details(
    model_name,
):

    return {
        "name": model_name,
        "owned_by": "Groq",
    }