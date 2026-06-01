# Project 01 - Terminal Chatbot

## Overview

This project implements a simple terminal-based chatbot that communicates with a locally hosted Large Language Model (LLM) through LM Studio using the OpenAI Python SDK.

The goal of the project is to understand:

* Python project structure
* Configuration management
* Prompt engineering basics
* OpenAI SDK fundamentals
* LM Studio integration
* Request and response flow
* Python imports and modules
* Application entry points

---

## Project Structure

01_terminal_chatbot

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

│   ├── llm.py

│   └── prompts.py

└── tests

```
└── test_app.py
```

---

## Component Responsibilities

### app.py

Handles user interaction.

Responsibilities:

* Accept user input
* Send requests to the LLM
* Display model responses
* Manage application loop

### config.py

Stores configuration values.

Examples:

* Model name
* API endpoint
* Temperature
* Token limits

### prompts.py

Stores system prompts that define model behavior.

### llm.py

Handles communication with LM Studio and the LLM.

Responsibilities:

* Create OpenAI client
* Build message payloads
* Send requests
* Process responses

---

## Request Flow

User

↓

app.py

↓

ask_llm()

↓

OpenAI SDK

↓

LM Studio API

↓

Qwen Model

↓

LM Studio API

↓

ask_llm()

↓

app.py

↓

User

---

## Requirements

* Python 3.11+
* LM Studio
* A downloaded LLM loaded in LM Studio

---

## Installation

Install dependencies:

pip install -r requirements.txt

---

## Running the Application

Start LM Studio.

Load a chat model.

Enable the local server.

Run:

python app.py

To exit:

quit

---

## Learning Outcomes

By completing this project you should understand:

* Functions
* Imports
* Modules
* Configuration files
* System prompts
* OpenAI SDK basics
* LLM request lifecycle
* Response objects
* Token generation
* Local model inference

---

## Future Improvements

* Error handling
* Conversation memory
* Streaming responses
* Multiple model support
* Logging
* Prompt templates
* RAG integration
