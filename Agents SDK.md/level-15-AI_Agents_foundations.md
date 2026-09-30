# OpenAI Agents SDK — Multi-Agent Systems with Handoffs

## 1. Why Do We Need Multiple Agents?

A single agent can handle many tasks:

```text
User
 ↓
One Agent
 ↓
Answer
```

But imagine a customer-support system handling:

* Billing
* Shipping
* Technical problems
* Refunds
* Account problems

One giant agent could handle everything, but that can make the instructions and responsibilities complicated.

Instead, we can create specialized agents:

```text
                    Triage Agent
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      Billing         Shipping       Technical
       Agent            Agent           Agent
```

Each specialist has a focused responsibility.

---

# 2. Two Main Multi-Agent Patterns

The Agents SDK supports two important ways of structuring multi-agent systems:

```text
                Multi-Agent Systems
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
         Handoffs             Manager
      Decentralized           Centralized
```

The difference is **who remains in control**.

---

# 3. Pattern 1 — Handoffs

Handoffs are also called the **decentralized model**.

The basic idea:

> One agent receives the request and transfers control to another specialized agent.

For example:

```text
User
 ↓
Triage Agent
 ↓
"Math question"
 ↓
Math Agent
 ↓
Answer
```

Once the handoff happens, the specialist becomes responsible for the conversation.

---

# 4. Handoff Mental Model

Think of a handoff like transferring a phone call.

```text
Customer
   │
   │ "I have a billing problem."
   ↓
Support/Triage Agent
   │
   │ "This belongs to billing."
   ↓
Billing Agent
   │
   └── takes over
```

The triage agent doesn't continue controlling the conversation.

The specialist takes over.

---

# 5. Example — Customer Support

Imagine:

```text
                    Triage Agent
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       Billing        Shipping       Technical
        Agent           Agent           Agent
```

User:

> "Why was I charged twice?"

Triage:

```text
This is a billing issue.
```

Handoff:

```text
Triage → Billing Agent
```

Billing Agent handles the conversation.

---

# 6. What Does the Specialist Receive?

An important point from the lesson:

> The specialist can see the conversation context/history associated with the run.

For example:

```text
User:
"My package hasn't arrived and tracking says delivered."

Triage:
"This looks like a shipping issue."

          ↓ HANDOFF

Shipping Agent:
sees the relevant conversation context
```

So the specialist doesn't necessarily need the user to repeat the entire problem.

---

# 7. Why Are Handoffs Useful?

Handoffs are useful when:

* Different tasks require different expertise.
* You want specialized instructions.
* You want routing to happen automatically.
* One specialist should take ownership after routing.

Examples:

```text
Customer Support
    ↓
Billing / Shipping / Technical
```

```text
Education
    ↓
Math / History / Physics
```

```text
Healthcare information system
    ↓
Appointments / Billing / General information
```

The agents should be designed according to the application's requirements and safety constraints.

---

# 8. Pattern 2 — Manager

The second pattern is the **Manager pattern**, also called the **centralized model**.

Here:

> One central manager remains in control and delegates work to specialized agents.

Mental model:

```text
                    Manager
                       │
             ┌─────────┼─────────┐
             ↓         ↓         ↓
         Research    Writer    Reviewer
           Agent      Agent      Agent
```

The manager does **not** hand over control permanently.

It stays in charge.

---

# 9. Manager Pattern Example

Imagine a project manager agent.

User:

> "Create a report about electric vehicles."

Manager decides:

```text
Manager
   │
   ├── Research Agent
   │
   ├── Writing Agent
   │
   └── Review Agent
```

The manager might:

1. Ask Research Agent for information.
2. Give research to Writer Agent.
3. Send the draft to Reviewer Agent.
4. Receive feedback.
5. Ask Writer Agent to revise.
6. Produce the final response.

The manager coordinates the whole process.

---

# 10. Handoff vs Manager

This is the most important comparison in the lesson.

| Feature                           | Handoff                  | Manager                 |
| --------------------------------- | ------------------------ | ----------------------- |
| Architecture                      | Decentralized            | Centralized             |
| Initial agent                     | Triage/router            | Manager                 |
| Specialist takes control?         | Yes                      | No                      |
| Central agent remains in control? | No                       | Yes                     |
| Specialist relationship           | Handoff                  | Agent-as-tool           |
| Good for                          | Routing                  | Coordination            |
| Example                           | Customer support routing | Project/report workflow |

### The key question:

> **After the specialist is called, who controls the conversation?**

If the specialist takes over:

```text
Handoff
```

If the manager stays in control:

```text
Manager
```

---

# 11. Very Important: Handoff ≠ Agent as Tool

You already learned **Agents as Tools** in the previous lesson.

Don't mix them up.

## Handoff

```text
Agent A
   │
   │ handoff
   ↓
Agent B
   │
   └── takes over
```

Control moves to Agent B.

---

## Agent as Tool

```text
Manager
   │
   │ calls specialist
   ↓
Specialist Agent
   │
   ↓
Result
   │
   ↓
Manager
   │
   └── continues
```

Control stays with the Manager.

### Memory rule

> **Handoff = transfer control.**

> **Agent as Tool = delegate work, keep control.**

---

# 12. Which Pattern Should You Use?

The lesson gives this basic rule:

### Use Handoffs

When you primarily need:

```text
Route → Specialist takes over
```

Example:

```text
Customer Support
      ↓
Triage
      ↓
Billing
```

### Use Manager

When you need:

```text
Coordinate → Delegate → Combine results
```

Example:

```text
Manager
  ↓
Research
  ↓
Writing
  ↓
Review
  ↓
Manager
```

### Easy rule

> **Simple routing → Handoff**

> **Complex coordination → Manager**

---

# 13. Building a Handoff System

Now let's build the course example.

We will create:

```text
Triage Agent
    │
    ├── Math Tutor
    │
    └── History Tutor
```

---

# 14. Step 1 — Create the Math Agent

```python
from agents import Agent
```

Then:

```python
math_agent = Agent(
    name="Math Tutor",
    instructions="""
    You are a helpful math tutor.
    Solve math questions clearly.
    Explain the calculation step by step.
    """
)
```

This agent specializes in mathematics.

---

# 15. Step 2 — Create the History Agent

```python
history_agent = Agent(
    name="History Tutor",
    instructions="""
    You are a helpful history tutor.
    Answer history questions clearly.
    Include useful historical context.
    """
)
```

Now we have two specialists:

```text
Math Tutor
    ↓
Math questions

History Tutor
    ↓
History questions
```

---

# 16. Step 3 — Handoff Descriptions

A specialist needs a useful description for routing.

Conceptually:

```text
Math Tutor
"Handles mathematical calculations and math questions."

History Tutor
"Handles questions about historical events, people, and civilizations."
```

Why?

Because the triage agent needs to understand:

> "When should I send a question to this agent?"

The handoff description acts as guidance for that decision.

---

# 17. Step 4 — Create the Triage Agent

Now create the router.

Conceptually:

```python
triage_agent = Agent(
    name="Triage",
    instructions="""
    Route the user's question to the appropriate specialist.
    Use the Math Tutor for mathematics questions.
    Use the History Tutor for history questions.
    """,
    handoffs=[
        math_agent,
        history_agent
    ]
)
```

The important part is:

```python
handoffs=[
    math_agent,
    history_agent
]
```

This tells the Triage Agent:

> These are the agents you are allowed to hand off to.

---

# 18. What Does `handoffs=[...]` Mean?

Suppose:

```python
handoffs=[
    math_agent,
    history_agent
]
```

Then the triage agent has two possible destinations:

```text
             Triage
                │
         ┌──────┴──────┐
         ↓             ↓
    Math Tutor    History Tutor
```

The Triage Agent decides which one is appropriate.

---

# 19. Under the Hood: Handoffs Become Tool-Like Actions

This is an important conceptual point.

The SDK exposes handoffs to the agent as callable routing capabilities.

Conceptually:

```text
Triage Agent
      │
      ├── handoff_to_math
      │
      └── handoff_to_history
```

The LLM sees descriptions of the available handoffs and can select the appropriate one.

So when the user asks:

```text
"What is 15% of 240?"
```

the model can determine:

```text
This is a math question.
        ↓
handoff → Math Tutor
```

---

# 20. Step 5 — Run the Triage Agent

Now run:

```python
from agents import Runner

result = Runner.run_sync(
    triage_agent,
    "What is 15% of 240?"
)

print(result.final_output)
```

The important point:

> We run the **Triage Agent**, not the Math Agent directly.

The Triage Agent determines where the request should go.

---

# 21. Complete Handoff Example

A simplified version:

```python
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()


math_agent = Agent(
    name="Math Tutor",
    instructions="""
    You are a helpful math tutor.
    Solve math questions clearly.
    Explain calculations step by step.
    """,
    model="YOUR_MODEL_NAME",
    handoff_description="Handles mathematical questions and calculations."
)


history_agent = Agent(
    name="History Tutor",
    instructions="""
    You are a helpful history tutor.
    Answer history questions clearly.
    Include useful historical context.
    """,
    model="YOUR_MODEL_NAME",
    handoff_description="Handles questions about history and historical events."
)


triage_agent = Agent(
    name="Triage",
    instructions="""
    You are a routing agent.

    Send math questions to the Math Tutor.
    Send history questions to the History Tutor.
    """,
    model="YOUR_MODEL_NAME",
    handoffs=[
        math_agent,
        history_agent
    ]
)


result = Runner.run_sync(
    triage_agent,
    "What is 15% of 240?"
)

print(result.final_output)
```

The exact model configuration can vary by SDK/API version; the important part of this lesson is the **agent/handoff structure**.

---

# 22. Trace: Math Question

User asks:

```text
What is 15% of 240?
```

Let's follow every step.

### Step 1

```text
User
 ↓
Triage Agent
```

Triage reads the question.

---

### Step 2

Triage determines:

```text
This is mathematics.
```

---

### Step 3

It selects:

```text
Math Tutor
```

---

### Step 4

Handoff:

```text
Triage
   │
   │ HANDOFF
   ↓
Math Tutor
```

---

### Step 5

Math Tutor solves:

```text
15% of 240

= 15 / 100 × 240

= 36
```

---

### Step 6

Math Tutor produces the answer.

The important architecture is:

```text
User
 ↓
Triage
 ↓
Math Tutor
 ↓
Answer
```

---

# 23. Trace: History Question

Now:

```text
Who built the Great Wall of China?
```

Flow:

```text
User
 ↓
Triage
 ↓
"History question"
 ↓
Handoff
 ↓
History Tutor
 ↓
Answer
```

The Triage Agent doesn't need to answer the history question itself.

Its job is routing.

---

# 24. What Is the Triage Agent's Job?

Think of it as a receptionist.

```text
                   Receptionist
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
    Billing         Technical       Shipping
```

The receptionist doesn't solve every problem.

It asks:

> "Which department should handle this?"

The Triage Agent does something similar:

```text
Triage Agent
=
AI receptionist/router
```

---

# 25. Why Not Just Give One Agent Everything?

You could do:

```text
One giant agent
    │
    ├── Math
    ├── History
    ├── Coding
    ├── Billing
    ├── Shipping
    ├── Research
    └── Everything else
```

But as the system grows, its instructions and tool set can become increasingly complex.

Specialized agents can provide:

```text
Focused instructions
Focused tools
Focused responsibility
Focused behavior
```

For example:

```text
Math Agent
→ Math tools + math instructions

History Agent
→ History tools + history instructions

Coding Agent
→ Code tools + coding instructions
```

---

# 26. Specialization

This is the main benefit of multi-agent systems.

Instead of:

```text
One Agent
knows everything
```

we create:

```text
Specialized Agents
```

For example:

```text
              Triage
                 │
       ┌─────────┼─────────┐
       ↓         ↓         ↓
     Math      History    Coding
     Agent      Agent      Agent
```

Each agent can have a different:

* Instruction set
* Tool set
* Model
* Guardrails
* Output format
* Responsibility

---

# 27. Handoffs With More Agents

The course example has two specialists.

Production systems could have more:

```text
                       Triage
                         │
       ┌───────┬─────────┼────────┬────────┐
       ↓       ↓         ↓        ↓        ↓
    Billing Shipping Technical Account  Refunds
     Agent    Agent     Agent     Agent    Agent
```

The triage agent determines the appropriate destination.

---

# 28. Important Difference From Normal Tool Calling

With normal function tools:

```text
LLM
 ↓
Python function
 ↓
Result
 ↓
LLM
```

With handoffs:

```text
Triage Agent
 ↓
Specialist Agent
 ↓
Specialist handles conversation
```

So a handoff is not simply:

> "Calculate something."

It is:

> "Another agent should now handle this task."

---

# 29. Handoff vs Function Tool

### Function tool

```text
Agent
 ↓
calculate_tax()
 ↓
result
 ↓
Agent continues
```

The function performs a specific operation.

### Handoff

```text
Triage Agent
 ↓
Math Agent
 ↓
Math Agent takes over
```

The handoff transfers responsibility to another agent.

---

# 30. Handoff vs Agent as Tool

This is worth memorizing.

### Handoff

```text
A
 ↓
B
 ↓
B owns the conversation
```

### Agent as Tool

```text
A
 ↓
B
 ↓
result
 ↓
A
```

### Memory trick

> **Handoff = "You take it from here."**

> **Agent as Tool = "Go do this and report back."**

---

# 31. Manager Architecture

Now let's visualize the second pattern.

```text
                         USER
                           │
                           ▼
                       MANAGER
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
        Researcher       Writer       Reviewer
          Agent           Agent          Agent
             │             │             │
             └─────────────┼─────────────┘
                           ↓
                       MANAGER
                           │
                           ↓
                     Final Answer
```

The Manager stays in control.

---

# 32. Handoff Architecture

Compare:

```text
                         USER
                           │
                           ▼
                        TRIAGE
                           │
                    ┌──────┴──────┐
                    ↓             ↓
                  Math          History
                  Agent          Agent
                    │
                    └── takes over
```

The specialist becomes the active agent.

---

# 33. The Most Important Question

When designing a multi-agent system, ask:

> **Do I want to transfer control or delegate work?**

### Transfer control

```text
Handoff
```

### Delegate work but retain control

```text
Manager + Agent as Tool
```

This single question will help you distinguish the two architectures.

---

# 34. Complete Comparison

```text
HANDOFF
=======

User
 ↓
Triage
 ↓
Specialist
 ↓
Final response

Control:
Triage → Specialist


MANAGER
=======

User
 ↓
Manager
 ↓
Specialist
 ↓
Result
 ↓
Manager
 ↓
Another specialist
 ↓
Result
 ↓
Manager
 ↓
Final response

Control:
Manager → Manager → Manager
```

---

# 35. Core Pattern 🧠

### Handoff pattern

> **Route → Transfer control → Specialist takes over**

```text
Triage
 ↓
Choose specialist
 ↓
Handoff
 ↓
Specialist
 ↓
Answer
```

### Manager pattern

> **Manager → Delegate → Receive result → Coordinate → Final answer**

```text
Manager
 ↓
Specialist
 ↓
Result
 ↓
Manager
 ↓
Final answer
```

---

# 36. Remember This Pattern

### Handoffs

```python
triage_agent = Agent(
    name="Triage",
    instructions="Route the question.",
    handoffs=[
        math_agent,
        history_agent
    ]
)
```

The mental model:

```text
handoffs=[agents]
        ↓
"These agents can take over from me."
```

---

# 37. Handoff Description

One small but important detail:

```python
handoff_description="Handles mathematical questions and calculations."
```

This helps describe **when the handoff should be selected**.

Think:

```text
Agent instructions
=
"What should this agent do?"

Handoff description
=
"When should the triage agent send work here?"
```

That's an excellent distinction to remember.

---

# 38. Full Architecture of the Lesson

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │  Triage Agent   │
                  │                 │
                  │ "Who should     │
                  │  handle this?"  │
                  └────────┬────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
            Math question       History question
                 │                   │
                 ▼                   ▼
          ┌─────────────┐     ┌──────────────┐
          │ Math Tutor  │     │History Tutor │
          └──────┬──────┘     └──────┬───────┘
                 │                   │
                 ▼                   ▼
              Answer              Answer
```

---

# 39. How This Fits Into the Agents SDK

You've now learned:

```text
                 Agents SDK
                     │
        ┌────────────┼─────────────┐
        ↓            ↓             ↓
      Agent        Runner         Tools
        │
        ├── Instructions
        ├── Model
        ├── Tools
        ├── Handoffs
        └── Guardrails
```

Handoffs add another layer:

```text
Agent A
   │
   │ handoff
   ↓
Agent B
```

This lets you construct multi-agent systems.

---

# 40. Final Mental Model

Keep this diagram in your notes:

```text
                 MULTI-AGENT SYSTEMS
                         │
             ┌───────────┴───────────┐
             ↓                       ↓
         HANDOFF                  MANAGER
      Decentralized              Centralized
             │                       │
             ↓                       ↓
        Triage Agent             Manager Agent
             │                       │
       chooses specialist      calls specialists
             │                  as tools
             ↓                       │
       Specialist                  Result
             │                       │
       TAKES CONTROL                ↓
                               Manager stays
                                 in control
```

## One-line takeaway

> **Handoffs transfer control from one agent to another; the Manager pattern keeps one central agent in control and uses specialized agents as tools.**

## Three patterns you've now learned

```text
1. Single Agent
   User → Agent → Tools → Answer

2. Handoff
   User → Triage → Specialist takes over

3. Manager
   User → Manager → Specialist → Manager → Answer
```

### Memorize this:

> **Handoff = "You take over."**

> **Manager = "You do this and report back."**
