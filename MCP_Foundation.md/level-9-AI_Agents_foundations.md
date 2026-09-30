# MCP + LangChain — How They Work Together

> **Goal:** Understand where LangChain fits when using MCP, how the MCP Client connects to an MCP Server, and how an MCP Server can connect an AI agent to APIs such as the OCI Usage API.

---

# 1. The Three Things That Must Be Separated

When learning MCP with an OCI example, three different things can easily get mixed together:

1. **OCI Usage API**
2. **MCP Server**
3. **How the Python program starts the MCP Server**

They are different layers.

```text
OCI Usage API
      ↓
Provides OCI usage/cost data

MCP Server
      ↓
Exposes OCI functionality through MCP

Python Program
      ↓
Starts and communicates with the MCP Server
```

---

# 2. What Is an API?

An **API** is a way for one program to ask another system for something.

Imagine Oracle has a system containing cloud-cost information:

```text
┌─────────────────────────┐
│                         │
│  Usage / Cost Database  │
│                         │
└─────────────────────────┘
```

Your program wants to ask:

> "How much did I spend?"

Oracle provides an API for that.

```text
Your Program
      │
      │ API Request
      ↓
Oracle's System
      │
      │ API Response
      ↓
Your Program
```

### Simple definition

> **API = an interface that allows one software system to communicate with another system.**

---

# 3. What Is the OCI Usage API?

**OCI = Oracle Cloud Infrastructure**

OCI contains information about resources such as:

```text
VMs
Databases
Storage
Networking
...
```

It also provides information about usage and costs.

Oracle provides an API that allows software to retrieve that information.

This is the **OCI Usage API**.

### Mental model

```text
OCI Usage API
      ↓
Programmatic door
      ↓
OCI usage / cost information
```

### Remember

> **OCI Usage API = a programmatic interface for accessing OCI usage/cost information.**

---

# 4. What Is a REST API?

A **REST API** commonly communicates using HTTP/HTTPS.

Conceptually:

```text
Your Program
      │
      │ HTTPS Request
      ↓
OCI Usage REST API
      │
      ↓
Usage Data
```

So:

```text
OCI Usage API
      ≈
OCI Usage REST API
```

The important distinction is:

> **API tells us what interface is provided.**

> **REST tells us the communication style used by the API.**

---

# 5. Now Introduce the MCP Server

Suppose Oracle already has:

```text
OCI
 │
 ↓
OCI Usage REST API
 │
 ↓
Cost Data
```

Now Oracle wants AI applications to access this functionality through MCP.

Oracle can provide an **OCI Usage MCP Server**.

```text
OCI Usage MCP Server
          │
          ↓
OCI Usage REST API
```

The MCP Server acts as an **adapter/bridge** between the MCP world and the OCI API.

---

# 6. Why Do We Need the MCP Server?

An AI agent understands the MCP interface:

```text
tools/list
tools/call
```

But the OCI API has its own API format.

The MCP Server connects these two worlds:

```text
AI / MCP World
      │
      │ MCP
      ↓
OCI Usage MCP Server
      │
      │ OCI REST API
      ↓
Oracle OCI
```

### Mental model

> **MCP Server = translator/adapter between an AI application's MCP communication and an underlying service/API.**

---

# 7. The Two Connections

This is one of the most important concepts.

There are **two completely different connections**:

```text
Your Python Program
        │
        │ stdio
        ↕
   MCP Server
        │
        │ HTTPS
        ↓
OCI Usage REST API
```

### Connection A — Python ↔ MCP Server

```text
Python Program
      ↕
   MCP Server
```

In this example, communication uses:

```text
stdin
stdout
```

or:

```text
stdio
```

### Connection B — MCP Server ↔ OCI

```text
MCP Server
      ↓
OCI Usage REST API
```

This communication uses:

```text
HTTPS
```

### Key idea

```text
Python Program
      │
      │ stdio
      ↓
MCP Server
      │
      │ HTTPS
      ↓
OCI API
```

**stdio and HTTPS are two different connections.**

---

# 8. What Does "Spawn the MCP Server" Mean?

Suppose you have:

```text
oci_usage_mcp_agent.py
```

Your Python program can tell the operating system:

> "Start this other program."

The operating system starts:

```text
oracle.oci-usage-mcp-server
```

as a separate process.

This is called **spawning a process**.

```text
Python Program
      │
      │ Start
      ↓
MCP Server Process
```

---

# 9. What Is a Subprocess?

A **subprocess** is simply another process started by a program.

For example:

```text
Main Process
     │
     ├── Subprocess 1
     ├── Subprocess 2
     └── Subprocess 3
```

In the MCP example:

```text
Main Python Process
        │
        ↓
MCP Server Subprocess
```

The Python program is the **parent process**.

The MCP Server is the **child/subprocess**.

---

# 10. Simple Analogy — Python Starting Notepad

Imagine your Python program starts Notepad:

```text
Python Program
      │
      │ "Start Notepad"
      ↓
Notepad Process
```

Now two programs are running:

```text
┌─────────────────┐
│ Python Program  │
└─────────────────┘

┌─────────────────┐
│ Notepad         │
└─────────────────┘
```

Python started Notepad.

We can say:

> **Python spawned the Notepad process.**

The MCP example works similarly.

---

# 11. The OCI MCP Example

Your program:

```text
oci_usage_mcp_agent.py
```

starts:

```text
oracle.oci-usage-mcp-server
```

Conceptually:

```text
┌─────────────────────────────┐
│ Your Python Program         │
│                             │
│ LangChain + MCP Client      │
└──────────────┬──────────────┘
               │
               │ starts
               ↓
┌─────────────────────────────┐
│ Oracle MCP Server           │
│                             │
│ oracle.oci-usage-mcp-server │
└─────────────────────────────┘
```

Both processes can be running on your computer.

---

# 12. How Do They Communicate?

They communicate through:

```text
stdin
stdout
```

Together this is called:

```text
stdio
```

So:

```text
Your Python Program
       ↕
     stdio
       ↕
Oracle MCP Server
```

This is what is meant by:

> **"The MCP server is spawned as a subprocess."**

---

# 13. Complete OCI Architecture

Put everything together:

```text
YOUR COMPUTER
────────────────────────────────────

┌──────────────────────────────┐
│ Your Python Program          │
│                              │
│ LangChain Agent              │
│ MCP Client                   │
└──────────────┬───────────────┘
               │
               │ stdio
               ↕
┌──────────────────────────────┐
│ Oracle MCP Server            │
│                              │
│ oracle.oci-usage-mcp-server  │
└──────────────┬───────────────┘
               │
               │ HTTPS
               ↓
────────────────────────────────────
             INTERNET
               ↓
┌──────────────────────────────┐
│ Oracle Cloud                 │
│                              │
│ OCI Usage REST API           │
└──────────────────────────────┘
```

### Plain English

> **Your Python program talks to the MCP Server locally through stdio.**

> **The MCP Server talks to Oracle Cloud through HTTPS.**

---

# 14. Follow One Real Request

Suppose the user asks:

> **"How much did I spend on storage in the last 30 days?"**

## Step 1 — User

```text
User
 ↓
"How much did I spend on storage?"
```

## Step 2 — LangChain Agent

The LLM decides:

> "I need OCI usage data."

It sees an MCP-provided tool such as:

```text
get_summarized_usage
```

## Step 3 — MCP Client

The MCP Client sends an MCP request to the locally running MCP Server.

```text
Python Program
      │
      │ MCP Request
      │ stdio
      ↓
Oracle MCP Server
```

## Step 4 — MCP Server

The Oracle MCP Server receives the request.

Conceptually:

> "I need to ask OCI for this information."

## Step 5 — MCP Server Calls OCI

The MCP Server makes the HTTPS request:

```text
Oracle MCP Server
      │
      │ HTTPS
      ↓
OCI Usage REST API
```

## Step 6 — OCI Responds

```text
OCI Usage REST API
      │
      ↓
Usage / Cost Data
```

## Step 7 — Result Returns

```text
OCI
 ↓
MCP Server
 ↓
stdio
 ↓
MCP Client
 ↓
LangChain Agent
```

## Step 8 — LLM Generates the Answer

```text
Agent
 ↓
LLM
 ↓
"Your storage cost was $X."
```

---

# 15. Important: Your Python Program Does Not Directly Call OCI

In this architecture:

```text
❌ NOT:

Python Program
      ↓
OCI Usage REST API
```

Instead:

```text
✅:

Python Program
      ↓
MCP Client
      ↓ stdio
Oracle MCP Server
      ↓ HTTPS
OCI Usage REST API
```

The MCP Server handles the OCI-specific API communication.

---

# 16. Why Doesn't the Python Program Use HTTPS Directly?

Because one purpose of using the MCP Server is to avoid implementing all the OCI-specific integration inside the agent application.

Your application mainly needs to understand:

```text
MCP
```

The MCP Server handles the OCI-specific integration.

Conceptually:

```text
Your Agent
     ↓
MCP
     ↓
Oracle MCP Server
     ↓
OCI API
```

Oracle has already built the integration into the MCP Server.

---

# 17. MCP vs API

This distinction is extremely important.

## API

An API is an interface provided by a service.

Example:

```text
OCI Usage REST API
```

It provides access to OCI usage information.

### API answers:

> **"How can software communicate with this service?"**

---

## MCP

MCP is a **standard protocol for AI applications to interact with tools and context**.

Example:

```text
MCP Client
     ↓
MCP Server
     ↓
Tool
```

### MCP answers:

> **"How can AI applications discover and use tools through a standardized interface?"**

---

# 18. MCP Server Can Wrap an API

This is the key relationship:

```text
                MCP
                 ↓
       ┌──────────────────┐
       │   MCP Server     │
       │                  │
       │ get_summarized_  │
       │ usage()          │
       └────────┬─────────┘
                │
                ↓
          OCI REST API
                │
                ↓
           OCI Data
```

The MCP Server exposes something like:

```text
get_summarized_usage
```

while internally communicating with:

```text
OCI Usage REST API
```

---

# 19. Real-World Analogy

Imagine a hotel.

You speak to the receptionist:

> "I need my bill."

The receptionist communicates with the hotel's internal billing system.

```text
YOU
 ↓
RECEPTIONIST
 ↓
HOTEL BILLING SYSTEM
```

You don't directly interact with the billing database.

Similarly:

```text
AI Agent
   ↓
MCP Server
   ↓
OCI API
```

The MCP Server acts like a standardized **receptionist/adapter** between the AI application and the underlying service.

---

# 20. "Oracle MCP Server" Does Not Mean "Oracle Cloud Server"

This wording can cause confusion.

When the instructor says:

> **"Oracle's OCI Usage MCP Server"**

they mean **software created/published by Oracle**.

In this particular architecture, that software can be launched locally as a process.

```text
Oracle-created software
        ↓
Running on your computer
        ↓
Communicates with Oracle Cloud
```

So it does **not necessarily mean** your Python program is connecting to a remote MCP Server hosted by Oracle.

---

# 21. Why Does `uvx` Appear?

You may see:

```text
uvx oracle.oci-usage-mcp-server
```

Conceptually, your Python MCP Client tells the operating system:

```text
Start this command:
        ↓
uvx oracle.oci-usage-mcp-server
```

`uvx` runs the Python package and starts the MCP Server process.

So:

```text
Your Python Program
        │
        │ spawn
        ↓
       uvx
        │
        ↓
Oracle MCP Server Process
```

Then:

```text
Your Python Program
        ↕
      stdio
        ↕
Oracle MCP Server
```

---

# 22. The Most Important Architecture to Memorize

```text
              YOUR COMPUTER
┌───────────────────────────────────┐
│                                   │
│  Python Agent                     │
│      │                            │
│      ↓                            │
│  LangChain Agent                  │
│      │                            │
│      ↓                            │
│  MCP Client                       │
│      │                            │
│      │ stdio                      │
│      ↕                            │
│  Oracle MCP Server                │
│                                   │
└──────────────┬────────────────────┘
               │
               │ HTTPS
               ↓
        ┌───────────────┐
        │ Oracle Cloud  │
        │               │
        │ OCI Usage API │
        └───────────────┘
```

### Memorize this sentence:

> **Your Python program talks to the MCP Server locally through stdio, while the MCP Server talks to Oracle Cloud through HTTPS.**

---

# 23. Where Does LangChain Fit?

This is the most important connection.

MCP does **not replace LangChain**.

They operate at different layers.

```text
LangChain
    ↓
Builds / runs the agent

MCP
    ↓
Standardizes tool connection
```

So:

```text
LangChain = Agent / Orchestration Layer

MCP = Tool-Connection / Integration Layer
```

---

# 24. Before MCP

Before using MCP, tools could live directly inside your LangChain application.

Example:

```python
from langchain_core.tools import tool

@tool
def add(a, b):
    return a + b

@tool
def multiply(a, b):
    return a * b

tools = [add, multiply]
```

Then:

```python
agent = create_agent(
    model=model,
    tools=tools
)
```

Architecture:

```text
User
 ↓
LangChain Agent
 ↓
LLM
 ↓
LangChain Tools
 ↓
Python Functions
```

The tools are part of your application.

---

# 25. After MCP

With MCP, the tools can be provided by an external MCP Server.

```text
User
 ↓
LangChain Agent
 ↓
LLM
 ↓
MCP Client
 ↓
MCP Server
 ↓
External System / API
```

For OCI:

```text
User
 ↓
LangChain Agent
 ↓
LLM
 ↓
MCP Client
 ↓
stdio
 ↓
Oracle OCI Usage MCP Server
 ↓
HTTPS
 ↓
OCI Usage REST API
```

The LangChain Agent is still there.

---

# 26. Where Exactly Is LangChain in the Code?

The course can still use something conceptually like:

```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=tools
)
```

The important change is:

> **Where do `tools` come from?**

---

# 27. Before MCP — Tools Created Locally

You write the tools yourself:

```python
@tool
def add(a, b):
    return a + b

@tool
def multiply(a, b):
    return a * b

tools = [add, multiply]
```

Then:

```python
agent = create_agent(
    model=model,
    tools=tools
)
```

Architecture:

```text
LangChain Agent
      ↓
LangChain Tools
      ↓
Local Python Functions
```

---

# 28. After MCP — Tools Come From MCP

Instead of manually creating every external tool:

```python
client = MultiServerMCPClient(...)

tools = await client.get_tools()
```

Conceptually:

```text
Oracle MCP Server
       ↓
   tools/list
       ↓
   MCP Client
       ↓
LangChain-compatible tools
       ↓
LangChain Agent
```

Then:

```python
agent = create_agent(
    model=model,
    tools=tools
)
```

### Important

The agent creation is still handled by **LangChain**.

The tools are now being discovered/provided through **MCP**.

---

# 29. Full LangChain + MCP Architecture

```text
                         USER
                           │
                           ↓
                  ┌─────────────────┐
                  │    LangChain    │
                  │     Agent       │
                  └────────┬────────┘
                           │
                           ↓
                          LLM
                           │
                    "I need usage data"
                           │
                           ↓
                  ┌─────────────────┐
                  │   MCP Client    │
                  └────────┬────────┘
                           │
                       MCP / stdio
                           │
                           ↓
             ┌──────────────────────────┐
             │ Oracle OCI Usage         │
             │ MCP Server               │
             └────────────┬─────────────┘
                          │
                       HTTPS
                          │
                          ↓
             ┌──────────────────────────┐
             │ OCI Usage REST API       │
             └────────────┬─────────────┘
                          │
                          ↓
                    OCI Cost Data
```

---

# 30. What Actually Changed?

This is the core architectural difference.

## Before MCP

```text
LangChain Agent
      ↓
LangChain Tools
      ↓
Python Functions
```

## After MCP

```text
LangChain Agent
      ↓
MCP Client
      ↓
MCP Server
      ↓
External Tools / APIs
```

### Key change

> **The agent did not disappear.**

> **The tool connection changed.**

Instead of tools being tightly implemented inside the LangChain application, they can be exposed through an MCP Server.

---

# 31. LangChain vs MCP — Simple Mental Model

Think of the system as two layers.

### LangChain

Responsible for the **agent**:

```text
User
 ↓
Agent
 ↓
LLM
 ↓
Reason / Decide
 ↓
Call Tool
 ↓
Use Result
 ↓
Answer
```

### MCP

Responsible for the **standardized tool connection**:

```text
MCP Client
     ↓
MCP Protocol
     ↓
MCP Server
     ↓
Tool / Resource / External System
```

Together:

```text
User
 ↓
LangChain Agent
 ↓
LLM
 ↓
MCP Client
 ↓
MCP Server
 ↓
External System
```

---

# 32. The Restaurant Analogy

A simple way to remember the difference:

### LangChain = Manager / Waiter

LangChain manages the interaction:

```text
User asks something
       ↓
Agent decides what to do
       ↓
Calls appropriate tool
       ↓
Gets result
       ↓
Produces answer
```

### MCP = Standard communication system

MCP provides a standardized way to connect to external tools:

```text
LangChain
    ↓
MCP Client
    ↓
MCP Server
    ↓
Tool
```

### OCI MCP Server = Specialist

The OCI MCP Server knows how to communicate with OCI:

```text
MCP Server
    ↓
OCI Usage REST API
```

---

# 33. Complete Mental Model

Think about the responsibilities like this:

```text
┌───────────────────────────────────────┐
│              LangChain                │
│                                       │
│  Agent / Orchestration                │
│  LLM interaction                      │
│  Tool selection                       │
│  Agent loop                           │
└──────────────────┬────────────────────┘
                   │
                   │ MCP
                   ↓
┌───────────────────────────────────────┐
│                MCP                    │
│                                       │
│  Standard tool communication          │
│  Client ↔ Server                      │
└──────────────────┬────────────────────┘
                   │
                   ↓
┌───────────────────────────────────────┐
│             MCP Server                │
│                                       │
│  Exposes capabilities                 │
│  Handles service-specific integration │
└──────────────────┬────────────────────┘
                   │
                   ↓
┌───────────────────────────────────────┐
│          External System              │
│                                       │
│  OCI API / Database / Service / Tool  │
└───────────────────────────────────────┘
```

---

# 34. What Does the MCP Client Do?

The MCP Client sits between your application and the MCP Server.

```text
LangChain Agent
      │
      ↓
MCP Client
      │
      ↓
MCP Server
```

It can communicate with the server to discover and use its capabilities.

Conceptually:

```text
MCP Client
    │
    ├── Discover tools
    │
    ├── Discover resources
    │
    └── Call tools
```

For example:

```text
MCP Client
     │
     │ tools/list
     ↓
MCP Server
     │
     ↓
Available tools
```

Then:

```text
MCP Client
     │
     │ tools/call
     ↓
MCP Server
```

---

# 35. What Does the MCP Server Do?

The MCP Server exposes capabilities through MCP.

For the OCI example:

```text
MCP Server
     │
     └── get_summarized_usage
```

Internally, it may communicate with:

```text
OCI Usage REST API
```

So:

```text
MCP Server
     │
     ├── MCP interface
     │
     └── OCI API integration
```

---

# 36. The Complete Request Flow

For:

> **"How much did I spend on storage in the last 30 days?"**

The complete flow is:

```text
1. User
      ↓
2. LangChain Agent
      ↓
3. LLM
      ↓
4. Select OCI usage tool
      ↓
5. MCP Client
      ↓
6. MCP Server
      ↓
7. OCI Usage REST API
      ↓
8. OCI Cost Data
      ↓
9. MCP Server
      ↓
10. MCP Client
      ↓
11. LangChain Agent
      ↓
12. LLM
      ↓
13. Final Answer
```

---

# 37. Why the Agent Code Barely Changes

This is an important MCP benefit.

Suppose your LangChain agent already knows how to work with tools:

```python
agent = create_agent(
    model=model,
    tools=tools
)
```

You can change the source of those tools.

### Local tools

```text
Python Functions
      ↓
tools
      ↓
LangChain Agent
```

### MCP tools

```text
MCP Server
      ↓
MCP Client
      ↓
tools
      ↓
LangChain Agent
```

The agent can still operate on a list of tools.

The main architectural change is **where those tools come from**.

---

# 38. Before vs After MCP

| Aspect                   | Before MCP                   | With MCP                 |
| ------------------------ | ---------------------------- | ------------------------ |
| Agent                    | LangChain Agent              | LangChain Agent          |
| LLM                      | LLM                          | LLM                      |
| Tool source              | Local Python tools           | MCP Server               |
| Tool connection          | Direct                       | MCP                      |
| External API integration | Application may implement it | MCP Server can handle it |
| Standard protocol        | Application-specific         | MCP                      |
| OCI integration          | Application code             | OCI MCP Server           |

---

# 39. The Three Most Important Layers

For this example, remember:

```text
┌─────────────────────────────┐
│ 1. LangChain                │
│                             │
│ Agent / Orchestration       │
└──────────────┬──────────────┘
               │
               ↓
┌─────────────────────────────┐
│ 2. MCP                      │
│                             │
│ Standard Tool Connection    │
└──────────────┬──────────────┘
               │
               ↓
┌─────────────────────────────┐
│ 3. OCI API                  │
│                             │
│ Actual Cloud Data / Service │
└─────────────────────────────┘
```

---

# 40. Interview Answer — Where Does LangChain Fit in MCP?

### Short answer

> **LangChain is still responsible for building and running the AI agent, including the LLM interaction and orchestration. MCP provides a standardized protocol for connecting that agent to external tools and services. An MCP Client connects the LangChain application to an MCP Server, which can then communicate with an underlying API such as the OCI Usage REST API.**

### Even shorter

> **LangChain manages the agent; MCP standardizes the agent's connection to external tools.**

---

# 41. Interview Answer — What Is the Difference Between an API and MCP?

> **An API is an interface exposed by a service for software communication, while MCP is a standardized protocol designed for AI applications to discover and interact with tools and context. An MCP Server can use an underlying API and expose its functionality as MCP tools.**

---

# 42. Interview Answer — What Does "Spawn an MCP Server" Mean?

> **It means the application starts the MCP Server as a separate process, usually as a subprocess. In a local stdio setup, the parent application communicates with that server process through standard input and output.**

---

# 43. Interview Answer — Does MCP Replace LangChain?

> **No. They operate at different layers. LangChain can provide the agent and orchestration layer, while MCP provides a standardized way for that agent to connect to external tools and services.**

---

# 44. Interview Answer — Does the Python Agent Directly Call the OCI API?

For this architecture:

> **No. The Python application communicates with the OCI MCP Server through the MCP Client. The MCP Server handles the OCI-specific communication with the OCI Usage REST API.**

Architecture:

```text
Python Agent
     ↓
MCP Client
     ↓
MCP Server
     ↓
OCI Usage REST API
```

---

# 45. Quick Revision

```text
API
↓
Interface for software communication

REST API
↓
API commonly accessed through HTTP/HTTPS

OCI Usage API
↓
Provides OCI usage/cost information

MCP
↓
Standard protocol for AI tool/context interaction

MCP Client
↓
Connects the AI application to an MCP Server

MCP Server
↓
Exposes capabilities through MCP

stdio
↓
Local process communication through stdin/stdout

HTTPS
↓
Network communication with OCI

LangChain
↓
Agent / orchestration layer

uvx
↓
Runs the MCP server package/process

Subprocess
↓
Separate process started by another program
```

---

# 46. Final Architecture to Memorize

```text
                         USER
                           │
                           ↓
                  ┌─────────────────┐
                  │    LangChain    │
                  │     Agent       │
                  └────────┬────────┘
                           │
                           ↓
                          LLM
                           │
                           ↓
                  ┌─────────────────┐
                  │   MCP Client    │
                  └────────┬────────┘
                           │
                        MCP / stdio
                           │
                           ↓
             ┌──────────────────────────┐
             │ Oracle OCI Usage         │
             │ MCP Server               │
             └────────────┬─────────────┘
                          │
                        HTTPS
                          │
                          ↓
             ┌──────────────────────────┐
             │ OCI Usage REST API       │
             └────────────┬─────────────┘
                          │
                          ↓
                    OCI Cost Data
```

---

# 47. Final Mental Model

The entire lesson can be reduced to:

```text
LangChain
   ↓
Builds / runs the agent

MCP
   ↓
Standardizes tool communication

MCP Client
   ↓
Connects the agent to an MCP Server

MCP Server
   ↓
Exposes external capabilities

OCI Usage REST API
   ↓
Provides actual OCI usage/cost data
```

### The one sentence to remember

> **LangChain decides and orchestrates; MCP standardizes how the agent connects to external tools; the MCP Server exposes those tools and can communicate with underlying APIs such as the OCI Usage REST API.**

### The one architecture to remember

```text
LangChain Agent
      ↓
MCP Client
      ↓
MCP Server
      ↓
External API / Service
```

For OCI:

```text
LangChain Agent
      ↓
MCP Client
      ↓ stdio
OCI Usage MCP Server
      ↓ HTTPS
OCI Usage REST API
      ↓
OCI Cost Data
```

---

# 48. Final Checklist

* [ ] I understand what an API is.
* [ ] I understand what the OCI Usage API provides.
* [ ] I understand what a REST API is.
* [ ] I understand what an MCP Server is.
* [ ] I understand that an MCP Server can wrap an existing API.
* [ ] I understand the difference between stdio and HTTPS.
* [ ] I understand what spawning a subprocess means.
* [ ] I understand why `uvx` appears in the setup.
* [ ] I understand that LangChain has not disappeared.
* [ ] I understand that LangChain manages the agent/orchestration layer.
* [ ] I understand that MCP provides standardized tool communication.
* [ ] I understand what the MCP Client does.
* [ ] I understand what the MCP Server does.
* [ ] I understand how LangChain and MCP work together.
* [ ] I understand the complete OCI request flow.
* [ ] I can explain **LangChain vs MCP vs API** in an interview.
