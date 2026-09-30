# OpenAI Agent Stack

> **Module:** OpenAI Responses API + Agents SDK
> **Goal:** Build AI Agents using OpenAI's native agent stack

---

# 1. What Is an AI Agent?

An AI Agent can be understood as:

```text
AI Agent = LLM + Tools + Loop
```

### Components

## LLM — Brain 🧠

The LLM:

* Understands user input
* Reasons about the task
* Plans next steps
* Chooses tools

Example:

```text
User:
Find cheapest flight Austin → Zurich
```

The LLM determines:

```text
I need a flight search tool.
```

---

## Tools — Hands 🛠️

Tools allow an agent to interact with external systems.

Examples:

* Web Search
* File Search
* Calculator
* APIs
* Database
* Booking Systems
* Code Interpreter

Example:

```text
search_flight()
book_flight()
```

---

## Loop — Nervous System 🔄

The loop keeps the agent working until the task is complete.

```text
Reason
  ↓
Act
  ↓
Observe
  ↓
Reason Again
  ↓
Stop
```

This is the basic **ReAct-style loop**.

---

# 2. Agent Properties

## Goal-Directed

The agent works toward an objective.

```text
Book cheapest flight
```

---

## Autonomous

The agent can decide its next action.

```text
Search Flight
      ↓
Compare Prices
      ↓
Book Ticket
```

---

## Tool Usage

The agent can interact with external systems.

```text
LLM
 ↓
Tool
 ↓
API
```

---

## Iterative

The agent can improve its result step-by-step.

```text
Search
  ↓
Observe
  ↓
Search Again
  ↓
Answer
```

---

# 3. OpenAI Agent Stack

The OpenAI Agent Stack can be viewed as layers:

```text
┌────────────────────────────┐
│      Your Application      │
│    UI + Business Logic     │
└─────────────┬──────────────┘
              │
┌─────────────▼──────────────┐
│        Agents SDK          │
│                            │
│ Multi-Agent                │
│ Guardrails                 │
│ Handoffs                   │
│ Tracing                    │
└─────────────┬──────────────┘
              │
┌─────────────▼──────────────┐
│       Responses API        │
│                            │
│ Stateful                   │
│ Tools                      │
│ Function Calling           │
│ Web Search                 │
│ File Search                │
│ Code Interpreter            │
└─────────────┬──────────────┘
              │
┌─────────────▼──────────────┐
│       OpenAI Models        │
│                            │
│ GPT-5.5                    │
│ GPT-5                      │
│ GPT-4.1                    │
└────────────────────────────┘
```

### Layer relationship

```text
Your Application
       ↓
Agents SDK
       ↓
Responses API
       ↓
OpenAI Models
```

---

# 4. OpenAI Models

The bottom layer contains the models.

```text
GPT Models
```

Examples from this module:

```text
GPT-5
GPT-5.5
GPT-4.1
```

## Reasoning Models

Examples:

```text
GPT-5
GPT-5.5
```

Used for tasks such as:

* Complex reasoning
* Math
* Coding
* Planning
* Agents
* Multi-step tasks

---

## Fast Models

Example:

```text
GPT-4.1
```

Focus:

* Faster responses
* Lower latency
* Simpler tasks

---

# 5. Responses API

The **Responses API** is the lower-level OpenAI API layer used for building agentic applications.

It provides capabilities such as:

* Stateful interactions
* Function calling
* Built-in tools
* Web Search
* File Search
* Code Interpreter

Basic conceptual usage:

```python
response = client.responses.create(...)
```

---

# 6. Stateful Responses

The Responses API can maintain state across interactions.

Example:

```text
User:
Hello

User:
What did I ask before?
```

The model can use the conversation state to understand the previous interaction.

Mental model:

```text
Conversation
     ↓
Responses API
     ↓
Stateful interaction
```

---

# 7. Function Calling

Function calling allows the model to request the execution of a tool.

Conceptually:

```text
LLM
 ↓
Tool Call
 ↓
Tool Executes
 ↓
Tool Result
 ↓
LLM
 ↓
Final Answer
```

Example:

```text
LLM
 ↓
call search_tool()
 ↓
Get Search Result
 ↓
Generate Answer
```

The model decides **when a tool is needed**, while the application/tool system handles the actual execution.

---

# 8. Built-in Tools

The Responses API provides built-in tools such as:

```text
Web Search
File Search
Code Interpreter
```

Conceptually:

```text
Responses API
      │
      ├── Web Search
      ├── File Search
      └── Code Interpreter
```

This allows an agentic application to use capabilities without implementing every capability from scratch.

---

# 9. Agents SDK

The **Agents SDK** is the higher-level framework layer.

Conceptually:

```text
Agents SDK
      ↓
Responses API
      ↓
OpenAI Models
```

The SDK provides higher-level agent capabilities such as:

* Agents
* Multi-Agent Systems
* Guardrails
* Handoffs
* Tracing

---

# 10. Agents

The SDK allows you to define specialized agents.

Examples:

```text
Math Agent
Travel Agent
Research Agent
```

Conceptually:

```text
User
 ↓
Agent
 ↓
Model
 ↓
Tools
```

---

# 11. Multi-Agent Systems

Multiple specialized agents can work together.

```text
             Main Agent
                 │
        ┌────────┼────────┐
        ↓        ↓        ↓
   Research    Math     Travel
    Agent      Agent     Agent
```

Each agent can specialize in a particular responsibility.

---

# 12. Guardrails

**Guardrails** are safety or validation mechanisms around agent behavior.

Conceptually:

```text
User Input
    ↓
Guardrail
    ↓
Agent
    ↓
Tool
    ↓
Result
```

They can be used to check whether inputs or outputs meet defined requirements.

---

# 13. Handoffs

A **handoff** allows one agent to pass work to another specialized agent.

Example:

```text
User
 ↓
Main Agent
 ↓
"Travel question"
 ↓
Travel Agent
 ↓
Answer
```

Another example:

```text
Main Agent
    ↓
Research Agent
    ↓
Research Result
    ↓
Main Agent
```

---

# 14. Tracing

**Tracing** helps inspect what happened during agent execution.

Conceptually:

```text
User
 ↓
Agent
 ↓
LLM
 ↓
Tool
 ↓
Result
 ↓
Final Answer
```

Tracing lets developers inspect the execution flow for debugging and understanding agent behavior.

---

# 15. Overall Architecture

```text
User
  ↓
Application
  ↓
Agents SDK
  ↓
Responses API
  ↓
Model
  ↓
Tools
  ↓
External Systems
```

Expanded:

```text
                         USER
                           │
                           ↓
                  ┌─────────────────┐
                  │  Application    │
                  └────────┬────────┘
                           │
                           ↓
                  ┌─────────────────┐
                  │   Agents SDK    │
                  │                 │
                  │ Agent           │
                  │ Handoffs        │
                  │ Guardrails      │
                  │ Tracing         │
                  └────────┬────────┘
                           │
                           ↓
                  ┌─────────────────┐
                  │ Responses API   │
                  │                 │
                  │ Tools           │
                  │ Function Calls  │
                  │ State           │
                  └────────┬────────┘
                           │
                           ↓
                  ┌─────────────────┐
                  │ OpenAI Model    │
                  └────────┬────────┘
                           │
                           ↓
                    External Tools
```

---

# 16. Responses API vs Agents SDK

This is one of the most important distinctions.

## Responses API

The Responses API gives you lower-level control.

You may need to build/manage:

```text
Loop
Tools
Memory / State
Retries
Orchestration
```

Conceptually:

```text
Reason
  ↓
Tool
  ↓
Observe
  ↓
Repeat
```

You have more direct control over the workflow.

---

## Agents SDK

The Agents SDK provides higher-level agent functionality.

It provides capabilities such as:

```text
Agent
Tool Handling
Multi-Agent
Guardrails
Handoffs
Tracing
```

The SDK handles more of the agent infrastructure for you.

---

# 17. Simple Mental Model

## Responses API

Think:

```text
Building the engine yourself
```

You have more control over the underlying workflow.

```text
You
 ↓
Responses API
 ↓
Build your agent logic
```

---

## Agents SDK

Think:

```text
Driving a ready-made car
```

More agent infrastructure is already provided.

```text
You
 ↓
Agents SDK
 ↓
Build your application/agent behavior
```

### Core idea

```text
Responses API
      ↓
More direct control

Agents SDK
      ↓
Higher-level agent framework
```

---

# 18. Flight Booking Example

User:

```text
Find cheapest flight Austin → Zurich
and book it.
```

---

## Using Responses API

Your application may need to manage logic such as:

```text
Search Tool
     ↓
Parse Result
     ↓
Compare Prices
     ↓
Booking Tool
     ↓
Retry Logic
     ↓
Error Handling
     ↓
Loop
```

The application controls more of the workflow.

---

## Using Agents SDK

The SDK provides higher-level agent infrastructure for handling things such as:

```text
Agent
 ↓
Reasoning
 ↓
Tool Calling
 ↓
Loop
 ↓
Handoffs / Guardrails / Tracing
```

Your application focuses more on defining:

```text
Agent
Tools
Instructions
Business Logic
```

---

# 19. OpenAI Agent Stack vs LangChain vs MCP

These technologies operate at different conceptual layers.

## LangChain

LangChain can provide the agent/orchestration layer:

```text
LLM
 ↓
Tools
 ↓
Agent Loop
```

---

## MCP

MCP provides a standardized tool-connection protocol:

```text
Agent
 ↓
MCP Client
 ↓
MCP Server
 ↓
External Systems
```

---

## OpenAI Agents SDK

The Agents SDK provides a higher-level agent framework around OpenAI's stack:

```text
Agent
 ↓
Responses API
 ↓
Tools
 ↓
External Systems
```

---

# 20. Combining Agents SDK and MCP

MCP does not have to be an alternative to an agent framework.

An agent framework can use MCP-provided tools.

Conceptually:

```text
User
  ↓
Agents SDK
  ↓
Agent
  ↓
MCP Client
  ↓
MCP Server
  ↓
External System
```

This means:

```text
Agents SDK
     ↓
Agent / Orchestration

MCP
     ↓
Standardized Tool Connection
```

---

# 21. Future Architecture

A larger architecture can combine built-in tools, MCP servers, APIs, databases, and external systems.

```text
User
  ↓
Application
  ↓
Agents SDK
  ↓
Responses API
  ↓
OpenAI Model
  ↓
Tools
  ├── Web Search
  ├── File Search
  ├── Code Interpreter
  ├── MCP Servers
  ├── APIs
  ├── Database
  └── External Systems
```

This shows that MCP can be **one source of tools** inside a larger agent architecture.

---

# 22. Tool Layer Mental Model

Think of tools as the agent's "hands":

```text
                  Agent
                    │
                    ↓
                  Tools
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
   Web Search   File Search   APIs
        │           │           │
        ↓           ↓           ↓
      Web         Files      Services
```

Tools allow the model to interact with systems beyond its internal knowledge.

---

# 23. Agent Stack Mental Model

```text
┌──────────────────────────────┐
│      Your Application        │
│                              │
│ UI + Business Logic          │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│        Agents SDK            │
│                              │
│ Agents                       │
│ Multi-Agent                  │
│ Handoffs                     │
│ Guardrails                   │
│ Tracing                      │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│       Responses API          │
│                              │
│ State                        │
│ Function Calling             │
│ Built-in Tools               │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│        OpenAI Models         │
│                              │
│ Reasoning / Generation       │
└──────────────────────────────┘
```

---

# 24. Key Relationships

Remember these relationships:

```text
Agents SDK
     ↓
uses
     ↓
Responses API
     ↓
uses
     ↓
OpenAI Models
```

And:

```text
Agents SDK
     ↓
can work with
     ↓
Tools
```

Tools can include:

```text
Web Search
File Search
Code Interpreter
MCP Servers
APIs
Databases
External Systems
```

---

# 25. Before vs After Adding MCP

### Without MCP

```text
User
 ↓
Agents SDK
 ↓
Responses API
 ↓
Model
 ↓
Application Tools
```

### With MCP

```text
User
 ↓
Agents SDK
 ↓
Responses API
 ↓
Model
 ↓
MCP Client
 ↓
MCP Server
 ↓
External System
```

The agent framework remains.

MCP changes **how external tools can be connected**.

---

# 26. Responses API — Core Mental Model

```text
User
 ↓
Responses API
 ↓
Model
 ↓
Tool Call
 ↓
Tool Result
 ↓
Model
 ↓
Response
```

The application can control the overall workflow.

---

# 27. Agents SDK — Core Mental Model

```text
User
 ↓
Agent
 ↓
Model
 ↓
Tool
 ↓
Result
 ↓
Agent
 ↓
Final Answer
```

The SDK provides higher-level infrastructure around the agent workflow.

---

# 28. Decision Guide

Use the **Responses API** when you want more direct control over the underlying workflow and tool interactions.

```text
Need more direct control?
          │
         YES
          ↓
   Responses API
```

Use the **Agents SDK** when you want higher-level agent functionality such as:

```text
Multi-Agent
Guardrails
Handoffs
Tracing
Orchestration
```

Conceptually:

```text
Need higher-level agent framework?
          │
         YES
          ↓
      Agents SDK
```

---

# 29. Important Interview Questions

## What is an AI Agent?

> **An AI Agent is a system that combines an LLM with tools and an execution loop so it can reason about a goal, take actions, observe results, and continue until the task is completed.**

---

## What is the Responses API?

> **The Responses API is OpenAI's API layer for building agentic applications, providing capabilities such as stateful interactions, function calling, and built-in tools.**

---

## What is the Agents SDK?

> **The Agents SDK is a higher-level framework for building agents with capabilities such as multi-agent workflows, guardrails, handoffs, and tracing.**

---

## Does the Agents SDK replace the Responses API?

> **No. The Agents SDK is built on top of the Responses API and provides higher-level agent abstractions.**

---

## What is the difference between Responses API and Agents SDK?

> **The Responses API provides a lower-level foundation with more direct control, while the Agents SDK provides higher-level infrastructure for building and orchestrating agents.**

---

## Does MCP replace the Agents SDK?

> **No. MCP and the Agents SDK solve different problems. The Agents SDK provides agent orchestration, while MCP standardizes communication between AI applications and external tool providers.**

---

# 30. Key Takeaways

```text
✅ Agent = LLM + Tools + Loop

✅ Models provide reasoning and generation capabilities.

✅ Responses API provides a lower-level foundation for agentic applications.

✅ Function calling allows models to request tool execution.

✅ Built-in tools provide capabilities such as Web Search,
   File Search, and Code Interpreter.

✅ Agents SDK provides a higher-level agent framework.

✅ Agents SDK supports agents, multi-agent workflows,
   guardrails, handoffs, and tracing.

✅ Agents SDK is built on the Responses API.

✅ Tools give agents capabilities beyond the model itself.

✅ MCP provides a standardized way to connect agents
   to external tool providers.

✅ MCP can be used alongside an agent framework.

✅ Responses API → More direct control.

✅ Agents SDK → Higher-level agent infrastructure.
```

---

# 31. Final Mental Model

The entire OpenAI Agent Stack can be remembered as:

```text
                    USER
                      ↓
              YOUR APPLICATION
                      ↓
                AGENTS SDK
                      ↓
               RESPONSES API
                      ↓
                OPENAI MODEL
                      ↓
                   TOOLS
              ┌───────┼────────┐
              ↓       ↓        ↓
           Built-in   MCP     APIs
            Tools    Servers
              ↓       ↓        ↓
              └──── External Systems ────┘
```

### One-Line Summary

> **Models provide intelligence → Responses API provides the core agentic API layer → Agents SDK provides higher-level agent orchestration → Tools connect agents to the outside world → Your application turns everything into a useful product.**
