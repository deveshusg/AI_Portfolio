# ==================================================
# MODEL MANAGEMENT
# ==================================================
#
# Purpose
# --------------------------------------------------
# Central location for:
#
# - Available models
# - Default model
# - Model display cleanup
#
# Why This File Exists
# --------------------------------------------------
# Keeps model-related configuration out of
# app.py and llm.py.
#
# When adding or removing models, only this
# file should need modification.
#
# ==================================================

# ==================================================
# AVAILABLE MODELS
# ==================================================
#
# Purpose
# --------------------------------------------------
# Models displayed in the sidebar dropdown.
#
# Ordering
# --------------------------------------------------
# Most recommended models appear first.
#
# ==================================================

AVAILABLE_MODELS = [

    "groq/compound",

    "groq/compound-mini",

    "openai/gpt-oss-120b",

    "openai/gpt-oss-20b",

    "qwen/qwen3-32b",

    "meta-llama/llama-4-scout-17b-16e-instruct",

    "llama-3.3-70b-versatile",
]

# ==================================================
# DEFAULT MODEL
# ==================================================
#
# Purpose
# --------------------------------------------------
# Used when:
#
# - User starts a new session
# - No model is selected
#
# ==================================================

DEFAULT_MODEL = (
    "groq/compound"
)

# ==================================================
# SESSION STATE INITIALIZATION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Ensures model-related session variables
# always exist.
#
# ==================================================

def initialize_model_state(
    session_state
):

    if (
        "selected_model"
        not in session_state
    ):

        session_state[
            "selected_model"
        ] = DEFAULT_MODEL

# ==================================================
# AVAILABLE MODELS FOR UI
# ==================================================
#
# Purpose
# --------------------------------------------------
# Returns model list for dropdown display.
#
# Exists primarily to keep app.py cleaner.
#
# ==================================================

def get_sorted_models(
    session_state
):

    return AVAILABLE_MODELS

# ==================================================
# MODEL NAME CLEANUP
# ==================================================
#
# Purpose
# --------------------------------------------------
# Ensures model names are always strings.
#
# Useful because Streamlit widgets may return
# None during initialization.
#
# ==================================================

def clean_model_name(
    model_name
):

    if model_name is None:

        return None

    return (
        str(model_name)
        .strip()
    )