# MCP — Model Context Protocol

> **Goal:** Understand how MCP changes an AI agent architecture by separating the agent from the tools it uses.

---

# 1. What Is MCP?

**MCP = Model Context Protocol**

MCP provides a standardized way for an AI application to connect to external **tools and context**.

The key idea is:

> **MCP creates a standardized connection between an AI application and external tools/context.**

Instead of putting every tool directly inside the agent application, MCP allows tools to be provided by an external **MCP server**.

---

# 2. Why Do We Need MCP?

Consider a simple math agent.

The user asks:

```text
15 × 8 ÷ 3
```

The agent needs to perform multiple tool calls:

```text
multiply
   ↓
divide
```

Without MCP, the tools can be implemented directly inside the same Python application as the agent.

With MCP, the tools can live on an external MCP server.

This creates a separation between:

```text
Agent / AI Application
```

and:

```text
Tools
```

---

# 3. Before MCP

Without MCP, the architecture looks roughly like:

```text
User
  ↓
Agent
  ↓
LLM
  ↓
Tools defined in the same application
  ├── multiply()
  └── divide()
```

The Python application contains both:

```text
Agent / Client Logic
+
Tool Implementations
```

The agent can directly access the Python functions.

---

# 4. Architecture Without MCP

A more detailed view:

```text
Agent Application
│
├── LLM
├── Agent Loop
├── multiply()
├── divide()
└── Tool Execution
```

Everything is tightly connected inside the same application.

For example:

```text
User
 ↓
Agent
 ↓
LLM
 ↓
multiply()
 ↓
divide()
 ↓
Final Answer
```

The tool implementations are part of the agent application itself.

---

# 5. After MCP

MCP separates the agent from the tools.

The architecture becomes:

```text
User
  ↓
Agent / MCP Client
  ↓
LLM
  ↓
MCP Client
  ↓
MCP Server
  ├── multiply
  └── divide
```

The important change is:

```text
Agent
   │
   │ MCP
   ↓
MCP Server
   │
   ├── multiply()
   └── divide()
```

The math tools now live on the **MCP server** rather than directly inside the agent application.

---

# 6. Architecture With MCP

A more complete view:

```text
Agent Application
│
├── LLM
├── Agent Loop
└── MCP Client
        │
        │ MCP
        ↓
   MCP Server
   │
   ├── multiply()
   └── divide()
```

The agent no longer needs to contain the actual tool implementations.

Instead, it communicates with the MCP server.

---

# 7. The Four Important MCP Concepts

The main concepts introduced in this module are:

```text
1. Host
2. Client
3. Server
4. Primitives
```

These concepts describe how an AI application interacts with MCP servers and the capabilities they provide.

---

# 8. What Is the Host?

The **host** is the AI application that the user interacts with.

Simple mental model:

```text
Host
=
The application containing/using the AI agent
```

Examples can include:

```text
AI assistant
IDE
Desktop AI application
```

The host is the application in which the AI interaction takes place.

---

# 9. What Is the MCP Client?

The **MCP client** is the component that connects the host/agent to an MCP server.

Architecture:

```text
Host
  ↓
MCP Client
  ↓
MCP Server
```

The client handles communication between the AI application and the MCP server.

A useful mental model:

```text
Host
=
AI application

MCP Client
=
Connection component

MCP Server
=
Provider of capabilities
```

---

# 10. What Is an MCP Server?

An **MCP server** provides capabilities to an MCP client.

For example, a math MCP server could provide:

```text
Math MCP Server
      ↓
 ┌───────────┐
 │ multiply  │
 │ divide    │
 │ add       │
 └───────────┘
```

The server owns the actual tool implementations.

For the math-agent example:

```text
MCP Server
│
├── multiply()
├── divide()
└── add()
```

The agent can access these capabilities through the MCP client.

---

# 11. What Are MCP Primitives?

MCP servers expose capabilities through important primitives.

The three primitives introduced here are:

```text
Tools
Resources
Prompts
```

They represent different types of capabilities that an MCP server can expose.

The important point for now is:

```text
MCP Server
     ↓
  Primitives
     ↓
Tools / Resources / Prompts
```

---

# 12. Tools

**Tools** represent capabilities that an AI application can use to perform actions.

For example:

```text
multiply()
divide()
add()
```

In the math-agent example:

```text
User
 ↓
Agent
 ↓
MCP Client
 ↓
MCP Server
 ↓
multiply()
 ↓
divide()
 ↓
Result
```

The tool implementations live on the MCP server.

---

# 13. Resources

**Resources** are another MCP primitive used to provide context or data to an AI application.

The three important primitives introduced in this module are:

```text
Tools
Resources
Prompts
```

The key distinction is that MCP does not only provide tools; it also provides standardized ways to expose other types of capabilities and context.

---

# 14. Prompts

**Prompts** are another MCP primitive.

They allow MCP servers to expose reusable prompt-related capabilities to AI applications.

Therefore, the basic MCP primitive model is:

```text
MCP Primitives
│
├── Tools
├── Resources
└── Prompts
```

---

# 15. The Production Idea

One of the most important ideas in MCP is:

> **In production, the server is often published by someone else. You only write the client.**

For learning, we may build the complete system ourselves:

```text
Your Agent
    +
Your MCP Client
    +
Your MCP Server
```

But in a real production environment, it can look like:

```text
Your Agent
    +
Your MCP Client
    ↓
Someone else's MCP Server
    ↓
Their tools / data
```

This means the agent developer does not necessarily implement the MCP server.

Instead, the developer connects the AI application to an existing MCP server.

---

# 16. Production Architecture

Conceptually:

```text
Your AI Agent
      ↓
MCP Client
      ↓
Company's MCP Server
      ↓
Company Tools / Databases / APIs
```

For example:

```text
AI Agent
   ↓
MCP Client
   ↓
External MCP Server
   ↓
Tools
   ├── Database
   ├── APIs
   ├── Search
   └── Business systems
```

The exact tools depend on what capabilities the server exposes.

---

# 17. Learning vs Production

### Learning

You may build everything:

```text
Your Agent
    +
Your MCP Client
    +
Your MCP Server
```

This helps you understand how the complete architecture works.

### Production

A more common architecture is:

```text
Your Agent
    +
Your MCP Client
    ↓
Existing MCP Server
    ↓
External Tools / Data
```

The MCP server may be developed and maintained by another team, company, or service provider.

---

# 18. Why This Separation Matters

Without MCP:

```text
Agent Application
│
├── LLM
├── Agent Loop
├── multiply()
├── divide()
└── Tool Execution
```

The agent application contains the tool implementations.

With MCP:

```text
Agent Application
│
├── LLM
├── Agent Loop
└── MCP Client
        │
        │ MCP
        ↓
   MCP Server
   │
   ├── multiply()
   └── divide()
```

Now:

```text
Agent Logic
     ≠
Tool Implementation
```

They are separated.

This is the major architectural change demonstrated by MCP.

---

# 19. Same Math Agent — Before vs After MCP

The course uses the same math-agent example so that the architectural difference is easy to understand.

### User request

```text
15 × 8 ÷ 3
```

The agent needs:

```text
multiply()
```

followed by:

```text
divide()
```

---

## Before MCP

```text
User
 ↓
Agent
 ↓
LLM
 ↓
multiply()
 ↓
Result
 ↓
divide()
 ↓
Result
 ↓
Final Answer
```

The functions are directly available inside the application.

---

## After MCP

```text
User
 ↓
Agent
 ↓
LLM
 ↓
MCP Client
 ↓
MCP Server
 ↓
multiply()
 ↓
Result
 ↓
MCP Client
 ↓
MCP Server
 ↓
divide()
 ↓
Result
 ↓
Final Answer
```

The agent communicates with the external server to use the tools.

---

# 20. MCP Changes the Agent Architecture

The most important architectural difference is:

### Without MCP

```text
Agent
│
├── LLM
├── Agent Loop
├── Tools
└── Tool Execution
```

### With MCP

```text
Agent
│
├── LLM
├── Agent Loop
└── MCP Client
        │
        │ MCP
        ↓
   MCP Server
        │
        └── Tools
```

So MCP introduces a clear boundary:

```text
AI Application
       │
       │ MCP
       ↓
External Capabilities
```

---

# 21. What the MCP Client Does

The MCP client acts as the communication layer between the AI application and the MCP server.

Conceptually:

```text
Agent
  ↓
MCP Client
  ↓
MCP Server
```

The client allows the agent application to communicate with capabilities provided by the server.

The client does not need to contain the actual implementation of:

```text
multiply()
divide()
```

Those implementations can remain on the server.

---

# 22. What the MCP Server Does

The server provides the capabilities.

For the math example:

```text
MCP Server
│
├── multiply()
├── divide()
└── add()
```

The server owns these implementations.

The agent accesses them through MCP.

Therefore:

```text
Client
=
Connects to capabilities

Server
=
Provides capabilities
```

---

# 23. MCP Mental Model

A simple mental model:

```text
Host
 ↓
MCP Client
 ↓
MCP Server
 ↓
Capabilities
```

Where:

```text
Host
→ AI application

Client
→ Connects to server

Server
→ Provides capabilities

Primitives
→ Tools / Resources / Prompts
```

---

# 24. MCP Is Not the Agent

An important distinction:

```text
MCP ≠ AI Agent
```

MCP is a protocol/interface for connecting AI applications with external capabilities.

An agent can use MCP as part of its architecture:

```text
AI Agent
│
├── LLM
├── Agent Loop
└── MCP Client
        ↓
    MCP Server
        ↓
      Tools
```

So:

```text
Agent
=
System architecture

MCP
=
Standardized connection/interface
```

---

# 25. MCP and Tool Separation

The key architectural principle is:

```text
Agent Logic
      │
      │ MCP
      ↓
Tool Provider
```

Instead of:

```text
Agent Logic
      +
Tool Implementations
```

This separation can allow different AI applications to connect to MCP servers that provide useful capabilities.

---

# 26. The Core MCP Flow

The entire concept can be summarized as:

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
Tool / Resource / Prompt
  ↓
Result / Context
  ↓
MCP Client
  ↓
Agent / LLM
  ↓
Final Response
```

For a multi-step math task:

```text
15 × 8 ÷ 3
      ↓
   multiply
      ↓
    120
      ↓
    divide
      ↓
     40
```

The agent can use the MCP-provided tools to perform the required operations.

---

# 27. Most Important Questions

## What does MCP stand for?

> MCP stands for **Model Context Protocol**.

---

## What problem does MCP solve?

> MCP provides a standardized way for AI applications to connect to external tools and context.

---

## What is the main architectural change introduced by MCP?

> MCP separates the AI agent/application from the implementations of the tools it uses by connecting them through an MCP client and server.

---

## What is an MCP host?

> The host is the AI application that the user interacts with and that uses the AI agent.

---

## What is an MCP client?

> The MCP client is the component that connects the host or agent to an MCP server and handles communication with it.

---

## What is an MCP server?

> An MCP server provides capabilities such as tools, resources, and prompts to an MCP client.

---

## What are MCP primitives?

```text
Tools
Resources
Prompts
```

They are the main types of capabilities introduced in this module.

---

## Does the MCP server have to be written by the agent developer?

> No. In production, an MCP server may be created and published by another team or organization, while the agent developer primarily writes the client that connects to it.

---

## Is MCP an AI model?

> No. MCP is a protocol for standardized communication between AI applications and external capabilities.

---

## Is MCP an AI agent?

> No. An agent is an application/system architecture. MCP can be one part of that architecture for connecting the agent to external capabilities.

---

# 28. Quick Revision

```text
MCP
=
Model Context Protocol
```

```text
Main Purpose
=
Standardized connection between
AI applications and external capabilities
```

```text
MCP Architecture

Host
 ↓
MCP Client
 ↓
MCP Server
 ↓
Tools / Resources / Prompts
```

```text
Before MCP

Agent
 ├── LLM
 ├── Agent Loop
 └── Tools
```

```text
After MCP

Agent
 ├── LLM
 ├── Agent Loop
 └── MCP Client
        ↓
    MCP Server
        ↓
      Tools
```

```text
Host
=
AI application
```

```text
Client
=
Communication component
```

```text
Server
=
Capability provider
```

```text
Primitives
=
Tools + Resources + Prompts
```

---

# 29. Final Mental Model

The most important picture to remember is:

```text
                 USER
                   │
                   ▼
                 HOST
            AI APPLICATION
                   │
                   ▼
              AI AGENT
                   │
                   ▼
                  LLM
                   │
                   ▼
              MCP CLIENT
                   │
                   │
                   │ MCP
                   ▼
              MCP SERVER
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
        TOOLS   RESOURCES  PROMPTS
          │
          ▼
     External Systems
```

The key architectural change is:

```text
BEFORE MCP

Agent
 │
 ├── LLM
 ├── Agent Loop
 ├── multiply()
 └── divide()
```

becomes:

```text
AFTER MCP

Agent
 │
 ├── LLM
 ├── Agent Loop
 └── MCP Client
          │
          │ MCP
          ▼
     MCP Server
       │
       ├── multiply()
       └── divide()
```

> **MCP = a standardized way for an AI application to discover and use capabilities provided by an external server.**
