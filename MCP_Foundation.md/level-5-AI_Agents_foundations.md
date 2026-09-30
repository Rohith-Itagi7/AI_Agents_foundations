# MCP Core Components, Lifecycle, JSON-RPC & Transports

## 1. MCP Core Primitives

MCP servers expose three major types of primitives:

```text
MCP Server
│
├── Tools
├── Resources
└── Prompts
```

A simple way to remember them:

> **Tools = Do something**
> **Resources = Read something**
> **Prompts = Structure something**

---

# 2. Tools

**Tools are actions that the model can request the system to perform.**

You can think of a tool as a function.

Examples:

```text
multiply()
divide()
search_github()
query_database()
read_file()
send_message()
```

For example:

```text
multiply(15, 8)
```

actually performs an operation and produces a result:

```text
120
```

### Mental model

```text
Tool
 ↓
DO something
 ↓
Result
```

Tools are the **most commonly used MCP primitive**.

When people casually talk about "using MCP," they are very often talking primarily about **MCP tools**.

---

# 3. Resources

**Resources are data sources that the model can read.**

Unlike tools, resources are not primarily about performing an action with a side effect.

Examples could include:

```text
Files
Documents
Database information
Application data
Configuration
Other readable data
```

Mental model:

```text
Resource
   ↓
READ something
   ↓
Information
```

### Tools vs Resources

| Primitive    | Main purpose                  | Mental model        |
| ------------ | ----------------------------- | ------------------- |
| **Tool**     | Perform an action             | Do something        |
| **Resource** | Provide/read data             | Read something      |
| **Prompt**   | Provide a structured template | Structure something |

---

# 4. Prompts

**Prompts are reusable templates that structure interactions.**

Instead of typing a long prompt manually, an application can expose a predefined prompt.

For example, imagine an application provides:

```text
/review
```

The user selects `/review`.

Behind the scenes, the system could load a predefined prompt template such as:

```text
Review the following code.
Identify:
1. Bugs
2. Performance issues
3. Security issues
4. Suggested improvements
```

The user doesn't have to type the entire prompt.

### Mental model

```text
Prompt
  ↓
STRUCTURE something
  ↓
Predefined interaction
```

Prompts can therefore act somewhat like a **UI shortcut for a predefined interaction**.

---

# 5. Easy Way to Remember the Three Primitives

Remember:

```text
TOOLS
  ↓
DO

RESOURCES
  ↓
READ

PROMPTS
  ↓
STRUCTURE
```

Or:

> **Tools do. Resources read. Prompts structure.**

This is one of the easiest MCP mnemonics.

---

# 6. MCP Connection Lifecycle

MCP follows a client-server architecture.

The connection goes through four major phases:

```text
1. Initialize
       ↓
2. Discover
       ↓
3. Operate
       ↓
4. Shutdown
```

Let's understand each one.

---

# 7. Phase 1 — Initialize

The first phase is the **initialization handshake**.

The MCP client sends an initialization request to the server.

Conceptually:

```text
Client
   │
   │ initialize
   ↓
Server
```

The client tells the server things such as:

* Protocol version
* Client capabilities

The server responds with its:

* Protocol version
* Server capabilities

Then the client sends an initialization notification indicating that it is ready.

Conceptually:

```text
CLIENT                              SERVER

  │                                   │
  │──── initialize ──────────────────>│
  │    version + capabilities         │
  │                                   │
  │<─── initialize response ──────────│
  │    version + capabilities         │
  │                                   │
  │──── initialized notification ────>│
  │                                   │
  │          Ready                    │
```

This is basically the **handshake**.

### Why do this?

Both sides need to establish:

> "Who are you, which protocol version do you support, and what capabilities do you have?"

before normal communication begins.

---

# 8. Phase 2 — Discover

After initialization, the client needs to know:

> **What does this server provide?**

The client can discover:

```text
Tools
Resources
Prompts
```

For example:

```text
Client
   │
   │ What tools do you provide?
   ↓
Server
   │
   ├── multiply
   ├── divide
   ├── add
   └── sqrt
```

For tools, the server provides schemas describing things such as:

* Tool name
* Description
* Input parameters
* Parameter types

---

# 9. Dynamic Tool Discovery

This is one of the **most important MCP concepts**.

Previously, with a normal LangChain tool setup, you might explicitly write:

```python
tools = [
    multiply,
    divide,
    add
]
```

The application already knows the tools.

With MCP, the client can ask the server:

```text
tools/list
```

The server responds:

```text
I provide:

multiply
add
divide
sqrt
```

Therefore, the client can **discover tools dynamically**.

### Without dynamic discovery

```text
Your code
   ↓
Hard-coded tools
   ↓
multiply
divide
add
```

### With MCP

```text
Your client
   ↓
"What tools do you have?"
   ↓
MCP Server
   ↓
Tool definitions
   ↓
Client learns available tools
```

This reduces the need to hard-code tool definitions into the client application.

---

# 10. Phase 3 — Operate

This is where the actual work happens.

Suppose the user asks:

```text
What is 15 × 8 ÷ 3?
```

The flow becomes:

```text
User
 ↓
Host / Agent
 ↓
LLM
```

The LLM sees the available tools.

It decides:

```text
First:
multiply(15, 8)
```

The client sends the request to the MCP server:

```text
Client
   ↓
MCP Server
   ↓
multiply(15, 8)
```

The server executes it:

```text
15 × 8 = 120
```

The result returns:

```text
MCP Server
   ↓
Client
   ↓
LLM
```

The LLM now sees:

```text
multiply result = 120
```

and realizes it still needs:

```text
divide(120, 3)
```

Then:

```text
LLM
 ↓
Client
 ↓
MCP Server
 ↓
divide(120, 3)
 ↓
40
 ↓
Client
 ↓
LLM
```

Finally:

```text
LLM
 ↓
Final answer
```

---

# 11. Complete Operate Flow

```text
                 USER
                   │
                   ↓
                 HOST
                   │
                   ↓
                  LLM
                   │
             decides tool
                   │
                   ↓
              MCP Client
                   │
             tool request
                   │
                   ↓
              MCP Server
                   │
             execute tool
                   │
                   ↓
                Result
                   │
                   ↓
              MCP Client
                   │
                   ↓
                  LLM
                   │
          reason about result
                   │
             another tool?
             /          \
           YES           NO
            ↓             ↓
        MCP Client     Final answer
```

This is the MCP version of the **ReAct loop** you learned earlier.

---

# 12. Phase 4 — Shutdown

When the interaction is finished, the connection can be closed.

Conceptually:

```text
Client
   ↓
Close transport connection
   ↓
Server
```

The transport connection is shut down.

So the complete lifecycle is:

```text
INITIALIZE
     ↓
DISCOVER
     ↓
OPERATE
     ↓
SHUTDOWN
```

---

# 13. MCP Lifecycle — Easy Memory Trick

Remember:

> **Connect → Discover → Work → Disconnect**

Which corresponds to:

```text
Initialize → Discover → Operate → Shutdown
```

---

# 14. What is JSON-RPC 2.0?

MCP uses **JSON-RPC 2.0** for its messages.

JSON-RPC is a JSON-based protocol for making **remote procedure calls**.

In simple terms:

```text
Client
  ↓
Structured JSON message
  ↓
Server
  ↓
Execute operation
  ↓
Structured JSON response
```

It gives MCP a standardized message format.

---

# 15. Why JSON-RPC?

A key property important for MCP is that JSON-RPC supports communication that can work in a **bidirectional** manner.

This fits MCP's client-server communication model.

The course contrasts this with REST, which is commonly used for request/response APIs.

The important point for now is:

> **JSON-RPC provides the structured message format MCP uses to communicate between clients and servers.**

---

# 16. Basic JSON-RPC Message Structure

A JSON-RPC message contains information such as:

```text
JSON-RPC version
ID
Method
Parameters
```

A request conceptually looks like:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "multiply",
    "arguments": {
      "a": 15,
      "b": 8
    }
  }
}
```

Let's understand it.

### `jsonrpc`

```text
"jsonrpc": "2.0"
```

Specifies the JSON-RPC version.

### `id`

```text
"id": 1
```

Identifies the request.

The response can use the same ID so the client knows which request the result belongs to.

### `method`

```text
"method": "tools/call"
```

Specifies what operation is being requested.

### `params`

Contains the parameters required for that operation.

---

# 17. JSON-RPC Response

If the tool executes successfully, the server returns a result.

Conceptually:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "120"
      }
    ]
  }
}
```

The important concept is:

```text
Request
   ↓
result
```

If something goes wrong:

```text
Request
   ↓
error
```

So a response contains either:

```text
result
```

or:

```text
error
```

---

# 18. You Usually Don't Write JSON-RPC Manually

In real applications, you generally don't manually construct all these JSON-RPC messages.

Frameworks handle the protocol details.

Examples mentioned in the course include:

* FastMCP
* LangChain

So instead of manually writing:

```json
{
  "method": "tools/call",
  ...
}
```

you might simply call a framework API.

The framework handles:

```text
Your code
 ↓
Framework
 ↓
JSON-RPC message
 ↓
MCP server
```

### Why learn the structure then?

Because it is extremely useful when:

* Debugging
* Reading logs
* Understanding errors
* Understanding network traces
* Understanding what frameworks are doing underneath

---

# 19. Two Important MCP Tool Methods

For MCP tools, two methods are particularly important:

```text
tools/list
tools/call
```

Think:

```text
tools/list
    ↓
"What tools exist?"

tools/call
    ↓
"Execute this tool."
```

---

# 20. `tools/list`

`tools/list` is used to discover available tools.

The client asks:

```text
What tools do you have?
```

Conceptually:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

Notice:

```text
No specific tool is being executed.
```

The client is simply requesting the available tools.

---

# 21. `tools/list` Response

The server might respond with:

```text
multiply
add
divide
sqrt
```

along with their schemas.

Conceptually:

```json
{
  "tools": [
    {
      "name": "multiply",
      "description": "Multiply two numbers",
      "inputSchema": "..."
    },
    {
      "name": "divide",
      "description": "Divide two numbers",
      "inputSchema": "..."
    }
  ]
}
```

The exact schema structure can vary according to the protocol specification and implementation, but the important idea is:

> The server tells the client what tools exist and how to call them.

---

# 22. Why `tools/list` Is Important

It enables:

> **Dynamic tool discovery**

The client doesn't need to hard-code:

```python
multiply
divide
add
sqrt
```

Instead:

```text
Client
   ↓
tools/list
   ↓
Server
   ↓
Available tools
```

The server becomes the source of the tool definitions.

---

# 23. `tools/call`

`tools/call` is used when a specific tool needs to be executed.

Suppose the LLM decides:

```text
Call multiply
with:
a = 15
b = 8
```

The client sends:

```text
tools/call
```

Conceptually:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "multiply",
    "arguments": {
      "a": 15,
      "b": 8
    }
  }
}
```

The MCP server then executes:

```text
multiply(15, 8)
```

Result:

```text
120
```

---

# 24. `tools/list` vs `tools/call`

This distinction is extremely important.

| Method       | Purpose                  |
| ------------ | ------------------------ |
| `tools/list` | Discover available tools |
| `tools/call` | Execute a specific tool  |

Think:

```text
tools/list
     ↓
"What can I use?"

tools/call
     ↓
"Use this."
```

---

# 25. Complete Tool Flow

Let's put everything together.

### Step 1 — Discover

```text
Client
  ↓
tools/list
  ↓
Server
  ↓
multiply
divide
add
sqrt
```

### Step 2 — LLM decides

```text
User:
15 × 8 ÷ 3

LLM:
I need multiply first.
```

### Step 3 — Call

```text
Client
  ↓
tools/call
  ↓
multiply(15, 8)
```

### Step 4 — Execute

```text
Server
  ↓
multiply(15, 8)
  ↓
120
```

### Step 5 — Return result

```text
Server
  ↓
Client
  ↓
LLM
```

### Step 6 — Continue reasoning

```text
LLM:
120 ÷ 3 is required.
```

### Step 7 — Second call

```text
Client
  ↓
tools/call
  ↓
divide(120, 3)
  ↓
40
```

### Step 8 — Final answer

```text
LLM
 ↓
40
```

---

# 26. JSON-RPC vs Transport

This distinction is **very important**.

Do not think:

```text
JSON-RPC = transport
```

Instead:

```text
JSON-RPC
    ↓
Message format / protocol

Transport
    ↓
How those messages physically move
```

For example:

```text
             MCP
              │
      ┌───────┴────────┐
      │                │
 JSON-RPC          Transport
 Message              │
 Format          ┌─────┴─────┐
                 │           │
               stdio    Streamable HTTP
```

JSON-RPC defines the structure of the messages.

The transport determines how those messages travel between client and server.

---

# 27. MCP Transport Mechanisms

The lesson introduces two major transport mechanisms:

```text
1. stdio
2. Streamable HTTP
```

---

# 28. Transport 1 — stdio

**stdio** means:

```text
standard input
standard output
```

It is useful for **local MCP servers**.

The host application can start the MCP server as a **child process** on the same machine.

Conceptually:

```text
Same Computer
────────────────────────────

Host
 │
 └── MCP Client
       │
       │ stdin/stdout
       ↓
   MCP Server
```

Communication occurs through:

```text
stdin
stdout
```

similar to piping commands in a terminal.

---

# 29. Example of Local stdio Architecture

Imagine you have:

```text
C:\my-agent\
    agent.py
    math_server.py
```

Your host starts the MCP server locally.

Conceptually:

```text
agent.py
   │
   │ spawn process
   ↓
math_server.py
```

The two processes communicate through standard input/output.

No network server needs to be exposed.

---

# 30. Advantages of stdio

For local MCP servers:

* Simple
* Low overhead
* No network configuration
* Useful for local tools
* Server runs directly on user's machine

### Limitation

The MCP server must be installed and available locally.

The host needs to be able to start that process.

---

# 31. Transport 2 — Streamable HTTP

**Streamable HTTP** is designed for MCP servers that are accessed remotely.

Conceptually:

```text
User Machine
────────────────────

Host
 ↓
MCP Client
 ↓
HTTP
 ↓
Internet
 ↓
Remote MCP Server
────────────────────
```

The client communicates using HTTP.

The server can also stream responses back.

The course mentions **Server-Sent Events (SSE)** as part of the streaming mechanism.

---

# 32. Why Streamable HTTP?

It is useful for:

* Remote MCP servers
* Cloud deployments
* Multiple clients
* HTTP-based authentication
* Network-accessible services

Conceptually:

```text
Client 1 ─────┐
Client 2 ─────┼──→ Remote MCP Server
Client 3 ─────┘
```

---

# 33. Older SSE-only Transport

The course also mentions an older **SSE-only transport**.

The newer approach is:

```text
Streamable HTTP
```

which supersedes the older SSE-only approach in the MCP transport evolution described by the course.

The important thing to remember for this module is:

```text
Older:
SSE-only

Current course focus:
Streamable HTTP
```

---

# 34. Same Protocol, Different Transport

This is a very important architectural idea.

Whether MCP is local or remote:

```text
                MCP
                 │
             JSON-RPC 2.0
                 │
        ┌────────┴────────┐
        ↓                 ↓
      stdio       Streamable HTTP
        ↓                 ↓
     Local            Remote
```

The JSON-RPC message structure remains the same.

Only the transport changes.

---

# 35. Local vs Remote

| Feature          | stdio                     | Streamable HTTP      |
| ---------------- | ------------------------- | -------------------- |
| Typical use      | Local server              | Remote server        |
| Communication    | stdin/stdout              | HTTP                 |
| Network required | No                        | Usually yes          |
| Server location  | Same machine              | Remote/cloud         |
| Common use case  | Local files/tools         | Cloud services       |
| Authentication   | Local process permissions | HTTP/auth mechanisms |

---

# 36. The Full MCP Architecture

Now combine everything from this lesson and the previous lesson:

```text
                              USER
                                │
                                ↓
                         ┌─────────────┐
                         │    HOST     │
                         │             │
                         │     LLM     │
                         │      ↓      │
                         │ Agent Loop  │
                         └──────┬──────┘
                                │
                          MCP Client
                                │
                         JSON-RPC 2.0
                                │
                    ┌───────────┴───────────┐
                    │                       │
                  stdio             Streamable HTTP
                    │                       │
                    ↓                       ↓
             Local MCP Server       Remote MCP Server
                    │                       │
             ┌──────┼──────┐        ┌──────┼──────┐
             ↓      ↓      ↓        ↓      ↓      ↓
           Tools Resources Prompts  Tools Resources Prompts
```

---

# 37. MCP Request Flow

For a tool call, think:

```text
USER
 ↓
HOST
 ↓
LLM
 ↓
MCP CLIENT
 ↓
JSON-RPC REQUEST
 ↓
MCP SERVER
 ↓
TOOL
 ↓
RESULT
 ↓
MCP SERVER
 ↓
MCP CLIENT
 ↓
LLM
 ↓
FINAL ANSWER
```

---

# 38. How This Connects to Your Previous Agent Lessons

Previously you learned:

```text
Agent
 =
LLM + Tools + Loop
```

The tools were directly available to the agent runtime.

Now MCP introduces a standardized external tool layer:

```text
Agent
 =
LLM + Loop + MCP Client
                  ↓
             MCP Server
                  ↓
                Tools
```

So MCP does **not replace the agent**.

It changes **how the agent/application accesses external capabilities**.

---

# 39. Before MCP vs With MCP

### Before

```text
Agent
│
├── LLM
├── Agent Loop
├── multiply()
├── divide()
└── Tool execution
```

The application owns the tools.

### With MCP

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
        ├── multiply
        └── divide
```

The tools are exposed by the MCP server.

---

# 40. The Most Important Concepts From This Lesson

### Primitive layer

```text
Tools     → DO
Resources → READ
Prompts   → STRUCTURE
```

### Lifecycle layer

```text
Initialize
     ↓
Discover
     ↓
Operate
     ↓
Shutdown
```

### Tool discovery

```text
tools/list
     ↓
"What tools exist?"
```

### Tool execution

```text
tools/call
     ↓
"Execute this tool."
```

### Message layer

```text
JSON-RPC 2.0
```

### Transport layer

```text
Local  → stdio
Remote → Streamable HTTP
```

---

# 41. Final Mental Model

Imagine MCP as a restaurant ordering system:

```text
HOST
= Customer-facing application

MCP CLIENT
= Communication/order layer

MCP SERVER
= Service provider

TOOLS
= Actions the service can perform

RESOURCES
= Information the service can provide

PROMPTS
= Predefined interaction templates

JSON-RPC
= Standard format for the messages

TRANSPORT
= How the messages travel
```

The analogy is only for remembering the roles; the actual MCP architecture is more precise.

---

# 42. One-Minute Revision

If you need to revise this lesson quickly:

```text
MCP has 3 primitives:

Tools
→ perform actions

Resources
→ provide/read data

Prompts
→ predefined interaction templates
```

```text
MCP lifecycle:

Initialize
→ handshake

Discover
→ find tools/resources/prompts

Operate
→ actually use them

Shutdown
→ close connection
```

```text
Important tool methods:

tools/list
→ discover tools

tools/call
→ execute a tool
```

```text
Message format:

JSON-RPC 2.0
```

```text
Transport:

stdio
→ local MCP server

Streamable HTTP
→ remote MCP server
```

### The core idea

> **JSON-RPC defines what the MCP messages look like; transport defines how those messages travel; MCP primitives define what capabilities the server exposes.**
