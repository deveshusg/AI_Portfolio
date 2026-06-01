# AI Portfolio

A hands-on portfolio documenting my journey from basic LLM interactions to production-style AI systems built entirely on local infrastructure.

The objective of this repository is to understand how modern AI applications work under the hood by building each component from scratch instead of relying solely on high-level abstractions.

---

# Repository Goals

This repository is designed to help me:

* Understand Large Language Models (LLMs)
* Learn how AI applications are built end-to-end
* Build local AI systems using open-source models
* Understand memory architectures and context management
* Learn embeddings and vector databases
* Build Retrieval-Augmented Generation (RAG) systems
* Develop AI agents
* Learn evaluation and observability techniques
* Create portfolio-quality AI projects

---

# Technology Stack

## Programming

* Python
* Git
* GitHub

## Local AI

* LM Studio
* GGUF Models
* Qwen
* Gemma

## Application Development

* Streamlit
* FastAPI (planned)

## Retrieval & Search

* ChromaDB
* FAISS
* Sentence Transformers

## AI Frameworks

* LangChain
* LangGraph (planned)

---

# Repository Structure

```text
AI_Portfolio/
│
├── docs/
│
├── models/
│
├── shared/
│   ├── config/
│   ├── evaluation/
│   ├── prompts/
│   └── utils/
│
├── projects/
│   ├── 01_terminal_chatbot/
│   ├── 02_chat_memory/
│   ├── 03_streamlit_chatbot/
│   ├── 04_pdf_chat/
│   ├── 05_embeddings/
│   ├── 06_vector_database/
│   ├── 07_rag/
│   ├── 08_multi_document_rag/
│   ├── 09_ai_agent/
│   ├── 10_evaluation_observability/
│   └── 11_local_knowledge_assistant/
│
├── requirements.txt
└── README.md
```

---

# Learning Roadmap

The projects are intentionally ordered so that each project builds on concepts learned in previous projects.

---

## Quick Start

If you would like to run any project in this repository locally, see:


docs/setup_and_run_guide.md


The guide contains complete setup instructions, environment configuration, model setup, and execution steps for every project.


## Project 01 — Terminal Chatbot

### Status

✅ Complete

### Objective

Build a simple chatbot that communicates with a local LLM through LM Studio.

### Features

* Local model inference
* Configuration management
* Prompt management
* Terminal interface

### Skills Learned

* API communication
* Project structure
* Environment management
* Prompt engineering basics

---

## Project 02 — Conversation Memory

### Status

✅ Complete

### Objective

Extend the chatbot to remember previous messages and maintain conversational context.

### Features

* Conversation history
* Context persistence
* Memory management
* History injection

### Skills Learned

* Context windows
* Memory systems
* Chat history architecture
* Conversation state management

---

## Project 03 — Streamlit Chatbot

### Status

✅ Complete

### Objective

Transform the chatbot into a web application with improved usability and memory handling.

### Features

* Streamlit web interface
* Multi-chat support
* Conversation persistence
* Memory summarization
* Automatic memory compression
* Model switching
* Export functionality
* Regenerate responses
* Continue generation

### Skills Learned

* Streamlit
* State management
* Memory summarization
* User interface development
* Session handling

---

## Project 04 — PDF Chat

### Status

⬜ Planned

### Objective

Build a system capable of answering questions about uploaded PDF documents.

### Planned Features

* PDF upload
* Text extraction
* Text chunking
* Document question answering

### Skills Targeted

* PDF processing
* Document pipelines
* Retrieval workflows

---

## Project 05 — Embeddings

### Status

⬜ Planned

### Objective

Learn how text is transformed into vectors that capture semantic meaning.

### Skills Targeted

* Embedding models
* Semantic similarity
* Vector representations

---

## Project 06 — Vector Database

### Status

⬜ Planned

### Objective

Store and retrieve embeddings efficiently.

### Skills Targeted

* ChromaDB
* FAISS
* Similarity search
* Indexing

---

## Project 07 — Retrieval-Augmented Generation (RAG)

### Status

⬜ Planned

### Objective

Build an end-to-end retrieval system that augments LLM responses with external knowledge.

### Skills Targeted

* Retrieval pipelines
* Context augmentation
* Grounded generation

---

## Project 08 — Multi-Document RAG

### Status

⬜ Planned

### Objective

Allow querying across multiple documents simultaneously.

### Skills Targeted

* Multi-document retrieval
* Ranking strategies
* Advanced retrieval workflows

---

## Project 09 — AI Agent

### Status

⬜ Planned

### Objective

Build autonomous agents capable of reasoning and tool usage.

### Skills Targeted

* Agent frameworks
* Tool calling
* Planning
* Reasoning loops

---

## Project 10 — Evaluation & Observability

### Status

⬜ Planned

### Objective

Measure, monitor, and evaluate AI system performance.

### Skills Targeted

* Evaluation metrics
* Monitoring
* Experiment tracking
* AI observability

---

## Project 11 — Local Knowledge Assistant

### Status

⬜ Planned

### Objective

Combine all previous projects into a fully local AI assistant.

### Skills Targeted

* End-to-end AI architecture
* Knowledge retrieval
* Agent workflows
* Production-style design

---

# Current Progress

| Project                       | Status     |
| ----------------------------- | ---------- |
| 01 Terminal Chatbot           | ✅ Complete |
| 02 Chat Memory                | ✅ Complete |
| 03 Streamlit Chatbot          | ✅ Complete |
| 04 PDF Chat                   | ⬜ Planned  |
| 05 Embeddings                 | ⬜ Planned  |
| 06 Vector Database            | ⬜ Planned  |
| 07 RAG                        | ⬜ Planned  |
| 08 Multi-Document RAG         | ⬜ Planned  |
| 09 AI Agent                   | ⬜ Planned  |
| 10 Evaluation & Observability | ⬜ Planned  |
| 11 Local Knowledge Assistant  | ⬜ Planned  |

---

# Development Approach

This repository is developed using an AI-assisted learning workflow.

Tools such as ChatGPT are used to:

* Explain concepts and architectures
* Review implementation approaches
* Assist with debugging
* Accelerate documentation
* Generate ideas and alternatives
* Support project planning

All projects are manually built, tested, modified, debugged, and understood as part of the learning process.

The goal is not simply to use AI tools, but to develop a practical understanding of how modern AI systems are designed, implemented, evaluated, and deployed.

---

# Author

**Devesh Gupta**

Credit Risk Analyst building expertise in Artificial Intelligence, Machine Learning, LLM Applications, RAG Systems, and AI Engineering through hands-on project development.
