# Project 01 - Terminal Chatbot

Completion Date: 2026-05-31

## Objective

Build a terminal chatbot using LM Studio and OpenAI SDK.

## Key Concepts Learned

- Project structure
- Separation of concerns
- config.py
- prompts.py
- llm.py
- app.py
- OpenAI SDK
- Client object
- Response object
- Imports
- __name__ == "__main__"
- Temperature
- Max Tokens

## Challenges

- Understanding imports
- Understanding client creation
- Understanding __name__

## Key Insight

Importing a module executes the module and creates objects/functions in memory before making them available to other files.

## Future Improvements

- Error handling
- Memory
- Streaming
- Environment variables

# Project 02 - Memory Chatbot

Completion Date: 2026-05-31

## Objective

Build a chatbot that remembers previous conversation turns.

## Concepts Learned

* Message history
* Context windows
* Conversation memory
* Environment variables
* python-dotenv
* Multi-turn conversations

## Key Insight

Memory is not magic.

The model remembers only because previous messages are sent back with each new request.

## Future Work

* Persistent memory
* Token counting
* Memory trimming
* Summarization
