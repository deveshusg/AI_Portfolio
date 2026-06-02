# ==================================================
# IMPORTS
# ==================================================
#
# os
# --------------------------------------------------
# Reads values from local .env files.
#
# streamlit
# --------------------------------------------------
# Reads values from Streamlit Cloud secrets.
#
# dotenv
# --------------------------------------------------
# Loads .env file automatically when running
# locally.
#
# ==================================================

import os

import streamlit as st

from dotenv import load_dotenv

from src.model_manager import (
    DEFAULT_MODEL as MODEL_MANAGER_DEFAULT
)

# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================
#
# Purpose
# --------------------------------------------------
# Loads values from .env when running locally.
#
# Streamlit Cloud ignores .env and instead uses
# secrets.toml.
#
# ==================================================

load_dotenv()

# ==================================================
# SECRET MANAGEMENT
# ==================================================
#
# Purpose
# --------------------------------------------------
# Unified way of reading configuration values.
#
# Priority
# --------------------------------------------------
# 1. .env
# 2. Streamlit Secrets
# 3. Default Value
#
# This allows the same code to run both:
#
# - Locally
# - Streamlit Cloud
#
# ==================================================

def get_secret(
    key,
    default=None
):

    value = os.getenv(
        key
    )

    if value:

        return value

    try:

        return st.secrets.get(
            key,
            default
        )

    except Exception:

        return default

# ==================================================
# API CONFIGURATION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Stores credentials and model defaults.
#
# ==================================================

GROQ_API_KEY = get_secret(
    "GROQ_API_KEY"
)

DEFAULT_MODEL = get_secret(
    "GROQ_MODEL",
    MODEL_MANAGER_DEFAULT
)

# ==================================================
# MODEL SETTINGS
# ==================================================
#
# Purpose
# --------------------------------------------------
# Controls generation behavior.
#
# Temperature
# --------------------------------------------------
# Higher:
#     More creative.
#
# Lower:
#     More deterministic.
#
# ==================================================

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

# ==================================================
# MEMORY SETTINGS
# ==================================================
#
# Purpose
# --------------------------------------------------
# Controls conversation memory behavior.
#
# MAX_HISTORY_MESSAGES
# --------------------------------------------------
# Number of recent messages included after
# summarization.
#
# SUMMARY_TRIGGER_MESSAGES
# --------------------------------------------------
# Number of messages required before automatic
# summary generation can occur.
#
# ==================================================

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

# ==================================================
# MODEL INFORMATION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Supplies metadata to the sidebar.
#
# Displayed In:
# --------------------------------------------------
# Sidebar
# → Model Details
#
# ==================================================

MODEL_INFO = {

    "groq/compound": {

        "parameters":
        "Compound",

        "family":
        "Groq",

        "type":
        "Multi-Model System",

        "speed":
        "Very Fast"
    },

    "groq/compound-mini": {

        "parameters":
        "Mini",

        "family":
        "Groq",

        "type":
        "Multi-Model System",

        "speed":
        "Very Fast"
    },

    "openai/gpt-oss-120b": {

        "parameters":
        "120B",

        "family":
        "GPT-OSS",

        "type":
        "Open Model",

        "speed":
        "Fast"
    },

    "openai/gpt-oss-20b": {

        "parameters":
        "20B",

        "family":
        "GPT-OSS",

        "type":
        "Open Model",

        "speed":
        "Very Fast"
    },

    "qwen/qwen3-32b": {

        "parameters":
        "32B",

        "family":
        "Qwen",

        "type":
        "LLM",

        "speed":
        "Fast"
    },

    "meta-llama/llama-4-scout-17b-16e-instruct": {

        "parameters":
        "17B",

        "family":
        "Llama 4",

        "type":
        "MoE",

        "speed":
        "Fast"
    },

    "llama-3.3-70b-versatile": {

        "parameters":
        "70B",

        "family":
        "Llama 3.3",

        "type":
        "LLM",

        "speed":
        "Fast"
    }
}