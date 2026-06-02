import streamlit as st
from datetime import datetime

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

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "rename_chat" not in st.session_state:
    st.session_state.rename_chat = False

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title(
    "🤖 Local AI Chatbot"
)

models = get_available_models()

if not models:

    st.error(
        "Could not connect to LM Studio."
    )

    st.stop()

# --------------------------------------------------
# Model Selection Safety
# --------------------------------------------------

if st.session_state.selected_model is None:

    st.session_state.selected_model = (
        models[0]
    )

if (
    st.session_state.selected_model
    not in models
):

    st.session_state.selected_model = (
        models[0]
    )

selected_model = st.sidebar.selectbox(
    "Model",
    models,
    index=models.index(
        st.session_state.selected_model
    )
)

st.session_state.selected_model = (
    selected_model
)

# --------------------------------------------------
# Model Details
# --------------------------------------------------

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

# --------------------------------------------------
# Conversation Stats
# --------------------------------------------------

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
            for m in current_chat["messages"]
            if m["role"] == "user"
        )

        assistant_messages = sum(
            1
            for m in current_chat["messages"]
            if m["role"] == "assistant"
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

            except Exception as e:

                st.error(
                    f"Summary failed: {e}"
                )

# --------------------------------------------------
# New Chat
# --------------------------------------------------

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

    save_chat(chat)

    st.rerun()

# --------------------------------------------------
# Existing Chats
# --------------------------------------------------

st.sidebar.divider()

st.sidebar.subheader(
    "Chats"
)

all_chats = list_chats()

if st.session_state.current_chat_id:

    selected_chat = []

    remaining_chats = []

    for c in all_chats:

        if (
            c["chat_id"]
            ==
            st.session_state.current_chat_id
        ):

            selected_chat.append(c)

        else:

            remaining_chats.append(c)

    all_chats = (
        selected_chat
        +
        remaining_chats
    )

# --------------------------------------------------
# Chat Selection
# --------------------------------------------------

for chat_info in all_chats:

    is_selected = (

        chat_info["chat_id"]

        ==

        st.session_state.current_chat_id

    )

    label = chat_info["title"]

    if is_selected:

        label = f"▶ {label}"

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

    if is_selected:

        with st.sidebar.expander(
            "Chat Actions",
            expanded=False
        ):

            if st.button(
                "✏ Rename",
                key=f"rename_{chat_info['chat_id']}"
            ):

                st.session_state.rename_chat = True

            if st.button(
                "🗑 Delete",
                key=f"delete_{chat_info['chat_id']}"
            ):

                delete_chat(
                    chat_info["chat_id"]
                )

                st.session_state.current_chat = None

                st.session_state.current_chat_id = None

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

# --------------------------------------------------
# Rename Dialog
# --------------------------------------------------

@st.dialog(
    "Rename Chat"
)
def rename_chat_dialog():

    chat = st.session_state.current_chat

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

# --------------------------------------------------
# Main Window
# --------------------------------------------------

if st.session_state.current_chat is None:

    st.title(
        "🤖 Local AI Chatbot"
    )

    st.info(
        "No chats available. Click New Chat to begin."
    )

    st.stop()

chat = st.session_state.current_chat

# --------------------------------------------------
# Chat Header
# --------------------------------------------------

st.title(
    chat["title"]
)

# --------------------------------------------------
# Display Messages
# --------------------------------------------------

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
                    f"Assistant • {message['model']}"
                )

        st.markdown(
            message["content"]
        )

# --------------------------------------------------
# Conversation Info
# --------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.caption(
        f"Last answer came from: {chat['model']}"
    )

with col2:

    st.caption(
        f"Next answer will come from: {selected_model}"
    )

# --------------------------------------------------
# Action Buttons
# --------------------------------------------------

last_message_is_assistant = (

    len(chat["messages"]) > 0

    and

    chat["messages"][-1]["role"]

    ==

    "assistant"

)

button_col1, button_col2 = st.columns(2)

# --------------------------------------------------
# Regenerate Response
# --------------------------------------------------

with button_col1:

    if (
        last_message_is_assistant
    ):

        if st.button(
            f"🔄 Regenerate Using {selected_model}",
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
                        == "token"
                    ):

                        regenerated_response += (
                            event["content"]
                        )

                    elif (
                        event["type"]
                        == "finish"
                    ):

                        finish_reason = (
                            event["reason"]
                        )

            chat["messages"].append(
                {
                    "role": "assistant",
                    "content":
                    regenerated_response,
                    "model":
                    selected_model,
                    "timestamp":
                    datetime.now().isoformat()
                }
            )

            chat[
                "last_finish_reason"
            ] = finish_reason

            chat["model"] = (
                selected_model
            )

            chat = update_summary_if_needed(
                chat,
                selected_model
            )

            save_chat(
                chat
            )

            st.session_state.current_chat = (
                chat
            )

            st.rerun()

# --------------------------------------------------
# Continue Generating
# --------------------------------------------------

with button_col2:

    if (
        chat.get(
            "last_finish_reason"
        ) == "length"
    ):

        if st.button(
            "⏩ Continue Generating",
            use_container_width=True
        ):

            last_assistant_index = None

            for i in range(
                len(chat["messages"]) - 1,
                -1,
                -1
            ):

                if (
                    chat["messages"][i]["role"]
                    == "assistant"
                ):

                    last_assistant_index = i

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
                            == "token"
                        ):

                            extra_text += (
                                event["content"]
                            )

                        elif (
                            event["type"]
                            == "finish"
                        ):

                            finish_reason = (
                                event["reason"]
                            )

                    chat["messages"][
                        last_assistant_index
                    ]["content"] += (
                        "\n\n"
                        + extra_text
                    )

                    chat[
                        "last_finish_reason"
                    ] = finish_reason

                    chat["model"] = (
                        selected_model
                    )

                    chat = update_summary_if_needed(
                        chat,
                        selected_model
                    )

                    save_chat(
                        chat
                    )

                    st.session_state.current_chat = (
                        chat
                    )

                    st.rerun()

# --------------------------------------------------
# Input Area
# --------------------------------------------------

st.divider()

user_prompt = st.chat_input(
    "Type your message..."
)

if user_prompt:

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

        chat["title"] = " ".join(
            words[:6]
        )

        if len(words) > 6:

            chat["title"] += "..."

    # --------------------------------------------------
    # Prevent Duplicate User Messages
    # --------------------------------------------------

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
                "role": "user",
                "content":
                user_prompt,
                "timestamp":
                datetime.now().isoformat()
            }
        )

    # --------------------------------------------------
    # Display User Message
    # --------------------------------------------------

    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_prompt
        )

    # --------------------------------------------------
    # Generate Assistant Response
    # --------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        response_container = (
            st.empty()
        )

        full_response = ""

        messages_for_llm = (
            build_context_for_llm(
                chat
            )
        )

        finish_reason = None

        for event in stream_llm(
            messages_for_llm,
            selected_model
        ):

            if (
                event["type"]
                == "token"
            ):

                full_response += (
                    event["content"]
                )

                response_container.markdown(
                    full_response
                )

            elif (
                event["type"]
                == "finish"
            ):

                finish_reason = (
                    event["reason"]
                )

    # --------------------------------------------------
    # Save Assistant Message
    # --------------------------------------------------

    chat["messages"].append(
        {
            "role": "assistant",
            "content":
            full_response,
            "model":
            selected_model,
            "timestamp":
            datetime.now().isoformat()
        }
    )

    chat[
        "last_finish_reason"
    ] = finish_reason

    chat["model"] = (
        selected_model
    )

    # --------------------------------------------------
    # Automatic Memory Summarization
    # --------------------------------------------------

    chat = update_summary_if_needed(
        chat,
        selected_model
    )

    # --------------------------------------------------
    # Persist Chat
    # --------------------------------------------------

    save_chat(
        chat
    )

    st.session_state.current_chat = (
        chat
    )

    st.rerun()