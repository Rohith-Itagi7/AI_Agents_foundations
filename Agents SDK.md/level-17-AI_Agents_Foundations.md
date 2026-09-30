# Complete Customer Support Agent System

## 1. What This Lesson Is About

This lesson combines everything learned in the previous lessons into one complete project.

The project is a **Customer Support Agent System**.

It combines:

* OpenAI Agents Stack
* Responses API
* Agents SDK
* Function tools
* Hosted tools
* Multi-agent systems
* Handoffs
* Input guardrails
* Tracing

The main architecture is:

```text
                         USER
                           │
                           ▼
                 ┌──────────────────┐
                 │ Support Guardrail│
                 └────────┬─────────┘
                          │
                     Is it support?
                      /          \
                    NO            YES
                    │              │
                    ▼              ▼
                  STOP          TRIAGE AGENT
                                  │
                       ┌──────────┼──────────┐
                       │          │          │
                       ▼          ▼          ▼
                  Order Status  Refund      FAQ
                     Agent      Agent       Agent
                       │          │          │
                       ▼          ▼          ▼
                  Function     Function   Web Search
                    Tool         Tool       Tool
```

---

# 2. The Three Specialized Agents

The system contains one Triage Agent and three specialized agents.

```text
Customer Support System
│
├── Triage Agent
│
├── Order Status Agent
│
├── Refund Agent
│
└── FAQ Agent
```

Each agent has a specific responsibility.

---

# 3. Triage Agent

## What is the Triage Agent?

The **Triage Agent** is the entry point for customer requests.

Every customer message reaches it after passing the support guardrail.

Its job is **not necessarily to solve the problem itself**.

Its job is to decide:

> "Which specialist should handle this request?"

Example:

```text
User:
"Where is my order?"

        ↓

Triage Agent

        ↓

Order Status Agent
```

Another example:

```text
User:
"I want to return my product."

        ↓

Triage Agent

        ↓

Refund Agent
```

Another:

```text
User:
"What is your return policy?"

        ↓

Triage Agent

        ↓

FAQ Agent
```

This is the **routing pattern**.

---

# 4. Order Status Agent

The Order Status Agent handles:

> "Where is my order?"

It uses a **custom Python function tool**.

For example:

```text
User
 ↓
Triage
 ↓
Order Status Agent
 ↓
Lookup Order Tool
 ↓
Order data
 ↓
LLM
 ↓
Friendly response
```

The custom tool could conceptually be:

```python
@function_tool
def lookup_order(order_id: str):
    ...
```

The actual implementation might query:

* Database
* API
* Dictionary
* Internal service
* MCP server

In the course demo, it uses a simple Python dictionary.

---

# 5. Refund Agent

The Refund Agent handles refund requests.

It also uses a **custom function tool**.

Conceptually:

```text
User
 ↓
Triage
 ↓
Refund Agent
 ↓
Process Refund Tool
 ↓
Refund Result
 ↓
LLM
 ↓
Customer Response
```

The important concept is:

> **Custom function tools = functionality you define yourself.**

The tool could eventually interact with a real payment/refund system.

---

# 6. FAQ Agent

The FAQ Agent handles general questions.

Unlike the previous two agents, it does not use a custom Python function.

It uses an **OpenAI hosted tool**:

> **Web Search**

Architecture:

```text
User
 ↓
Triage
 ↓
FAQ Agent
 ↓
Web Search
 ↓
Search Result
 ↓
LLM
 ↓
Answer
```

This demonstrates another important concept:

```text
Custom capability → Function tool

Built-in capability → Hosted tool
```

---

# 7. Input Guardrail

The system also has an input guardrail.

Its purpose is:

> **Only allow customer-support-related questions into the system.**

For example:

```text
"What is the status of order ORD-001?"
```

Allowed:

```text
Support question = TRUE
```

But:

```text
"Write me a Python program."
```

could be rejected:

```text
Support question = FALSE
```

Architecture:

```text
User
 ↓
Support Topic Checker
 ↓
Is this a support question?
 │
 ├── NO → 🚨 Tripwire → STOP
 │
 └── YES
       ↓
     Triage
```

---

# 8. Complete System

Now put everything together:

```text
                         USER
                           │
                           ▼
                ┌────────────────────┐
                │  INPUT GUARDRAIL   │
                │                    │
                │ Support Checker    │
                └─────────┬──────────┘
                          │
                  ┌───────┴───────┐
                  │               │
                FALSE            TRUE
                  │               │
                  ▼               ▼
              🚨 STOP         TRIAGE AGENT
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
          ORDER STATUS         REFUND            FAQ
             AGENT              AGENT            AGENT
                 │                │                │
                 ▼                ▼                ▼
          Lookup Order       Process Refund     Web Search
             Tool                Tool             Tool
                 │                │                │
                 └────────────────┼────────────────┘
                                  │
                                  ▼
                             FINAL RESPONSE
```

This one diagram contains almost the entire module.

---

# 9. Where Each Course Concept Appears

| Concept            | Where it appears              |
| ------------------ | ----------------------------- |
| OpenAI Agent Stack | Overall architecture          |
| Responses API      | LLM calls                     |
| Agents SDK         | Agent orchestration           |
| Function calling   | Order + Refund tools          |
| Hosted tools       | FAQ Web Search                |
| Multi-agent system | Triage + specialists          |
| Handoffs           | Triage → specialist           |
| Guardrails         | Support-only input check      |
| Tripwire           | Blocks unsupported requests   |
| Tracing            | Observes the entire execution |

This is why this lesson is important.

It isn't introducing one isolated feature.

It is showing how the features **work together**.

---

# 10. Example Request: "Where Is My Order?"

Let's trace one complete request.

User sends:

```text
Where is my order? ORD-001
```

The request passes through several stages.

---

# Phase 1 — Support Guardrail

The first thing that happens is the **Support Topic Guardrail**.

Important:

> The Triage Agent doesn't immediately start processing the request.

Instead:

```text
User
 ↓
Support Guardrail
```

The guardrail uses a small checker agent.

The checker asks the LLM:

> "Is this a customer-support question?"

For:

```text
Where is my order? ORD-001
```

the checker returns:

```text
is_support_question = True
```

Therefore:

```text
Guardrail
    ↓
PASS
    ↓
Continue
```

---

# 11. Why Does the Guardrail Take Time?

The guardrail itself contains an LLM call.

So the architecture is:

```text
User
 ↓
Guardrail
 ↓
LLM call
 ↓
Checker result
```

The course trace showed this taking around **5 seconds in that particular demo run**.

The important lesson isn't the exact number.

The important lesson is:

> **An LLM-based guardrail itself can add latency because it may require another model call.**

This is an important production consideration.

---

# 12. Phase 2 — Triage Agent

Once the guardrail passes:

```text
Support Guardrail
       ↓
   Triage Agent
```

The Triage Agent receives:

```text
Where is my order? ORD-001
```

Its instructions tell it that order-related questions should go to the Order Status Agent.

So it decides:

```text
ORDER QUESTION
     ↓
Order Status Agent
```

This is a **handoff**.

---

# 13. What Actually Happens During a Handoff?

A very important detail:

> **The handoff itself doesn't require an LLM call.**

The LLM decides that a handoff should happen.

But once that decision is made, the SDK can transfer control to the other agent.

Conceptually:

```text
Triage Agent
     │
     │ LLM decides:
     │ "Order Status Agent"
     ▼
Handoff
     │
     ▼
Order Status Agent
```

The actual switching of control is handled by the SDK.

So:

```text
LLM decision → requires LLM call

Agent switching → SDK operation
```

This distinction is important.

---

# 14. Phase 3 — Order Status Agent

Now the Order Status Agent takes control.

It receives:

```text
Where is my order? ORD-001
```

The agent has access to:

```text
lookup_order()
```

The model sees the tool schema.

It decides:

> "I need to call Lookup Order."

So it generates a tool call.

Conceptually:

```json
{
    "name": "lookup_order",
    "arguments": {
        "order_id": "ORD-001"
    }
}
```

---

# 15. Tool Execution

Now the actual Python function runs.

Important:

> **The LLM does not execute the Python function.**

The architecture is:

```text
LLM
 ↓
Tool Call Request
 ↓
Agents SDK
 ↓
Python Function
 ↓
Result
```

For example:

```text
lookup_order("ORD-001")
```

might return:

```text
Status: Shipped
Expected delivery: October 2
Carrier: XYZ
```

---

# 16. Why Is the Tool Fast?

In the course demo, the tool is just local Python code.

For example:

```python
orders = {
    "ORD-001": {
        "status": "Shipped",
        "delivery": "October 2"
    }
}
```

Looking up a dictionary entry is extremely fast.

Therefore:

```text
LLM call → relatively slow

Python dictionary lookup → extremely fast
```

The course example showed the local function taking only a few milliseconds.

---

# 17. But Real Production Tools Can Be Slower

The same tool could eventually connect to:

* PostgreSQL
* MongoDB
* REST API
* Payment system
* CRM
* ERP
* MCP server
* Remote microservice

For example:

```text
Agent
 ↓
MCP Client
 ↓
Remote MCP Server
 ↓
Database/API
 ↓
Result
```

That could introduce network latency.

So don't memorize:

> "Tools are always fast."

Instead memorize:

> **Local Python functions can be very fast; remote tools can introduce network latency.**

---

# 18. Tool Result Goes Back to the LLM

After the tool finishes:

```text
lookup_order()
      ↓
Order Data
```

The result is returned to the agent.

The LLM now receives the tool result and can understand it.

For example:

```text
Status: Shipped
Delivery: October 2
```

Then the LLM generates a customer-friendly response:

```text
Your order ORD-001 has been shipped and is
expected to arrive on October 2.
```

So the full flow is:

```text
User
 ↓
Order Status Agent
 ↓
LLM
 ↓
Lookup Order Tool
 ↓
Order Data
 ↓
LLM
 ↓
Final Answer
```

Notice there are **two LLM stages** around the tool.

---

# 19. Why Are There Two LLM Calls?

This is extremely important.

### First LLM call

The model decides:

> "I need to use the lookup_order tool."

```text
Question
 ↓
LLM
 ↓
Tool Call
```

### Tool executes

```text
lookup_order("ORD-001")
 ↓
Order data
```

### Second LLM call

The model sees the result and decides:

> "Now I'll explain this information to the customer."

```text
Tool Result
 ↓
LLM
 ↓
Natural-language response
```

Therefore:

```text
LLM
 ↓
Tool
 ↓
LLM
```

is a very common agent pattern.

---

# 20. Complete Trace

The entire request can be visualized as:

```text
User
 │
 │ "Where is my order? ORD-001"
 ▼
Support Guardrail
 │
 │ LLM call
 ▼
Topic Checker
 │
 │ TRUE
 ▼
Triage Agent
 │
 │ LLM call
 ▼
Handoff
 │
 │ SDK operation
 ▼
Order Status Agent
 │
 │ LLM call
 ▼
Lookup Order Tool
 │
 │ Python execution
 ▼
Order Data
 │
 ▼
LLM
 │
 │ Final response
 ▼
User
```

This is the **actual agent journey**.

---

# 21. Understanding the Trace

The course uses OpenAI tracing to visualize this entire process.

A trace can show:

```text
Run
│
├── Guardrail
│   └── Topic Checker
│
├── Triage Agent
│
├── Handoff
│
├── Order Status Agent
│
├── Lookup Order Tool
│
├── Tool Result
│
├── LLM Call
│
└── Final Output
```

This gives you visibility into the entire workflow.

---

# 22. The Most Important Production Lesson: Latency

The course example took a little over **11 seconds** overall in that particular run.

The trace showed approximately:

```text
Total ≈ 11.4 seconds
```

with:

```text
4 LLM API calls
```

The exact timing is specific to that demo run and shouldn't be treated as a universal benchmark.

The important observation was:

```text
Most time
    ↓
LLM API calls

Very little time
    ↓
Local Python code
    ↓
Guardrail logic
    ↓
Handoff
    ↓
Lookup function
```

---

# 23. Where Should You Optimize?

This is one of the most useful lessons from the project.

Suppose your agent takes:

```text
11 seconds
```

You might initially think:

> "My Python tool must be slow."

But tracing could show:

```text
LLM call #1 → 5 sec
LLM call #2 → 2 sec
LLM call #3 → 2 sec
LLM call #4 → 1.5 sec

Python tools → milliseconds
Handoff → almost instant
```

Therefore, in **this particular architecture**, reducing Python function execution time from:

```text
2 ms → 1 ms
```

won't meaningfully improve the total user experience.

Reducing unnecessary LLM calls could have a much larger effect.

---

# 24. LLM Calls Are Often the Expensive Part

Agent architecture can accidentally create many model calls.

For example:

```text
Guardrail
 ↓
Triage
 ↓
Specialist
 ↓
Tool
 ↓
Specialist
 ↓
Reviewer
 ↓
Final Agent
```

Potentially:

```text
LLM
LLM
LLM
LLM
LLM
LLM
```

Each call can add:

* Latency
* Token usage
* Cost
* More opportunities for failure

Therefore:

> **Agent optimization often means reducing unnecessary model calls and unnecessary context.**

---

# 25. Tracing Helps You Find Bottlenecks

Without tracing:

```text
User
 ↓
11 seconds
 ↓
Answer
```

You don't know why it took 11 seconds.

With tracing:

```text
5.0 sec → Guardrail LLM
2.0 sec → Triage LLM
2.0 sec → Specialist LLM
1.5 sec → Final LLM
0.002 sec → Python tool
```

Now the bottleneck is visible.

This is why observability is so important in production AI systems.

---

# 26. Tool Latency vs LLM Latency

A useful mental model:

```text
                    LATENCY
                       │
         ┌─────────────┴─────────────┐
         │                           │
      LLM Calls                  Tool Calls
         │                           │
   Often significant           Depends on tool
         │                           │
   API/network/model            Local → fast
   processing                    Remote → potentially slower
```

Never assume one category is always slower.

**Measure it with tracing.**

---

# 27. Customer Support Routing Examples

### Example 1 — Order

```text
User:
"Where is ORD-001?"

        ↓

Support Guardrail
        ↓
      PASS
        ↓
Triage Agent
        ↓
Order Status Agent
        ↓
Lookup Order Tool
        ↓
Answer
```

---

### Example 2 — Refund

```text
User:
"I want a refund for ORD-002."

        ↓

Support Guardrail
        ↓
      PASS
        ↓
Triage Agent
        ↓
Refund Agent
        ↓
Process Refund Tool
        ↓
Answer
```

---

### Example 3 — FAQ

```text
User:
"What is your return policy?"

        ↓

Support Guardrail
        ↓
      PASS
        ↓
Triage Agent
        ↓
FAQ Agent
        ↓
Web Search
        ↓
Answer
```

---

### Example 4 — Off-topic

```text
User:
"Write a Python game for me."

        ↓

Support Guardrail
        ↓
      FALSE
        ↓
🚨 Tripwire
        ↓
STOP
```

The request never reaches the Triage Agent.

---

# 28. Handoff vs Tool

This project demonstrates an important distinction.

## Handoff

Transfers control between agents.

```text
Triage
  ↓
Order Agent
```

Think:

> **"You take over."**

---

## Tool Call

The current agent asks a tool to perform an operation.

```text
Order Agent
  ↓
lookup_order()
  ↓
result
  ↓
Order Agent continues
```

Think:

> **"Do this task and give me the result."**

---

# 29. Hosted Tool vs Function Tool

The project also demonstrates both.

### Function Tool

You write the Python function.

```text
Agent
 ↓
Your Python function
```

Examples:

* `lookup_order()`
* `process_refund()`

### Hosted Tool

The capability is provided by the platform.

```text
Agent
 ↓
OpenAI hosted web search
```

You don't have to implement the search engine yourself.

---

# 30. The Complete Concept Map

This single project connects the entire module:

```text
                     OPENAI AGENT SYSTEM
                              │
                              ▼
                       Support Guardrail
                              │
                              ▼
                        Triage Agent
                              │
               ┌──────────────┼──────────────┐
               │              │              │
               ▼              ▼              ▼
         Order Agent      Refund Agent     FAQ Agent
               │              │              │
               ▼              ▼              ▼
         Function Tool    Function Tool   Web Search
               │              │              │
               └──────────────┼──────────────┘
                              │
                              ▼
                         Final Answer

                    ┌─────────────────┐
                    │    TRACING      │
                    │                 │
                    │ Watches all of  │
                    │ the above       │
                    └─────────────────┘
```

---

# 31. Full Module Revision

Now you can connect all six lessons.

## Lesson 1 — OpenAI Agent Stack

Mental model:

```text
Application
    ↓
Agents SDK
    ↓
Responses API
    ↓
OpenAI Model
```

---

## Lesson 2 — Responses API

Provides the core interface for communicating with OpenAI models.

```text
Input
 ↓
Responses API
 ↓
Model Output
```

---

## Lesson 3 — Agents SDK

Provides higher-level agent abstractions:

```text
Agent
Runner
Tools
Handoffs
Guardrails
Tracing
```

---

## Lesson 4 — Tools & Function Calling

Allows the agent to interact with external capabilities.

```text
LLM
 ↓
Tool Call
 ↓
Tool Execution
 ↓
Result
 ↓
LLM
```

---

## Lesson 5 — Multi-Agent Handoffs

Allows multiple specialized agents to cooperate.

```text
Triage
 ↓
Specialist
```

---

## Lesson 6 — Guardrails & Safety

Protects the agent.

```text
Input
 ↓
Guardrail
 ↓
Agent
 ↓
Output Guardrail
```

---

## Final Project

Everything comes together:

```text
User
 ↓
Input Guardrail
 ↓
Triage Agent
 ↓
Handoff
 ↓
Specialist Agent
 ↓
Tool
 ↓
LLM
 ↓
Final Response

Tracing watches the whole execution.
```

---

# 32. The Most Important Architecture to Memorize

If you want one diagram for your notebook, remember this:

```text
                         USER
                           │
                           ▼
                    INPUT GUARDRAIL
                           │
                      SAFE / UNSAFE
                       /         \
                     NO           YES
                     │             │
                     ▼             ▼
                   STOP          TRIAGE
                                   │
                         ┌─────────┼─────────┐
                         │         │         │
                         ▼         ▼         ▼
                      ORDER      REFUND     FAQ
                       AGENT      AGENT     AGENT
                         │         │         │
                         ▼         ▼         ▼
                       TOOL      TOOL     WEB SEARCH
                         │         │         │
                         └─────────┼─────────┘
                                   │
                                   ▼
                              FINAL ANSWER

                    ┌─────────────────────┐
                    │      TRACING        │
                    │                     │
                    │  Observes everything│
                    └─────────────────────┘
```

---

# 33. Production Thinking

When building a real agent system, don't only ask:

> "Does it give the correct answer?"

Also ask:

### Safety

```text
Can malicious input get through?
Can the agent perform unauthorized actions?
Can sensitive data leak?
```

### Routing

```text
Did the request reach the correct specialist?
```

### Tool usage

```text
Did the agent call the correct tool?
Did it use correct arguments?
```

### Performance

```text
How many LLM calls happened?
How long did each take?
```

### Cost

```text
How many tokens were consumed?
Which step is expensive?
```

### Reliability

```text
What happens when the tool fails?
What happens when an API times out?
What happens when the model chooses incorrectly?
```

Tracing gives you the visibility needed to answer many of these questions.

---

# 34. Key Takeaways

### 1. Triage routes

> **Triage Agent = router**

It decides which specialist should handle the request.

### 2. Specialists execute

> **Specialized agents = focused workers**

They handle specific categories of tasks.

### 3. Handoffs transfer control

> **Handoff = "You take over."**

### 4. Tools perform actions

> **Tool = capability/action available to the agent.**

### 5. Function tools are your custom capabilities

```text
Python function
     ↓
@function_tool
     ↓
Agent can request it
```

### 6. Hosted tools provide built-in capabilities

Example:

```text
FAQ Agent
   ↓
Web Search
```

### 7. Guardrails protect the system

```text
Input
 ↓
Guardrail
 ↓
Agent
```

### 8. Tracing provides observability

```text
Agent Run
 ↓
Trace
 ↓
Inspect
```

### 9. Optimize based on measurements

Don't guess what is slow.

Use traces to determine:

```text
Where is the time spent?
Where are the tokens spent?
How many LLM calls happen?
Which tools are called?
```

### 10. The complete agent formula

```text
AGENT SYSTEM

LLM
+
Tools
+
Loop
+
Handoffs
+
Guardrails
+
Observability
```

---

# 35. One-Line Revision

> **Guardrails keep the agent safe, Triage routes the request, Handoffs transfer control, Tools perform actions, the LLM reasons between steps, and Tracing shows the entire journey.**

That is essentially the complete architecture you have learned throughout this OpenAI Agents SDK module.
