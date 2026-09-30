# Real-World MCP Demo — Oracle OCI Usage MCP Server

## 1. What is this demo showing?

The goal is to answer a natural-language question such as:

> **"Show me the cost for the last 30 days as a daily breakdown by service."**

Instead of writing code that directly calls Oracle's billing API, the application uses an **MCP server published by Oracle**.

The architecture is:

```text
User
 ↓
LangChain Agent
 ↓
MCP Client
 ↓ stdio / JSON-RPC
Oracle OCI Usage MCP Server
 ↓ HTTPS
OCI Usage API
 ↓
OCI Billing / Usage Data
```

The important difference from the earlier Math MCP demo is:

```text
Math Demo:
We wrote the server.

Real-world demo:
Oracle wrote the server.
```

---

# 2. What is the application trying to achieve?

The application wants to retrieve OCI cost information.

The user asks:

```text
Show me the cost for the last 30 days
as a daily breakdown by service.
```

The agent needs information from OCI.

Instead of directly writing:

```text
Python → OCI REST API
```

the application uses:

```text
Python
  ↓
MCP Client
  ↓
Oracle MCP Server
  ↓
OCI Usage API
```

---

# 3. The complete architecture

This is the most important diagram from the demo:

```text
                    USER
                      │
                      │ Natural language
                      ↓
              ┌───────────────┐
              │ LangChain     │
              │ Agent         │
              └───────┬───────┘
                      │
                      ↓
              ┌───────────────┐
              │ MCP Client    │
              └───────┬───────┘
                      │
                 stdio / MCP
                      │
                      ↓
       ┌──────────────────────────────┐
       │ Oracle OCI Usage MCP Server  │
       └──────────────┬───────────────┘
                      │
                    HTTPS
                      │
                      ↓
       ┌──────────────────────────────┐
       │ OCI Usage REST API           │
       └──────────────┬───────────────┘
                      │
                      ↓
              OCI Usage / Cost Data
```

There are **two different communication paths**:

### Path 1

```text
Your application
       ↓
MCP server
```

Uses:

**stdio + MCP/JSON-RPC**

### Path 2

```text
MCP server
       ↓
OCI Usage API
```

Uses:

**HTTPS**

---

# 4. The user doesn't need to know the OCI API

This is one of the main benefits.

Without MCP, your application might need to understand:

```text
OCI API endpoint
HTTP method
request format
authentication
parameters
response format
error handling
```

With the MCP server:

```text
Agent
 ↓
get_summarized_usage
 ↓
MCP server handles OCI API
```

The Oracle MCP server handles the underlying OCI integration.

---

# 5. What tool does the MCP server provide?

The demo uses:

```text
get_summarized_usage
```

This is the tool the agent calls to retrieve OCI usage information.

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

The agent doesn't implement this function itself.

Oracle's MCP server provides it.

---

# 6. The natural-language question

The demo gives the agent:

```text
Show me the cost for last 30 days
as a daily breakdown by service.
```

The LLM interprets this.

It needs to determine things such as:

```text
Time period:
last 30 days

Granularity:
daily

Group by:
service
```

Then it decides that the appropriate tool is:

```text
get_summarized_usage
```

---

# 7. What happens internally?

The flow is roughly:

```text
User:
"Show me the cost for the last 30 days
as a daily breakdown by service."

                 ↓

             LLM / Agent

                 ↓

"I need OCI usage information."

                 ↓

      get_summarized_usage

                 ↓

             MCP Client

                 ↓

        MCP Server (Oracle)

                 ↓

          OCI Usage API

                 ↓

          OCI billing data

                 ↓

        MCP Server response

                 ↓

             MCP Client

                 ↓

               Agent

                 ↓

          Final explanation
```

---

# 8. The important thing: the agent is not calculating the bill

The LLM isn't sitting there thinking:

```text
$1300 + $1400 + $1951 + ...
```

to somehow recreate the OCI billing system.

Instead, it asks the external tool for the actual usage data.

So:

```text
LLM
 ↓
"I need this data."
 ↓
Tool call
 ↓
OCI
 ↓
Actual usage data
```

This is an example of **grounding an agent in external data**.

---

# 9. Why is this better than directly calling the API?

Imagine several companies want to build applications around OCI billing.

### Approach 1 — Direct API integration

Every application has to implement:

```text
Authentication
API requests
Parameters
Error handling
Response parsing
OCI-specific logic
```

For example:

```text
SaaS App A ─────→ OCI API
SaaS App B ─────→ OCI API
Internal App ────→ OCI API
AI Agent ────────→ OCI API
```

Lots of separate integrations.

---

# 10. MCP approach

Oracle provides the MCP server:

```text
                    ┌── SaaS App
                    │
                    ├── AI Agent
OCI MCP Server ─────┼── Internal App
                    │
                    └── Other MCP Host
```

Each application communicates with the standard MCP interface.

The MCP server handles:

```text
MCP → OCI API
```

This is the **standardized interface** idea.

---

# 11. Why does the demo create a CSV?

The application produces the result in two ways.

### Output 1 — Terminal

The data is printed to the console.

### Output 2 — CSV

The application creates a CSV file.

Why?

Because the instructor wants to compare the MCP result against the actual OCI Console.

The CSV makes it easier to inspect:

```text
Date
Service
Cost
Total
```

and compare the values.

---

# 12. Why compare against OCI Console?

This is actually a very useful testing technique.

The instructor wants to establish:

> "Did the MCP server actually return the correct billing data?"

So there are two sources:

### Source A

MCP:

```text
Agent
 ↓
MCP Server
 ↓
OCI Usage API
 ↓
CSV
```

### Source B

OCI Console:

```text
OCI Console
 ↓
Cost Analysis
```

Then compare them.

---

# 13. The test

The demo asks for approximately:

```text
Last 30 days
```

with:

```text
Daily breakdown
By service
```

The MCP output produces values such as:

```text
Block Storage
Database
VMware
...
```

and a total.

The instructor then opens the OCI Console and runs the same Cost Analysis query.

---

# 14. Why is matching "to the cent" important?

Suppose the MCP result says:

```text
Total = $6,200.17
```

and the OCI Console says:

```text
Total = $6,200.17
```

Then we have evidence that the MCP server is retrieving the same underlying billing information.

The demo also compares individual services.

For example:

```text
Block Storage ≈ $1,300
Database      ≈ $1,400
VMware        ≈ $1,951
```

and the totals match the console.

This is essentially a **validation test**.

---

# 15. The agent code

The demo points out that the important part of the code is relatively small.

Conceptually:

```python
client = MCPClient(
    server="oracle.oci-usage-mcp-server"
)
```

Then:

```python
agent = create_agent(
    model=model,
    tools=tools
)
```

Then the question:

```python
question = """
Show me the cost for last 30 days
as a daily breakdown by service.
"""
```

And:

```python
result = agent.invoke(question)
```

The exact APIs can vary by library/version, but the architecture is the important part.

---

# 16. The MCP server is spawned as a subprocess

This is a key detail from the demo.

The client doesn't necessarily connect to some remote MCP server over HTTP.

Instead, it can start the Oracle MCP server locally.

Conceptually:

```text
Your Python program
        │
        │ spawn
        ↓
Oracle MCP Server process
```

Then:

```text
Your Python program
        ↕
      stdio
        ↕
Oracle MCP Server
```

---

# 17. Why is it still called Oracle's MCP server?

Because Oracle created and published the server software.

You are simply running that software locally.

Think about a Python package.

If you install a package created by another company:

```bash
pip install some-package
```

the package can run on your machine even though **you didn't write it**.

Same basic idea here.

```text
Oracle-created MCP server
        ↓
download/run locally
        ↓
your machine
```

---

# 18. Then where does the internet connection happen?

This is the critical architecture detail:

```text
YOUR MACHINE
──────────────────────────────

Your Agent
    │
    │ stdio
    ↓
Oracle MCP Server
    │
    │ HTTPS
    ↓

──────────────────────────────
        INTERNET

    ↓

OCI Cloud
    ↓
OCI Usage API
```

So your agent doesn't directly send an HTTPS request to OCI.

The **MCP server process** does that.

---

# 19. Why use MCP instead of directly calling OCI?

The lesson's argument is about standardization.

Without MCP:

```text
AI Application
       ↓
OCI-specific API integration
```

With MCP:

```text
AI Application
       ↓
Standard MCP interface
       ↓
Oracle MCP Server
       ↓
OCI API
```

Now another MCP-compatible AI application can potentially use the same server.

---

# 20. This is the "define once, use everywhere" idea

Oracle creates:

```text
OCI Usage MCP Server
```

Then different hosts can potentially use it:

```text
                    ┌── LangChain
                    │
OCI Usage MCP ──────┼── Codex
Server              │
                    ├── Claude
                    │
                    ├── Cursor
                    │
                    └── Custom Agent
```

The underlying OCI integration doesn't need to be rewritten separately inside every AI application.

---

# 21. Where does the LLM add value?

Getting raw billing data is only one part.

Once the agent has the data, the LLM can analyze it.

For example:

```text
User:
"Show me my OCI costs for the last 30 days."
```

Tool:

```text
get_summarized_usage()
```

returns:

```text
Date | Service | Cost
...
```

The LLM can then explain:

```text
Your largest cost categories were X, Y, and Z.
There was a noticeable decrease after a certain date.
```

The important separation is:

```text
MCP
 ↓
gets reliable external data

LLM
 ↓
interprets/explains the data
```

---

# 22. This is a very common agent architecture

You can generalize this beyond OCI.

Imagine:

### GitHub MCP server

```text
User
 ↓
Agent
 ↓
GitHub MCP Server
 ↓
GitHub API
```

### Slack MCP server

```text
User
 ↓
Agent
 ↓
Slack MCP Server
 ↓
Slack API
```

### Database MCP server

```text
User
 ↓
Agent
 ↓
Database MCP Server
 ↓
Database
```

### OCI MCP server

```text
User
 ↓
Agent
 ↓
OCI MCP Server
 ↓
OCI API
```

Same pattern.

---

# 23. The big distinction: MCP vs API

This is worth remembering.

An **API** exposes functionality to software.

An **MCP server** exposes tools/resources/prompts through the MCP standard.

For this example:

```text
OCI API
   ↓
OCI-specific interface
```

while:

```text
OCI MCP Server
   ↓
Standard MCP interface
```

The MCP server can therefore act as an adapter between an existing API and AI applications.

---

# 24. What happens if the MCP server didn't exist?

Suppose you want your AI agent to answer:

> "How much did our OCI services cost last month?"

Without the MCP server, you might need to:

```text
1. Learn OCI API
2. Implement authentication
3. Build HTTP requests
4. Handle OCI parameters
5. Parse responses
6. Handle errors
7. Give the data to the LLM
```

With the MCP server:

```text
1. Connect to MCP server
2. Discover tools
3. Agent calls get_summarized_usage
4. Receive data
5. Give data to LLM
```

The vendor handles the OCI-specific integration.

---

# 25. One subtle but important point

MCP **doesn't magically give the LLM access to OCI**.

There are still multiple components:

```text
LLM
 ↓
Agent
 ↓
MCP Client
 ↓
MCP Server
 ↓
OCI API
```

Every layer has a responsibility.

### LLM

Understands the user request and decides which tool to use.

### Agent

Runs the reasoning/tool loop.

### MCP Client

Communicates with the MCP server.

### MCP Server

Exposes the standardized tools and translates the request to the underlying service.

### OCI API

Actually provides the OCI usage data.

---

# 26. Full execution trace

Let's trace the demo from beginning to end.

### Step 1 — User asks

```text
"Show me the cost for the last 30 days
as a daily breakdown by service."
```

### Step 2 — Agent receives question

```text
LangChain Agent
```

### Step 3 — Agent has discovered:

```text
get_summarized_usage
```

### Step 4 — LLM decides

```text
I need to call get_summarized_usage.
```

### Step 5 — MCP client sends request

```text
tools/call
```

with appropriate arguments.

### Step 6 — Oracle MCP server receives it

```text
get_summarized_usage(...)
```

### Step 7 — Oracle MCP server calls

```text
OCI Usage REST API
```

over HTTPS.

### Step 8 — OCI returns usage data.

### Step 9 — MCP server converts/returns the result through MCP.

### Step 10 — MCP client receives it.

### Step 11 — Agent gives the result back to the LLM.

### Step 12 — LLM interprets the data.

### Step 13 — Application prints the result and creates CSV.

Complete:

```text
USER
 ↓
LANGCHAIN AGENT
 ↓
LLM
 ↓
MCP CLIENT
 ↓
stdio / JSON-RPC
 ↓
ORACLE OCI MCP SERVER
 ↓
HTTPS
 ↓
OCI USAGE API
 ↓
OCI DATA
 ↑
ORACLE OCI MCP SERVER
 ↑
MCP CLIENT
 ↑
AGENT
 ↑
LLM
 ↑
USER
```

---

# 27. What the demo proves

The demo isn't merely showing:

> "MCP can call a tool."

The earlier math demo already showed that.

This demo proves something more important:

> **An AI application can consume a real MCP server created by a third-party provider without implementing the underlying service integration itself.**

That's the real-world value.

---

# 28. Math MCP vs Real OCI MCP

|             | Math MCP                  | OCI Usage MCP                         |
| ----------- | ------------------------- | ------------------------------------- |
| Server      | We wrote it               | Oracle provides it                    |
| Client      | We wrote it               | We write/use it                       |
| Tool        | Math functions            | OCI usage                             |
| Backend     | Python function           | OCI REST API                          |
| Debugging   | We can inspect both sides | We primarily inspect protocol/results |
| Reusability | Demonstration             | Real-world integration                |
| Main lesson | How MCP works             | Why MCP is useful                     |

---

# 29. The 5 things I want you to remember

### 1. OCI

**Oracle Cloud Infrastructure**

```text
Oracle's cloud platform
```

### 2. OCI Usage API

Provides OCI usage/cost information.

### 3. OCI Usage MCP Server

Oracle's MCP wrapper around that functionality.

```text
MCP Server
    ↓
OCI Usage API
```

### 4. Your application

Doesn't directly call OCI.

```text
Your Agent
    ↓
MCP Client
    ↓
OCI MCP Server
```

### 5. MCP's real-world value

```text
Vendor builds integration once
             ↓
        MCP Server
             ↓
Many AI applications can use it
```

---

# 30. The simplest mental model

Think of the OCI MCP server as a **translator**.

Your AI application speaks:

```text
MCP
```

Oracle's backend speaks:

```text
OCI API
```

The MCP server sits between them:

```text
       AI WORLD
          │
          │ MCP
          ↓
┌─────────────────────┐
│ OCI MCP Server      │
│                     │
│ "Translator"        │
└──────────┬──────────┘
           │
           │ OCI API / HTTPS
           ↓
       OCI WORLD
```

That's why the MCP server is so useful.

**Your agent doesn't need to learn every vendor's API. It can interact through the standardized MCP interface.**
