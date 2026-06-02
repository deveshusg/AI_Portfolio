import json
from pathlib import Path
from datetime import datetime
import shutil

from src.prompts import DEFAULT_SYSTEM_PROMPT


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONVERSATIONS_DIR = PROJECT_ROOT / "data" / "conversations"
EXPORTS_DIR = PROJECT_ROOT / "data" / "exports"

CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Create Chat
# --------------------------------------------------

def create_chat(model_name):

    timestamp = datetime.now()

    chat_id = timestamp.strftime("chat_%Y%m%d_%H%M%S")

    chat_data = {
    "chat_id": chat_id,
    "title": "New Chat",
    "model": model_name,
    "created_at": timestamp.isoformat(),
    "updated_at": timestamp.isoformat(),
    "system_prompt": DEFAULT_SYSTEM_PROMPT,
    "summary": "",
    "last_summary_count": 0,
    "last_finish_reason": None,
    "messages": []
    }

    return chat_data


# --------------------------------------------------
# Save Chat
# --------------------------------------------------

def save_chat(chat_data):

    chat_file = (
        CONVERSATIONS_DIR /
        f"{chat_data['chat_id']}.json"
    )

    chat_data["updated_at"] = datetime.now().isoformat()

    with open(chat_file, "w", encoding="utf-8") as file:

        json.dump(
            chat_data,
            file,
            indent=4,
            ensure_ascii=False
        )


# --------------------------------------------------
# Load Chat
# --------------------------------------------------

def load_chat(chat_id):

    chat_file = (
        CONVERSATIONS_DIR /
        f"{chat_id}.json"
    )

    if not chat_file.exists():

        return None

    with open(chat_file, "r", encoding="utf-8") as file:

        return json.load(file)


# --------------------------------------------------
# List Chats
# --------------------------------------------------

def list_chats():

    chats = []

    for file in CONVERSATIONS_DIR.glob("*.json"):

        try:

            with open(file, "r", encoding="utf-8") as f:

                chat = json.load(f)

                chats.append(
                    {
                        "chat_id": chat["chat_id"],
                        "title": chat["title"],
                        "model": chat["model"],
                        "updated_at": chat["updated_at"]
                    }
                )

        except Exception:

            continue

    chats.sort(
        key=lambda x: x["updated_at"],
        reverse=True
    )

    return chats


# --------------------------------------------------
# Rename Chat
# --------------------------------------------------

def rename_chat(chat_id, new_title):

    chat = load_chat(chat_id)

    if chat is None:

        return False

    chat["title"] = new_title

    save_chat(chat)

    return True


# --------------------------------------------------
# Delete Chat
# --------------------------------------------------

def delete_chat(chat_id):

    chat_file = (
        CONVERSATIONS_DIR /
        f"{chat_id}.json"
    )

    if chat_file.exists():

        chat_file.unlink()

        return True

    return False


# --------------------------------------------------
# Export JSON
# --------------------------------------------------

def export_chat_json(chat_id):

    source_file = (
        CONVERSATIONS_DIR /
        f"{chat_id}.json"
    )

    export_file = (
        EXPORTS_DIR /
        f"{chat_id}.json"
    )

    if not source_file.exists():

        return False

    shutil.copy2(
        source_file,
        export_file
    )

    return True


# --------------------------------------------------
# Export Markdown
# --------------------------------------------------

def export_chat_markdown(chat_id):

    chat = load_chat(chat_id)

    if chat is None:

        return False

    markdown_file = (
        EXPORTS_DIR /
        f"{chat_id}.md"
    )

    with open(
        markdown_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            f"# {chat['title']}\n\n"
        )

        file.write(
            f"Model: {chat['model']}\n\n"
        )

        file.write(
            f"Created: {chat['created_at']}\n\n"
        )

        file.write("---\n\n")

        for message in chat["messages"]:

            role = message["role"].title()

            content = message["content"]

            file.write(
                f"## {role}\n\n"
            )

            file.write(
                f"{content}\n\n"
            )

    return True