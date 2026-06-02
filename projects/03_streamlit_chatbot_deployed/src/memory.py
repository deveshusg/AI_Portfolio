# ==================================================
# IMPORTS
# ==================================================
#
# json
# --------------------------------------------------
# Stores conversations as JSON files.
#
# pathlib
# --------------------------------------------------
# Cross-platform file and folder handling.
#
# datetime
# --------------------------------------------------
# Creates timestamps for chats and messages.
#
# shutil
# --------------------------------------------------
# Used for exporting chat files.
#
# ==================================================

import json

from pathlib import Path

from datetime import datetime

import shutil

from src.prompts import (
    DEFAULT_SYSTEM_PROMPT
)

# ==================================================
# PROJECT PATHS
# ==================================================
#
# Purpose
# --------------------------------------------------
# Centralized location for all project folders.
#
# Folder Structure
# --------------------------------------------------
#
# project/
#
# ├── data/
# │   ├── conversations/
# │   └── exports/
#
# ==================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

CONVERSATIONS_DIR = (
    PROJECT_ROOT
    / "data"
    / "conversations"
)

EXPORTS_DIR = (
    PROJECT_ROOT
    / "data"
    / "exports"
)

# ==================================================
# DIRECTORY CREATION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Automatically creates folders if they do
# not already exist.
#
# This allows first-time project startup
# without manual setup.
#
# ==================================================

CONVERSATIONS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==================================================
# CREATE CHAT
# ==================================================
#
# Purpose
# --------------------------------------------------
# Creates a brand-new conversation object.
#
# Stored Fields
# --------------------------------------------------
# chat_id
# title
# model
# timestamps
# summary
# message history
#
# ==================================================

def create_chat(
    model_name
):

    timestamp = (
        datetime.now()
    )

    chat_id = (
        timestamp.strftime(
            "chat_%Y%m%d_%H%M%S"
        )
    )

    return {

        "chat_id":
        chat_id,

        "title":
        "New Chat",

        "model":
        model_name,

        "created_at":
        timestamp.isoformat(),

        "updated_at":
        timestamp.isoformat(),

        "system_prompt":
        DEFAULT_SYSTEM_PROMPT,

        "summary":
        "",

        "last_summary_count":
        0,

        "last_finish_reason":
        None,

        "messages":
        []
    }

# ==================================================
# SAVE CHAT
# ==================================================
#
# Purpose
# --------------------------------------------------
# Writes a conversation to disk.
#
# Storage Format
# --------------------------------------------------
# JSON
#
# ==================================================

def save_chat(
    chat_data
):

    chat_file = (

        CONVERSATIONS_DIR

        /

        f"{chat_data['chat_id']}.json"

    )

    chat_data[
        "updated_at"
    ] = datetime.now().isoformat()

    with open(
        chat_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chat_data,
            file,
            indent=4,
            ensure_ascii=False
        )

# ==================================================
# LOAD CHAT
# ==================================================
#
# Purpose
# --------------------------------------------------
# Reads a conversation from disk.
#
# Returns
# --------------------------------------------------
# dict
# None
#
# ==================================================

def load_chat(
    chat_id
):

    chat_file = (

        CONVERSATIONS_DIR

        /

        f"{chat_id}.json"

    )

    if not chat_file.exists():

        return None

    with open(
        chat_file,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(
            file
        )

# ==================================================
# LIST CHATS
# ==================================================
#
# Purpose
# --------------------------------------------------
# Returns metadata for every saved chat.
#
# Used By
# --------------------------------------------------
# Sidebar chat list.
#
# Sorted By
# --------------------------------------------------
# Most recently updated first.
#
# ==================================================

def list_chats():

    chats = []

    for file in (
        CONVERSATIONS_DIR.glob(
            "*.json"
        )
    ):

        try:

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as handle:

                chat = json.load(
                    handle
                )

                chats.append(
                    {

                        "chat_id":
                        chat["chat_id"],

                        "title":
                        chat["title"],

                        "model":
                        chat["model"],

                        "updated_at":
                        chat["updated_at"]
                    }
                )

        except Exception:

            continue

    chats.sort(
        key=lambda item:
        item["updated_at"],
        reverse=True
    )

    return chats

# ==================================================
# RENAME CHAT
# ==================================================
#
# Purpose
# --------------------------------------------------
# Updates a chat title.
#
# ==================================================

def rename_chat(
    chat_id,
    new_title
):

    chat = load_chat(
        chat_id
    )

    if chat is None:

        return False

    chat["title"] = (
        new_title
    )

    save_chat(
        chat
    )

    return True

# ==================================================
# DELETE CHAT
# ==================================================
#
# Purpose
# --------------------------------------------------
# Permanently removes a conversation.
#
# ==================================================

def delete_chat(
    chat_id
):

    chat_file = (

        CONVERSATIONS_DIR

        /

        f"{chat_id}.json"

    )

    if chat_file.exists():

        chat_file.unlink()

        return True

    return False

# ==================================================
# EXPORT CHAT AS JSON
# ==================================================
#
# Purpose
# --------------------------------------------------
# Copies the original conversation file into
# the exports folder.
#
# ==================================================

def export_chat_json(
    chat_id
):

    source_file = (

        CONVERSATIONS_DIR

        /

        f"{chat_id}.json"

    )

    export_file = (

        EXPORTS_DIR

        /

        f"{chat_id}.json"

    )

    if not source_file.exists():

        return False

    shutil.copy2(
        source_file,
        export_file
    )

    return True

# ==================================================
# EXPORT CHAT AS MARKDOWN
# ==================================================
#
# Purpose
# --------------------------------------------------
# Creates a human-readable Markdown version
# of the conversation.
#
# Useful For
# --------------------------------------------------
# Documentation
# Notes
# Research
# Knowledge Base Creation
#
# ==================================================

def export_chat_markdown(
    chat_id
):

    chat = load_chat(
        chat_id
    )

    if chat is None:

        return False

    markdown_file = (

        EXPORTS_DIR

        /

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

        file.write(
            "---\n\n"
        )

        for message in chat["messages"]:

            role = (
                message["role"]
                .title()
            )

            content = (
                message["content"]
            )

            file.write(
                f"## {role}\n\n"
            )

            file.write(
                f"{content}\n\n"
            )

    return True