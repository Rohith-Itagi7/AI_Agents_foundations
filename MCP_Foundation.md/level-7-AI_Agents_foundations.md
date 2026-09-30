# Real-World MCP — OCI Usage MCP Server

## 1. Why move beyond the Math MCP Server?

The Math MCP server was useful for learning because we controlled everything:

```text
We wrote the client
        +
We wrote the MCP server
        +
We wrote the tools
```

So if something went wrong, we could inspect both sides.

For example:

```text
Client
  ↓
MCP Server
  ↓
divide()
```

We could open the server code and add:

```python
print("divide tool called")
```

to debug it.

But this is **not how MCP is normally used in production**.

---

# 2. Real-world MCP

In a real application, the server is usually created by someone else.

For example:

```text
Oracle
SaaS company
Another engineering team
Third-party vendor
```

They publish an MCP server.

You only build/use the client.

```text
             YOU
              │
              ↓
          MCP Client
              │
              ↓
       Third-party MCP Server
              │
              ↓
        External API / System
```

You don't need to know how the server internally works.

You interact with it through the MCP protocol.

---

# 3. The key difference

## Learning example

```text
You
 ├── MCP Client
 └── MCP Server
       └── Tools
```

You own everything.

## Production example

```text
You
 └── MCP Client
       │
       ↓
Oracle / Vendor / Team
 └── MCP Server
       │
       ↓
External API
```

Someone else owns the server.

This is where MCP becomes especially useful.

---

# 4. The real-world example: OCI Usage MCP Server

The lesson uses an Oracle Cloud Infrastructure example.

The server is called:

```text
OCI Usage MCP Server
```

According to the lesson, it is published by:

**Oracle**

and published as a Python package on:

**PyPI**

The package mentioned in the lesson is:

```text
oracle.oci-usage-mcp-server
```

The important point is:

> **We did not build this MCP server. Oracle did.**

---

# 5. What does the OCI Usage MCP Server actually do?

The MCP server acts as a bridge.

It exposes OCI usage/billing functionality through MCP.

Architecture:

```text
Your MCP Client
      │
      │ MCP / stdio
      ↓
OCI Usage MCP Server
      │
      │ HTTPS
      ↓
OCI Usage REST API
      │
      ↓
OCI Cloud
```

So the MCP server is essentially acting as an adapter.

---

# 6. What does it wrap?

The lesson says the MCP server wraps the:

```text
OCI Usage REST API
```

Specifically, the usage endpoint behind OCI's cost-analysis/billing functionality.

So instead of your application directly calling the OCI REST API, you can interact with the MCP server.

### Without MCP

Your application might directly call:

```text
Your application
      ↓
OCI REST API
```

### With MCP

```text
Your application
      ↓
MCP Client
      ↓
OCI Usage MCP Server
      ↓
OCI REST API
```

The MCP server becomes the standardized interface between your AI application and OCI's API.

---

# 7. Very important: Who calls the OCI REST API?

This is one of the most important details in the lesson.

Your client **does NOT directly call the OCI REST API**.

Instead:

```text
Your Python code
      ↓
MCP Client
      ↓
OCI Usage MCP Server
      ↓
OCI REST API
```

The **MCP server** is responsible for communicating with OCI.

So:

```text
YOU → MCP
```

and:

```text
MCP SERVER → OCI API
```

---

# 8. Two different connections

Look carefully at the architecture from the slide.

```text
┌──────────────┐      stdio      ┌──────────────────────┐
│ Your Python  │ <-------------> │ OCI Usage MCP Server │
│ MCP Client   │                 │                      │
└──────────────┘                 └──────────┬───────────┘
                                            │
                                          HTTPS
                                            │
                                            ↓
                                   ┌─────────────────┐
                                   │ OCI Usage API   │
                                   └─────────────────┘
```

There are **two completely different connections**.

### Connection 1

```text
Your Python program
        ↕
MCP Server
```

Transport:

```text
stdio
```

### Connection 2

```text
MCP Server
        ↓
OCI API
```

Transport:

```text
HTTPS
```

Do not mix these two up.

---

# 9. Is the Oracle MCP server running remotely?

This is a subtle but extremely important point.

The **Oracle-created MCP server software** is being run locally in the example.

Your machine has:

```text
Your Python program
       +
OCI MCP server process
```

These two processes communicate locally using:

```text
stdin/stdout
```

The MCP server then reaches Oracle's cloud services over HTTPS.

So:

```text
LOCAL MACHINE
─────────────────────────────────

Your Python program
       │
       │ stdio
       ↓
OCI MCP Server
       │
       │ HTTPS
       ↓
─────────────────────────────────
        INTERNET
       ↓
Oracle Cloud / OCI API
```

### Therefore:

The MCP server is **third-party software**, but the server process itself is running locally in this example.

That distinction is easy to miss.

---

# 10. Why does this architecture look strange?

You might initially think:

> "If Oracle provides the server, shouldn't my code connect directly to Oracle over the internet?"

Not necessarily.

MCP allows the vendor to distribute a server program that you run locally.

That local server then handles communication with the vendor's cloud service.

So:

```text
Vendor-created software
        ↓
runs locally
        ↓
communicates with vendor cloud
```

This is different from:

```text
Your code
        ↓
remote MCP server over HTTP
```

Both architectures are possible.

---

# 11. What does the MCP server expose?

The OCI Usage MCP server in this lesson has a very small tool surface.

It exposes **one tool**:

```text
get_summarized_usage
```

Conceptually:

```text
OCI Usage MCP Server
        │
        └── get_summarized_usage()
```

Many real MCP servers can expose dozens of tools, but this example intentionally keeps things simple.

---

# 12. What does `get_summarized_usage` do?

It retrieves summarized usage/cost information.

The tool accepts arguments such as:

```text
tenant_id
start_time
end_time
group_by
granularity
query_type
```

Conceptually:

```python
get_summarized_usage(
    tenant_id=...,
    start_time=...,
    end_time=...,
    group_by=...,
    granularity=...,
    query_type=...
)
```

The exact implementation is hidden from your client.

That is an important MCP concept.

---

# 13. You don't need to know the server implementation

Suppose the server exposes:

```text
get_summarized_usage
```

Your client only needs to know:

```text
Tool name
Tool description
Input parameters
Input types
Required arguments
```

You don't need to know:

```text
How Oracle implemented it
Which Python functions it uses
Which internal classes it uses
How it constructs the REST request
How authentication works internally
```

The MCP protocol gives you the interface.

---

# 14. Think of MCP like an API contract

Imagine a restaurant.

You see:

```text
MENU
──────
Pizza
Burger
Pasta
```

You don't need to know:

```text
How the chef cooks the food
Which oven they use
Which internal kitchen process they follow
```

You simply order:

```text
Pizza
```

MCP works similarly.

The server exposes:

```text
Tool
Input
Output
```

The client uses that contract.

---

# 15. What stays the same?

Moving from our Math MCP server to the OCI MCP server does **not** fundamentally change the MCP client architecture.

The following remain the same:

### MCP Client

You still have a client.

### JSON-RPC

Communication still uses the MCP protocol and JSON-RPC messaging.

### Tool discovery

You still discover tools.

Conceptually:

```text
tools/list
```

### Tool execution

You still call tools.

Conceptually:

```text
tools/call
```

### stdio

In this particular example, the client still communicates with the MCP server using:

```text
stdio
```

So the client-side workflow remains:

```text
Connect
   ↓
Initialize
   ↓
Discover tools
   ↓
Give tools to agent
   ↓
Agent chooses tool
   ↓
Call tool
   ↓
Receive result
```

---

# 16. What changes?

The biggest changes are:

### 1. Who owns the server?

Math demo:

```text
You
```

OCI example:

```text
Oracle
```

### 2. What does the server wrap?

Math demo:

```text
Python functions
```

OCI example:

```text
OCI Usage REST API
```

So:

```text
                  Math MCP       OCI MCP
                  --------       -------
Server owner      You            Oracle
Server wraps      Python tools   OCI API
Tools             Math           Usage/billing
```

---

# 17. The architecture comparison

## Math example

```text
Your Agent
    │
    │ stdio
    ↓
Your Math MCP Server
    │
    ↓
Your Python Functions
```

You own both sides.

---

## OCI example

```text
Your Agent
    │
    │ stdio
    ↓
Oracle OCI Usage MCP Server
    │
    │ HTTPS
    ↓
OCI Usage REST API
```

You only own the client.

Oracle owns the server.

---

# 18. What is PyPI?

The lesson mentions:

```text
PyPI
```

PyPI means:

> **Python Package Index**

It is a large public repository for Python packages.

For example, developers can install Python packages using:

```bash
pip install package-name
```

The OCI MCP server is published as a Python package.

So the server can be obtained through Python's package ecosystem.

---

# 19. What is `uvx`?

The lesson introduces another important tool:

```text
uvx
```

`uvx` is part of the **uv** Python tooling ecosystem.

The easiest mental model is:

> **`uvx` is roughly like `npx`, but for Python tools.**

Node.js:

```text
npx some-package
```

Python:

```text
uvx some-python-tool
```

The idea is:

```text
Run a Python tool
without manually installing it into your main environment.
```

---

# 20. Why use `uvx`?

Without `uvx`, you might need to do something like:

```bash
pip install oracle.oci-usage-mcp-server
```

Then worry about:

```text
dependencies
versions
virtual environments
package conflicts
```

With `uvx`, the package can be run in an isolated environment.

Conceptually:

```text
uvx
 │
 ├── obtain package
 ├── create/use isolated environment
 ├── install dependencies
 ├── run tool
 └── cache it for reuse
```

This makes running MCP servers convenient.

---

# 21. First run vs later runs

Conceptually, the first time you run:

```text
uvx oracle.oci-usage-mcp-server
```

the tooling may need to obtain the package and dependencies.

Afterward, cached artifacts can be reused where appropriate.

So the general idea is:

```text
First run
    ↓
Download/package setup
    ↓
Isolated environment
    ↓
Run MCP server
```

Later:

```text
Run
 ↓
Reuse cached environment/artifacts when possible
 ↓
Start server
```

---

# 22. What is the code snippet doing?

The slide shows something conceptually like:

```python
from mcp import StdioServerParameters

server_params = StdioServerParameters(
    command="uvx",
    args=["oracle.oci-usage-mcp-server"],
    env={
        "OCI_CONFIG_PROFILE": "DEFAULT"
    },
)
```

Let's understand this **line by line**.

---

# 23. `StdioServerParameters`

```python
from mcp import StdioServerParameters
```

This tells the MCP client:

> "I want to configure an MCP server that I will communicate with through stdio."

The configuration describes how to start the server.

---

# 24. `command="uvx"`

```python
command="uvx"
```

This means:

> "Use the `uvx` executable to start the MCP server."

The client essentially knows:

```text
I need to start a process.
The command to start it is:

uvx
```

---

# 25. `args=[...]`

```python
args=["oracle.oci-usage-mcp-server"]
```

This tells `uvx` which Python tool/package to run.

Conceptually:

```text
uvx
   +
oracle.oci-usage-mcp-server
```

becomes:

```bash
uvx oracle.oci-usage-mcp-server
```

---

# 26. `env`

The configuration also provides environment variables.

For example:

```python
env={
    "OCI_CONFIG_PROFILE": "DEFAULT"
}
```

This supplies environment/configuration information to the MCP server process.

The server can use this information when communicating with OCI.

The exact authentication/configuration mechanism depends on the OCI setup.

---

# 27. What happens when the client starts?

Imagine your Python program executes this configuration.

The sequence is approximately:

```text
Your Python Client
       │
       │ "Start the server"
       ↓
     uvx
       │
       ↓
OCI Usage MCP Server
       │
       │ stdin/stdout
       ↕
Your MCP Client
```

The client can now communicate with the server.

---

# 28. What happens after the server starts?

The MCP lifecycle begins.

Conceptually:

```text
1. Initialize
       ↓
2. Discover tools
       ↓
3. Agent receives tool information
       ↓
4. User asks question
       ↓
5. Agent chooses get_summarized_usage
       ↓
6. MCP client calls server
       ↓
7. Server calls OCI API
       ↓
8. OCI returns usage data
       ↓
9. MCP server returns result
       ↓
10. Agent produces answer
```

---

# 29. The complete real-world flow

Suppose the user asks:

> "What was my OCI usage cost during this period?"

The flow becomes:

```text
USER
 │
 ↓
AI AGENT
 │
 │ decides:
 │ "I need usage data."
 ↓
MCP CLIENT
 │
 │ tools/call
 ↓
OCI USAGE MCP SERVER
 │
 │ converts request into
 │ OCI API request
 ↓
OCI USAGE REST API
 │
 ↓
OCI CLOUD
 │
 │ usage data
 ↓
OCI USAGE MCP SERVER
 │
 │ MCP result
 ↓
MCP CLIENT
 │
 ↓
AI AGENT
 │
 ↓
FINAL ANSWER
```

---

# 30. Notice where the LLM is NOT involved

This is important.

The LLM does not directly perform:

```text
OCI authentication
OCI REST API request
HTTP request construction
```

Instead:

```text
LLM
 ↓
chooses tool
 ↓
MCP client
 ↓
MCP server
 ↓
OCI API
```

The server handles the actual integration with OCI.

---

# 31. Why is this better than every AI application integrating OCI separately?

Imagine 10 AI applications need OCI usage information.

### Without MCP

Each application could need its own OCI integration:

```text
App 1 → OCI API
App 2 → OCI API
App 3 → OCI API
App 4 → OCI API
...
App 10 → OCI API
```

That creates repeated integration work.

### With MCP

Oracle can provide one MCP server:

```text
                    ┌── App 1
                    │
                    ├── App 2
Oracle MCP Server ──┼── App 3
                    │
                    ├── App 4
                    │
                    └── App 10
```

Each MCP-compatible application uses the standardized interface.

This is the **real-world value of MCP**.

---

# 32. Why the server doesn't need to be open source

This is another important concept.

Your application can consume an MCP server without needing to inspect its source code.

You only care about its exposed interface:

```text
What tools exist?
What arguments do they accept?
What results/errors do they return?
```

For example:

```text
tools/list
```

might tell you:

```text
get_summarized_usage

Arguments:
tenant_id
start_time
end_time
group_by
granularity
query_type
```

You can use the tool without knowing its implementation.

---

# 33. Debugging changes in the real world

This is why the instructor says:

> "You cannot add a print statement to the server."

With your own server:

```text
Something fails
      ↓
Open server code
      ↓
Add print()
      ↓
Debug
```

With a third-party server:

```text
Something fails
      ↓
Inspect MCP communication
      ↓
Check tools/list
      ↓
Check tools/call
      ↓
Check arguments
      ↓
Check returned error
      ↓
Check external API/auth/configuration
```

You debug through the **interface**, not by modifying the server.

---

# 34. This makes protocol understanding more important

When you own both sides:

```text
Client + Server
```

you can inspect everything.

When you only own:

```text
Client
```

you need to understand the protocol.

For example:

```text
Did initialization succeed?

Did tools/list return the expected tool?

Did the tool schema contain the expected arguments?

Did tools/call contain the correct arguments?

Did the server return an error?

Did the underlying API fail?
```

MCP becomes the boundary between your application and somebody else's system.

---

# 35. Why MCP "earns its keep" here

For a simple calculator:

```text
add(2, 3)
```

MCP might be unnecessary.

You can simply write:

```python
def add(a, b):
    return a + b
```

But consider:

```text
OCI billing
GitHub
Slack
Jira
Databases
Cloud infrastructure
Enterprise systems
```

These systems already have complex APIs.

Instead of every AI application writing custom integrations, a provider can expose an MCP server.

Then:

```text
AI Application
      ↓
Standard MCP Interface
      ↓
Vendor's MCP Server
      ↓
Vendor's existing APIs
```

That's where MCP becomes much more valuable.

---

# 36. One very important distinction

Do not confuse:

### MCP Server

with:

### The underlying service/API

In this example:

```text
MCP Server
    ≠
OCI REST API
```

The MCP server is an **adapter/wrapper** around the OCI API.

Think:

```text
                 MCP interface
                      ↓
             ┌─────────────────┐
AI App ─────→│ OCI MCP Server  │
             └────────┬────────┘
                      ↓
                 OCI REST API
```

The MCP server translates between the MCP world and OCI's API world.

---

# 37. A simple analogy

Imagine you want to order from a restaurant.

### Without an MCP-style adapter

Every customer has to learn the restaurant's internal system.

```text
Customer
   ↓
Restaurant's internal API
```

### With an MCP server

The restaurant provides a standardized waiter/interface:

```text
Customer
   ↓
Standard interface
   ↓
Restaurant
```

The customer only needs to understand the interface.

The restaurant handles the internal complexity.

---

# 38. The three layers you should remember

For this OCI example, remember:

### Layer 1 — Your application

```text
AI Agent / MCP Client
```

### Layer 2 — MCP server

```text
OCI Usage MCP Server
```

### Layer 3 — Real service

```text
OCI Usage REST API
```

Therefore:

```text
YOUR CODE
    ↓
MCP
    ↓
ORACLE MCP SERVER
    ↓
OCI API
```

---

# 39. Math MCP vs OCI MCP

| Feature                   | Math MCP         | OCI Usage MCP            |
| ------------------------- | ---------------- | ------------------------ |
| Server creator            | You              | Oracle                   |
| Client creator            | You              | You                      |
| Server runs               | Local            | Local in this example    |
| Client → server transport | stdio            | stdio                    |
| Server → external system  | None             | HTTPS                    |
| Server wraps              | Python functions | OCI Usage API            |
| Number of tools in lesson | 4                | 1                        |
| Tool example              | `multiply()`     | `get_summarized_usage()` |
| Can modify server?        | Yes              | No                       |
| Main purpose              | Learning         | Real-world integration   |

---

# 40. The most important architecture diagram

Memorize this:

```text
                 YOUR MACHINE
┌──────────────────────────────────────────┐
│                                          │
│  Your AI Agent                           │
│       │                                  │
│       ↓                                  │
│  MCP Client                              │
│       │                                  │
│       │ stdio / JSON-RPC                 │
│       ↓                                  │
│  OCI Usage MCP Server                    │
│       │                                  │
└───────┼──────────────────────────────────┘
        │
        │ HTTPS
        ↓
┌──────────────────────────┐
│       Oracle Cloud       │
│                          │
│   OCI Usage REST API     │
│          ↓               │
│   Usage / Cost Data      │
└──────────────────────────┘
```

### The key observation:

**The stdio connection is local.**

**The HTTPS connection is between the MCP server and OCI.**

---

# 41. The entire lesson in one picture

```text
                    USER
                      │
                      ↓
                 AI AGENT
                      │
                      ↓
                 MCP CLIENT
                      │
                 tools/list
                 tools/call
                      │
                 JSON-RPC
                      │
                    stdio
                      │
                      ↓
          OCI USAGE MCP SERVER
          (created by Oracle)
                      │
                      │ HTTPS
                      ↓
             OCI USAGE REST API
                      │
                      ↓
                USAGE DATA
                      │
                      ↑
          OCI USAGE MCP SERVER
                      │
                      ↑
                 MCP CLIENT
                      │
                      ↑
                  AI AGENT
                      │
                      ↑
                    USER
```

---

# 42. What you should remember for MCP

If you remember only these **7 points**, you understand the lesson:

### 1. Real-world MCP servers are usually created by someone else.

```text
Vendor / company / another team
```

### 2. Your application usually acts as the client.

```text
Your App → MCP Client
```

### 3. You interact through the MCP protocol.

```text
tools/list
tools/call
```

### 4. You don't need the server's source code.

You need its exposed interface.

### 5. An MCP server can wrap an existing API.

```text
MCP Server → REST API
```

### 6. Local stdio and remote HTTPS can coexist.

```text
Your App
   ↓ stdio
MCP Server
   ↓ HTTPS
Cloud API
```

### 7. This is where MCP's "define once, use everywhere" idea becomes valuable.

```text
One MCP server
      ↓
Many AI applications
```

---

# 43. One-line interview answer

If someone asks:

**"What is a real-world use case of MCP?"**

You can say:

> "A vendor such as Oracle can expose an existing service like its usage API through an MCP server. AI applications only need an MCP client to discover and call those tools, instead of each application building a custom integration with the vendor's API."

That is the central idea of this lesson.
