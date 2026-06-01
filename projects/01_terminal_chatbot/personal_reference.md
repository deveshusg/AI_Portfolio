Project 01: Terminal Chatbot

Before writing code, define the objective.

Objective

Build a chatbot that:

Accepts user input
Sends it to LM Studio
Gets a response from Qwen
Prints the response
Repeats until user exits


<!-- =========================================================================== -->
Imagine you're sitting at your terminal and type:

```text
What is machine learning?
```

The terminal passes this text to `app.py`, which acts like a receptionist and traffic controller. `app.py` doesn't know anything about AI models or APIs; its job is simply to collect your input and ask another component to handle it. It calls a function inside `llm.py`, passing your question as an argument. Inside `llm.py`, the first thing that happens is that it imports configuration values from `config.py`, such as the model name (`qwen2.5-1.5b-instruct`), the LM Studio API endpoint (`http://127.0.0.1:1234/v1`), the temperature setting, and any token limits. It also imports the system prompt from `prompts.py`, which contains instructions that shape the model's behavior. At this point, your original question has not been modified yet; the code is simply gathering the additional information needed to build a proper request.

Now `llm.py` constructs a Python object called a **payload**. Conceptually it looks like:

```python
{
    "model": "qwen2.5-1.5b-instruct",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What is machine learning?"
        }
    ],
    "temperature": 0.7
}
```

Think of this payload as a fully completed work order. Your question is only one field inside it. The system prompt, model name, and settings are additional instructions attached before the request leaves your application.

Next, the OpenAI Python SDK takes this Python object and converts it into JSON, which is a standard format for transmitting data between applications. It then sends the JSON as an HTTP request to LM Studio running locally on your computer. At this stage the information is no longer moving between Python files; it is moving across a network interface, even though the destination is still your own machine (`127.0.0.1` means "this computer"). LM Studio receives the HTTP request, validates it, identifies which model the request targets, and forwards the prompt to the loaded Qwen model.

This is where the actual AI work begins. Qwen does not understand strings or English sentences directly. Before any reasoning occurs, the tokenizer converts all text into tokens, which are numerical IDs. For example:

```text
"What"
↓
[3928]

"is"
↓
[374]

"machine"
↓
[12345]
```

The entire system prompt and your question become a long sequence of token IDs. These token IDs are then converted into vectors, which are large arrays of numbers representing meaning in a mathematical space. The vectors flow through dozens of transformer layers inside the neural network. Each layer applies billions of learned weights that were acquired during training. The model does not retrieve a stored answer from a database. Instead, it repeatedly performs one task:

```text
Given all previous tokens,
what is the most probable next token?
```

Suppose the model predicts:

```text
Machine
```

It appends that token to the sequence. Then it asks again:

```text
Given everything so far,
what is the next most probable token?
```

Perhaps:

```text
learning
```

Then:

```text
is
```

Then:

```text
a
```

This loop repeats hundreds of times. The response is literally built one token at a time. The model is not generating a paragraph all at once; it is continuously extending a sequence by predicting the next token until it decides to stop.

Once Qwen finishes generating tokens, the process reverses. The generated token IDs are detokenized back into human-readable text. LM Studio packages that text into a JSON response and sends it back through the local API. The OpenAI SDK receives the JSON, converts it into Python objects, and returns it to `llm.py`. `llm.py` extracts the actual answer text from the response object and returns a simple string to `app.py`. Finally, `app.py` prints that string to the terminal, where you see the answer.

So the complete journey is:

```text
You
↓
Terminal
↓
app.py
↓
llm.py
↓
config.py + prompts.py
↓
Payload Creation
↓
OpenAI SDK
↓
HTTP Request
↓
LM Studio
↓
Tokenizer
↓
Qwen Transformer Model
↓
Token Generation
↓
Detokenization
↓
LM Studio
↓
HTTP Response
↓
OpenAI SDK
↓
llm.py
↓
app.py
↓
Terminal
↓
You
```

The key realization at this level is that your question changes form multiple times during the journey:

```text
English Text
↓
Python String
↓
JSON Payload
↓
HTTP Request
↓
Token IDs
↓
Vectors/Tensors
↓
Predicted Token IDs
↓
English Text
↓
Python String
↓
Terminal Output
```

The information is the "same idea" throughout the journey, but it is repeatedly transformed into formats that each component can understand. That transformation pipeline is what most AI applications are really doing. The model itself is only one stage in a much larger data-processing system.
