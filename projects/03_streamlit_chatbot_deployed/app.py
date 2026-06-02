# ==================================================
# IMPORTS
# ==================================================
#
# Standard Library
# --------------------------------------------------
# datetime
#     Used for timestamps on messages.
#
# uuid
#     Used to generate anonymous chat IDs for
#     feedback submissions.
#
# ==================================================

from datetime import datetime
import uuid

# ==================================================
# THIRD PARTY LIBRARIES
# ==================================================
#
# streamlit
#     Main UI framework.
#
# ==================================================

import streamlit as st

# ==================================================
# PROJECT MODULES
# ==================================================
#
# Configuration
# Memory Management
# LLM Operations
# Feedback Storage
# Model Management
#
# ==================================================

from src.feedback import save_feedback

from src.config import (
    MODEL_INFO,
    SUMMARY_TRIGGER_MESSAGES
)

from src.memory import (
    create_chat,
    save_chat,
    load_chat,
    list_chats,
    rename_chat,
    delete_chat,
    export_chat_json,
    export_chat_markdown
)

from src.llm import (
    get_available_models,
    stream_llm,
    continue_response,
    build_context_for_llm,
    update_summary_if_needed,
    generate_summary
)

from src.model_manager import (
    initialize_model_state,
    get_sorted_models,
    clean_model_name,
)

# ==================================================
# PAGE CONFIGURATION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Controls:
#
# - Browser tab title
# - Browser tab icon
# - Layout width
#
# wide layout gives more space for long chats.
#
# ==================================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ==================================================
# SESSION STATE INITIALIZATION
# ==================================================
#
# Streamlit reruns the script frequently.
#
# Session State is used to preserve:
#
# - Current chat
# - Current chat id
# - Selected model
# - Rename dialog state
#
# ==================================================

if "current_chat" not in st.session_state:

    st.session_state.current_chat = None

if "current_chat_id" not in st.session_state:

    st.session_state.current_chat_id = None

if "selected_model" not in st.session_state:

    st.session_state.selected_model = None

if "rename_chat" not in st.session_state:

    st.session_state.rename_chat = False

if "chat_id" not in st.session_state:

    st.session_state.chat_id = (
        str(uuid.uuid4())[:8]
    )

# ==================================================
# SIDEBAR
# ==================================================
#
# Purpose
# --------------------------------------------------
# Contains:
#
# - Model selection
# - Model details
# - Conversation statistics
# - Feedback button
# - Chat list
#
# ==================================================

st.sidebar.title(
    "🤖 AI Chatbot"
)

# ==================================================
# MODEL STATE INITIALIZATION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Prepares model-related session variables.
#
# Current use:
#
# - Exhausted model tracking
# - Future model management features
#
# ==================================================

initialize_model_state(
    st.session_state
)

# ==================================================
# AVAILABLE MODELS
# ==================================================
#
# Purpose
# --------------------------------------------------
# Get models prepared for display.
#
# ==================================================

models = get_sorted_models(
    st.session_state
)

if not models:

    st.error(
        "No models available."
    )

    st.stop()

# ==================================================
# MODEL SELECTION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Maintains selected model across reruns.
#
# Process
# --------------------------------------------------
# 1. Get currently selected model.
# 2. Clean display formatting.
# 3. Build dropdown.
# 4. Save selection.
#
# ==================================================

current_model = (
    clean_model_name(
        st.session_state.get(
            "selected_model"
        )
    )
)

if current_model is None:

    current_model = (
        clean_model_name(
            models[0]
        )
    )

model_lookup = {

    clean_model_name(model): index

    for index, model

    in enumerate(models)
}

if current_model not in model_lookup:

    current_model = (
        clean_model_name(
            models[0]
        )
    )

selected_model_display = (
    st.sidebar.selectbox(
        "Model",
        models,
        index=model_lookup[
            current_model
        ]
    )
)

selected_model = (
    clean_model_name(
        selected_model_display
    )
)

st.session_state.selected_model = (
    selected_model
)

# ==================================================
# MODEL DETAILS
# ==================================================
#
# Purpose
# --------------------------------------------------
# Displays metadata about the currently
# selected model.
#
# Information comes from MODEL_INFO.
#
# ==================================================

model_info = MODEL_INFO.get(
    selected_model,
    {}
)

with st.sidebar.expander(
    "Model Details",
    expanded=False
):

    st.write(
        f"Family: {model_info.get('family', 'Unknown')}"
    )

    st.write(
        f"Parameters: {model_info.get('parameters', 'Unknown')}"
    )

    st.write(
        f"Type: {model_info.get('type', 'Unknown')}"
    )

    st.write(
        f"Speed: {model_info.get('speed', 'Unknown')}"
    )

# ==================================================
# CONVERSATION STATISTICS
# ==================================================
#
# Purpose
# --------------------------------------------------
# Displays useful information about the
# currently loaded conversation.
#
# Includes:
#
# - Message counts
# - Summary status
# - Last model used
# - Summary controls
#
# ==================================================

with st.sidebar.expander(
    "Conversation Stats",
    expanded=False
):

    if (
        st.session_state.current_chat
        is not None
    ):

        current_chat = (
            st.session_state.current_chat
        )

        total_messages = len(
            current_chat["messages"]
        )

        user_messages = sum(
            1
            for message
            in current_chat["messages"]
            if message["role"] == "user"
        )

        assistant_messages = sum(
            1
            for message
            in current_chat["messages"]
            if message["role"] == "assistant"
        )

        st.write(
            f"Messages: {total_messages}"
        )

        st.write(
            f"User Messages: {user_messages}"
        )

        st.write(
            f"Assistant Messages: {assistant_messages}"
        )

        st.write(
            f"Created: {current_chat['created_at']}"
        )

        st.write(
            f"Updated: {current_chat['updated_at']}"
        )

        st.write(
            f"Last Model: {current_chat['model']}"
        )

        st.write(
            f"Summary Available: {'Yes' if current_chat['summary'] else 'No'}"
        )

        st.write(
            f"Summary Length: {len(current_chat['summary'])}"
        )

        st.write(
            f"Last Summary Count: {current_chat.get('last_summary_count', 0)}"
        )

        st.write(
            f"Summary Trigger: {SUMMARY_TRIGGER_MESSAGES}"
        )

        if st.button(
            "Generate Summary Now"
        ):

            try:

                current_chat["summary"] = (
                    generate_summary(
                        current_chat["messages"],
                        selected_model
                    )
                )

                current_chat[
                    "last_summary_count"
                ] = len(
                    current_chat["messages"]
                )

                save_chat(
                    current_chat
                )

                st.session_state.current_chat = (
                    current_chat
                )

                st.success(
                    "Summary generated."
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Summary failed: {error}"
                )

# ==================================================
# NEW CHAT CREATION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Creates a completely new conversation.
#
# Process
# --------------------------------------------------
# 1. Create empty chat object.
# 2. Save chat.
# 3. Make it active.
# 4. Refresh UI.
#
# ==================================================

if st.sidebar.button(
    "+ New Chat"
):

    chat = create_chat(
        selected_model
    )

    st.session_state.current_chat = (
        chat
    )

    st.session_state.current_chat_id = (
        chat["chat_id"]
    )

    save_chat(
        chat
    )

    st.rerun()

# ==================================================
# FEEDBACK DIALOG
# ==================================================
#
# Purpose
# --------------------------------------------------
# Allows users to submit feedback.
#
# Information Stored
# --------------------------------------------------
# - Name
# - Email
# - Feedback
# - Session Chat ID
# - Recent Chat History
#
# Chat History
# --------------------------------------------------
# Only the most recent 20 messages are stored.
#
# This keeps feedback records small while still
# providing enough context for debugging and
# improvement analysis.
#
# ==================================================

@st.dialog(
    "Feedback"
)
def feedback_dialog():

    name = st.text_input(
        "Name"
    )

    email = st.text_input(
        "Email"
    )

    feedback = st.text_area(
        "Feedback",
        height=150,
    )

    if st.button(
        "Submit Feedback"
    ):

        if feedback.strip():

            chat_log = "\n\n".join(
                [
                    (
                        f"{message['role'].upper()}: "
                        f"{message['content']}"
                    )
                    for message in (
                        st.session_state
                        .current_chat
                        .get(
                            "messages",
                            []
                        )[-20:]
                    )
                ]
            )

            save_feedback(
                name=name,
                email=email,
                feedback=feedback,
                chat_id=(
                    st.session_state.chat_id
                ),
                chat_log=chat_log
            )

            st.success(
                "Thank you for your feedback!"
            )

        else:

            st.warning(
                "Please enter feedback."
            )

# ==================================================
# FEEDBACK BUTTON
# ==================================================
#
# Purpose
# --------------------------------------------------
# Makes feedback accessible without scrolling
# through chat history.
#
# ==================================================

st.sidebar.divider()

if st.sidebar.button(
    "📝 Feedback"
):

    feedback_dialog()

st.sidebar.caption(
    "Help improve the chatbot"
)

# ==================================================
# CHAT LIST SECTION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Displays all saved chats.
#
# Behavior
# --------------------------------------------------
# Active chat is displayed first.
#
# ==================================================

st.sidebar.divider()

st.sidebar.subheader(
    "Chats"
)

all_chats = list_chats()

# ==================================================
# MOVE ACTIVE CHAT TO TOP
# ==================================================
#
# Purpose
# --------------------------------------------------
# Makes navigation easier when many chats exist.
#
# ==================================================

if st.session_state.current_chat_id:

    selected_chat = []

    remaining_chats = []

    for chat_info in all_chats:

        if (
            chat_info["chat_id"]
            ==
            st.session_state.current_chat_id
        ):

            selected_chat.append(
                chat_info
            )

        else:

            remaining_chats.append(
                chat_info
            )

    all_chats = (
        selected_chat
        +
        remaining_chats
    )

# ==================================================
# CHAT SELECTION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Loads an existing chat into memory.
#
# Visual Indicator
# --------------------------------------------------
# ▶ indicates currently selected chat.
#
# ==================================================

for chat_info in all_chats:

    is_selected = (

        chat_info["chat_id"]

        ==

        st.session_state.current_chat_id

    )

    label = (
        chat_info["title"]
    )

    if is_selected:

        label = (
            f"▶ {label}"
        )

    if st.sidebar.button(
        label,
        key=chat_info["chat_id"]
    ):

        chat = load_chat(
            chat_info["chat_id"]
        )

        st.session_state.current_chat = (
            chat
        )

        st.session_state.current_chat_id = (
            chat_info["chat_id"]
        )

        st.rerun()

# ==================================================
# CHAT ACTIONS
# ==================================================
#
# Purpose
# --------------------------------------------------
# Provides actions for the currently
# selected chat.
#
# Available Actions
# --------------------------------------------------
# - Rename
# - Delete
# - Export JSON
# - Export Markdown
#
# Only visible for the active chat.
#
# ==================================================

    if is_selected:

        with st.sidebar.expander(
            "Chat Actions",
            expanded=False
        ):

            if st.button(
                "✏ Rename",
                key=f"rename_{chat_info['chat_id']}"
            ):

                st.session_state.rename_chat = (
                    True
                )

            if st.button(
                "🗑 Delete",
                key=f"delete_{chat_info['chat_id']}"
            ):

                delete_chat(
                    chat_info["chat_id"]
                )

                st.session_state.current_chat = (
                    None
                )

                st.session_state.current_chat_id = (
                    None
                )

                st.rerun()

            if st.button(
                "⬇ Export JSON",
                key=f"json_{chat_info['chat_id']}"
            ):

                export_chat_json(
                    chat_info["chat_id"]
                )

                st.toast(
                    "JSON exported"
                )

            if st.button(
                "⬇ Export Markdown",
                key=f"md_{chat_info['chat_id']}"
            ):

                export_chat_markdown(
                    chat_info["chat_id"]
                )

                st.toast(
                    "Markdown exported"
                )

# ==================================================
# RENAME CHAT DIALOG
# ==================================================
#
# Purpose
# --------------------------------------------------
# Allows users to rename the active chat.
#
# Process
# --------------------------------------------------
# 1. Enter new name.
# 2. Save to storage.
# 3. Update session state.
# 4. Refresh UI.
#
# ==================================================

@st.dialog(
    "Rename Chat"
)
def rename_chat_dialog():

    chat = (
        st.session_state.current_chat
    )

    new_name = st.text_input(
        "New Chat Name",
        value=chat["title"]
    )

    if st.button(
        "Save"
    ):

        rename_chat(
            chat["chat_id"],
            new_name.strip()
        )

        chat["title"] = (
            new_name.strip()
        )

        st.session_state.current_chat = (
            chat
        )

        st.session_state.rename_chat = (
            False
        )

        st.rerun()

if st.session_state.rename_chat:

    rename_chat_dialog()

# ==================================================
# MAIN WINDOW INITIALIZATION
# ==================================================
#
# Purpose
# --------------------------------------------------
# A chat must be selected before the main
# interface can be shown.
#
# If no chat exists:
# - Show guidance message.
# - Stop execution.
#
# ==================================================

if st.session_state.current_chat is None:

    st.title(
        "🤖 AI Chatbot"
    )

    st.info(
        "No chats available. Click New Chat to begin."
    )

    st.stop()

chat = (
    st.session_state.current_chat
)

# ==================================================
# CHAT HEADER
# ==================================================
#
# Purpose
# --------------------------------------------------
# Display current conversation title.
#
# ==================================================

st.title(
    chat["title"]
)

# ==================================================
# MESSAGE HISTORY
# ==================================================
#
# Purpose
# --------------------------------------------------
# Render every stored message.
#
# Message Types
# --------------------------------------------------
# user
# assistant
#
# Additional Information
# --------------------------------------------------
# Assistant messages display the model that
# generated the response.
#
# ==================================================

for message in chat["messages"]:

    with st.chat_message(
        message["role"]
    ):

        if (
            message["role"]
            ==
            "assistant"
        ):

            if (
                "model"
                in message
            ):

                st.caption(
                    (
                        "Assistant • "
                        f"{message['model']}"
                    )
                )

        st.markdown(
            message["content"]
        )

# ==================================================
# CONVERSATION INFORMATION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Shows:
#
# - Last model used
# - Next model selected
#
# Useful when users frequently switch
# between models.
#
# ==================================================

st.divider()

info_col_1, info_col_2 = (
    st.columns(2)
)

with info_col_1:

    st.caption(
        (
            "Last answer came from: "
            f"{chat['model']}"
        )
    )

with info_col_2:

    st.caption(
        (
            "Next answer will come from: "
            f"{selected_model}"
        )
    )

# ==================================================
# RESPONSE ACTIONS
# ==================================================
#
# Purpose
# --------------------------------------------------
# Provides controls for:
#
# - Regeneration
# - Continuation
#
# ==================================================

last_message_is_assistant = (

    len(chat["messages"]) > 0

    and

    chat["messages"][-1]["role"]

    ==

    "assistant"

)

action_col_1, action_col_2 = (
    st.columns(2)
)

# ==================================================
# REGENERATE RESPONSE
# ==================================================
#
# Purpose
# --------------------------------------------------
# Removes the most recent assistant response.
#
# Sends the same conversation context back
# to the selected model.
#
# Generates a fresh answer.
#
# ==================================================

with action_col_1:

    if last_message_is_assistant:

        if st.button(
            (
                "🔄 Regenerate Using "
                f"{selected_model}"
            ),
            use_container_width=True
        ):

            chat["messages"].pop()

            messages_for_llm = (
                build_context_for_llm(
                    chat
                )
            )

            regenerated_response = ""

            finish_reason = None

            with st.spinner(
                "Regenerating..."
            ):

                for event in stream_llm(
                    messages_for_llm,
                    selected_model
                ):

                    if (
                        event["type"]
                        ==
                        "token"
                    ):

                        regenerated_response += (
                            event["content"]
                        )

                    elif (
                        event["type"]
                        ==
                        "finish"
                    ):

                        finish_reason = (
                            event["reason"]
                        )

            chat["messages"].append(
                {
                    "role":
                    "assistant",

                    "content":
                    regenerated_response,

                    "model":
                    selected_model,

                    "timestamp":
                    datetime.now()
                    .isoformat()
                }
            )

            chat[
                "last_finish_reason"
            ] = finish_reason

            chat["model"] = (
                selected_model
            )

            chat = (
                update_summary_if_needed(
                    chat,
                    selected_model
                )
            )

            save_chat(
                chat
            )

            st.session_state.current_chat = (
                chat
            )

            st.rerun()

# ==================================================
# CONTINUE GENERATION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Used when a model stops because it reaches
# its output length limit.
#
# Continues generation from the current
# conversation state.
#
# ==================================================

with action_col_2:

    if (
        chat.get(
            "last_finish_reason"
        )
        ==
        "length"
    ):

        if st.button(
            "⏩ Continue Generating",
            use_container_width=True
        ):

            last_assistant_index = (
                None
            )

            for index in range(

                len(chat["messages"]) - 1,

                -1,

                -1

            ):

                if (
                    chat["messages"][index]["role"]
                    ==
                    "assistant"
                ):

                    last_assistant_index = (
                        index
                    )

                    break

            if (
                last_assistant_index
                is not None
            ):

                with st.spinner(
                    "Generating more text..."
                ):

                    extra_text = ""

                    finish_reason = None

                    for event in continue_response(
                        chat["messages"],
                        selected_model
                    ):

                        if (
                            event["type"]
                            ==
                            "token"
                        ):

                            extra_text += (
                                event["content"]
                            )

                        elif (
                            event["type"]
                            ==
                            "finish"
                        ):

                            finish_reason = (
                                event["reason"]
                            )

                    chat["messages"][
                        last_assistant_index
                    ]["content"] += (

                        "\n\n"

                        +

                        extra_text

                    )

                    chat[
                        "last_finish_reason"
                    ] = finish_reason

                    chat["model"] = (
                        selected_model
                    )

                    chat = (
                        update_summary_if_needed(
                            chat,
                            selected_model
                        )
                    )

                    save_chat(
                        chat
                    )

                    st.session_state.current_chat = (
                        chat
                    )

                    st.rerun()

# ==================================================
# INPUT AREA
# ==================================================
#
# Purpose
# --------------------------------------------------
# Provides the chat input box used to submit
# prompts to the selected model.
#
# ==================================================

st.divider()

user_prompt = st.chat_input(
    "Type your message..."
)

# ==================================================
# USER PROMPT RECEIVED
# ==================================================

if user_prompt:

    # ==============================================
    # AUTO CHAT TITLE GENERATION
    # ==============================================
    #
    # Purpose
    # ----------------------------------------------
    # Uses the first user message to generate a
    # meaningful chat title.
    #
    # Example
    # ----------------------------------------------
    # User:
    # "Explain IFRS 9 staging methodology"
    #
    # Title:
    # "Explain IFRS 9 staging..."
    #
    # ==============================================

    if (
        chat["title"]
        ==
        "New Chat"
    ):

        words = (
            user_prompt
            .strip()
            .split()
        )

        chat["title"] = (
            " ".join(
                words[:6]
            )
        )

        if len(words) > 6:

            chat["title"] += "..."

    # ==============================================
    # PREVENT DUPLICATE USER MESSAGES
    # ==============================================

    if (

        len(chat["messages"]) == 0

        or

        chat["messages"][-1]["role"]
        != "user"

        or

        chat["messages"][-1]["content"]
        != user_prompt

    ):

        chat["messages"].append(
            {
                "role":
                "user",

                "content":
                user_prompt,

                "timestamp":
                datetime.now()
                .isoformat()
            }
        )

    # ==============================================
    # DISPLAY USER MESSAGE
    # ==============================================

    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_prompt
        )

    # ==============================================
    # ASSISTANT RESPONSE GENERATION
    # ==============================================

    with st.chat_message(
        "assistant"
    ):

        response_container = (
            st.empty()
        )

        full_response = ""

        finish_reason = None

        response_failed = False

        messages_for_llm = (
            build_context_for_llm(
                chat
            )
        )

        for event in stream_llm(
            messages_for_llm,
            selected_model
        ):

            # --------------------------------------
            # Streaming Tokens
            # --------------------------------------

            if (
                event["type"]
                ==
                "token"
            ):

                full_response += (
                    event["content"]
                )

                response_container.markdown(
                    full_response
                )

            # --------------------------------------
            # Generation Finished
            # --------------------------------------

            elif (
                event["type"]
                ==
                "finish"
            ):

                finish_reason = (
                    event["reason"]
                )

            # --------------------------------------
            # Model Error Handling
            # --------------------------------------

            elif (
                event["type"]
                ==
                "model_error"
            ):

                response_failed = True

                friendly = (
                    event.get(
                        "friendly",
                        {}
                    )
                )

                title = (
                    friendly.get(
                        "title",
                        "Model Error"
                    )
                )

                message = (
                    friendly.get(
                        "message",
                        "An unexpected error occurred."
                    )
                )

                suggestion = (
                    friendly.get(
                        "suggestion",
                        "Please try again."
                    )
                )

                response_container.empty()

                st.error(
                    f"⚠ {title}"
                )

                st.markdown(
                    f"""
**What happened?**

{message}

**What can I do?**

{suggestion}
"""
                )

                with st.expander(
                    "Technical Details"
                ):

                    st.code(
                        event["error"]
                    )

                    st.caption(
                        "Copy the text above when reporting issues."
                    )

                break

    # ==============================================
    # SAVE ASSISTANT MESSAGE
    # ==============================================
    #
    # Purpose
    # ----------------------------------------------
    # Save only successful responses.
    #
    # Prevents:
    # - Empty messages
    # - Error messages
    # - Failed generations
    #
    # ==============================================

    if (

        not response_failed

        and

        full_response.strip()

    ):

        chat["messages"].append(
            {
                "role":
                "assistant",

                "content":
                full_response,

                "model":
                selected_model,

                "timestamp":
                datetime.now()
                .isoformat()
            }
        )

        chat[
            "last_finish_reason"
        ] = finish_reason

        chat["model"] = (
            selected_model
        )

        # ==========================================
        # MEMORY SUMMARY UPDATE
        # ==========================================

        chat = (
            update_summary_if_needed(
                chat,
                selected_model
            )
        )

        # ==========================================
        # SAVE CHAT
        # ==========================================

        save_chat(
            chat
        )

        st.session_state.current_chat = (
            chat
        )

    st.rerun()

