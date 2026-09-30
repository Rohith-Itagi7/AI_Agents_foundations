# OpenAI Responses API

## 1. What is the Responses API?

The **Responses API** is an OpenAI API for interacting with OpenAI models.

At the simplest level:

```text
Your Python Code
      ↓
Responses API
      ↓
OpenAI Model
      ↓
Response
```

You give the model some input:

```text
"Explain MCP to me."
```

and receive a response.

But the Responses API can do much more than simple text generation. It supports things such as:

* Multi-turn conversation state
* Function calling
* Web search
* File search
* Code execution
* Computer use
* Remote MCP servers
* Other tool workflows

OpenAI's current documentation describes the Responses API as a core API for these tool-enabled workflows.

---

# 2. Where does Responses API fit?

Remember the OpenAI stack:

```text
┌────────────────────────────┐
│      YOUR APPLICATION      │
│ UI + Business Logic        │
└─────────────┬──────────────┘
              ↓
┌────────────────────────────┐
│       AGENTS SDK            │
│ Agents / Handoffs /         │
│ Guardrails / Orchestration  │
└─────────────┬──────────────┘
              ↓
┌────────────────────────────┐
│       RESPONSES API         │
│ Conversation + Tools +      │
│ Model interaction           │
└─────────────┬──────────────┘
              ↓
┌────────────────────────────┐
│       OPENAI MODELS         │
└────────────────────────────┘
```

### Important

The **Agents SDK sits above the Responses API**.

So:

```text
Agents SDK
     ↓
Responses API
     ↓
Model
```

You can use the Responses API directly when you want more control, or use a higher-level agent framework when you want more agent orchestration.

---

# 3. Responses API vs old Chat Completions

The course is teaching a simplification compared with the older Chat Completions interface.

### Older style

You commonly worked with a message array:

```python
response = client.chat.completions.create(
    model="...",
    messages=[
        {"role": "user", "content": "Explain MCP"}
    ]
)

answer = response.choices[0].message.content
```

You had to navigate through:

```text
response
 ↓
choices[0]
 ↓
message
 ↓
content
```

---

# 4. Responses API style

The basic structure is simpler:

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="MODEL_NAME",
    input="Explain MCP to me."
)

print(response.output_text)
```

The important difference is:

```text
Input
 ↓
response
 ↓
output_text
```

Instead of:

```text
response
 ↓
choices
 ↓
message
 ↓
content
```

### Mental model

Remember:

> **Responses API = simpler interface for model responses + tools + state.**

---

# 5. Basic setup

Install the OpenAI Python SDK:

```bash
pip install openai
```

Then configure your API key through an environment variable.

For example:

```text
OPENAI_API_KEY=your_key
```

Then:

```python
from openai import OpenAI

client = OpenAI()
```

The SDK reads the API key from the environment.

### Security rule

Don't do this:

```python
client = OpenAI(api_key="my-secret-key")
```

inside code that you commit to GitHub.

Instead:

```text
Environment variable
        ↓
OpenAI SDK
        ↓
API
```

---

# 6. First Responses API call

Conceptually:

```python
response = client.responses.create(
    model="MODEL_NAME",
    input="What is MCP?"
)

print(response.output_text)
```

Let's understand every part.

### `client`

```python
client = OpenAI()
```

Creates the OpenAI API client.

---

### `responses.create()`

```python
client.responses.create(...)
```

Means:

> "Create a model response."

---

### `model`

```python
model="MODEL_NAME"
```

Specifies which OpenAI model should process the request.

---

### `input`

```python
input="What is MCP?"
```

This is what you're asking the model.

---

### `output_text`

```python
response.output_text
```

Gets the generated text conveniently.

---

# 7. Core Feature #1 — Simple Input and Output

The first major idea from the lesson is:

```text
Simple input
      ↓
Responses API
      ↓
Simple output
```

For example:

```python
response = client.responses.create(
    model="MODEL_NAME",
    input="Explain recursion to a beginner."
)

print(response.output_text)
```

You don't need to manually construct a conversation array for this simple request.

---

# 8. Core Feature #2 — Conversation State

This is one of the most important concepts.

Suppose you have:

### Turn 1

```text
User:
My name is Alice and I love hiking.
```

Model:

```text
Nice to meet you, Alice!
```

Then:

### Turn 2

```text
User:
What is my hobby?
```

The model needs access to the previous context.

---

# 9. `previous_response_id`

The Responses API supports chaining responses using:

```python
previous_response_id
```

Conceptually:

```text
Response 1
    ↓
Response 2
    ↓
Response 3
    ↓
Response 4
```

Example:

```python
first = client.responses.create(
    model="MODEL_NAME",
    input="My name is Alice and I love hiking."
)

second = client.responses.create(
    model="MODEL_NAME",
    previous_response_id=first.id,
    input="What is my hobby?"
)

print(second.output_text)
```

The second request references the first response:

```text
first.id
   ↓
previous_response_id
```

OpenAI's current documentation still supports this response-chaining mechanism.

---

# 10. What is actually happening?

Think of it like this:

```text
FIRST REQUEST

User:
"My name is Alice and I love hiking."

        ↓

Responses API

        ↓

Response #001
        │
        └── ID = abc123
```

Then:

```text
SECOND REQUEST

input:
"What is my hobby?"

previous_response_id:
"abc123"

        ↓

Responses API

        ↓

Model can continue the conversation
```

So you don't have to manually reconstruct the whole conversation every time.

---

# 11. Important correction about tokens

The course says response chaining means you consume fewer tokens because you don't resend the conversation.

Be careful with that statement.

The current OpenAI documentation explicitly says:

> Even when using `previous_response_id`, previous input tokens in the chain are billed as input tokens.

So the better mental model is:

### It simplifies state management

rather than:

### It automatically makes long conversations cheaper.

You still need to think about context length and token usage.

---

# 12. Conversations API

There is also a more durable conversation-state mechanism in the current OpenAI platform: the **Conversations API**.

Conceptually:

```text
Conversation
     │
     ├── User message
     ├── Assistant response
     ├── Tool call
     ├── Tool result
     └── More messages
```

A conversation can have its own durable identifier and be used with the Responses API across interactions.

So today you can think of conversation state in two useful ways:

```text
Responses API
 ├── previous_response_id
 │
 └── Conversations API
```

---

# 13. Core Feature #3 — Built-in Tools

This is where Responses API becomes much more interesting.

A normal model:

```text
User
 ↓
LLM
 ↓
Answer
```

With tools:

```text
User
 ↓
LLM
 ↓
Decides whether tool is needed
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
Answer
```

The current OpenAI tools documentation lists built-in capabilities including web search, file search, computer use, code execution, image generation, and remote MCP connections, along with function calling and other tool mechanisms.

---

# 14. Web Search

Web search lets the model retrieve current information.

Conceptually:

```python
response = client.responses.create(
    model="MODEL_NAME",
    tools=[
        {"type": "web_search"}
    ],
    input="What happened in AI today?"
)
```

The model can decide that web search is needed.

Current OpenAI documentation shows web search being configured as a tool on a Responses API request.

---

# 15. Why does the model decide whether to search?

Suppose you ask:

```text
What is the capital of France?
```

The model already knows:

```text
Paris
```

A web search isn't necessarily needed.

But:

```text
What are the latest AI developments this week?
```

requires current information.

So conceptually:

```text
User question
      ↓
Model
      ↓
Need external/current information?
      │
   ┌──┴──┐
   NO    YES
   ↓      ↓
Answer   Web Search
            ↓
          Results
            ↓
          Model
            ↓
          Answer
```

OpenAI's documentation describes the model as automatically deciding whether to use a configured tool based on the prompt.

---

# 16. File Search

File search is for retrieving information from files.

Example:

```text
You upload:
company_policy.pdf
employee_handbook.pdf
product_docs.pdf
```

Then ask:

```text
"What is our refund policy?"
```

The model can use file search to retrieve relevant information from your uploaded files.

Mental model:

```text
Your Files
    ↓
File Search
    ↓
Relevant information
    ↓
Model
    ↓
Answer
```

---

# 17. Code Interpreter / Code Execution

This gives the model access to a code-execution environment for tasks such as analysis.

Example:

```text
User:
Analyze this CSV and find the average revenue.
```

Conceptually:

```text
User
 ↓
Model
 ↓
Code tool
 ↓
Python execution
 ↓
Result
 ↓
Model
 ↓
Answer
```

This is useful for:

* Data analysis
* Calculations
* Processing files
* Generating charts
* Numerical operations

The current OpenAI documentation lists code interpreter under its computer/code tooling.

---

# 18. Computer Use

Computer-use capabilities allow models to interact with computer interfaces.

Conceptually:

```text
Model
 ↓
Computer tool
 ↓
Click
 ↓
Type
 ↓
Read screen
 ↓
Continue
```

For example:

```text
Open website
↓
Click button
↓
Fill form
↓
Submit
```

The exact availability and configuration depend on the model/tool integration, so don't treat the course's "experimental/beta" wording as a current status claim. OpenAI's current documentation has a dedicated computer-use tool category.

---

# 19. MCP + Responses API

This connects directly to what you just learned.

Responses API can also work with **remote MCP servers**.

So your previous MCP architecture:

```text
Agent
 ↓
MCP Client
 ↓
MCP Server
 ↓
External API
```

can now appear as part of an OpenAI tool-enabled workflow:

```text
Your Application
       ↓
Responses API
       ↓
OpenAI Model
       ↓
MCP Tool
       ↓
MCP Server
       ↓
External System
```

OpenAI's current tools documentation explicitly lists remote MCP servers as a supported tool integration.

---

# 20. The big picture

You have now learned these pieces:

```text
                  YOUR APPLICATION
                         │
                         ↓
                ┌────────────────┐
                │ Responses API  │
                └───────┬────────┘
                        │
                        ↓
                     MODEL
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
      Web Search    File Search   Function
                                    Calling
          │             │             │
          ↓             ↓             ↓
       Internet       Files       Your Code
                                      │
                                      ↓
                                 External API
```

And MCP can also be another tool connection:

```text
                         MODEL
                           │
                           ↓
                       MCP Tool
                           │
                           ↓
                      MCP Server
                           │
                           ↓
                    External System
```

---

# 21. Responses API vs Agents SDK

This distinction is extremely important for the next lessons.

### Responses API

Think:

> **"I want direct control over the model interaction and tool calls."**

You can build your own orchestration.

```text
Your Code
   ↓
Responses API
   ↓
Model
   ↓
Tools
```

---

### Agents SDK

Think:

> **"I want a framework for building agents and orchestrating them."**

```text
Your Code
   ↓
Agents SDK
   ↓
Responses API
   ↓
Model + Tools
```

So:

```text
Agents SDK
     ↓
Responses API
     ↓
Model
```

---

# 22. Why is Responses API important for Agents?

Remember your earlier definition:

```text
Agent = LLM + Tools + Loop
```

Responses API gives you the model interaction and tool mechanisms.

But if you're building the loop/orchestration yourself, you might have:

```text
while not finished:

    ask model

    if model requests tool:
        execute tool

    give result back to model

    continue
```

That's where the Agents SDK becomes useful.

It gives you higher-level agent abstractions.

---

# 23. The complete mental model

You can now connect all your previous lessons:

```text
                    USER
                      │
                      ↓
               YOUR APPLICATION
                      │
                      ↓
                ┌───────────┐
                │ Agents SDK│
                └─────┬─────┘
                      │
                      ↓
                Responses API
                      │
                      ↓
                    MODEL
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
      Tools         MCP          Handoffs
        │             │             │
        ↓             ↓             ↓
     APIs       MCP Servers      Other Agents
```

---

# 24. What you should remember from this lesson

### 1. Responses API

```text
Core interface for interacting with OpenAI models.
```

### 2. Simple input/output

```python
input="..."
       ↓
response.output_text
```

### 3. Conversation state

```text
previous_response_id
```

can chain responses.

The current platform also provides the Conversations API for durable conversation state.

### 4. Tools

Responses API supports tool-enabled workflows such as:

```text
Web Search
File Search
Function Calling
Code Execution
Computer Use
MCP
```

with availability depending on the model and integration.

### 5. Model decides

When tools are configured, the model can determine whether a tool is useful for the request.

### 6. Agents SDK

```text
Agents SDK
     ↓
Responses API
```

The SDK is the higher-level agent-building layer.

---

# 25. One thing to update from the course

The transcript says the latest model "as of this recording" is GPT-5.5 and uses GPT-4.1 in examples. Those are **course-era examples**, not current model guidance.

OpenAI's current model documentation lists the GPT-5.6 family, including GPT-5.6 Sol, Terra, and Luna, and says the latest models are available through the Responses API.

So when you practice the code, **use the model ID currently recommended in the OpenAI docs/account you are using**, rather than blindly copying an old course model name.

---

# 🔥 Final mental model

```text
                    RESPONSES API
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ↓                ↓                ↓
     INPUT        CONVERSATION         TOOLS
                      STATE
                         │
                  previous_response_id
                         │
                         ↓
                       MODEL
                         │
       ┌─────────┬───────┼────────┬──────────┐
       ↓         ↓       ↓        ↓          ↓
      Web      Files   Functions  Code      MCP
     Search    Search  /Custom    Exec     Servers
```

**The most important sentence:**

> **Responses API is the core model-interaction layer; it lets you send input, maintain conversation state, and connect models to tools. The Agents SDK builds a higher-level agent orchestration layer on top of it.**
