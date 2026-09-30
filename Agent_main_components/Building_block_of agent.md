# OCI Enterprise AI Agents — Building Blocks

## 1. Big Picture

OCI Enterprise AI Agents provides several building blocks for creating agentic applications.

The four major areas covered in this lesson are:

```text
┌───────────────────────────────────────────────┐
│ OCI Enterprise AI Agents                     │
│                                               │
│  1. Responses API       → Agent engine       │
│  2. Agent Tools         → Agent capabilities │
│  3. Memory              → Agent continuity   │
│  4. Lower-level APIs    → More control       │
└───────────────────────────────────────────────┘
```

### Simple mental model

> **Responses API = brain/engine**
>
> **Tools = hands**
>
> **Memory = notebook**
>
> **Lower-level APIs = building blocks for customization**

---

# 2. OCI Responses API

The **OCI Responses API** is presented in the course as the primary API for building agents.

It is:

* OpenAI-compatible
* Based on/conforms to the Open Responses specification
* Designed to support multi-step reasoning
* Designed to support tool calling

Instead of manually implementing every part of an agent loop, the Responses API provides an interface through which the model can reason and use tools.

---

# 3. What Does "Multi-Step" Mean?

Suppose a user asks:

> "Analyze this document, calculate the total, and compare it with our database."

The agent might need to perform:

```text
User request
     ↓
Read/search file
     ↓
Execute code
     ↓
Call business API
     ↓
Analyze results
     ↓
Final answer
```

The important point is that an agent may need **multiple tool interactions** before it can answer.

The Responses API supports this type of workflow.

---

# 4. Tool Calling

The model can use different types of tools.

The lesson mentions:

* Code Interpreter
* File Search
* Custom Functions
* MCP Servers

Conceptually:

```text
                    User
                     ↓
              Responses API
                     ↓
                  Model
                     ↓
       ┌─────────────┼──────────────┐
       ↓             ↓              ↓
   File Search   Code Interpreter   MCP
       ↓             ↓              ↓
    Documents      Python         External
                                   systems
```

The model decides when a tool is useful, and the agent system handles the tool execution.

---

# 5. Multi-Model Routing

The Responses API also supports **multi-model routing**.

This means an application can use different models for different tasks.

For example:

```text
Simple classification
        ↓
     Model A

Complex reasoning
        ↓
     Model B

Embedding/retrieval
        ↓
     Model C
```

The lesson mentions support for models from providers such as:

* OpenAI
* Grok
* Gemini
* Llama
* Cohere

### Why is this useful?

Different tasks have different requirements.

One model might be:

* cheaper
* faster
* better for a specific task

while another might provide stronger reasoning.

Therefore:

> **You don't necessarily need one model for everything.**

---

# 6. Responses API and State

The lesson also connects the Responses API with several forms of state and memory:

* Conversation state
* Long-term memory
* Context optimization/compaction

This means an agent can maintain useful context without your application having to manually reconstruct everything from scratch.

---

# 7. Agent Tools ⚙️

The core idea:

> **Tools give an agent the ability to do things beyond generating text.**

Without tools:

```text
User
 ↓
LLM
 ↓
Text
```

With tools:

```text
User
 ↓
Agent
 ↓
LLM
 ↓
Tool
 ↓
External system / computation / data
 ↓
Result
 ↓
LLM
 ↓
Answer
```

This is the same concept we learned earlier:

> **LLM = brain**
>
> **Tools = hands**

---

# 8. Four Built-in Tool Categories

The lesson identifies four important OCI agent tool categories:

1. File Search
2. Code Interpreter
3. Function Calling
4. MCP Calling

Memorize these four.

---

# 9. Tool 1 — File Search

### What does it do?

File Search allows an agent to retrieve relevant information from uploaded documents using semantic retrieval.

The files are associated with a **vector store**.

Conceptually:

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Store
    ↓
Semantic Search
    ↓
Relevant content
    ↓
LLM
```

### Example

Suppose you upload:

```text
company_policy.pdf
employee_handbook.pdf
refund_policy.pdf
```

User asks:

> "What is our refund policy?"

The agent can search the documents and retrieve relevant information.

---

# 10. File Search vs Normal Search

Normal keyword search might look for:

```text
"refund"
```

Semantic search can understand that:

```text
"Can I get my money back?"
```

may be related to:

```text
"refund policy"
```

even when the exact words differ.

This is why embeddings/vector stores are useful.

---

# 11. Tool 2 — Code Interpreter

**Code Interpreter** allows the agent to execute Python code in a sandboxed environment.

This is useful for:

* Data analysis
* Calculations
* Transformations
* Working with structured data
* Generating computational results

Example:

User:

> "Calculate the average revenue from this CSV and identify the highest month."

The agent can:

```text
CSV
 ↓
Code Interpreter
 ↓
Python
 ↓
Calculate statistics
 ↓
Results
 ↓
LLM
 ↓
Natural-language explanation
```

### Important

The code runs in a **sandbox**.

That means it is intended to be isolated from the main production environment.

---

# 12. Tool 3 — Function Calling

Function calling allows you to define your own functions that an agent can invoke.

For example:

```python
def get_order_status(order_id):
    ...
```

The function might:

* Query a database
* Call a business API
* Trigger a workflow
* Retrieve customer information

Conceptually:

```text
User
 ↓
LLM
 ↓
"Call get_order_status"
 ↓
Your function
 ↓
Database/API
 ↓
Result
 ↓
LLM
 ↓
Answer
```

### Important distinction

The LLM does **not** magically execute your Python function.

It produces a structured request such as:

```text
Tool: get_order_status
Argument:
order_id = "ORD-001"
```

The runtime/application executes the actual function.

This is the same architecture you learned with LangChain and the OpenAI Agents SDK.

---

# 13. Tool 4 — MCP Calling

MCP calling allows the agent to connect to **remote MCP servers**.

You already learned MCP:

```text
Agent
 ↓
MCP Client
 ↓
MCP Server
 ↓
External Tool/System
```

For example:

```text
OCI Agent
    ↓
MCP Server
    ↓
GitHub
```

or:

```text
OCI Agent
    ↓
MCP Server
    ↓
Database
```

or:

```text
OCI Agent
    ↓
MCP Server
    ↓
Business API
```

### Why MCP?

MCP provides a standardized way of exposing tools and capabilities to AI applications.

---

# 14. Four Tools — Easy Memory Trick

Remember:

> **Files → Code → Functions → MCP**

| Tool             | Main purpose                |
| ---------------- | --------------------------- |
| File Search      | Search documents            |
| Code Interpreter | Run Python/computation      |
| Function Calling | Your custom business logic  |
| MCP Calling      | Connect to remote MCP tools |

---

# 15. Memory 🧠

The lesson introduces **three types of memory**.

These solve different problems.

```text
Memory
├── Short-term → Conversations
├── Long-term → Persistent information
└── Context optimization → Compaction/summarization
```

---

# 16. Memory Type 1 — Conversations API

The **Conversations API** manages short-term, session-based conversation history.

Example:

```text
User:
"My name is Alex."

Agent:
"Nice to meet you, Alex."

User:
"What is my name?"

Agent:
"Your name is Alex."
```

The conversation history allows the agent to understand the previous interaction.

### Mental model

> **Short-term memory = notepad during a meeting**

It contains what has been discussed during the relevant conversation.

---

# 17. Short-Term Memory

Without conversation state:

```text
Request 1
 ↓
Model

Request 2
 ↓
Model
```

The second request may not know what happened in Request 1.

With conversation state:

```text
Request 1
 ↓
Conversation History
 ↓
Request 2
 ↓
Model sees relevant previous context
```

---

# 18. Memory Type 2 — Long-Term Memory

Long-term memory persists information across sessions.

For example:

### Session 1

```text
User:
"I prefer concise answers."
```

The information can potentially be stored as long-term memory.

### Session 2

Later:

```text
User:
"Explain RAG."
```

The system can use the stored preference when responding.

Other examples:

* User preferences
* Past decisions
* Accumulated knowledge
* Persistent facts relevant to the application

### Mental model

> **Long-term memory = personal journal**

It survives beyond one conversation/session.

---

# 19. Short-Term vs Long-Term Memory

|             | Short-Term                      | Long-Term                        |
| ----------- | ------------------------------- | -------------------------------- |
| API/concept | Conversations                   | Long-term memory                 |
| Lifetime    | Session/conversation            | Across sessions                  |
| Stores      | Conversation turns              | Persistent information           |
| Example     | "What did I say 2 minutes ago?" | "What preferences have I saved?" |
| Analogy     | Meeting notepad                 | Personal journal                 |

### Remember:

> **Conversation memory = what happened in this session.**
>
> **Long-term memory = what should remain useful later.**

---

# 20. Memory Type 3 — Context Compaction

There is another problem.

LLMs have a limited **context window**.

Imagine an extremely long conversation:

```text
Message 1
Message 2
Message 3
...
Message 500
Message 501
...
Message 1000
```

Sending the entire conversation forever can become inefficient or exceed the model's context capacity.

So the system can perform **context compaction**.

---

# 21. What Is Context Compaction?

Context compaction means summarizing a long conversation while preserving important information.

Example:

### Original

```text
3-hour meeting

1000s of words
+
many questions
+
decisions
+
details
```

### After compaction

```text
Key decisions:
- Use PostgreSQL
- Deploy in OCI
- Deadline: Friday
- Alice owns backend
- Bob owns frontend
```

The important information remains while unnecessary details are reduced.

---

# 22. Context Compaction Mental Model

Think:

> **Context compaction = summarizing a three-hour meeting into useful bullet points.**

It helps the agent remain useful as conversations become long.

---

# 23. Three Memory Concepts Together

```text
                    AGENT MEMORY
                         │
          ┌──────────────┼───────────────┐
          ↓              ↓               ↓
     Conversations   Long-Term      Context
          │           Memory        Compaction
          ↓              ↓               ↓
    Current session   Across       Reduce long
                      sessions      context
```

Easy memory trick:

> **Conversation remembers now.**
>
> **Long-term remembers later.**
>
> **Compaction remembers the important parts when context gets too large.**

---

# 24. Lower-Level APIs

The high-level Responses API and built-in tools won't cover every possible application.

For advanced use cases, OCI provides lower-level APIs.

The lesson highlights:

1. Vector Stores API
2. Files API
3. Containers API

Think of these as **more granular building blocks**.

---

# 25. Vector Stores API

The Vector Stores API is useful for managing vector-based retrieval.

Typical workflow:

```text
Document
   ↓
Upload
   ↓
Chunk
   ↓
Embed
   ↓
Vector Store
   ↓
Semantic Search
```

This can form the foundation of a custom RAG system.

---

# 26. Why Would You Use the Vector Stores API?

Suppose the built-in File Search doesn't provide enough control for your application.

You may want to control:

* How documents are processed
* How retrieval works
* How your RAG pipeline is structured
* How information is stored/retrieved

Then lower-level APIs give you more control.

### High-level approach

```text
File Search
   ↓
Easy retrieval
```

### Lower-level approach

```text
Your RAG pipeline
       ↓
Vector Store
       ↓
Your retrieval logic
```

---

# 27. Files API

The **Files API** handles file uploads and file management.

Conceptually:

```text
Your Application
      ↓
Files API
      ↓
Uploaded file
      ↓
Agent/tool can process it
```

Examples of files could include:

* PDFs
* CSVs
* Text documents
* Other supported data files

The exact supported file types/capabilities should be checked in the current OCI documentation.

---

# 28. Containers API

The **Containers API** allows custom containers to be run for specialized processing.

Think:

> "I need an isolated environment where my specialized processing can execute."

For example:

```text
Agent
 ↓
Container
 ↓
Custom processing
 ↓
Result
 ↓
Agent
```

This can be useful when standard tools aren't sufficient.

---

# 29. Why Lower-Level APIs?

The course gives three major use cases:

### Custom RAG

```text
Documents
 ↓
Custom chunking
 ↓
Custom embedding
 ↓
Vector store
 ↓
Custom retrieval
 ↓
LLM
```

### Specialized data processing

```text
Agent
 ↓
Custom processing
 ↓
Specialized result
```

### Isolated tool execution

```text
Agent
 ↓
Container
 ↓
Custom tool/process
```

---

# 30. High-Level vs Low-Level

This distinction is important.

### High-level

Use the provided agent tools and Responses API.

```text
Application
    ↓
Responses API
    ↓
Built-in tools
```

Advantages:

* Easier
* Faster to build
* Less infrastructure/code
* Good for common use cases

### Lower-level

Use APIs such as:

* Vector Stores API
* Files API
* Containers API

```text
Application
    ↓
Lower-level APIs
    ↓
Custom architecture
```

Advantages:

* More control
* More customization
* Better for specialized architectures

Trade-off:

* More engineering
* More decisions
* More responsibility

---

# 31. Full OCI Agent Building-Block Architecture

Put everything together:

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │ Responses API   │
                  │                 │
                  │ Agent engine    │
                  └────────┬────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        File Search   Code Interpreter  Functions
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                      MCP Calling
                           │
                           ▼
                    External Systems


       MEMORY
       ├── Conversations
       ├── Long-term memory
       └── Context compaction


       LOWER-LEVEL APIs
       ├── Vector Stores
       ├── Files
       └── Containers
```

---

# 32. How This Connects to Your Previous Learning

You have already learned:

```text
Agent = LLM + Tools + Loop
```

This lesson maps OCI components onto that architecture.

### LLM / model

Provides intelligence.

### Responses API

Provides the agent-facing API and multi-step/tool-calling capabilities.

### Tools

Give the agent capabilities:

```text
File Search
Code Interpreter
Function Calling
MCP
```

### Memory

Maintains context:

```text
Conversation
Long-term memory
Compaction
```

### Lower-level APIs

Give developers more control over:

```text
Retrieval
Files
Execution environments
```

So the bigger picture becomes:

```text
             OCI AGENT
                 │
      ┌──────────┼──────────┐
      ↓          ↓          ↓
   MODEL       TOOLS      MEMORY
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
     Files     Code    Functions
                         │
                         ↓
                        MCP

              ↓

       LOWER-LEVEL CONTROL
       ├── Vector Stores
       ├── Files
       └── Containers
```

---

# 33. High-Level API vs Lower-Level API — Important Pattern

Think about it like Python.

### High-level

```python
sort(data)
```

You simply ask for sorting.

### Lower-level

You manually control:

```text
comparison
partitioning
memory
algorithm
data structures
```

You get more control but more responsibility.

Similarly:

> **High-level OCI tools = convenience**
>
> **Lower-level APIs = control**

---

# 34. Important Interview Questions

### Q1. What is OCI Responses API?

It is an API for building agentic applications that supports multi-step reasoning and tool calling, with OpenAI-compatible interfaces according to the course.

---

### Q2. What are the four agent tool categories?

```text
1. File Search
2. Code Interpreter
3. Function Calling
4. MCP Calling
```

---

### Q3. What does File Search do?

It enables semantic retrieval from uploaded documents using vector-store-based retrieval.

---

### Q4. What does Code Interpreter do?

It executes Python in a sandboxed environment for computation and data analysis.

---

### Q5. What is Function Calling?

It allows an agent to invoke developer-defined functions for custom application/business logic.

---

### Q6. What is MCP Calling?

It allows the agent to connect to remote MCP servers and use their standardized tools.

---

### Q7. What are the three types of memory?

```text
1. Conversation/session memory
2. Long-term memory
3. Context optimization/compaction
```

---

### Q8. What is context compaction?

Automatically summarizing/reducing long conversation context while retaining important information so it fits within the model's context window.

---

### Q9. What does the Vector Stores API provide?

Infrastructure/API-level capabilities for storing and searching vectorized information, useful for custom semantic retrieval and RAG architectures.

---

### Q10. When would you use lower-level APIs?

When the high-level tools aren't sufficient and you need more control over:

* RAG
* Data processing
* File management
* Custom execution
* Storage/retrieval architecture

---

# 35. One-Page Revision

## OCI Agent Building Blocks

### Responses API

> **Main API for building agents**

Supports:

* Multi-step workflows
* Tool calling
* Multiple models
* Conversation/state capabilities
* Memory/context capabilities

---

### Four Tools

```text
FILE SEARCH
→ Search documents

CODE INTERPRETER
→ Run Python

FUNCTION CALLING
→ Run custom business logic

MCP CALLING
→ Connect remote MCP servers
```

---

### Three Memory Types

```text
CONVERSATIONS
→ Short-term/session memory

LONG-TERM MEMORY
→ Persistent information across sessions

CONTEXT COMPACTION
→ Summarize long context
```

---

### Three Lower-Level APIs

```text
VECTOR STORES
→ Custom semantic retrieval/RAG

FILES
→ File upload/management

CONTAINERS
→ Specialized isolated processing
```

---

# 36. Final Mental Model

Memorize this diagram:

```text
                 OCI AGENT
                    │
                    ▼
             RESPONSES API
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
     TOOLS        MEMORY      MODELS
       │            │
   ┌───┼───┐    ┌───┼────┐
   │   │   │    │   │    │
 Files Code Functions Conversation
              MCP         Long-term
                           Compaction

                    │
                    ▼
             LOWER-LEVEL APIs
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
      Vector      Files    Containers
       Stores
```

### The one sentence to remember:

> **OCI's Responses API provides the agent interface, tools give the agent capabilities, memory gives it continuity, and lower-level APIs give developers deeper control.**
