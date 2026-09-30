# OpenAI Agents Module — Roadmap

## 1. What is this module about?

This module teaches how to build AI agents using two main OpenAI technologies:

1. **Responses API**
2. **Agents SDK**

The module then builds on those to cover:

* Tools / function calling
* Multi-agent systems
* Handoffs
* Guardrails and safety
* A complete agent project

---

# 2. Module roadmap

The course has **7 lessons**:

```text
1. OpenAI Agent Stack
        ↓
2. Responses API Basics
        ↓
3. Agents SDK Fundamentals
        ↓
4. Tools & Function Calling
        ↓
5. Multi-Agent Systems & Handoffs
        ↓
6. Guardrails & Safety
        ↓
7. Complete Project
```

Each lesson builds on the previous one.

---

# 3. Lesson 1 — OpenAI Agent Stack

First, the course explains the overall OpenAI agent architecture.

The two important pieces are:

```text
Responses API
      +
Agents SDK
```

You should understand **how these two fit together** before building agents.

---

# 4. Lesson 2 — Responses API Basics

The Responses API is the interface you use to interact with OpenAI models.

At the basic level:

```text
Your Python application
        ↓
Responses API
        ↓
OpenAI model
        ↓
Response
        ↓
Your application
```

The lesson will teach:

* What the Responses API is
* How it works
* How to make your first API call
* How to send input to a model
* How to receive the model's response

---

# 5. Lesson 3 — Agents SDK Fundamentals

Now we move from simply calling a model to **building an agent**.

Basic idea:

```text
Normal model call:

User → Model → Answer
```

Agent:

```text
User
 ↓
Agent
 ↓
Model
 ↓
Decision
 ↓
Action / Tool
 ↓
Observation
 ↓
Model
 ↓
Final answer
```

The Agents SDK provides the framework for building this type of system.

The lesson will build your **first agent**.

---

# 6. Lesson 4 — Tools & Function Calling

A model by itself mainly produces information.

Tools give the agent the ability to **do things**.

For example:

```text
Agent
 ├── Web search
 ├── Calculator
 ├── Database
 ├── API
 ├── Python function
 └── External service
```

The important concept is **function calling**.

The model can decide:

> "I need this tool."

Then the agent runtime executes the function and gives the result back to the model.

Conceptually:

```text
User
 ↓
Agent
 ↓
LLM
 ↓
"I need calculator"
 ↓
Tool call
 ↓
Calculator
 ↓
Result
 ↓
LLM
 ↓
Final answer
```

This should look familiar from your LangChain + MCP lessons.

---

# 7. Lesson 5 — Multi-Agent Systems & Handoffs

One agent doesn't have to do everything.

You can create specialized agents.

For example:

```text
                    Main Agent
                        │
             ┌──────────┼──────────┐
             ↓          ↓          ↓
        Math Agent   Coding Agent  Research Agent
```

Each specialized agent can have its own:

* Instructions
* Tools
* Responsibilities

### Handoff

A **handoff** means one agent transfers responsibility for the task to another agent.

For example:

```text
User
 ↓
Triage Agent
 ↓
"That's a coding question."
 ↓
Coding Agent
 ↓
Answer
```

The key idea:

> **One agent decides that another specialized agent should take over.**

---

# 8. Lesson 6 — Guardrails & Safety

Agents can take actions, so safety becomes important.

Remember what you learned earlier:

```text
Chatbot:
User → LLM → Answer

Agent:
User → Agent → Tools → External systems
```

An agent might:

```text
read data
write data
call APIs
send messages
execute code
```

Therefore, we need guardrails.

Examples:

```text
Input validation
Tool restrictions
Output validation
Permission checks
Human approval
```

Conceptually:

```text
User
 ↓
Input Guardrail
 ↓
Agent
 ↓
Tool Guardrail
 ↓
Tool
 ↓
Output Guardrail
 ↓
User
```

---

# 9. Lesson 7 — Complete Project

Finally, everything is combined.

You will take the concepts from the previous lessons:

```text
Responses API
       +
Agents SDK
       +
Tools
       +
Function Calling
       +
Multi-Agent Systems
       +
Handoffs
       +
Guardrails
```

and build a complete project.

---

# 10. How this connects to what you already learned

This is VERY important because you just finished the LangChain + MCP section.

You have now seen **three different layers/approaches**.

### LangChain

```text
LangChain
   ↓
Agent
   ↓
Tools
```

### MCP

```text
Agent
   ↓
MCP Client
   ↓
MCP Server
   ↓
External system/API
```

### OpenAI Agents SDK

```text
Agents SDK
   ↓
Agent
   ↓
Tools
   ↓
External systems
```

These aren't necessarily competing concepts.

They solve different parts of the architecture.

---

# 11. The mental progression

Your course is essentially moving through this progression:

```text
LLM
 ↓
Agent
 ↓
Agent + Tools
 ↓
Agent + Tools + MCP
 ↓
Multiple Agents
 ↓
Agent + Handoffs
 ↓
Agent + Guardrails
```

And now you're learning how to build that using **OpenAI's agent stack**.

---

# 12. What you should know by the end

By the end of this module, you should be able to explain:

### Responses API

> How do I interact with OpenAI models programmatically?

### Agents SDK

> How do I build an agent around the model?

### Tools

> How do I give the agent capabilities beyond generating text?

### Function calling

> How does the model request a tool/function?

### Multi-agent

> How can multiple specialized agents work together?

### Handoffs

> How can one agent transfer a task to another agent?

### Guardrails

> How do I control and validate what my agent does?

### Complete project

> How do I combine all of these into a working agentic application?

---

# 13. One-line summary

**Responses API → communicate with models**

**Agents SDK → build agents**

**Tools/function calling → give agents capabilities**

**Handoffs → connect specialized agents**

**Guardrails → control agent behavior**

**Complete project → combine everything**

---

## The architecture to keep in your head

```text
                 USER
                   │
                   ↓
             ┌───────────┐
             │   AGENT   │
             └─────┬─────┘
                   │
                   ↓
            OpenAI Model
                   │
          ┌────────┴────────┐
          ↓                 ↓
       Tool 1            Tool 2
          │                 │
          ↓                 ↓
      External           External
       system             system

                   +
             Other Agents
                   │
                Handoffs

                   +
              Guardrails
```

The next lesson will make the **Responses API** concrete, so the natural progression is:

**first understand how you call the model → then understand how the Agents SDK turns that model into an agent.**
