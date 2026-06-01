# Setup and Run Guide

This document explains how to run every project in this repository from a clean machine.

---

# Prerequisites

Install:

* Git
* Python 3.11+
* VS Code (recommended)
* LM Studio

---

# Step 1 — Fork Repository

Click:

Fork

on GitHub.

---

# Step 2 — Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI_Portfolio.git
```

Move into repository:

```bash
cd AI_Portfolio
```

---

# Step 3 — Create Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/Mac:

```bash
python -m venv .venv

source .venv/bin/activate
```

---

# Step 4 — Install Dependencies

Repository-level:

```bash
pip install -r requirements.txt
```

For a specific project:

Example:

```bash
cd projects/03_streamlit_chatbot

pip install -r requirements.txt
```

---

# Step 5 — Install LM Studio

Download:

https://lmstudio.ai

Install.

---

# Step 6 — Download Model

Recommended:

* Gemma 3 1B
* Gemma 3 4B
* Qwen 3 4B

Load model.

Start local server.

Example:

```text
http://127.0.0.1:1234/v1
```

---

# Step 7 — Create Environment File

Copy:

```text
.env.example
```

to:

```text
.env
```

Example:

```env
BASE_URL=http://127.0.0.1:1234/v1

DEFAULT_MODEL=google/gemma-3-1b

TEMPERATURE=0.7

MAX_TOKENS=100

MAX_HISTORY_MESSAGES=20

SUMMARY_TRIGGER_MESSAGES=50
```

---

# Project 01 — Terminal Chatbot

Move into:

```bash
cd projects/01_terminal_chatbot
```

Run:

```bash
python app.py
```

Expected:

```text
Chat session started
```

---

# Project 02 — Chat Memory

Move into:

```bash
cd projects/02_chat_memory
```

Run:

```bash
python app.py
```

Expected:

```text
Conversation history retained
```

---

# Project 03 — Streamlit Chatbot

Move into:

```bash
cd projects/03_streamlit_chatbot
```

Run:

```bash
streamlit run app.py
```

Expected:

Browser opens:

```text
http://localhost:8501
```

Features:

* Chat interface
* Multi-chat sessions
* Conversation persistence
* Memory summarization
* Export conversations

---

# Verifying Memory Summarization

Environment:

```env
MAX_HISTORY_MESSAGES=20
SUMMARY_TRIGGER_MESSAGES=50
```

Test:

1. Send 50+ messages
2. Observe summary generation
3. Confirm old messages compressed into memory summary

---

# Common Issues

## LM Studio Not Running

Error:

```text
Connection refused
```

Fix:

Start LM Studio server.

---

## Model Not Loaded

Error:

```text
Model unavailable
```

Fix:

Load model inside LM Studio.

---

## Missing Packages

Error:

```text
ModuleNotFoundError
```

Fix:

```bash
pip install -r requirements.txt
```

---

# Current Supported Projects

| Project              | Status   |
| -------------------- | -------- |
| 01 Terminal Chatbot  | Complete |
| 02 Chat Memory       | Complete |
| 03 Streamlit Chatbot | Complete |

Projects 04–11 are currently under development.
