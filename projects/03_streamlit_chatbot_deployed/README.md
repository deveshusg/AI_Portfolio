# Local AI Chatbot with Memory

## 1. Project Overview

### What is this project?

This project is a locally hosted AI chatbot built using Streamlit, LM Studio, and Python.

The objective is to recreate a ChatGPT-like experience while keeping all model inference and conversation data on the user's machine.

Unlike cloud-based AI systems, this project does not require:

* OpenAI API credits
* Internet access for inference
* External storage of conversations

All conversations, memory summaries, and model interactions occur locally.

The chatbot supports:

* Multiple conversations
* Conversation persistence
* Model switching
* Response regeneration
* Continue generation
* Automatic memory summarization
* JSON and Markdown exports

The application is designed as a stepping stone toward more advanced AI systems such as:

* PDF Chat
* Embedding Search
* Vector Databases
* Retrieval-Augmented Generation (RAG)
* AI Agents

---

### Technologies Used

| Technology    | Purpose                      |
| ------------- | ---------------------------- |
| Python        | Core application logic       |
| Streamlit     | Web interface                |
| LM Studio     | Local model hosting          |
| OpenAI SDK    | Communication with LM Studio |
| JSON          | Conversation storage         |
| python-dotenv | Configuration management     |

---

### Example Workflow

A user enters:

 text
What is credit risk?
 

The application performs the following sequence:

 text
User Input
↓
Build Context
↓
Send Context to LM Studio
↓
Local LLM Generates Response
↓
Display Response
↓
Store Conversation
↓
Update Memory Summary
 

The user experiences a simple chatbot interface, but internally several modules coordinate to make this happen.

---

## 2. Why This Project Exists

### The Problem

Most beginner chatbot tutorials create systems that work like this:

 text
User Message
↓
LLM
↓
Response
 

Although this works for a few messages, it fails for long conversations.

For example:

 text
User: My name is Devesh.

...50 messages later...

User: What is my name?
 

The model may forget because the earlier messages are no longer included in the context window.

This is known as the context limitation problem.

---

### Why Context Matters

Large Language Models do not truly remember previous conversations.

They only know what is included in the current prompt.

A model receiving:

 text
Message 49
Message 50
 

cannot know what happened in:

 text
Message 1
Message 2
Message 3
 

unless those messages are provided again.

Therefore memory must be engineered.

---

### Traditional Solution

Many chatbots simply resend the entire conversation every time.

Example:

 text
System Prompt
+
Message 1
+
Message 2
+
Message 3
...
+
Message 200
 

This approach creates several problems:

| Issue            | Result               |
| ---------------- | -------------------- |
| Larger prompts   | Slower responses     |
| More tokens      | Higher memory usage  |
| Context overflow | Information lost     |
| Scaling problems | Poor user experience |

---

### Solution Used in This Project

This chatbot implements memory summarization.

Instead of sending the entire conversation forever:

 text
System Prompt
+
All Messages Ever
 

the chatbot eventually converts older messages into a compact summary.

Example:

 text
User likes Python.
User is learning AI.
Discussed Streamlit.
Working on local chatbot project.
 

The model then receives:

 text
System Prompt
+
Conversation Summary
+
Recent Messages
 

This dramatically reduces context size while preserving important information.

---

### Why This Approach Was Chosen

This project focuses on learning:

* Memory management
* Context engineering
* Chatbot architecture

before introducing:

* Embeddings
* Vector Databases
* Retrieval-Augmented Generation (RAG)

The summary-based approach is simpler and provides a strong foundation for later retrieval systems.

---

## 3. System Architecture

### High-Level Architecture

The application contains five major layers.

 text
┌─────────────────┐
│      User       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     app.py      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     llm.py      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    LM Studio    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Local AI Model │
└─────────────────┘
 

---

### Layer 1 – User

The user interacts through the Streamlit interface.

Actions include:

* Sending messages
* Creating chats
* Switching models
* Regenerating responses
* Continuing responses
* Exporting conversations

The user never directly interacts with the model.

---

### Layer 2 – Streamlit Interface

Streamlit is responsible for:

 text
Rendering UI
Capturing User Input
Displaying Responses
Managing Buttons
Managing Session State
 

Examples:

 python
st.chat_input()
st.chat_message()
st.sidebar.button()
 

The interface itself does not generate AI responses.

It only collects information and displays results.

---

### Layer 3 – app.py

`app.py` acts as the application's controller.

Responsibilities:

 text
Create Conversations
Load Conversations
Display Conversations
Build Requests
Handle Responses
Save Data
Manage Memory Updates
 

Think of `app.py` as the project manager coordinating all other modules.

---

### Layer 4 – llm.py

`llm.py` is responsible for all AI interactions.

Key responsibilities:

 text
Connect to LM Studio
Send Messages
Stream Responses
Generate Summaries
Build Context
Manage Memory Compression
 

This file contains most of the chatbot intelligence.

---

### Layer 5 – LM Studio

LM Studio hosts local language models.

Examples:

 text
Gemma
Llama
Qwen
Mistral
Phi
 

LM Studio exposes an OpenAI-compatible API.

This allows Python code to communicate with local models using the same SDK normally used for OpenAI.

---

### Request Lifecycle

When a user sends:

 text
What is probability?
 

the following occurs:

 text
User Input
↓
app.py
↓
build_context_for_llm()
↓
stream_llm()
↓
LM Studio
↓
Local Model
↓
Response Tokens
↓
Streamlit UI
↓
Conversation Saved
↓
Memory Check
 

This cycle repeats for every user message.

---

### Why This Architecture Was Chosen

The design separates responsibilities.

| File      | Responsibility        |
| --------- | --------------------- |
| app.py    | Application control   |
| llm.py    | AI logic              |
| memory.py | Storage               |
| config.py | Configuration         |
| .env      | Environment variables |

Benefits:

* Easier debugging
* Easier testing
* Easier feature additions
* Better maintainability
* Cleaner code organization

---

# 4. Folder Structure

One of the most important software engineering principles is separation of concerns.

Instead of putting everything inside a single file, responsibilities are divided across multiple files and folders.

This makes the application:

* Easier to understand
* Easier to debug
* Easier to extend
* Easier to maintain

The project structure is:

 text
project/
│
├── app.py
│
├── src/
│   ├── config.py
│   ├── llm.py
│   └── memory.py
│
├── data/
│   └── conversations/
│
├── exports/
│
├── .env
│
├── requirements.txt
│
└── README.md
 

---

## app.py

This is the main application entry point.

When Streamlit starts, it executes:

 bash
streamlit run app.py
 

Everything begins here.

Responsibilities:

* Render UI
* Create chats
* Load chats
* Display messages
* Receive user input
* Trigger LLM calls
* Save conversations
* Trigger memory summarization

Think of `app.py` as the project's conductor.

It does not generate AI responses itself.

Instead, it coordinates other modules.

---

## src/config.py

This file centralizes configuration.

Instead of hardcoding values throughout the application:

 python
temperature = 0.7
max_tokens = 100
 

they are stored in one place.

Responsibilities:

* Load environment variables
* Define model metadata
* Expose configuration values

Benefits:

* Easier changes
* Cleaner code
* Environment flexibility

---

## src/llm.py

This file handles all communication with AI models.

Responsibilities:

* Connect to LM Studio
* Get available models
* Stream responses
* Generate summaries
* Build context windows
* Manage memory compression

This file contains most of the chatbot intelligence.

Whenever the chatbot "thinks", the logic usually starts here.

---

## src/memory.py

This file manages persistence.

Responsibilities:

* Create chats
* Save chats
* Load chats
* Rename chats
* Delete chats
* Export chats

Without this file:

 text
Close Application
↓
Everything Lost
 

With this file:

 text
Close Application
↓
Reopen Application
↓
Everything Restored
 

---

## data/conversations/

Every conversation is stored as a JSON file.

Example:

 text
data/
└── conversations/
    ├── chat_001.json
    ├── chat_002.json
    └── chat_003.json
 

Each file represents a complete conversation.

Advantages:

* Human readable
* Easy debugging
* Easy backup
* Easy migration

---

## exports/

Exported conversations are stored here.

Supported formats:

 text
JSON
Markdown
 

Purpose:

* Sharing conversations
* Backups
* Documentation
* Record keeping

---

## .env

Stores environment variables.

Example:

 env
BASE_URL=http://127.0.0.1:1234/v1

DEFAULT_MODEL=google/gemma-3-1b

TEMPERATURE=0.7

MAX_TOKENS=100

MAX_HISTORY_MESSAGES=10

SUMMARY_TRIGGER_MESSAGES=20
 

The application loads these values at startup.

---

## requirements.txt

Lists all Python dependencies.

Example:

 text
streamlit
openai
python-dotenv
 

Allows others to install the project quickly:

 bash
pip install -r requirements.txt
 

---

## README.md

The file you are currently reading.

Purpose:

* Explain architecture
* Explain design decisions
* Explain implementation details
* Document lessons learned

A strong README allows another developer to understand the project without reading every source file.

---

# 5. Configuration System

## Why Configuration Exists

Imagine every file contained:

 python
TEMPERATURE = 0.7
 

Now imagine wanting:

 python
TEMPERATURE = 0.5
 

You would need to modify multiple files.

This creates maintenance problems.

Instead:

 text
Configuration
↓
Single Source of Truth
↓
Application Reads Configuration
 

This project follows that approach.

---

## Environment Variables

The application uses a `.env` file.

Example:

 env
BASE_URL=http://127.0.0.1:1234/v1

DEFAULT_MODEL=google/gemma-3-1b

TEMPERATURE=0.7

MAX_TOKENS=100

MAX_HISTORY_MESSAGES=10

SUMMARY_TRIGGER_MESSAGES=20
 

These values are loaded when the application starts.

---

## BASE_URL

Example:

 env
BASE_URL=http://127.0.0.1:1234/v1
 

Purpose:

Specifies where LM Studio is running.

Explanation:

 text
Streamlit
↓
OpenAI SDK
↓
BASE_URL
↓
LM Studio
↓
Local Model
 

Without a valid endpoint, no model requests can be processed.

---

## DEFAULT_MODEL

Example:

 env
DEFAULT_MODEL=google/gemma-3-1b
 

Purpose:

Defines the initial model loaded when the application starts.

Users can still switch models later.

---

## TEMPERATURE

Example:

 env
TEMPERATURE=0.7
 

Purpose:

Controls creativity.

Lower values:

 text
0.0
0.1
0.2
 

Characteristics:

* Predictable
* Deterministic
* Consistent

Higher values:

 text
0.8
0.9
1.0
 

Characteristics:

* Creative
* Varied
* Less predictable

Current setting:

 text
0.7
 

which balances creativity and consistency.

---

## MAX_TOKENS

Example:

 env
MAX_TOKENS=100
 

Purpose:

Limits maximum response size.

Without limits:

 text
Model may generate very long outputs.
 

With limits:

 text
Controlled response length.
 

---

## MAX_HISTORY_MESSAGES

Example:

 env
MAX_HISTORY_MESSAGES=10
 

Purpose:

Defines how many recent messages remain after summarization begins.

Before summary:

 text
All messages included.
 

After summary:

 text
Summary
+
Last 10 messages
 

This keeps prompts small and efficient.

---

## SUMMARY_TRIGGER_MESSAGES

Example:

 env
SUMMARY_TRIGGER_MESSAGES=20
 

Purpose:

Determines when memory compression starts.

Example:

 text
Messages 1-19
↓
No summary

Message 20
↓
Generate summary
 

This value can be changed without modifying code.

---

## Why Configuration Matters

Benefits:

| Benefit         | Explanation                          |
| --------------- | ------------------------------------ |
| Flexibility     | Change behavior without editing code |
| Simplicity      | Centralized settings                 |
| Maintainability | Easier updates                       |
| Portability     | Different environments supported     |

---

# 6. Complete Chat Lifecycle

This section explains every step that occurs when a user sends a message.

Understanding this flow is the key to understanding the entire application.

---

## Step 1 — User Enters Message

The process begins with:

 python
st.chat_input()
 

Example:

 text
User:
What is probability?
 

At this moment:

 text
No AI response exists yet.
 

The application only has user input.

---

## Step 2 — Message Added to Chat History

The application creates:

 python
{
    "role": "user",
    "content": "What is probability?"
}
 

and appends it to:

 python
chat["messages"]
 

Now the conversation history grows.

---

## Step 3 — Build Context

The application calls:

 python
build_context_for_llm(chat)
 

This is one of the most important functions in the project.

Purpose:

Convert conversation history into a prompt that the model can understand.

---

## Before Summarization

Context looks like:

 text
System Prompt
+
User Message 1
+
Assistant Message 1
+
User Message 2
+
Assistant Message 2
 

Everything is included.

---

## After Summarization

Context becomes:

 text
System Prompt
+
Conversation Summary
+
Recent Messages
 

The model receives less information but retains important context.

---

## Step 4 — Send Context to LM Studio

The application calls:

 python
stream_llm()
 

Internally:

 text
Python
↓
OpenAI SDK
↓
HTTP Request
↓
LM Studio
↓
Selected Model
 

The request contains:

* System prompt
* Summary (if available)
* Recent conversation messages

---

## Step 5 — Model Generates Tokens

The model does not generate a complete answer immediately.

Instead:

 text
H
He
Hel
Hell
Hello
 

Tokens arrive incrementally.

This process is called streaming.

---

## Step 6 — Streamlit Displays Tokens

As tokens arrive:

 python
response_container.markdown(...)
 

updates the interface.

The user experiences:

 text
Typing effect
 

similar to ChatGPT.

---

## Step 7 — Assistant Message Saved

Once generation completes:

 python
chat["messages"].append(...)
 

stores the assistant response.

Now both sides of the conversation are preserved.

---

## Step 8 — Memory System Executes

Immediately after saving the response:

 python
update_summary_if_needed(...)
 

runs.

The function checks:

 text
How many messages exist?
 

If the threshold has not been reached:

 text
Do nothing.
 

If the threshold has been reached:

 text
Generate summary.
Save summary.
Update summary metadata.
 

---

## Step 9 — Conversation Saved

Finally:

 python
save_chat(chat)
 

writes everything to disk.

Saved items include:

* Messages
* Summary
* Model
* Timestamps
* Chat title

Nothing is lost when the application closes.

---

## Step 10 — Application Reruns

Streamlit executes:

 python
st.rerun()
 

This refreshes the interface.

The user sees:

* Updated conversation
* Updated statistics
* Updated memory information

The cycle then repeats for the next message.

# 7. Memory System Deep Dive

The memory system is the most important feature in this project.

Without it, the chatbot would eventually forget earlier parts of the conversation.

With it, the chatbot can maintain context over long interactions while keeping prompt sizes manageable.

---

## The Core Problem

Large Language Models do not possess persistent memory.

Every request is independent.

The model only knows what is included in the current prompt.

For example:

 text id="j0g8yj"
Prompt A

User: My name is Devesh.
Assistant: Nice to meet you.
 

The model can answer:

 text id="wmy4co"
Your name is Devesh.
 

However, if a later request only contains:

 text id="3r4od4"
User: What is my name?
 

the model has no way to know.

The information was never provided.

---

## Naive Solution

A common beginner approach is:

 text id="6e9o7s"
Send entire conversation every time.
 

Example:

 text id="0gnb0v"
System Prompt
+
Message 1
+
Message 2
+
Message 3
...
+
Message 500
 

Initially this works.

As conversations grow, problems emerge.

---

## Problems With Full History

### Problem 1 – Growing Prompt Size

Every new message increases prompt size.

 text id="v6zjlwm"
10 messages
↓
20 messages
↓
100 messages
↓
500 messages
 

The prompt never stops growing.

---

### Problem 2 – Slower Responses

Larger prompts require:

 text id="0k2mpg"
More Processing
↓
Longer Inference Time
 

Response speed decreases.

---

### Problem 3 – Context Limits

Every model has a maximum context window.

Examples:

| Model         | Approximate Context Window |
| ------------- | -------------------------- |
| Small Models  | 4k–8k tokens               |
| Medium Models | 16k–32k tokens             |
| Large Models  | 128k+ tokens               |

Eventually:

 text id="75pql9"
Conversation Size
>
Context Window
 

Older information gets discarded.

---

## Memory Compression Strategy

This project uses summary-based memory.

Instead of preserving every message forever:

 text id="xwpxu6"
Old Messages
↓
Convert To Summary
↓
Store Summary
 

The summary becomes a compressed representation of the conversation.

---

## Memory Timeline

### Messages 1–19

No summary exists.

Context sent to the model:

 text id="80jlwm"
System Prompt
+
Message 1
+
Message 2
...
+
Message 19
 

---

### Message 20

The threshold is reached.

The application executes:

 python id="q5lzvs"
update_summary_if_needed()
 

The conversation is converted into a summary.

Example:

 text id="2jh7gw"
User is learning AI.
User is building a Streamlit chatbot.
Discussion included memory systems.
 

This summary is stored permanently.

---

### Messages 21–39

The summary now replaces most historical messages.

Context becomes:

 text id="z6d04w"
System Prompt
+
Summary
+
Recent Messages
 

This dramatically reduces prompt size.

---

### Message 40

The summary is updated.

Instead of recreating memory from scratch:

 text id="0d1zci"
Old Summary
+
New Messages
↓
Updated Summary
 

This is called incremental summarization.

---

### Why Incremental Summaries?

Advantages:

| Advantage            | Benefit             |
| -------------------- | ------------------- |
| Faster               | Less text processed |
| Smaller prompts      | Better performance  |
| Lower memory usage   | Better scalability  |
| Simpler architecture | Easier maintenance  |

---

## Summary Trigger Configuration

The threshold is configurable.

Example:

 env id="ktjzjd"
SUMMARY_TRIGGER_MESSAGES=20
 

Meaning:

 text id="43oqy7"
At 20 messages
↓
Generate summary
 

Changing the value requires no code modifications.

---

## Recent Message Retention

The summary alone is insufficient.

Recent conversational details may not yet be reflected in the summary.

Therefore:

 env id="3czj4e"
MAX_HISTORY_MESSAGES=10
 

keeps recent messages available.

Result:

 text id="mnlw48"
System Prompt
+
Summary
+
Last 10 Messages
 

This balances:

 text id="g4ecrq"
Memory
+
Efficiency
 

---

## Why This Design Was Chosen

The memory system was intentionally designed as:

 text id="pt71ea"
Simple
Reliable
Understandable
Extensible
 

before introducing:

* Embeddings
* Vector Databases
* Retrieval Systems

The goal was to learn memory fundamentals first.

---

# 8. Conversation Storage and JSON Schema

Every conversation is stored as a JSON file.

A single file represents an entire chat session.

Example:

 json id="22vvyy"
{
  "chat_id": "chat_20260601_235352",
  "title": "Credit Risk Discussion",
  "model": "google/gemma-3-1b",
  "summary": "",
  "last_summary_count": 0,
  "messages": []
}
 

---

## Why JSON?

JSON was selected because it is:

| Property       | Benefit                    |
| -------------- | -------------------------- |
| Human Readable | Easy debugging             |
| Lightweight    | Small files                |
| Portable       | Easy transfer              |
| Flexible       | Supports nested structures |

For learning projects, JSON is often superior to introducing databases too early.

---

## Chat ID

Example:

 json id="4j6u4o"
"chat_id": "chat_20260601_235352"
 

Purpose:

Uniquely identifies a conversation.

This value is used when:

* Loading chats
* Saving chats
* Renaming chats
* Deleting chats

---

## Title

Example:

 json id="6uqeqt"
"title": "Credit Risk Discussion"
 

Purpose:

Provides a human-readable identifier.

Displayed in the sidebar.

---

## Model

Example:

 json id="dffawf"
"model": "google/gemma-3-1b"
 

Purpose:

Tracks which model produced the most recent response.

This allows users to:

* Audit conversations
* Compare model outputs
* Resume work consistently

---

## Summary

Example:

 json id="rj0uik"
"summary": "User is learning AI..."
 

Purpose:

Stores compressed conversation memory.

Generated automatically.

Used when building future prompts.

---

## Last Summary Count

Example:

 json id="3vs65y"
"last_summary_count": 20
 

Purpose:

Tracks the last point at which summarization occurred.

Example:

 text id="r5dqvc"
Summary Generated
↓
20 Messages
↓
Store 20
 

Next summary occurs after another threshold interval.

---

## Messages Array

The heart of every conversation.

Example:

 json id="mzebix"
{
    "role": "user",
    "content": "What is probability?"
}
 

and

 json id="sjnklf"
{
    "role": "assistant",
    "content": "Probability measures uncertainty."
}
 

The array preserves the complete conversation history.

---

## Timestamps

Example:

 json id="siyh5t"
"timestamp": "2026-06-01T23:55:25"
 

Purpose:

Tracks when messages were created.

Useful for:

* Auditing
* Sorting
* Analytics

---

## Why Store Everything?

Even after summarization:

 text id="qolhgo"
Full Messages
+
Summary
 

are both retained.

Benefits:

* No information loss
* Future re-summarization possible
* Easier debugging
* Easier exports

---

# 9. Feature Walkthrough

This section explains every major feature available in the chatbot.

---

## Multiple Conversations

Users can create unlimited chats.

Example:

 text id="0qchjt"
Chat 1 – Credit Risk
Chat 2 – Statistics
Chat 3 – Python Learning
 

Each conversation is stored independently.

---

## Chat Persistence

Conversations survive application restarts.

Workflow:

 text id="fw8dmr"
Create Chat
↓
Save Chat
↓
Close Application
↓
Reopen Application
↓
Load Chat
 

No information is lost.

---

## Model Switching

Users can select different local models.

Examples:

 text id="13v18h"
Gemma
Qwen
Llama
Mistral
 

This allows experimentation with:

* Speed
* Accuracy
* Style

without changing application code.

---

## Regenerate Response

Purpose:

Create an alternative answer.

Process:

 text id="49vk2r"
Remove Last Assistant Message
↓
Send Same Context
↓
Generate New Response
 

Useful when a response is:

* Incorrect
* Incomplete
* Poorly worded

---

## Continue Generation

Purpose:

Handle responses that stop due to token limits.

Process:

 text id="l93y1e"
Response Truncated
↓
Continue Button
↓
Generate Remaining Text
 

The chatbot attempts to continue naturally without restarting the answer.

---

## Automatic Memory Summarization

Purpose:

Maintain long-term context.

Process:

 text id="zdg9hd"
Message Threshold Reached
↓
Generate Summary
↓
Store Summary
↓
Use Summary In Future Context
 

This enables long conversations without continuously increasing prompt size.

---

## JSON Export

Purpose:

Create a machine-readable backup.

Benefits:

* Re-importing
* Analysis
* Archival

---

## Markdown Export

Purpose:

Create a human-readable conversation record.

Benefits:

* Documentation
* Sharing
* Portfolio examples

---

## Chat Rename

Purpose:

Organize conversations.

Example:

 text id="vij4ao"
New Chat
↓
Credit Risk Modeling Notes
 

Makes navigation easier.

---

## Chat Delete

Purpose:

Remove conversations permanently.

Useful for:

* Cleanup
* Testing
* Storage management

---

## Why These Features Matter

Together these features transform the application from:

 text id="ddaqpv"
Simple LLM Wrapper
 

into:

 text id="0n2u6t"
Persistent Conversational System
 

which more closely resembles real-world AI products.

# 10. Model Management and LM Studio Integration

One of the most important architectural decisions in this project was separating the chatbot application from the language model itself.

The chatbot does not contain an AI model.

Instead, it communicates with models hosted by LM Studio.

This separation provides flexibility, scalability, and easier experimentation.

---

## What is LM Studio?

LM Studio is a desktop application that allows users to run Large Language Models locally.

Examples:

 text id="p0d7ea"
Gemma
Qwen
Llama
Mistral
Phi
DeepSeek
 

Instead of calling cloud APIs, the chatbot sends requests to LM Studio running on the user's machine.

Architecture:

 text id="8qg4ki"
Chatbot
↓
LM Studio
↓
Local Model
 

The chatbot never interacts with the model directly.

LM Studio acts as the bridge.

---

## Why Use LM Studio?

Without LM Studio:

 text id="mrbjlwm"
Application
↓
Model Files
↓
Inference Logic
 

The project becomes significantly more complicated.

With LM Studio:

 text id="6fzvxs"
Application
↓
LM Studio API
↓
Model
 

The complexity is reduced dramatically.

Benefits:

| Benefit              | Explanation              |
| -------------------- | ------------------------ |
| Easier setup         | No custom inference code |
| Model switching      | Change models instantly  |
| OpenAI compatibility | Reuse OpenAI SDK         |
| Local execution      | No cloud dependency      |
| Privacy              | Data remains on device   |

---

## OpenAI-Compatible API

One of LM Studio's most useful features is its OpenAI-compatible endpoint.

Example:

 env id="w8xw0m"
BASE_URL=http://127.0.0.1:1234/v1
 

The chatbot uses:

 python id="g9oqc3"
OpenAI(
    base_url=BASE_URL
)
 

This means the same SDK normally used for OpenAI can communicate with local models.

The application therefore remains portable.

Future migration to another provider would require minimal code changes.

---

## Discovering Available Models

When the application starts, it requests a list of available models.

Workflow:

 text id="g7x6e9"
Application Starts
↓
Request Model List
↓
LM Studio Returns Models
↓
Populate Dropdown
 

The user then sees available models inside the sidebar.

Example:

 text id="ljtq2s"
Gemma 3 1B
Qwen 3
Llama 3
Mistral
 

No hardcoding is required.

---

## Model Selection

The selected model is stored in session state.

Workflow:

 text id="d8vl3v"
User Selects Model
↓
Store Selection
↓
Future Requests Use Model
 

This allows different conversations to use different models.

---

## Why Store Model Names in Messages?

Each assistant response stores:

 json id="e4p2jq"
{
  "model": "google/gemma-3-1b"
}
 

Purpose:

 text id="lx4s0j"
Traceability
 

Months later, users can identify:

* Which model generated a response
* Which model performed best
* Which model was active during a conversation

---

## Streaming Responses

The chatbot does not wait for the full response.

Instead:

 text id="e2dl79"
Token
↓
Token
↓
Token
 

is streamed back continuously.

Benefits:

| Benefit         | Result                         |
| --------------- | ------------------------------ |
| Faster feedback | User sees progress immediately |
| Better UX       | Feels responsive               |
| Reduced waiting | No long blank screen           |

This creates the familiar ChatGPT-style typing effect.

---

## Why This Architecture Matters

Because models are decoupled from the application:

 text id="i8x5es"
Replace Model
↓
Keep Application
 

The chatbot remains useful even as better models become available.

This significantly increases the project's longevity.

---

# 11. Problems Encountered and Solutions Implemented

Every non-trivial software project encounters problems.

The development of this chatbot revealed several important architectural and implementation challenges.

---

## Problem 1 – No Persistent Conversations

### Initial State

Early versions worked like:

 text id="24cczn"
Start Chat
↓
Conversation Exists
↓
Close Application
↓
Conversation Lost
 

Every restart erased all history.

---

### Root Cause

No storage mechanism existed.

Conversation data lived only in memory.

---

### Solution

JSON-based persistence.

Workflow:

 text id="lsl5hs"
Conversation
↓
Save JSON
↓
Load JSON
↓
Restore Conversation
 

---

### Result

Users can:

* Close the application
* Restart Streamlit
* Continue existing chats

without losing information.

---

## Problem 2 – No Long-Term Memory

### Initial State

The model only knew recent messages.

Example:

 text id="r7s29v"
User:
My name is Devesh.

...many messages later...

User:
What is my name?
 

The model frequently forgot.

---

### Root Cause

Earlier messages were eventually excluded from context.

---

### Solution

Memory summarization.

Workflow:

 text id="rk7sj8"
Conversation
↓
Summary
↓
Store Summary
↓
Use Summary In Future Context
 

---

### Result

Long-term context became possible.

---

## Problem 3 – Summary Generation Not Triggering

### Symptom

The summary field remained empty.

Example:

 json id="gdd9rz"
"summary": ""
 

even after many messages.

---

### Root Cause

The summary update function was not consistently executed during normal conversation flow.

---

### Solution

The application now executes:

 python id="sqpr0n"
update_summary_if_needed()
 

after assistant responses are saved.

---

### Result

Summaries are automatically generated and persisted.

---

## Problem 4 – Hardcoded Thresholds

### Initial State

Values such as:

 python id="kr8zrl"
20
 

were embedded directly in code.

---

### Problems

Changing behavior required source-code modifications.

---

### Solution

Move thresholds into:

 env id="0x8tlw"
SUMMARY_TRIGGER_MESSAGES
MAX_HISTORY_MESSAGES
 

---

### Result

Behavior can be modified without touching application logic.

---

## Problem 5 – Role Alternation Issues

### Symptom

LM Studio occasionally rejected requests.

Example:

 text id="6im2qt"
Conversation roles must alternate
 

---

### Root Cause

Message histories sometimes contained invalid role sequences.

---

### Solution

Message normalization before requests.

Workflow:

 text id="44wrt6"
Validate Messages
↓
Clean Messages
↓
Send To Model
 

---

### Result

More reliable model interactions.

---

## Most Important Lesson

The most valuable lesson from this project is:

 text id="hbjlwm"
Building the UI is easy.

Managing context is hard.
 

Most chatbot complexity comes from:

* State management
* Memory management
* Context construction
* Persistence

rather than the model itself.

---

# 12. Current Limitations and Future Roadmap

Although the chatbot is functional, several limitations remain.

These limitations define the future development roadmap.

---

## Current Limitations

### Limitation 1 – Summary Memory Only

Current memory uses:

 text id="v4jlwm"
Summary
+
Recent Messages
 

This works well but is imperfect.

Information may occasionally be omitted from summaries.

---

### Limitation 2 – No Document Understanding

Current system only understands chat messages.

Users cannot upload:

* PDFs
* Word documents
* Research papers

for analysis.

---

### Limitation 3 – No Semantic Retrieval

Current memory retrieval is based on summaries.

The system cannot search:

 text id="kq6mbs"
Most Relevant Information
 

across large datasets.

---

### Limitation 4 – Single Knowledge Source

Knowledge comes only from:

 text id="ndt5eq"
Conversation History
 

External documents are not yet integrated.

---

### Limitation 5 – No Autonomous Actions

The chatbot can answer questions but cannot:

* Execute tasks
* Use tools
* Make decisions
* Perform workflows

independently.

---

# Future Roadmap

The project roadmap intentionally progresses from simple concepts to advanced AI systems.

---

## Phase 4 – PDF Chat

Goal:

Allow users to upload PDFs and ask questions.

Architecture:

 text id="3sd1h7"
PDF
↓
Text Extraction
↓
LLM
↓
Answer
 

New Concepts:

* File uploads
* PDF parsing
* Text extraction

---

## Phase 5 – Embeddings

Goal:

Represent text numerically.

Architecture:

 text id="9whr8a"
Text
↓
Embedding Model
↓
Vector
 

New Concepts:

* Embeddings
* Similarity
* Semantic meaning

---

## Phase 6 – Vector Database

Goal:

Store embeddings efficiently.

Architecture:

 text id="xodgmr"
Chunks
↓
Embeddings
↓
Vector Store
 

Potential technologies:

* ChromaDB
* FAISS

---

## Phase 7 – Retrieval-Augmented Generation (RAG)

Goal:

Retrieve relevant information before generation.

Architecture:

 text id="h6t7we"
Question
↓
Retriever
↓
Relevant Chunks
↓
LLM
↓
Answer
 

Benefits:

* Better accuracy
* Reduced hallucinations
* Large document support

---

## Phase 8 – Multi-Document RAG

Goal:

Search across multiple documents simultaneously.

Architecture:

 text id="5i8npz"
Document A
Document B
Document C
↓
Retriever
↓
Relevant Chunks
↓
LLM
 

This transforms the chatbot into a personal knowledge assistant.

---

## Phase 9 – AI Agent

Goal:

Move beyond answering questions.

Architecture:

 text id="0dujlwm"
User Goal
↓
Planning
↓
Tool Usage
↓
Execution
↓
Result
 

Potential capabilities:

* Research
* File manipulation
* Multi-step reasoning
* Workflow automation

---

# Project Status

Current Position:


✅ Streamlit Chatbot
✅ Persistence
✅ Model Management
✅ Memory Summarization

⬜ PDF Chat
⬜ Embeddings
⬜ Vector Database
⬜ RAG
⬜ Multi-Document RAG
⬜ Agent
 

The Streamlit Chatbot phase is complete.

The next milestone is the transition from conversational memory to document understanding through PDF Chat and embeddings.
