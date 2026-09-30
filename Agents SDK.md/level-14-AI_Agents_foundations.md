# OpenAI Agents SDK — Tools and Function Calling

## 1. Why Do Agents Need Tools?

An LLM by itself mainly produces text.

For example:

```text
User
 ↓
LLM
 ↓
Text response
```

But an agent becomes much more useful when it can perform actions:

```text
User
 ↓
Agent
 ↓
LLM
 ↓
Tool
 ↓
External result
 ↓
LLM
 ↓
Final answer
```

Examples:

* Search the web
* Search documents
* Run Python code
* Query a database
* Call an API
* Send an email
* Perform calculations
* Interact with another agent

### Mental model

```text
LLM = Brain
Tools = Hands
Runner = Loop
```

The LLM decides **what should happen**.

The tool performs the actual operation.

---

# 2. Three Types of Tools in the Agents SDK

The lesson introduces three categories:

```text
                    Tools
                      │
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
 Hosted Tools   Function Tools   Agents as Tools
```

## Type 1 — Hosted Tools

Tools provided/hosted by OpenAI.

Examples include capabilities such as:

* Web search
* File search
* Code interpreter
* Other hosted tool capabilities supported by the platform

The important idea is:

> You don't implement the underlying capability yourself.

You configure the hosted tool and make it available to the agent.

---

# 3. Hosted Tools

Suppose you want your agent to search the web.

Conceptually:

```text
Agent
  │
  ├── LLM
  │
  └── Web Search Tool
```

The model can decide:

```text
"Do I know the answer?"
        │
    ┌───┴───┐
    ↓       ↓
   Yes      No
    ↓       ↓
Answer   Web Search
            ↓
         Results
            ↓
           LLM
            ↓
         Answer
```

The advantage is that you don't need to build your own search engine integration for that capability.

---

# 4. Type 2 — Function Tools

Function tools are your **custom Python functions**.

This is one of the most important things in this lesson.

Suppose you already have:

```python
def add(a: float, b: float) -> float:
    return a + b
```

You can turn it into an agent tool using:

```python
@function_tool
```

Example:

```python
from agents import function_tool

@function_tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
```

Now `add()` isn't just an ordinary Python function.

It has been registered as a tool that the agent can use.

---

# 5. What Does `@function_tool` Do?

This:

```python
@function_tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
```

conceptually tells the SDK:

> "Make this Python function available as a tool that the model can call."

The SDK uses information from the function to create a tool schema.

---

# 6. Tool Schema

The LLM doesn't see your Python implementation directly.

For example, you write:

```python
@function_tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b
```

The SDK can expose information conceptually like:

```json
{
  "name": "multiply",
  "description": "Multiply two numbers together.",
  "parameters": {
    "type": "object",
    "properties": {
      "a": {
        "type": "number"
      },
      "b": {
        "type": "number"
      }
    },
    "required": ["a", "b"]
  }
}
```

The exact schema representation can vary, but the important information is:

```text
Tool name
Tool description
Parameters
Parameter types
Required parameters
```

The model uses this information to decide whether and how to call the tool.

---

# 7. Why Type Hints Matter

Look at:

```python
def multiply(a: float, b: float) -> float:
```

There are three pieces of information here:

```text
a: float
b: float
       ↓
input types

-> float
       ↓
return type
```

Type hints help the SDK understand the function's interface and generate the appropriate schema.

For example:

```python
def search_student(name: str) -> str:
```

tells the SDK:

```text
name = string
return value = string
```

---

# 8. Why the Docstring Matters

Look at:

```python
"""Multiply two numbers together."""
```

The docstring describes what the tool does.

The model can use that description when deciding which tool is appropriate.

For example:

```python
@function_tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
```

versus:

```python
@function_tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number."""
```

The model can distinguish:

```text
multiply → multiplication
divide   → division
```

### Remember

> **Good tool names + good descriptions + accurate type hints help the model select tools correctly.**

---

# 9. Type 3 — Agents as Tools

The third category is:

> **Agents as tools**

One agent can be exposed as a tool to another agent.

Conceptually:

```text
Manager Agent
      │
      ├── Math Agent
      ├── Research Agent
      └── Coding Agent
```

The manager can delegate work to specialized agents.

The SDK supports turning an agent into a tool through an interface such as:

```python
agent.as_tool(...)
```

Conceptually:

```text
Manager Agent
      ↓
"Research Agent"
      ↓
Research Agent performs task
      ↓
Result
      ↓
Manager Agent
```

### Agents as tools vs handoffs

Don't confuse these.

### Agents as tools

The manager remains in control and invokes another agent like a tool.

```text
Manager
  ↓
Worker Agent as Tool
  ↓
Result
  ↓
Manager continues
```

### Handoff

Control is transferred to another agent.

```text
Agent A
   ↓
Handoff
   ↓
Agent B
```

These are different orchestration patterns.

The course does not go deeply into agents-as-tools, so the important thing for now is simply knowing the concept.

---

# 10. Rule of Thumb for Choosing Tools

The lesson gives a useful rule.

### If a built-in/hosted capability already exists:

Use it.

For example:

```text
Need web search?
       ↓
Use hosted web search
```

Instead of building your own search tool immediately.

### If you need custom behavior:

Use a function tool.

```text
Need custom calculation?
       ↓
Write Python function
       ↓
@function_tool
```

### Simple rule

> **Built-in capability → Hosted Tool**
> **Custom logic → Function Tool**
> **Specialized agent capability → Agent as Tool**

---

# 11. Creating a Function Tool

Let's build a simple math tool.

```python
from agents import function_tool

@function_tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
```

Let's break this down.

### Step 1

```python
from agents import function_tool
```

Import the decorator.

---

### Step 2

```python
@function_tool
```

Tell the Agents SDK:

> Turn the following Python function into a tool.

---

### Step 3

```python
def add(a: float, b: float) -> float:
```

Define the function.

Inputs:

```text
a → float
b → float
```

Output:

```text
float
```

---

### Step 4

```python
"""Add two numbers together."""
```

Describe the tool.

---

### Step 5

```python
return a + b
```

The actual Python operation.

---

# 12. Multiple Tools

You can define several tools.

```python
from agents import function_tool

@function_tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@function_tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@function_tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return a / b


@function_tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b
```

Now we have:

```text
        Agent Tools
            │
    ┌───────┼────────┐
    ↓       ↓        ↓
   add  multiply   divide
            │
         subtract
```

---

# 13. Registering Tools With the Agent

Defining a tool is not enough.

The agent needs to know that the tool is available.

For example:

```python
agent = Agent(
    name="Math Agent",
    instructions="You are a helpful math assistant.",
    model="YOUR_MODEL_NAME",
    tools=[
        add,
        multiply,
        divide,
        subtract
    ]
)
```

The important part is:

```python
tools=[
    add,
    multiply,
    divide,
    subtract
]
```

This gives the agent access to those tools.

---

# 14. Complete Example

```python
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()


@function_tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@function_tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@function_tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return a / b


agent = Agent(
    name="Math Agent",
    instructions="""
    You are a helpful math assistant.
    Use the available tools when calculations are required.
    """,
    model="YOUR_MODEL_NAME",
    tools=[
        add,
        multiply,
        divide
    ]
)


result = Runner.run_sync(
    agent,
    "What is 15 multiplied by 8 and then divided by 3?"
)

print(result.final_output)
```

---

# 15. What Happens When We Ask the Question?

The user asks:

```text
What is 15 multiplied by 8 and then divided by 3?
```

The flow is:

```text
                 USER
                   │
                   ▼
             Runner.run_sync
                   │
                   ▼
                Agent
                   │
                   ▼
                  LLM
                   │
          "I need multiplication"
                   │
                   ▼
          multiply(15, 8)
                   │
                   ▼
                  120
                   │
                   ▼
                  LLM
                   │
          "Now I need division"
                   │
                   ▼
             divide(120, 3)
                   │
                   ▼
                   40
                   │
                   ▼
                  LLM
                   │
                   ▼
           "The answer is 40."
                   │
                   ▼
            final_output
```

---

# 16. Iteration 1

Initially:

```text
User:
15 × 8 ÷ 3
```

The LLM examines the available tools.

It sees:

```text
add
multiply
divide
```

It decides:

```text
I need multiply.
```

It requests:

```text
multiply(
    a=15,
    b=8
)
```

The SDK executes the Python function:

```python
15 * 8
```

Result:

```text
120
```

---

# 17. Iteration 2

The result goes back to the LLM.

The LLM now has:

```text
Original task:
15 × 8 ÷ 3

Previous tool result:
120
```

It determines:

```text
I still need to divide by 3.
```

So it requests:

```text
divide(
    a=120,
    b=3
)
```

Python executes:

```python
120 / 3
```

Result:

```text
40
```

---

# 18. Final Iteration

The LLM receives:

```text
40
```

Now it decides:

```text
No more tools are necessary.
```

It produces:

```text
The answer is 40.
```

The Runner returns:

```python
result.final_output
```

---

# 19. The Most Important Distinction

Remember:

## The LLM chooses the tool

```text
LLM
 ↓
"I need multiply"
```

## The SDK executes the tool

```text
Agents SDK
 ↓
multiply(15, 8)
 ↓
120
```

The LLM doesn't execute:

```python
15 * 8
```

The Python function does.

### Mental model

```text
LLM
=
Decision maker

Tool
=
Actual operation

Runner
=
Coordinates everything
```

---

# 20. Function Calling — What Does It Actually Mean?

"Function calling" does **not** mean:

> The LLM directly runs your Python function.

Instead:

```text
LLM
 ↓
Structured tool-call request
 ↓
Agents SDK
 ↓
Python function
 ↓
Result
 ↓
LLM
```

For example, conceptually the model might produce:

```json
{
  "name": "multiply",
  "arguments": {
    "a": 15,
    "b": 8
  }
}
```

The SDK receives that request.

Then it finds the corresponding Python function:

```python
multiply
```

and executes it.

---

# 21. Tool Calling Architecture

Memorize this:

```text
              ┌──────────────┐
              │     User     │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │    Runner    │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │     LLM      │
              └──────┬───────┘
                     │
              Tool call request
                     │
                     ↓
              ┌──────────────┐
              │ Agents SDK   │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │ Python Tool  │
              └──────┬───────┘
                     ↓
                  Result
                     │
                     ↓
                    LLM
                     │
                     ↓
                Final answer
```

---

# 22. What Does the SDK Automatically Handle?

Without a framework, you would have to manage things such as:

```text
Create tool schema
      ↓
Send schema to model
      ↓
Receive tool call
      ↓
Parse tool name
      ↓
Parse arguments
      ↓
Find Python function
      ↓
Execute function
      ↓
Handle errors
      ↓
Send result back to model
      ↓
Repeat loop
```

The Agents SDK handles much of this plumbing.

That's why the framework feels simple.

---

# 23. Tool Schema Generation

Your Python:

```python
@function_tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b
```

contains enough information for the SDK to construct the tool interface.

Conceptually:

```text
Python function
      │
      ├── Function name
      ├── Type hints
      ├── Docstring
      └── Return information
              ↓
        Tool definition
              ↓
        Model receives it
```

So:

> **Your Python function becomes the source of truth for the tool's interface.**

---

# 24. Tool Description Is Important

Imagine you have:

```python
@function_tool
def get_customer_data(id: str):
    """Get customer information using customer ID."""
```

The model can understand:

```text
Tool:
get_customer_data

Purpose:
Get customer information

Input:
id → string
```

That's why vague descriptions are bad.

Instead of:

```python
"""Get data."""
```

prefer:

```python
"""Retrieve customer profile information using a customer ID."""
```

A clear description helps the model choose the correct tool.

---

# 25. LangChain vs OpenAI Agents SDK

Since you already learned LangChain, this comparison is important.

## LangChain

Typical flow:

```text
Initialize Model
      ↓
Define Tools
      ↓
Create Agent
      ↓
Invoke Agent
      ↓
Parse Result
```

## OpenAI Agents SDK

Typical flow:

```text
Define Tools
      ↓
Define Agent
      ↓
Runner
      ↓
final_output
```

The course describes the Agents SDK as more lightweight and opinionated.

That is an architectural comparison, not a universal rule that one framework is always better.

---

# 26. Step 1 — Model Setup

### LangChain

You may explicitly initialize/configure the model:

```python
model = init_chat_model(...)
```

Then use the model while constructing your agent.

Conceptually:

```text
Model
 +
Tools
 +
Agent
```

### Agents SDK

The model can be specified directly in the Agent:

```python
agent = Agent(
    name="Math Agent",
    instructions="...",
    model="YOUR_MODEL_NAME",
    tools=[...]
)
```

Conceptually:

```text
Agent
 ├── Model
 ├── Instructions
 └── Tools
```

---

# 27. Step 2 — Tool Definition

### LangChain

```python
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b
```

### Agents SDK

```python
@function_tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b
```

The syntax is extremely similar.

The important difference is that these are decorators from different frameworks.

```text
LangChain
@tool

Agents SDK
@function_tool
```

---

# 28. Step 3 — Creating the Agent

### LangChain

The framework has multiple abstractions around:

* Models
* Prompts
* Chains
* Tools
* Agents
* Middleware
* Other integrations/orchestration features

### Agents SDK

You can define the core agent more directly:

```python
agent = Agent(
    name="Math Agent",
    instructions="You are a math assistant.",
    model="YOUR_MODEL_NAME",
    tools=[multiply, divide]
)
```

The conceptual structure is:

```text
Agent
 ├── Model
 ├── Instructions
 └── Tools
```

---

# 29. Step 4 — Running the Agent

### LangChain

You commonly invoke the agent through its invocation interface.

Conceptually:

```python
result = agent.invoke(...)
```

The exact input/result shape depends on the LangChain API/version and agent construction.

### Agents SDK

The Runner provides the execution abstraction:

```python
result = Runner.run_sync(
    agent,
    "What is 15 × 8?"
)
```

This gives you a clear separation:

```text
Agent
=
Definition

Runner
=
Execution
```

---

# 30. Step 5 — Getting the Answer

With the Agents SDK:

```python
result.final_output
```

is the convenient final answer surface.

Example:

```python
print(result.final_output)
```

So:

```text
Runner
 ↓
RunResult
 ↓
final_output
```

This is intentionally simple.

---

# 31. Comparison at a Glance

| Step          | LangChain                            | OpenAI Agents SDK             |
| ------------- | ------------------------------------ | ----------------------------- |
| Model         | Configure model separately           | Can configure inside `Agent`  |
| Custom tool   | `@tool`                              | `@function_tool`              |
| Agent         | Agent abstraction                    | `Agent(...)`                  |
| Execution     | Agent invocation                     | `Runner.run()` / `run_sync()` |
| Final answer  | Depends on result/message structure  | `result.final_output`         |
| Orchestration | Broad framework                      | Lightweight agent-focused SDK |
| Multi-agent   | Supported through framework patterns | Handoffs / agent-as-tool      |
| Guardrails    | Available through framework features | Built into SDK concepts       |
| Tracing       | LangSmith commonly used              | Built-in Agents SDK tracing   |

The exact APIs can evolve, so treat this as a conceptual comparison rather than a claim that every version has identical interfaces.

---

# 32. What Does "Lightweight" Mean Here?

It doesn't mean:

> Agents SDK has fewer capabilities.

It means the central agent abstraction is relatively direct.

Instead of thinking:

```text
Model
 ↓
Prompt
 ↓
Chain
 ↓
Parser
 ↓
Tool
 ↓
Agent
 ↓
Executor
```

you can often think:

```text
Agent
 ├── Model
 ├── Instructions
 └── Tools

Runner
 ↓
Execution
```

The Agents SDK is more opinionated about the agent architecture.

---

# 33. But Don't Think LangChain Is "Bad"

The lesson gives an opinion that Agents SDK can feel easier for beginners.

That's a **developer-experience preference**, not a technical law.

LangChain has a broad ecosystem and many integrations.

Agents SDK focuses more directly on agent primitives such as:

* Agents
* Tools
* Handoffs
* Guardrails
* Sessions
* Tracing

So choose based on your project's requirements.

---

# 34. One Very Important Connection

You've now seen the same tool-calling architecture in:

### LangChain

```text
User
 ↓
LangChain Agent
 ↓
LLM
 ↓
Tool Call
 ↓
LangChain
 ↓
Python Tool
 ↓
Result
 ↓
LLM
 ↓
Final Answer
```

### OpenAI Agents SDK

```text
User
 ↓
Agents SDK Runner
 ↓
LLM
 ↓
Tool Call
 ↓
Agents SDK
 ↓
Python Tool
 ↓
Result
 ↓
LLM
 ↓
Final Answer
```

The **framework implementation differs**, but the fundamental agent loop is very similar.

---

# 35. The Core Pattern 🧠

For function tools, memorize:

> **Write Python function → Add `@function_tool` → Register with Agent → Runner executes the loop**

```text
Python Function
      ↓
@function_tool
      ↓
Tool Schema
      ↓
Agent.tools
      ↓
Runner
      ↓
LLM chooses tool
      ↓
Python executes
      ↓
Result
      ↓
LLM
      ↓
Final Answer
```

---

# 36. Remember This Pattern

### Tool creation

```python
@function_tool
def tool_name(parameters: type) -> return_type:
    """Clearly describe what this tool does."""
    # actual Python logic
```

### Agent registration

```python
agent = Agent(
    name="...",
    instructions="...",
    model="...",
    tools=[tool_name]
)
```

### Execution

```python
result = Runner.run_sync(
    agent,
    user_question
)
```

### Final answer

```python
print(result.final_output)
```

---

# 37. Four Things You Should NEVER Forget

### 1. `@function_tool`

Turns your Python function into an agent tool.

### 2. Type hints

Help define the tool's input/output structure.

```python
a: float
b: float
```

### 3. Docstring

Describes the tool to the model.

```python
"""Multiply two numbers together."""
```

### 4. `tools=[...]`

Makes the tools available to the agent.

```python
tools=[add, multiply, divide]
```

---

# 38. Final Architecture

```text
                       USER
                         │
                         ▼
                  Runner.run_sync()
                         │
                         ▼
                      AGENT
              ┌──────────┼──────────┐
              │          │          │
            Model    Instructions  Tools
                                    │
                         ┌──────────┼──────────┐
                         ↓          ↓          ↓
                        add      multiply    divide
                         │          │          │
                         └──────────┼──────────┘
                                    ↓
                                   LLM
                                    │
                              "Which tool?"
                                    │
                                    ▼
                              Tool Call
                                    │
                                    ▼
                              Python Tool
                                    │
                                    ▼
                                 Result
                                    │
                                    ▼
                                   LLM
                                    │
                             More tools?
                              ↙       ↘
                            Yes        No
                             │          │
                           Loop       Final
                                        │
                                        ▼
                               result.final_output
```

---

# 39. Final Mental Model

Think of the whole system as:

```text
                 AGENT
                   │
          ┌────────┼────────┐
          ↓        ↓        ↓
        MODEL   INSTRUCTIONS TOOLS
                              │
                     ┌────────┼────────┐
                     ↓        ↓        ↓
                   Search   Math     Database
                     │        │        │
                     └────────┼────────┘
                              ↓
                         Runner Loop
                              │
                    ┌─────────┴─────────┐
                    ↓                   ↓
                 Tool call          Final answer
                    │
                    ↓
                 Execute
                    │
                    ↓
                  Result
                    │
                    └──────→ LLM
```

## One-line takeaway

> **Tools give the agent capabilities; the LLM decides when and which tool to call, while the Agents SDK/Runner handles the function-calling and execution loop.**

## The three tool types to remember

```text
1. Hosted Tools
   → Ready-made capabilities

2. Function Tools
   → Your custom Python functions

3. Agents as Tools
   → One agent used by another agent
```

For your current course, focus most heavily on **Hosted Tools + Function Tools**, because these are the foundations for the next agent-building steps.
