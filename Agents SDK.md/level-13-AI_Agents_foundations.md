# OpenAI Agents SDK — Your First Agent

## 1. What is the OpenAI Agents SDK?

The **OpenAI Agents SDK** is a Python framework for building agentic applications.

It gives you ready-made components for:

* Defining agents
* Giving agents tools
* Running the agent loop
* Connecting multiple agents
* Handoffs between agents
* Input/output guardrails
* Tracing and debugging
* Managing agent execution

The SDK uses the **Responses API** as its model interaction layer for OpenAI models by default.

### Mental model

Think of it like this:

```text
                 OpenAI Agents SDK
                        │
        ┌───────────────┼────────────────┐
        ↓               ↓                ↓
      Agent           Runner           Tools
        │               │
        │               └── Agent Loop
        │
        ├── Instructions
        ├── Model
        ├── Tools
        ├── Handoffs
        └── Guardrails
```

---

# 2. The Agent Formula

The basic idea of an agent remains:

```text
Agent
  =
LLM
+
Instructions
+
Tools
+
Agent Loop
```

For the Agents SDK, you can think of an agent as an LLM configured with instructions, tools, and optional capabilities such as handoffs, guardrails, and structured outputs.

### Example

Suppose we build a **History Tutor**.

```text
LLM
 ↓
History knowledge

Instructions
 ↓
"Answer clearly and include a fun fact"

Tools
 ↓
History search tool

Loop
 ↓
Decide → use tool → observe → continue
```

---

# 3. Six Important Agents SDK Concepts

The lesson introduces six important concepts.

## 1. Agent

The agent is the main object you define.

It contains things such as:

* Name
* Instructions
* Model
* Tools
* Handoffs
* Guardrails
* Output configuration

Example:

```python
agent = Agent(
    name="History Tutor",
    instructions="Answer history questions clearly.",
    model="..."
)
```

Think:

> **Agent = configuration/definition of what the AI worker is supposed to do.**

---

# 4. Runner

This is one of the most important concepts in this lesson.

The **Runner executes the agent**.

You can think of:

```text
Agent = blueprint
Runner = engine
```

For example:

```python
result = Runner.run_sync(
    agent,
    "Who was the first president of the United States?"
)
```

The Runner manages the execution loop.

Conceptually:

```text
User question
      ↓
    Runner
      ↓
     LLM
      ↓
Need tool?
  ↙       ↘
No        Yes
 ↓         ↓
Answer   Execute tool
 ↓         ↓
Final ← Tool result
          ↓
        LLM again
```

The current SDK documentation describes the Runner loop as repeatedly calling the LLM, executing tool calls or handoffs when requested, and stopping when a final output is produced or the turn limit is reached.

---

# 5. Tools

Tools are functions the agent can use to perform actions.

For example:

```python
def get_weather(city):
    ...
```

can be exposed as an agent tool.

The important distinction is:

```text
LLM
 ↓
decides which tool to call
 ↓
Runner / SDK
 ↓
executes the Python function
 ↓
result
 ↓
LLM
```

The LLM doesn't magically execute your Python function.

It requests a tool call, and the SDK handles execution.

This is the same concept we saw earlier with LangChain.

---

# 6. Handoffs

Handoffs allow one agent to transfer control to another agent.

This becomes useful when you have specialized agents.

Example:

```text
                 Triage Agent
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
     Math Agent   History Agent  Coding Agent
```

Suppose the user asks:

> "Explain how recursion works."

The triage agent could hand the task to a coding specialist.

Or:

> "Who was Napoleon?"

It could hand the task to the history specialist.

So:

> **Handoff = transfer control from one agent to another specialized agent.**

---

# 7. Guardrails

Guardrails are safety/validation mechanisms.

They can validate:

* Input
* Output
* Agent behavior

Conceptually:

```text
User Input
    ↓
Input Guardrail
    ↓
Agent
    ↓
Output Guardrail
    ↓
User
```

For example, an agent might be instructed to answer only questions related to a company's internal documentation.

A guardrail can help detect inputs or outputs that violate the application's rules.

---

# 8. Tracing

Tracing lets you inspect what happened during an agent run.

Instead of seeing only:

```text
Final answer: 40
```

you can inspect the execution:

```text
User request
     ↓
Agent
     ↓
LLM call
     ↓
Tool call
     ↓
Tool result
     ↓
LLM call
     ↓
Final answer
```

This is extremely useful for debugging agentic applications.

The current SDK provides a Trace viewer in the OpenAI Dashboard for reviewing agent runs.

---

# 9. Installing the SDK

The current package installation is:

```bash
pip install openai-agents
```

The official SDK documentation uses this package name.

You also need your API key available through the environment.

For example:

```env
OPENAI_API_KEY=your_api_key_here
```

Never commit your `.env` file to GitHub.

---

# 10. Your First Agent

The basic process is very small.

```text
1. Define Agent
        ↓
2. Run Agent
        ↓
3. Get Final Output
```

Let's understand each one.

---

# 11. Step 1 — Define the Agent

First import:

```python
from agents import Agent, Runner
```

Then:

```python
agent = Agent(
    name="History Tutor",
    instructions="""
    You are a friendly history tutor.
    You answer history questions clearly and concisely.
    Always include an interesting fun fact in your answers.
    """,
    model="..."
)
```

There are three important parts here.

### `name`

```python
name="History Tutor"
```

This identifies the agent.

Think:

> **Name = job title**

Examples:

```text
History Tutor
Math Tutor
Coding Assistant
Research Agent
Customer Support Agent
```

---

### `instructions`

```python
instructions="""
You are a friendly history tutor.
Answer history questions clearly.
Always include an interesting fun fact.
"""
```

This defines how the agent should behave.

Think:

> **Instructions = job description**

---

### `model`

```python
model="..."
```

This specifies the model used by the agent.

The course uses `gpt-5.5` in its example, but model names are version-specific. The current Agents SDK documentation lists the current supported/default model configuration separately, so don't treat the course's model name as a timeless requirement.

For learning the SDK, the important concept is:

```text
Agent
  ↓
Model
```

---

# 12. Step 2 — Run the Agent

Now we have:

```python
result = Runner.run_sync(
    agent,
    "Who was the first president of the United States?"
)
```

Here:

```text
Runner.run_sync()
       │
       ├── agent
       │
       └── user input
```

`run_sync()` means:

> Run the agent synchronously and wait for the result.

The SDK also supports asynchronous execution:

```python
result = await Runner.run(
    agent,
    "Who was the first president of the United States?"
)
```

The current SDK also provides `Runner.run_streamed()` for streaming events while the agent runs.

### Simple comparison

```text
run_sync()
↓
Normal synchronous Python

run()
↓
Async Python

run_streamed()
↓
Async + streaming events
```

---

# 13. Step 3 — Get the Final Output

After:

```python
result = Runner.run_sync(...)
```

we get a result object.

The easiest thing to access is:

```python
result.final_output
```

Example:

```python
print(result.final_output)
```

Possible output:

```text
George Washington was the first president
of the United States.

Fun fact: Washington is the only U.S. president
to have been unanimously elected by the Electoral College.
```

The SDK's `RunResult` exposes `final_output` as the normal surface for the final answer.

---

# 14. Complete First-Agent Code

A simple version is:

```python
from dotenv import load_dotenv

load_dotenv()

from agents import Agent, Runner


agent = Agent(
    name="History Tutor",
    instructions="""
    You are a friendly history tutor.
    You answer history questions clearly and concisely.
    Always include an interesting fun fact in your answers.
    """,
    model="YOUR_MODEL_NAME",
)


result = Runner.run_sync(
    agent,
    "Who was the first president of the United States?"
)

print(result.final_output)
```

That's enough to create and run a basic agent.

---

# 15. Why Is Runner So Important?

This is probably the **most important concept in this lesson**.

Without an agent framework, you might manually implement:

```text
Call LLM
   ↓
Check response
   ↓
Did it request a tool?
   ↓
Yes
   ↓
Execute tool
   ↓
Send result to LLM
   ↓
Check again
   ↓
Tool needed?
   ↓
...
   ↓
Final answer
```

The Runner manages this process for you.

So:

```text
Runner
   │
   ├── calls LLM
   ├── checks result
   ├── executes tools
   ├── handles handoffs
   ├── continues loop
   └── stops when final output is produced
```

That's why the Runner is a central part of the SDK.

---

# 16. The Agentic Loop

Let's imagine our agent has a calculator tool.

User asks:

```text
What is 15 × 8 ÷ 3?
```

The execution could look like:

```text
USER
 │
 │ "What is 15 × 8 ÷ 3?"
 ↓
RUNNER
 │
 ↓
LLM
 │
 │ "I need multiplication."
 ↓
Tool: multiply(15, 8)
 │
 ↓
120
 │
 ↓
LLM
 │
 │ "Now I need division."
 ↓
Tool: divide(120, 3)
 │
 ↓
40
 │
 ↓
LLM
 │
 │ "The answer is 40."
 ↓
RUNNER
 │
 ↓
final_output
```

So the loop is:

```text
Reason
  ↓
Act
  ↓
Observe
  ↓
Reason
  ↓
Act
  ↓
Observe
  ↓
Final Answer
```

This is the same **ReAct-style agent loop** you've already learned.

---

# 17. Where Does Responses API Fit?

This is another very important connection.

Remember the OpenAI stack:

```text
Your Application
       ↓
Agents SDK
       ↓
Responses API
       ↓
OpenAI Model
```

The Agents SDK sits above the Responses API.

When you run:

```python
Runner.run_sync(agent, question)
```

conceptually:

```text
Your Python code
       ↓
Agents SDK
       ↓
Runner
       ↓
Responses API
       ↓
OpenAI Model
```

The SDK manages the orchestration instead of you manually implementing the entire loop.

The official SDK documentation explicitly describes the distinction this way: the Agents SDK uses the Responses API by default for OpenAI models, while the SDK provides the orchestration layer for turns, tools, guardrails, handoffs, and sessions.

---

# 18. What Happens If There Are NO Tools?

Suppose:

```python
agent = Agent(
    name="History Tutor",
    instructions="Answer history questions."
)
```

User:

```text
Who was the first president of the United States?
```

Flow:

```text
User
 ↓
Runner
 ↓
LLM
 ↓
No tool needed
 ↓
Generate answer
 ↓
final_output
```

Very simple.

---

# 19. What Happens If There IS a Tool?

Suppose we add:

```text
search_history()
```

User asks:

```text
What happened during a specific historical event?
```

The model may decide that it needs the tool.

Then:

```text
User
 ↓
Runner
 ↓
LLM
 ↓
Tool required
 ↓
Tool execution
 ↓
Tool result
 ↓
LLM
 ↓
Final answer
```

If more tools are required:

```text
LLM
 ↓
Tool 1
 ↓
Result
 ↓
LLM
 ↓
Tool 2
 ↓
Result
 ↓
LLM
 ↓
Final answer
```

The Runner keeps managing these turns.

---

# 20. Your Course Code — Explained Line by Line

Your original code:

```python
from dotenv import load_dotenv
```

Imports the function that loads environment variables from `.env`.

---

```python
load_dotenv()
```

Loads:

```text
OPENAI_API_KEY
```

and other environment variables.

---

```python
from agents import Agent, Runner
```

Imports two major SDK components.

```text
Agent
 ↓
Defines the agent

Runner
 ↓
Runs the agent
```

---

```python
agent = Agent(
```

Creates an Agent object.

---

```python
name="History Tutor",
```

Gives the agent its name.

---

```python
instructions="""
You are a friendly history tutor.
You answer history questions clearly and concisely.
Always include an interesting fun fact in your answers.
""",
```

Defines the agent's behavior.

This becomes part of what the model receives as its instructions.

---

```python
model="YOUR_MODEL_NAME",
```

Specifies the model.

---

Then:

```python
result = Runner.run_sync(
    agent,
    "Who was the first president of the United States?"
)
```

means:

```text
Take this agent
      +
this user question
      ↓
Run the agent
      ↓
Return result
```

---

Finally:

```python
print(result.final_output)
```

prints the final answer.

---

# 21. Running the Same Agent Multiple Times

You can reuse the same agent.

```python
result = Runner.run_sync(
    agent,
    "Who was the first president of the United States?"
)

print(result.final_output)


result2 = Runner.run_sync(
    agent,
    "What caused World War I?"
)

print(result2.final_output)
```

Conceptually:

```text
              History Tutor Agent
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
    Question 1             Question 2
          ↓                     ↓
       Runner                Runner
          ↓                     ↓
        Answer                Answer
```

The same agent configuration can handle both questions.

---

# 22. Important: Separate Runs and Conversation Memory

One thing to understand carefully:

```python
Runner.run_sync(agent, question1)
Runner.run_sync(agent, question2)
```

does **not automatically mean** the second run has all conversational history from the first run.

For persistent/multi-turn conversation state, the SDK provides mechanisms such as:

* Sessions
* `previous_response_id`
* `conversation_id`
* Input-list replay

The current documentation explicitly distinguishes these approaches.

So don't think:

```text
same Agent object
=
automatic memory
```

They are different concepts.

---

# 23. LangChain vs OpenAI Agents SDK

You've already learned LangChain, so connect the concepts.

### LangChain

```text
Agent
 +
Tools
 +
Runner/orchestration
```

### OpenAI Agents SDK

```text
Agent
 +
Tools
 +
Runner
 +
Handoffs
 +
Guardrails
 +
Tracing
```

Both are frameworks for building agentic systems.

The underlying concept is still:

```text
LLM
 ↓
Decision
 ↓
Tool / Handoff
 ↓
Observation
 ↓
Continue
 ↓
Final answer
```

---

# 24. Responses API vs Agents SDK

This distinction is extremely important.

## Responses API

Lower-level control.

```text
Your code
   ↓
Responses API
   ↓
Model
```

You manage more of the orchestration yourself.

---

## Agents SDK

Higher-level agent orchestration.

```text
Your code
   ↓
Agents SDK
   ↓
Runner
   ↓
Responses API
   ↓
Model
```

The SDK handles more of the agent execution lifecycle.

### Mental model

```text
Responses API
=
"Give me the model interface."

Agents SDK
=
"Help me build and run the agent."
```

---

# 25. Current Runner Behavior

The current SDK Runner supports:

```python
Runner.run()
Runner.run_sync()
Runner.run_streamed()
```

### `run()`

Async execution:

```python
result = await Runner.run(
    agent,
    question
)
```

### `run_sync()`

Synchronous execution:

```python
result = Runner.run_sync(
    agent,
    question
)
```

### `run_streamed()`

Useful when you want events/results while the agent is executing.

```python
result = Runner.run_streamed(
    agent,
    question
)
```

The official documentation currently lists all three execution modes.

---

# 26. Important Safety Feature: Max Turns

An agent should not be allowed to loop forever.

The Runner has a turn limit.

Conceptually:

```text
Agent
 ↓
LLM
 ↓
Tool
 ↓
LLM
 ↓
Tool
 ↓
LLM
 ↓
...
```

If something goes wrong, the SDK can stop after the configured maximum number of turns.

The current Runner documentation describes `max_turns` and raises `MaxTurnsExceeded` if the limit is exceeded.

This connects directly to the **runaway execution** threat you learned earlier.

---

# 27. Tracing Mental Model

Suppose your agent performs:

```text
User
 ↓
Agent
 ↓
LLM call
 ↓
Search tool
 ↓
Search result
 ↓
LLM call
 ↓
Calculator tool
 ↓
Result
 ↓
LLM call
 ↓
Final answer
```

Without tracing:

```text
Final answer
```

With tracing:

```text
┌──────────────────────────┐
│ Agent Run                │
├──────────────────────────┤
│ LLM call                 │
│ Tool call: search        │
│ Tool result              │
│ LLM call                 │
│ Tool call: calculator    │
│ Tool result              │
│ LLM call                 │
│ Final output             │
└──────────────────────────┘
```

This is extremely useful when your agent gives an unexpected answer.

---

# 28. The Complete Architecture

Put everything together:

```text
                     USER
                       │
                       ▼
              ┌─────────────────┐
              │  Your Python    │
              │   Application    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Agents SDK     │
              │                 │
              │     Agent       │
              │       +         │
              │     Runner      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Responses API  │
              └────────┬────────┘
                       │
                       ▼
                    LLM
                       │
              ┌────────┴────────┐
              │                 │
          No tool            Tool needed
              │                 │
              │                 ▼
              │              Tool
              │                 │
              │                 ▼
              │              Result
              │                 │
              │                 └──────┐
              │                        │
              └────────────────────────┘
                       │
                       ▼
                 Final Output
                       │
                       ▼
                      USER
```

And for multiple agents:

```text
                     USER
                       │
                       ▼
                 Triage Agent
                       │
            ┌──────────┼──────────┐
            ↓          ↓          ↓
       Math Agent  History Agent  Coding Agent
            │          │          │
            └──────────┼──────────┘
                       ↓
                  Final Output
```

---

# 29. The Three Lines to Memorize

For your first Agents SDK agent, remember:

```python
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant."
)

result = Runner.run_sync(
    agent,
    "Hello!"
)

print(result.final_output)
```

That's the basic pattern.

---

# 30. Core Pattern 🧠

### Memorize this:

> **Define the Agent → Run it with Runner → Read `final_output`**

```text
Agent
 ↓
Runner
 ↓
final_output
```

And remember:

> **Agent = what the agent is.**
> **Runner = how the agent runs.**

---

# 31. Runner — Most Important Mental Model

Remember:

> **Runner = the agent loop manager.**

It can repeatedly handle:

```text
LLM
 ↓
Tool?
 ↓
Execute tool
 ↓
Result
 ↓
LLM again
 ↓
Handoff?
 ↓
Another agent
 ↓
Final output
```

So the Runner is not just a function that "calls the model."

It manages the execution of the agent workflow.

---

# 32. What You Should Know Before the Next Lessons

After this lesson, you should understand:

### Agent

```text
Agent = LLM + instructions + capabilities
```

### Runner

```text
Runner = executes/manages agent loop
```

### Tool

```text
Tool = function agent can request
```

### Handoff

```text
Handoff = transfer control to another agent
```

### Guardrail

```text
Guardrail = validation/safety layer
```

### Tracing

```text
Tracing = inspect what happened during execution
```

### Responses API

```text
Responses API = model interaction layer
```

### Agents SDK

```text
Agents SDK = higher-level agent orchestration framework
```

---

# 33. Final Mental Model

This is the one diagram I would memorize:

```text
                 OPENAI AGENTS SDK
                         │
              ┌──────────┴──────────┐
              │                     │
            Agent                 Runner
              │                     │
       ┌──────┼──────┐              │
       │      │      │              │
     Model  Tools  Instructions     │
              │                     │
              └─────────┬───────────┘
                        ↓
                  Agentic Loop
                        │
              ┌─────────┴─────────┐
              ↓                   ↓
          Tool call            Handoff
              │                   │
              ↓                   ↓
           Result             New Agent
              │                   │
              └─────────┬─────────┘
                        ↓
                  Final Output
                        │
                        ↓
                   Your App
```

And underneath:

```text
Agents SDK
     ↓
Responses API
     ↓
OpenAI Model
```

## One-line takeaway

> **The Agents SDK gives you an `Agent` to define behavior and a `Runner` to execute the agentic loop, while tools, handoffs, guardrails, and tracing add capabilities around that loop.**
