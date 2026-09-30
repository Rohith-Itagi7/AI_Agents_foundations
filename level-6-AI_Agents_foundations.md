# MCP + LangChain Agent — Before & After MCP

## 1. What Are We Changing?

Previously, our first agent looked like:

```text
User
 ↓
Agent
 ↓
LLM
 ↓
Local Python Tools
 ↓
Tool Result
 ↓
LLM
 ↓
Final Answer
```

The tools were defined directly inside the agent Python file.

For example:

```python
@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
```

And:

```python
tools = [
    add,
    multiply,
    divide,
    square_root
]
```

This works.

But there is a major limitation:

> **The tools are trapped inside that application.**

---

# 2. Before MCP

The original application contained:

```text
Agent Python File
│
├── LLM
├── Agent Loop
│
├── add()
├── multiply()
├── divide()
└── square_root()
```

The agent directly owns the tools.

### Example

```text
User
 ↓
Agent
 ↓
LLM
 ↓
multiply()
 ↓
120
 ↓
LLM
 ↓
Final Answer
```

The Python application directly executes:

```python
multiply(15, 8)
```

---

# 3. Problems With Local Tools

The local approach has several limitations.

### Problem 1 — Tools are hardcoded

The tools are defined directly inside the application.

```python
@tool
def multiply(...):
    ...
```

Another application doesn't automatically know this tool exists.

---

### Problem 2 — No easy sharing

Suppose you create:

```text
multiply()
divide()
add()
square_root()
```

inside your LangChain agent.

Now suppose you want Claude to use the same tools.

You would need another integration.

Likewise for another AI application.

---

### Problem 3 — Tool updates are coupled to the application

Suppose:

```python
divide()
```

has a bug.

You need to update the application containing that function.

If several applications have copied the same implementation, you potentially need to update each one.

---

### Problem 4 — No centralized tool ownership

The application owns:

```text
Tool definitions
Tool schemas
Tool execution
Tool registration
```

Everything is tightly coupled.

---

# 4. After MCP

MCP separates the tools from the agent.

Instead of:

```text
Agent
│
├── LLM
├── Loop
├── add()
├── multiply()
├── divide()
└── sqrt()
```

we have:

```text
Agent
│
├── LLM
├── Agent Loop
└── MCP Client
        │
        ↓
   MCP Server
        │
        ├── add()
        ├── multiply()
        ├── divide()
        └── sqrt()
```

Now the tools live independently on the MCP server.

---

# 5. The New Architecture

```text
                    USER
                      ↓
                    HOST
                      ↓
                     LLM
                      ↓
                 Agent Loop
                      ↓
                 MCP Client
                      ↓
                JSON-RPC / stdio
                      ↓
                 MCP Server
                      ↓
                  Tool
                      ↓
                 Tool Result
                      ↓
                 MCP Client
                      ↓
                     LLM
                      ↓
                Final Answer
```

The major addition is:

```text
MCP Client ↔ MCP Server
```

---

# 6. What Is FastMCP?

**FastMCP** is a framework for building MCP servers easily.

It handles much of the MCP infrastructure for you.

Instead of manually implementing:

* JSON-RPC messages
* Tool schemas
* Request handling
* Tool registration
* Protocol communication

you can use FastMCP abstractions.

The mental model is similar to the `@tool` decorator you saw in LangChain.

With FastMCP:

```python
@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b
```

FastMCP turns this Python function into an MCP tool.

---

# 7. MCP Server Code

A simple math MCP server conceptually looks like:

```python
from fastmcp import FastMCP

mcp = FastMCP("math")

@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@mcp.tool
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@mcp.tool
def square_root(x: float) -> float:
    """Calculate the square root of a number."""
    return x ** 0.5

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

The exact API can vary by FastMCP version, but the architecture is what matters.

---

# 8. What Does the Server Code Do?

The server essentially performs three major jobs.

```text
MCP Server
│
├── 1. Create server
│
├── 2. Register tools
│
└── 3. Run server
```

---

# 9. Step 1 — Create the MCP Server

```python
mcp = FastMCP("math")
```

This creates an MCP server named:

```text
math
```

Think:

```text
FastMCP("math")
       ↓
Math MCP Server
```

---

# 10. Step 2 — Register Tools

Example:

```python
@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b
```

The decorator:

```python
@mcp.tool
```

registers the function as an MCP tool.

---

# 11. How FastMCP Builds the Tool Schema

FastMCP can inspect your Python function.

For:

```python
def multiply(a: float, b: float) -> float:
```

it can determine:

```text
Tool name:
multiply

Inputs:
a → float
b → float

Return:
float
```

The docstring:

```python
"""Multiply two numbers together."""
```

becomes the tool description.

Conceptually:

```text
multiply
│
├── description
│   └── Multiply two numbers together.
│
├── a
│   └── float
│
└── b
    └── float
```

This information can be exposed during:

```text
tools/list
```

---

# 12. Why Type Hints Matter

Consider:

```python
def multiply(a: float, b: float) -> float:
```

The type hints communicate the expected input types.

```text
a → float
b → float
```

The framework can use this information to construct an input schema.

This is another reason type hints are useful beyond readability.

---

# 13. Why Docstrings Matter

Consider:

```python
"""Multiply two numbers together."""
```

The docstring tells the model/client what the tool does.

The model might see:

```text
Tool:
multiply

Description:
Multiply two numbers together.

Arguments:
a: float
b: float
```

The LLM can use this description when deciding whether the tool is appropriate.

So tool descriptions should be:

* Clear
* Specific
* Accurate

---

# 14. Step 3 — Run the Server

The server must actually start listening for MCP communication.

For a local server:

```python
mcp.run(transport="stdio")
```

This means the server communicates through:

```text
stdin
stdout
```

The server waits for JSON-RPC messages.

It doesn't independently start solving math problems.

It waits for a client to communicate with it.

---

# 15. Important: The Server Doesn't Run by Itself

This is a common beginner misunderstanding.

When you define:

```python
@mcp.tool
def multiply(...):
```

the tool isn't automatically being called.

The server is waiting.

Conceptually:

```text
MCP Server
     │
     ↓
Waiting...
     │
     ↓
Client sends request
     │
     ↓
Server executes tool
     │
     ↓
Returns result
```

Something has to start the server process.

In this example, the agent launches it as a subprocess.

---

# 16. Why `stdio`?

The server is running locally.

So:

```text
Agent
  ↓
MCP Client
  ↓
stdin/stdout
  ↓
MCP Server
```

There is:

* No network
* No port
* No HTTP server

The processes communicate through standard input/output.

---

# 17. Now We Need an MCP Client

MCP follows:

```text
Client ↔ Server
```

So after creating:

```text
Math MCP Server
```

we need:

```text
MCP Client
```

The client connects the agent to the server.

---

# 18. MultiServerMCPClient

The example uses:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
```

Then:

```python
client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": [server_path],
            "transport": "stdio",
        }
    }
)
```

This configuration tells the client how to start/connect to the server.

---

# 19. Understanding the Configuration

Let's break this down.

```python
{
    "math": {
        "command": "python",
        "args": [server_path],
        "transport": "stdio",
    }
}
```

There are several pieces.

---

# 20. `"math"`

```python
"math": {
```

`math` is a label chosen by you.

It helps identify the server.

For example:

```python
{
    "math": {...},
    "github": {...},
    "database": {...}
}
```

Now you can distinguish the different servers.

It doesn't mean the server must be named `"math"`.

It's simply a configuration label.

---

# 21. `"command": "python"`

```python
"command": "python"
```

This tells the client:

> Use Python to start the MCP server.

It is conceptually similar to running:

```bash
python mcp_math_server.py
```

in the terminal.

---

# 22. `"args": [server_path]`

```python
"args": [server_path]
```

This tells Python which script to execute.

Conceptually:

```text
python
  +
mcp_math_server.py
```

becomes:

```bash
python mcp_math_server.py
```

---

# 23. Finding the Server Path

The code uses:

```python
current_dir = os.path.dirname(
    os.path.abspath(__file__)
)

server_path = os.path.join(
    current_dir,
    "mcp_math_server.py"
)
```

Let's understand it.

### `__file__`

Python's:

```python
__file__
```

represents the current Python source file's path.

---

### `os.path.abspath(__file__)`

Converts it into an absolute path.

For example:

```text
C:\projects\mcp\first_agent_with_mcp.py
```

---

### `os.path.dirname(...)`

Gets the directory:

```text
C:\projects\mcp
```

---

### `os.path.join(...)`

Adds:

```text
mcp_math_server.py
```

Result:

```text
C:\projects\mcp\mcp_math_server.py
```

So:

```python
server_path
```

contains the absolute path to the MCP server.

---

# 24. `"transport": "stdio"`

```python
"transport": "stdio"
```

This tells the client:

> Communicate with this MCP server through standard input/output.

Therefore:

```text
MCP Client
    │
    │ stdin/stdout
    ↓
MCP Server
```

No network connection is required.

---

# 25. What Does the Client Actually Do?

The client effectively starts:

```bash
python mcp_math_server.py
```

as a subprocess.

Conceptually:

```text
Agent
 │
 │ starts
 ↓
Python Process
 │
 └── mcp_math_server.py
```

Then:

```text
Agent/MCP Client
      ↕
 stdin/stdout
      ↕
MCP Server
```

---

# 26. Why Is This Called a Subprocess?

A **subprocess** is a separate process started by another program.

For example:

```text
Main process
     │
     └── starts
          ↓
     Child process
```

Here:

```text
Agent
  │
  └── starts
        ↓
   MCP server process
```

The MCP server becomes the child process.

---

# 27. Discovering Tools

Once the client connects:

```python
tools = await client.get_tools()
```

This is a very important line.

It means:

> Connect to the configured MCP server(s) and discover their tools.

Conceptually:

```text
client.get_tools()
       ↓
MCP connection
       ↓
tools/list
       ↓
MCP Server
       ↓
Available tools
```

The server might respond:

```text
add
multiply
divide
square_root
```

---

# 28. Dynamic Discovery

This is one of the biggest differences from the original agent.

### Before MCP

You manually wrote:

```python
tools = [
    add,
    multiply,
    divide,
    square_root
]
```

### After MCP

You write:

```python
tools = await client.get_tools()
```

The server tells you what tools exist.

That's:

> **Dynamic tool discovery.**

---

# 29. What Happens Internally?

Conceptually:

```text
client.get_tools()
       ↓
MCP Client
       ↓
tools/list
       ↓
MCP Server
       ↓
Tool definitions
       ↓
MCP Client
       ↓
LangChain-compatible tools
```

The adapter converts the discovered MCP tools into tools the LangChain agent can use.

---

# 30. Creating the Agent

Then:

```python
agent = create_agent(
    model,
    tools=tools,
)
```

Notice something important.

The agent still receives:

```python
tools=tools
```

Just like before.

The difference is:

### Before

```text
tools = locally defined Python functions
```

### After

```text
tools = discovered MCP tools
```

The agent doesn't need to care where the tools came from.

---

# 31. This Is a Very Important Abstraction

From the LLM/agent's perspective:

```text
Tool
├── name
├── description
└── arguments
```

It doesn't necessarily care whether that tool is:

```text
Local Python function
```

or:

```text
MCP server tool
```

The MCP adapter makes the external tools usable by the agent.

---

# 32. `async` and `await`

The new MCP version uses:

```python
async def main():
```

and:

```python
tools = await client.get_tools()
```

Why?

Because MCP communication involves I/O.

For example:

```text
Start subprocess
      ↓
Communicate
      ↓
Wait for server
      ↓
Receive response
```

or with remote MCP:

```text
Send network request
      ↓
Wait
      ↓
Receive response
```

These operations can take time.

Therefore asynchronous programming is commonly used.

---

# 33. Why `await`?

When you write:

```python
tools = await client.get_tools()
```

it means approximately:

> Start/get the tools and wait for the asynchronous operation to finish before continuing.

Once the result arrives:

```text
tools
```

contains the discovered tools.

---

# 34. Running the Agent

The code then does:

```python
result = await agent.ainvoke({
    "messages": [("user", question)]
})
```

This is the asynchronous version of invoking the agent.

Conceptually:

```text
User Question
     ↓
Agent
     ↓
LLM
     ↓
Tool decision
     ↓
MCP Client
     ↓
MCP Server
     ↓
Tool
     ↓
Result
     ↓
LLM
     ↓
Final answer
```

---

# 35. Why `parallel_tool_calls=False`?

The example uses:

```python
model = ChatOpenAI(
    model="gpt-5.5",
    parallel_tool_calls=False
)
```

The important concept is **sequential tool execution**.

Consider:

```text
15 × 8 ÷ 3
```

The correct dependency is:

```text
Step 1:
15 × 8 = 120

Step 2:
120 ÷ 3 = 40
```

The second operation depends on the first result.

So:

```text
multiply(15, 8)
       ↓
120
       ↓
divide(120, 3)
       ↓
40
```

If a model tries to issue independent tool calls in parallel, it cannot use the result of the first call as the input to the second call at the same moment.

Therefore, for this teaching example, sequential tool calls are enforced.

---

# 36. Important: Parallel vs Sequential

### Sequential

```text
multiply
   ↓
result = 120
   ↓
divide(120, 3)
   ↓
40
```

### Parallel

```text
multiply(15,8) ─────→ ?
divide(15,3)   ─────→ ?
```

The second call does not have the result of the first call.

For dependent operations, sequential execution is appropriate.

---

# 37. Before MCP — Complete Flow

```text
USER
 ↓
AGENT
 ↓
LLM
 ↓
"I need multiply"
 ↓
Agent's local tool registry
 ↓
multiply()
 ↓
120
 ↓
LLM
 ↓
Final answer
```

The Python application directly owns and executes:

```python
multiply()
```

---

# 38. After MCP — Complete Flow

```text
USER
 ↓
AGENT
 ↓
LLM
 ↓
"I need multiply"
 ↓
MCP Client
 ↓
MCP Server
 ↓
multiply()
 ↓
120
 ↓
MCP Client
 ↓
Agent
 ↓
LLM
 ↓
Final answer
```

The biggest architectural difference:

```text
BEFORE:
Agent → local function

AFTER:
Agent → MCP Client → MCP Server → function
```

---

# 39. MCP Does NOT Replace the LLM

This is one of the most important points from the lesson.

MCP does **not** replace:

```text
LLM
```

The LLM still:

* Understands the user
* Reasons
* Chooses tools
* Provides arguments
* Interprets results
* Produces the final answer

So:

```text
LLM
=
same reasoning component
```

---

# 40. MCP Does NOT Replace the Agent Loop

The agent loop still exists:

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

MCP simply changes the **Act → Tool execution** portion.

---

# 41. The Exact Architectural Difference

### Before

```text
LLM
 ↓
Agent Loop
 ↓
Local Python Tool
 ↓
Result
```

### After

```text
LLM
 ↓
Agent Loop
 ↓
MCP Client
 ↓
MCP Server
 ↓
Tool
 ↓
Result
```

Therefore:

> **MCP inserts a standardized tool-execution layer.**

---

# 42. Responsibility Shift

This is another major insight from the lesson.

### Before MCP

Your agent application handles many responsibilities:

```text
Agent Application
│
├── Tool definitions
├── Tool schemas
├── Tool registry
├── Tool-name → Python-function mapping
├── Tool execution
├── Error handling
└── Agent orchestration
```

### After MCP

More tool-related responsibility moves toward the MCP server/framework:

```text
Agent Application
│
├── Agent reasoning
├── Agent loop
├── MCP client
└── Orchestration

MCP Server
│
├── Tool definitions
├── Tool schemas
├── Tool discovery
├── Tool execution
└── Tool-specific logic
```

The exact responsibilities depend on the framework, but architecturally the tool capability becomes separated from the agent application.

---

# 43. Agent Becomes an Orchestrator

This gives us an important phrase:

> **The agent becomes a tool orchestrator rather than a custom integration owner.**

The agent focuses on:

```text
What should I do?
Which tool should I use?
What arguments should I provide?
What should I do with the result?
```

The MCP server focuses on:

```text
What tools do I provide?
How do those tools work?
How do I execute them?
```

---

# 44. The LLM Doesn't Care Where the Tool Lives

Suppose the LLM sees:

```text
multiply
```

It decides:

```text
multiply(15, 8)
```

From the LLM's perspective, the result might have come from:

```text
Local Python
```

or:

```text
MCP Server
```

The LLM's basic reasoning process doesn't need to change.

It still sees:

```text
Tool name
Tool arguments
Tool result
```

This is a major benefit of abstraction.

---

# 45. Multi-Server MCP

The example uses:

```python
MultiServerMCPClient(...)
```

This allows configuration like:

```python
client = MultiServerMCPClient(
    {
        "math": {...},
        "github": {...},
        "database": {...},
    }
)
```

Conceptually:

```text
                  Agent
                    │
             Multi-server client
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
      Math       GitHub      Database
     Server       Server       Server
```

The underlying architecture still maintains individual client-server connections.

The multi-server abstraction manages them together.

---

# 46. Example Configuration

Conceptually:

```python
client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": [math_server_path],
            "transport": "stdio",
        },

        "github": {
            ...
        },

        "weather": {
            ...
        }
    }
)
```

Then:

```python
tools = await client.get_tools()
```

can discover tools from the configured servers and expose them together to the agent.

---

# 47. Build Once, Use Everywhere

This is one of the biggest practical advantages of MCP.

Suppose you create:

```text
Math MCP Server
```

with:

```text
add
multiply
divide
square_root
```

Now multiple AI applications can potentially use it:

```text
                  Math MCP Server
                 /       |       \
                /        |        \
             Agent     Claude    Cursor
               \        |        /
                \       |       /
                 Shared tools
```

Instead of rewriting the tools for every application.

---

# 48. Update Once

Suppose:

```text
divide()
```

has a bug.

Without MCP:

```text
Agent A → update
Agent B → update
Agent C → update
```

With a shared MCP server:

```text
                 MCP Server
                     │
                  divide()
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
        Agent A    Agent B    Agent C
```

Fix the server implementation.

The connected applications use the updated server implementation.

This centralization is useful when the server is actually shared and centrally deployed.

---

# 49. Mix and Match MCP Servers

You can combine different capabilities.

For example:

```text
Math Server
GitHub Server
Slack Server
Database Server
File Server
```

Your AI application can potentially use them together.

Conceptually:

```text
                   AI Agent
                      │
              MCP Client Layer
                      │
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
     GitHub          Slack        Database
     Server          Server        Server
```

This is where MCP becomes much more useful than the simple math example.

---

# 50. When MCP Is Overkill

This is an important practical point.

For:

```text
15 × 8
```

you probably don't need MCP.

A local Python function is simpler:

```python
def multiply(a, b):
    return a * b
```

Adding:

```text
Agent
 ↓
MCP Client
 ↓
MCP Server
 ↓
multiply()
```

adds architectural complexity.

Therefore:

> **MCP is not automatically better for every tool.**

---

# 51. When MCP Makes More Sense

MCP becomes more useful when tools are:

### External

For example:

```text
GitHub
Slack
Jira
Cloud APIs
Remote databases
```

### Reusable

When many AI applications need the same capability.

### Remote

When the capability exists on another machine/service.

### Shared

When multiple agents or applications need access to the same tool infrastructure.

### Independently maintained

When the tool implementation should be updated separately from the AI application.

---

# 52. Practical Examples

### GitHub

```text
Agent
 ↓
MCP Client
 ↓
GitHub MCP Server
 ↓
GitHub API
```

Possible capabilities:

```text
Search repositories
Read issues
Read pull requests
Create issues
```

---

### Database

```text
Agent
 ↓
MCP Client
 ↓
Database MCP Server
 ↓
Database
```

The agent doesn't need to embed all database integration logic directly into its own code.

---

### Slack

```text
Agent
 ↓
MCP Client
 ↓
Slack MCP Server
 ↓
Slack
```

---

### Remote machine

```text
Agent
 ↓
MCP Client
 ↓
Remote MCP Server
 ↓
Remote system
```

---

# 53. Full Before vs After Table

| Concept        | Before MCP            | After MCP              |
| -------------- | --------------------- | ---------------------- |
| LLM            | Same                  | Same                   |
| Agent loop     | Same                  | Same                   |
| Tool location  | Agent application     | MCP server             |
| Tool discovery | Often hardcoded       | Dynamic via MCP        |
| Tool execution | Local application     | MCP server             |
| Tool sharing   | Difficult             | Standardized/reusable  |
| Tool schema    | Application/framework | MCP server/framework   |
| Communication  | Direct function call  | MCP client/server      |
| Protocol       | Application-specific  | MCP/JSON-RPC           |
| Local tool     | Easy                  | Possible through stdio |
| Remote tool    | Custom integration    | MCP transport          |
| Architecture   | Tightly coupled       | Decoupled              |

---

# 54. The Code Difference

## Before

```python
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

tools = [multiply]
```

The tool is inside the agent application.

---

## After

### MCP Server

```python
@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b
```

### Agent

```python
client = MultiServerMCPClient({
    "math": {
        "command": "python",
        "args": [server_path],
        "transport": "stdio",
    }
})

tools = await client.get_tools()

agent = create_agent(
    model,
    tools=tools
)
```

Notice:

```text
Agent code:
No multiply() implementation
No divide() implementation
No add() implementation
```

It discovers them.

---

# 55. What `get_tools()` Really Means

When you write:

```python
tools = await client.get_tools()
```

mentally translate it to:

> **"Connect to the configured MCP servers, discover their available tools, and give me those tools in a form my agent can use."**

Underneath, conceptually:

```text
get_tools()
    ↓
Connect
    ↓
Initialize
    ↓
Discover
    ↓
tools/list
    ↓
Receive tool schemas
    ↓
Convert/adapt tools
    ↓
Return tools
```

---

# 56. Complete Execution Example

User asks:

```text
What is 15 multiplied by 8, then divided by 3?
```

### Step 1 — User

```text
15 × 8 ÷ 3
```

### Step 2 — LLM reasons

```text
I need multiply first.
```

### Step 3 — Agent sends request through MCP

```text
MCP Client
    ↓
tools/call
    ↓
multiply(15, 8)
```

### Step 4 — MCP server executes

```text
15 × 8 = 120
```

### Step 5 — Result returns

```text
120
```

### Step 6 — LLM reasons again

```text
Now I need 120 ÷ 3.
```

### Step 7 — Second MCP call

```text
MCP Client
    ↓
tools/call
    ↓
divide(120, 3)
```

### Step 8 — Server executes

```text
40
```

### Step 9 — Final answer

```text
40
```

---

# 57. Architecture Trace

```text
USER
 │
 │ "15 × 8 ÷ 3"
 ↓
HOST
 │
 ↓
LLM
 │
 │ Tool call: multiply(15,8)
 ↓
MCP CLIENT
 │
 │ JSON-RPC
 ↓
MCP SERVER
 │
 │ multiply()
 ↓
120
 │
 ↓
MCP CLIENT
 │
 ↓
LLM
 │
 │ Tool call: divide(120,3)
 ↓
MCP CLIENT
 │
 ↓
MCP SERVER
 │
 │ divide()
 ↓
40
 │
 ↓
LLM
 │
 ↓
FINAL ANSWER: 40
```

---

# 58. Why This Architecture Is Powerful

The main benefit is **separation of concerns**.

### Agent

Responsible for:

```text
Reasoning
Planning
Orchestration
Choosing tools
Interpreting results
```

### MCP server

Responsible for:

```text
Tool implementation
Tool schema
Tool execution
External-system integration
```

This gives:

```text
Agent
  ↓
"What should I do?"

MCP Server
  ↓
"How do I perform that capability?"
```

---

# 59. The Most Important Mental Model

Remember this transformation:

```text
BEFORE

LLM
 ↓
Agent
 ↓
Local Python Function
 ↓
Result
```

becomes:

```text
AFTER

LLM
 ↓
Agent
 ↓
MCP Client
 ↓
MCP Server
 ↓
Tool
 ↓
Result
```

MCP adds a **standardized tool execution layer**.

It does not replace:

```text
LLM
```

and it does not replace:

```text
Agent Loop
```

---

# 60. Final Architecture

```text
                         USER
                           │
                           ↓
                    ┌──────────────┐
                    │     HOST     │
                    │              │
                    │     LLM      │
                    │      ↓       │
                    │  Agent Loop  │
                    └──────┬───────┘
                           │
                     MCP Client
                           │
                    JSON-RPC / Transport
                           │
                           ↓
                    ┌──────────────┐
                    │ MCP SERVER   │
                    │              │
                    │ Tool Schema  │
                    │ Tool Logic   │
                    │ Tool Execution│
                    └──────┬───────┘
                           │
                           ↓
                    External System
```

---

# 61. Final Revision Notes

### Before MCP

```text
Tools live inside agent.
Tools are hardcoded.
Agent directly executes Python functions.
Sharing requires custom integration.
```

### After MCP

```text
Tools live on MCP server.
Agent discovers tools dynamically.
MCP client communicates with server.
Tools can be reused by multiple AI applications.
```

### FastMCP

```text
FastMCP
   ↓
Makes building MCP servers easier
   ↓
@mcp.tool
   ↓
Python function becomes MCP tool
```

### Client

```text
MultiServerMCPClient
   ↓
Connects to MCP server(s)
   ↓
Discovers tools
   ↓
Provides tools to LangChain agent
```

### Local transport

```text
stdio
   ↓
same machine
   ↓
subprocess
   ↓
stdin/stdout
```

### Main architectural change

```text
BEFORE

Agent → Local Tool


AFTER

Agent → MCP Client → MCP Server → Tool
```

### Core takeaway

> **MCP separates tool capability from the agent application. The agent remains responsible for reasoning and orchestration, while the MCP server owns and exposes the tools through a standardized interface.**
