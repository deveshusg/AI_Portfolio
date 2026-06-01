# Project 02 - Memory Chatbot

## Objective

Build a terminal-based chatbot that remembers previous conversation turns during the current session.

The chatbot communicates with a local LLM running in LM Studio using the OpenAI Python SDK.

---

## New Concepts Introduced

Compared with Project 01:

* Conversation memory
* Message history
* Multi-turn conversations
* Context management
* Environment variables
* Configuration loading with python-dotenv

---

## Project Structure

02_chat_memory

├── app.py

├── README.md

├── requirements.txt

├── .env

├── .env.example

├── data

│   ├── raw

│   └── processed

├── src

│   ├── config.py

│   ├── prompts.py

│   └── llm.py

└── tests

```
└── test_app.py
```

---

## Architecture

User

↓

app.py

↓

conversation_history

↓

ask_llm(messages)

↓

LM Studio

↓

Gemma 3 1B

↓

Response

↓

conversation_history

↓

User

---

## Memory Mechanism

Conversation history is stored in a Python list.

Each interaction is stored as a message object:

* system
* user
* assistant

The entire history is sent to the model with every request.

This allows the model to remember earlier parts of the conversation.

Example:

User:
My name is Devesh

Assistant:
Nice to meet you.

User:
What is my name?

Assistant:
Your name is Devesh.

---

## Requirements

* Python 3.11+
* LM Studio
* OpenAI Python SDK
* python-dotenv

---

## Installation

pip install -r requirements.txt

---

## Running

Start LM Studio.

Load:

google/gemma-3-1b

Start Local Server.

Run:

python app.py

Exit:

quit

---

## Current Limitations

Memory exists only during the current session.

Closing the application clears memory.

No token-aware memory trimming yet.

No long-term memory storage.

---

## Future Improvements

* Persistent memory
* Token counting
* Memory trimming
* Conversation summarization
* Logging
* Streaming responses
* Multiple model support
