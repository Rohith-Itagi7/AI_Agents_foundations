# Oracle AI Database — Agentic AI Capabilities

## 1. Big Picture

Oracle AI Database provides several capabilities for building AI-powered applications and agents.

This lesson focuses on **four major areas**:

```text
┌──────────────────────────────────────────────────┐
│             Oracle AI Database                   │
│                                                  │
│  1. Oracle AI Vector Search                      │
│     → Store/search vectors + business data      │
│                                                  │
│  2. Private Agent Factory                        │
│     → Build agents without code                 │
│                                                  │
│  3. Select AI Agent                              │
│     → Agent lives INSIDE the database           │
│                                                  │
│  4. Autonomous AI Database MCP Server            │
│     → External agents access database via MCP   │
└──────────────────────────────────────────────────┘
```

### The most important mental model

```text
Vector Search
      ↓
"Find relevant knowledge"

Agent Factory
      ↓
"Build agents without coding"

Select AI Agent
      ↓
"Agent lives inside the database"

Database MCP Server
      ↓
"External agents talk to the database"
```

---

# 2. Oracle AI Vector Search

## What is Oracle AI Vector Search?

**Oracle AI Vector Search** is a capability built directly into Oracle AI Database.

It allows you to:

* Store vector embeddings
* Index vectors
* Search vectors
* Keep vectors alongside traditional business data
* Use SQL to work with the data

The important idea is:

> **Vector data and traditional business data can live in the same database.**

---

# 3. Why Is This Useful?

Suppose a company has traditional business data:

```text
CUSTOMERS
ORDERS
PRODUCTS
EMPLOYEES
TRANSACTIONS
```

Now suppose you also want AI capabilities:

```text
Document embeddings
Product embeddings
Customer-query embeddings
Knowledge-base embeddings
```

Instead of necessarily creating a completely separate vector database, Oracle AI Vector Search allows vector data to coexist with traditional database data.

Conceptually:

```text
              Oracle AI Database
                     │
          ┌──────────┴──────────┐
          │                     │
   Traditional Data        Vector Data
          │                     │
     Orders, Users        Embeddings
     Products, etc.       Documents
          │                     │
          └──────────┬──────────┘
                     │
                  SQL/Search
```

---

# 4. Vector Search and RAG

You already learned RAG.

A typical RAG system needs:

```text
Documents
   ↓
Chunk
   ↓
Embedding
   ↓
Vector Store
   ↓
Semantic Search
   ↓
Relevant Documents
   ↓
LLM
   ↓
Answer
```

Oracle AI Vector Search can provide the vector-search component.

For example:

```text
User:
"What is our refund policy?"

        ↓

Create query embedding

        ↓

Oracle AI Vector Search

        ↓

Find semantically similar documents

        ↓

Relevant context

        ↓

LLM

        ↓

Answer
```

---

# 5. Oracle AI Vector Search vs Autonomous AI Vector Database

The lesson introduces another offering:

**Oracle Autonomous AI Vector Database**

The relationship is important.

### Oracle AI Vector Search

Think:

> **Underlying database/vector-search technology**

### Autonomous AI Vector Database

Think:

> **Managed cloud service using that technology**

Mental model:

```text
Oracle AI Vector Search
        ↓
Core technology
        ↓
Autonomous AI Vector Database
        ↓
Managed cloud service
```

---

# 6. Why "Autonomous"?

The managed service is designed to reduce operational work.

The course mentions that you don't have to worry as much about things such as:

* Provisioning
* Servers
* Manual tuning
* Security patching

The managed service handles these operational concerns.

### Analogy

Think of:

```text
AI Vector Search
=
Engine
```

while:

```text
Autonomous AI Vector Database
=
Complete managed vehicle using that engine
```

---

# 7. Status Mentioned in the Course

The course states that, **at the time of recording**:

* Oracle AI Vector Search was generally available.
* Autonomous AI Vector Database was in **LA (Limited Availability)**.

Availability changes over time, so for real deployment decisions you should check current Oracle documentation.

For this foundational lesson, the important concept is the **technology vs managed service distinction**, not memorizing the historical availability status.

---

# 8. Private Agent Factory

The second major capability is:

**Oracle AI Database Private Agent Factory**

The lesson often shortens this to:

> **Agent Factory**

It is described as a **no-code platform** for creating AI agents.

The target users include:

* Business users
* Engineers

The key idea:

> **Build, test, and deploy intelligent agents without writing application code.**

---

# 9. What Does Agent Factory Provide?

The lesson mentions:

### Pre-built agents

Two examples:

1. Knowledge Agent
2. Data Analysis Agent

It also provides:

* Visual Builder
* Templates
* Custom agentic workflows

So the workflow is more visual than traditional coding.

---

# 10. Traditional Agent Development vs Agent Factory

### Traditional approach

You might write:

```python
agent = Agent(
    name="My Agent",
    instructions="...",
    tools=[...]
)
```

Then write additional application code.

### Agent Factory

Conceptually:

```text
Select / Configure
       ↓
Visual Builder
       ↓
Configure workflow
       ↓
Test
       ↓
Deploy
```

The goal is to reduce the amount of code required.

---

# 11. When to Think About Agent Factory

When you hear:

> **"I want to create an enterprise agent without writing code."**

Think:

**Private Agent Factory**

Its main idea is **no-code agent creation**.

---

# 12. Select AI Agent

The third capability is particularly important.

It is called:

**Select AI Agent**

The key word from the lesson is:

> **INSIDE**

This is the concept you should remember.

---

# 13. What Does "Inside" Mean?

Normally, an agent framework lives in your application.

For example, with LangChain:

```text
Your Application
      ↓
LangChain Agent
      ↓
LLM
      ↓
Oracle Database
```

The agent is **outside the database**.

It connects to the database from the application layer.

Same idea with OpenAI Agents SDK:

```text
Application
     ↓
OpenAI Agents SDK
     ↓
Agent
     ↓
Database
```

Again:

> **Agent is outside → database is accessed from outside.**

---

# 14. Select AI Agent Flips the Architecture

Select AI Agent puts the agent **inside the Oracle AI Database**.

Instead of:

```text
Application
   ↓
Agent
   ↓
Database
```

the concept becomes:

```text
Oracle AI Database
┌─────────────────────────────┐
│                             │
│       Select AI Agent       │
│              ↓              │
│       Enterprise Data       │
│              ↓              │
│             SQL             │
│                             │
└─────────────────────────────┘
```

The agent becomes a **database citizen**.

---

# 15. Why Is This Important?

The agent can work closely with:

* Database data
* SQL
* Database tools
* Database configuration

The lesson describes an architecture where the agent:

1. Uses an LLM configured through an **AI Profile**
2. Accesses enterprise data through SQL/tools
3. Is managed through **PL/SQL packages**

---

# 16. AI Profile

An **AI Profile** configures the LLM-related settings used by Select AI capabilities.

Conceptually:

```text
Select AI Agent
      ↓
AI Profile
      ↓
Configured LLM
```

The database can therefore use an LLM while the agent itself is integrated into the database environment.

---

# 17. Select AI Agent vs LangChain

This is a very useful comparison.

### LangChain architecture

```text
Application
     ↓
LangChain
     ↓
Agent
     ↓
Database
```

### Select AI Agent architecture

```text
Oracle AI Database
     ↓
Select AI Agent
     ↓
SQL / Database tools
     ↓
Enterprise data
```

The major architectural difference is:

> **LangChain agent lives in application code. Select AI Agent lives inside the database environment.**

---

# 18. Why Would Database-Native Agents Matter?

Suppose a company has large amounts of sensitive enterprise information inside its database.

A database-native agent can be closely integrated with the database's data and SQL environment.

The lesson's key point is not that database-native agents replace every external framework.

Rather:

> **For database-centric workloads, the database itself can become the environment where the agent operates.**

---

# 19. Autonomous AI Database MCP Server

The fourth capability is:

**Oracle Autonomous AI Database MCP Server**

This brings us back to something you already learned:

**MCP — Model Context Protocol**

The purpose here is to let external AI agents/MCP clients access Autonomous AI Database capabilities through MCP.

---

# 20. The Critical Difference

The lesson emphasizes:

> This is **not** simply an MCP server that you download and run next to the database.

Instead:

> **The MCP server capability is part of the database service itself.**

Conceptually:

```text
External Agent
      ↓
   MCP Client
      ↓
Autonomous AI Database
      │
      └── MCP Server capability
```

The database itself responds to MCP requests.

---

# 21. Compare With Your Earlier MCP Architecture

Earlier you learned about a locally running MCP server:

```text
LangChain Agent
      ↓
MCP Client
      ↓
MCP Server
      ↓
External System
```

For example, you had a Python MCP server.

Here the architecture is different:

```text
External AI Agent
      ↓
MCP Client
      ↓
Oracle Autonomous AI Database
      ↓
Database capabilities/data
```

The database service itself provides the MCP capability.

---

# 22. Why Is MCP Useful Here?

Without a standardized interface, an external agent might need custom database integration code.

With MCP:

```text
Agent
 ↓
MCP
 ↓
Database capabilities
```

This gives AI applications a standardized way to interact with the database.

The course describes this as avoiding the need for custom integration code and manual security administration for the MCP connection.

---

# 23. The Four Capabilities Compared

This table is extremely important.

| Capability                        | Main idea                                       | Where is the key capability? |
| --------------------------------- | ----------------------------------------------- | ---------------------------- |
| Oracle AI Vector Search           | Store/search embeddings alongside business data | Database                     |
| Private Agent Factory             | Build agents without code                       | Database/cloud platform      |
| Select AI Agent                   | Autonomous agent integrated into database       | **Inside database**          |
| Autonomous AI Database MCP Server | External agents access database through MCP     | Database service             |

---

# 24. The Most Important Architectural Difference

You can understand all four by asking:

> **"Where does the AI capability live?"**

### Vector Search

```text
Database
 ↓
Vector storage/search
```

### Agent Factory

```text
Visual platform
 ↓
Agent creation
```

### Select AI Agent

```text
Database
 ↓
Agent lives INSIDE
```

### MCP Server

```text
External Agent
 ↓
MCP
 ↓
Database
```

---

# 25. Four Simple Mental Models

Memorize these:

### 🟦 Oracle AI Vector Search

> **"Store and search meaning inside the database."**

### 🟩 Private Agent Factory

> **"Build agents visually without code."**

### 🟨 Select AI Agent

> **"Put the agent inside the database."**

### 🟥 Database MCP Server

> **"Let outside agents talk to the database using MCP."**

---

# 26. How They Connect to Your Previous Learning

You've already learned:

### RAG

```text
Documents
 ↓
Embeddings
 ↓
Vector Search
 ↓
Relevant Context
 ↓
LLM
```

Oracle AI Vector Search provides the database capability needed for the vector-search part.

---

### Agent Frameworks

You've learned:

```text
LangChain
LangGraph
OpenAI Agents SDK
```

Normally:

```text
Application
 ↓
Agent Framework
 ↓
Database
```

Select AI Agent changes this relationship:

```text
Database
 ↓
Select AI Agent
 ↓
Enterprise Data
```

---

### MCP

You've learned:

```text
Agent
 ↓
MCP Client
 ↓
MCP Server
 ↓
Tool/System
```

Oracle Autonomous AI Database MCP Server provides the database-side MCP capability:

```text
Agent
 ↓
MCP Client
 ↓
Autonomous AI Database
```

---

# 27. Additional Oracle AI Database Innovations

The course explicitly says it is **not covering everything**.

It briefly mentions additional technologies such as:

* Oracle Deep Data Security
* Trusted Answer Search
* Oracle Vectors on Ice
* Oracle Private AI Services Container
* Other agentic AI innovations

You don't need to memorize these for the main architecture of this lesson.

The important point is:

> **Oracle AI Database has more AI capabilities than the four covered in this foundational module.**

---

# 28. Complete Mental Map

```text
                 ORACLE AI DATABASE
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
        ▼                ▼                 ▼
   VECTOR SEARCH    AGENT CAPABILITIES   MCP
        │                │                 │
        │         ┌──────┴──────┐          │
        │         │             │          │
        │         ▼             ▼          │
        │   Agent Factory   Select AI      │
        │         │             │          │
        │         │          INSIDE        │
        │         │         DATABASE       │
        │         │                        │
        └─────────┴────────────────────────┘
```

More simply:

```text
Oracle AI Database
│
├── Oracle AI Vector Search
│   └── Semantic search / RAG
│
├── Private Agent Factory
│   └── No-code agents
│
├── Select AI Agent
│   └── Agent inside database
│
└── Autonomous AI Database MCP Server
    └── External agents → MCP → Database
```

---

# 29. Interview Questions

### Q1. What is Oracle AI Vector Search?

A database capability that allows vector embeddings to be stored, indexed, and searched alongside traditional business data using Oracle AI Database.

---

### Q2. What is the difference between AI Vector Search and Autonomous AI Vector Database?

**AI Vector Search** is the underlying database technology/capability.

**Autonomous AI Vector Database** is a managed cloud service built around vector database capabilities.

---

### Q3. What is Oracle Private Agent Factory?

A no-code platform for building, testing, and deploying intelligent agents.

---

### Q4. What pre-built agents does Agent Factory provide according to the lesson?

* Knowledge Agent
* Data Analysis Agent

It also provides a visual builder and templates for custom workflows.

---

### Q5. What is special about Select AI Agent?

The key idea is:

> **The agent lives inside the Oracle AI Database.**

---

### Q6. How is Select AI Agent different from LangChain?

With LangChain, the agent normally lives in the application layer and accesses the database externally.

With Select AI Agent, the agent is integrated into the database environment itself.

---

### Q7. What is the Oracle Autonomous AI Database MCP Server?

It provides an MCP interface through which external AI agents/MCP clients can access Autonomous AI Database capabilities.

---

### Q8. Is the Autonomous AI Database MCP Server just a separate MCP server application?

According to the lesson, **no**.

The MCP capability is part of the database service itself rather than simply a third-party MCP server process that you download and run next to the database.

---

# 30. Final Revision Notes

## Four Things to Remember

```text
1️⃣ Vector Search
   → Search embeddings + business data

2️⃣ Agent Factory
   → Build agents without coding

3️⃣ Select AI Agent
   → Agent lives INSIDE database

4️⃣ Database MCP Server
   → External agents access database through MCP
```

### One-line memory trick

> **Search → Build → Live → Connect**

```text
Vector Search
     ↓
   SEARCH

Agent Factory
     ↓
    BUILD

Select AI Agent
     ↓
     LIVE
   (inside DB)

Database MCP
     ↓
   CONNECT
(external agents → DB)
```

## Final takeaway

The main lesson is that Oracle AI Database isn't only a place to store traditional business data. It provides multiple ways to bring **vectors, agents, retrieval, and standardized AI connectivity** into the database ecosystem.

The four architectures answer different questions:

* **Need semantic search/RAG?** → Vector Search
* **Want to build an agent without coding?** → Agent Factory
* **Want the agent itself integrated inside the database?** → Select AI Agent
* **Want external AI agents to interact with the database using a standard protocol?** → Database MCP Server
