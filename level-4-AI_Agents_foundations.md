# Model Context Protocol (MCP) — Fundamentals

## 1. What is MCP?

**MCP** stands for **Model Context Protocol**.

It is an **open standard** that allows AI applications to connect to:

* External tools
* Data sources
* APIs
* Databases
* File systems
* Other external systems

in a **consistent and standardized way**.

### Simple definition

> **MCP is a standardized protocol that allows AI applications to communicate with external tools and data sources.**

The important word is:

**Open standard**

MCP is not tied to a single AI vendor.

---

# 2. Why Does MCP Exist?

Before MCP, AI applications generally needed to create **custom integrations** for every external tool.

Imagine:

```text
AI Application 1 ───── Tool 1
AI Application 1 ───── Tool 2
AI Application 1 ───── Tool 3
AI Application 1 ───── Tool 4

AI Application 2 ───── Tool 1
AI Application 2 ───── Tool 2
AI Application 2 ───── Tool 3
AI Application 2 ───── Tool 4

AI Application 3 ───── Tool 1
AI Application 3 ───── Tool 2
AI Application 3 ───── Tool 3
AI Application 3 ───── Tool 4
```

There are:

* 3 AI applications
* 4 tools

Therefore:

```text
3 × 4 = 12 integrations
```

This becomes difficult to build and maintain.

---

# 3. The N × M Integration Problem

Suppose:

```text
N = number of AI applications
M = number of tools
```

Without MCP:

```text
Number of integrations = N × M
```

For example:

```text
N = 3
M = 4

N × M
= 3 × 4
= 12
```

Every AI application needs a custom connector for every tool.

As the number of applications and tools increases, the number of integrations grows quickly.

This is sometimes called the:

> **N × M integration problem**

---

# 4. How MCP Solves the Problem

MCP introduces a **standard interface** between AI applications and external capabilities.

Instead of:

```text
Every AI app ↔ Every tool
```

we have:

```text
AI App → MCP Client → MCP Server ← Tool/System
```

Each AI application needs an MCP client.

Each tool/system exposes an MCP server.

For the same example:

```text
3 AI applications
4 tools
```

We need:

```text
3 MCP clients
+
4 MCP servers

= 7 components/connections to standardize
```

Instead of:

```text
3 × 4 = 12
```

we conceptually have:

```text
3 + 4 = 7
```

So the architecture changes from:

```text
N × M
```

to:

```text
N + M
```

### Important

This is a **conceptual integration-complexity comparison**, not a claim that MCP literally reduces every production system to exactly N+M pieces.

The key idea is:

> **Each side implements the standard once instead of building a custom integration for every other side.**

---

# 5. USB-C Analogy

MCP is often described as:

> **"USB-C for AI"**

Think about USB-C.

Without a common connector standard, every device could require a different cable.

With USB-C:

```text
Device
   ↓
Standard USB-C interface
   ↓
Compatible device/accessory
```

Similarly, MCP provides a standard communication interface:

```text
AI Application
      ↓
  MCP Client
      ↓
   MCP Protocol
      ↓
  MCP Server
      ↓
Tool / Data / System
```

If both sides understand MCP, they can communicate regardless of who built them.

### Mental model

```text
USB-C
    ↓
Standard connectivity for devices

MCP
    ↓
Standard connectivity for AI applications
```

---

# 6. JSON-RPC 2.0

MCP is built on **JSON-RPC 2.0**.

### What is JSON-RPC?

JSON-RPC is a JSON-based protocol for making **remote procedure calls**.

A simple mental model:

```text
Client
   ↓
Request
   ↓
Server
   ↓
Execute operation
   ↓
Response
```

The communication is structured using JSON.

For example, conceptually:

```json
{
  "method": "multiply",
  "params": {
    "a": 15,
    "b": 8
  }
}
```

The server processes the request and returns a response.

The course will cover the details of JSON-RPC in the next lesson.

For now, remember:

> **MCP uses JSON-RPC 2.0 as the communication protocol between MCP clients and servers.**

---

# 7. MCP Architecture

MCP has three key participants:

```text
1. Host
2. Client
3. Server
```

The architecture looks like:

```text
                 HOST
        ┌─────────────────────┐
        │    AI Application   │
        │                     │
        │        LLM          │
        │         ↓           │
        │   Reasoning/Agent   │
        │                     │
        │   MCP Client 1 ────────── MCP Server 1
        │   MCP Client 2 ────────── MCP Server 2
        │   MCP Client 3 ────────── MCP Server 3
        │                     │
        └─────────────────────┘
```

Let's understand each part.

---

# 8. Host

The **host** is the AI application that the user interacts with.

Examples mentioned in the lesson include:

* Claude Desktop
* Cursor
* Visual Studio Code
* Other MCP-enabled AI applications

### Simple definition

> **Host = the AI application containing the agent/LLM experience that the user interacts with.**

For example:

```text
User
  ↓
Cursor
  ↓
Host
```

The host manages the overall AI application.

---

# 9. LLM Inside the Host

The host contains an LLM/AI model that performs reasoning.

Conceptually:

```text
Host
│
├── LLM
│     ↓
│   Reasoning
│
└── MCP Clients
```

The LLM may use a **ReAct-style reasoning process**:

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
...
```

The LLM decides what should happen, while the MCP infrastructure provides access to external capabilities.

---

# 10. MCP Client

The host creates one or more **MCP clients**.

For example:

```text
Host
│
├── MCP Client 1
├── MCP Client 2
└── MCP Client 3
```

The important rule from this lesson is:

> **Each MCP client maintains a dedicated one-to-one connection with one MCP server.**

So:

```text
Client 1 ───── Server 1
Client 2 ───── Server 2
Client 3 ───── Server 3
```

Not:

```text
Client 1 ───── Server 1
           └── Server 2
           └── Server 3
```

for the basic MCP architecture being taught here.

---

# 11. MCP Server

An **MCP server** is a program that exposes capabilities to an MCP client.

These capabilities can include:

* Tools
* Data/resources
* Prompt templates

For example:

```text
Math MCP Server
│
├── multiply
├── divide
└── add
```

Another MCP server might provide GitHub functionality:

```text
GitHub MCP Server
│
├── Search repositories
├── Read issues
├── Create issue
└── Get pull requests
```

Another might connect to a database:

```text
Database MCP Server
│
├── Query data
├── Read schema
└── Retrieve records
```

---

# 12. MCP Servers Can Connect to External Systems

An MCP server can act as a bridge to an external system.

For example:

```text
AI Application
      ↓
   MCP Client
      ↓
   MCP Server
      ↓
   GitHub
```

or:

```text
AI Application
      ↓
   MCP Client
      ↓
   MCP Server
      ↓
   Database
```

or:

```text
AI Application
      ↓
   MCP Client
      ↓
   MCP Server
      ↓
   Local File System
```

Other possible systems include:

* Slack
* APIs
* Cloud services
* Enterprise systems
* Databases
* Local files

---

# 13. Client and Server Are Decoupled

This is one of the **most important concepts in this lesson**.

The MCP client and MCP server are **decoupled**.

That means the server does not need to know which particular AI application is using it.

As long as the client follows the MCP protocol:

```text
Client A ─────┐
Client B ─────┼──→ MCP Server
Client C ─────┘
```

The server communicates using the standardized protocol.

### Mental model

```text
Client
  ↓
Standard MCP protocol
  ↓
Server
```

The client and server don't need to be created by the same company.

---

# 14. Why Decoupling Matters

Suppose:

```text
Company A
    ↓
creates MCP Server
    ↓
provides GitHub tools
```

Different AI applications can potentially connect to that server:

```text
Claude ───────┐
Cursor ───────┤
VS Code ──────┼──→ GitHub MCP Server
Other App ────┘
```

The MCP server doesn't need a completely different custom integration for every AI application.

That's the value of standardization.

---

# 15. What Can MCP Servers Provide?

According to the lesson, MCP servers can expose three important categories:

```text
MCP Server
│
├── Tools
├── Data / Resources
└── Prompts
```

### Tools

Actions that the AI can request.

Examples:

```text
search_github()
query_database()
send_message()
read_file()
```

### Data / Resources

Information that the AI can access.

Examples:

```text
database information
documents
files
application data
```

### Prompts

Reusable prompt templates that can be provided through MCP.

We will study these primitives in more detail later.

---

# 16. Host, Client, Server — Complete Picture

Put everything together:

```text
                         HOST
        ┌────────────────────────────────┐
        │                                │
        │              LLM               │
        │               ↓                │
        │          Agent Reasoning       │
        │                                │
        │     ┌────────────────────┐     │
        │     │    MCP Client 1    │──────────→ MCP Server 1
        │     └────────────────────┘     │
        │                                │
        │     ┌────────────────────┐     │
        │     │    MCP Client 2    │──────────→ MCP Server 2
        │     └────────────────────┘     │
        │                                │
        │     ┌────────────────────┐     │
        │     │    MCP Client 3    │──────────→ MCP Server 3
        │     └────────────────────┘     │
        │                                │
        └────────────────────────────────┘
```

Each client has a dedicated connection to its server.

---

# 17. Example — Math Agent

Let's connect this to the math agent from the previous modules.

Suppose the user asks:

```text
What is 15 × 8 ÷ 3?
```

The agent needs:

```text
multiply(15, 8)
divide(120, 3)
```

### Without MCP

The tools might directly live inside the agent application:

```text
Agent
│
├── LLM
├── multiply()
└── divide()
```

The agent can execute the Python functions directly through its tool runtime.

---

# 18. Math Agent With MCP

With MCP:

```text
User
 ↓
Host
 ↓
LLM
 ↓
MCP Client
 ↓
Math MCP Server
 ├── multiply
 └── divide
```

The architecture is now separated.

The math functions are provided by the MCP server.

The agent application communicates with that server through the MCP client.

---

# 19. Multiple MCP Servers

Imagine the AI application needs:

```text
GitHub
Slack
Database
File system
```

The host can have multiple MCP clients:

```text
                    HOST
                      │
                     LLM
                      │
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
   Client 1       Client 2       Client 3
       ↓              ↓              ↓
 GitHub Server   Slack Server   Database Server
```

Each basic client-server relationship is one-to-one.

---

# 20. Context Aggregation

Now comes an important architecture question.

If the host has multiple clients:

```text
Client 1 → Server 1
Client 2 → Server 2
Client 3 → Server 3
```

how does the AI application manage all the capabilities and information coming from those servers?

The **host is responsible for managing context aggregation across clients**.

Conceptually:

```text
Server 1 ──→ Client 1 ──┐
                        │
Server 2 ──→ Client 2 ──┼──→ Host → LLM
                        │
Server 3 ──→ Client 3 ──┘
```

The host brings together the relevant context/capabilities for the AI application.

---

# 21. Specialized Multi-Server Clients

The basic MCP model teaches:

```text
One Client ↔ One Server
```

However, specialized clients can make working with multiple servers easier.

For example, the course mentions a **multi-server MCP client from LangChain** that can load:

* Tools
* Prompts
* Resources

from multiple MCP servers.

Conceptually:

```text
Server 1 ──┐
Server 2 ──┼──→ Multi-server client
Server 3 ──┘          ↓
                  Combined capabilities
```

This does not change the basic concept that an individual MCP client connection is associated with a particular server.

---

# 22. MCP Transport Mechanisms

MCP communication uses JSON-RPC 2.0 and supports transport mechanisms.

The lesson introduces two:

### 1. Standard Input/Output — stdio

Used for **local MCP servers**.

Conceptually:

```text
Host
 ↓
MCP Client
 ↓
stdio
 ↓
Local MCP Server
```

This is useful when the MCP server runs locally on the same machine.

---

### 2. Streamable HTTP

Used for **remote MCP servers**.

Conceptually:

```text
Host
 ↓
MCP Client
 ↓
HTTP
 ↓
Remote MCP Server
```

The detailed behavior of these transports will be covered later.

---

# 23. Local vs Remote MCP Server

MCP servers can run:

### Locally

```text
Your computer
│
├── AI application
│
└── MCP server
```

### Remotely

```text
Your computer
│
└── AI application
       ↓
      Internet
       ↓
Remote MCP server
```

The MCP protocol provides the standardized communication layer.

---

# 24. Complete MCP Mental Model

Think of the components like this:

```text
┌─────────────────────────────────────┐
│               HOST                  │
│                                     │
│          LLM / AI Model             │
│                ↓                    │
│          Agent Reasoning            │
│                ↓                    │
│       ┌──────────────────┐          │
│       │   MCP Client     │          │
│       └────────┬─────────┘          │
└────────────────┼────────────────────┘
                 │
           JSON-RPC 2.0
                 │
                 ↓
        ┌──────────────────┐
        │   MCP Server     │
        ├──────────────────┤
        │ Tools            │
        │ Resources        │
        │ Prompts          │
        └────────┬─────────┘
                 │
                 ↓
       External System
```

---

# 25. The Most Important Distinction

Do not confuse these three:

| Component  | Main responsibility                                |
| ---------- | -------------------------------------------------- |
| **Host**   | Runs/manages the AI application and LLM experience |
| **Client** | Connects the host to an MCP server                 |
| **Server** | Exposes tools, resources/data, and prompts         |

Simple analogy:

```text
Host   = Restaurant
Client = Waiter
Server = Kitchen
```

The waiter communicates with the kitchen using an agreed communication method.

The restaurant/user experience doesn't need to know how the kitchen internally implements every dish.

The analogy isn't exact, but it helps remember the roles.

---

# 26. MCP in One Diagram

```text
                     USER
                       │
                       ↓
              ┌────────────────┐
              │      HOST      │
              │                │
              │      LLM       │
              │       ↓        │
              │ Agent Reasoning│
              │       ↓        │
              │  MCP Clients   │
              └───────┬────────┘
                      │
                MCP / JSON-RPC
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
   MCP Server 1  MCP Server 2  MCP Server 3
        ↓             ↓             ↓
     GitHub         Slack       Database
```

---

# 27. Key Takeaways

### MCP

**Model Context Protocol**

An open standard for connecting AI applications with external capabilities.

### Why MCP?

Without MCP:

```text
N AI apps × M tools
        ↓
     N × M
custom integrations
```

With MCP:

```text
N AI apps + M tools
        ↓
standardized MCP connectivity
```

### Architecture

```text
Host
 ↓
MCP Client
 ↓
MCP Server
 ↓
External System
```

### Three participants

```text
Host
Client
Server
```

### Server capabilities

```text
Tools
Resources/Data
Prompts
```

### Communication

```text
JSON-RPC 2.0
```

### Transport introduced in this lesson

```text
Local  → stdio
Remote → Streamable HTTP
```

### Most important idea

> **MCP standardizes the connection between AI applications and external capabilities.**

---

# 28. One-Sentence Mental Model

If you remember only one thing from this lesson:

> **The Host runs the AI application, the Client connects it to an MCP Server, and the Server exposes tools, resources, and prompts through a standardized MCP interface.**

---

# 29. Connection to What We Learned Earlier

Previously:

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

With MCP:

```text
User
 ↓
Host
 ↓
Agent / LLM
 ↓
MCP Client
 ↓
MCP Server
 ↓
External Tool/System
 ↓
MCP Server
 ↓
MCP Client
 ↓
Agent / LLM
 ↓
Final Answer
```

So MCP does **not replace the LLM or the agent loop**.

Instead, it standardizes **how the agent/application connects to external capabilities**.

That distinction is extremely important.
