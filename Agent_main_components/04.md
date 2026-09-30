# OCI Enterprise AI Agents — From Local Development to Production

## 1. The Big Picture

OCI Enterprise AI Agents Service provides **two major approaches** for building agentic applications.

```text
Approach 1
API Consumption

Your Application
      ↓
OCI Responses API
      ↓
OCI AI Infrastructure
```

and:

```text
Approach 2
Managed Application Deployment

Your Agent
      ↓
Container
      ↓
OCI Hosted Application
      ↓
Production Endpoint
```

The biggest difference is:

> **Where does your application run, and who manages the application runtime?**

---

# 2. Approach 1 — Build Agents with OCI Responses API

In this approach, **you run the application yourself**.

Your application could run on:

* Your laptop
* A VM
* Kubernetes
* Enterprise infrastructure
* A custom backend
* Another application

Your application then calls the **OCI Responses API**.

```text
                    YOUR SIDE
┌─────────────────────────────────────────┐
│                                         │
│ Laptop / VM / Kubernetes / Backend      │
│                                         │
│ Your Agent Application                  │
│                                         │
└──────────────────┬──────────────────────┘
                   │
                   │ API call
                   ▼
             OCI Responses API
                   │
                   ▼
          OCI AI Infrastructure
```

### What OCI manages

According to the lesson, OCI manages things such as:

* AI infrastructure
* Model execution
* Built-in tool reasoning capabilities

### What you manage

You manage your own application/runtime environment.

For example:

* Your Python application
* Your framework
* Your server
* Your deployment environment
* Your application logic

---

# 3. Example — Using OCI Responses API

Earlier in the course, you used the OpenAI SDK and changed the base URL to point toward OCI.

Conceptually:

```text
Your Python Code
       ↓
OpenAI-compatible SDK
       ↓
OCI Responses API
       ↓
OCI Model
       ↓
Response
```

The important thing is:

**Your application stays outside OCI's hosted agent application runtime.**

You are consuming OCI's AI capabilities through an API.

---

# 4. Approach 1 Mental Model

Think of it like using a cloud API.

For example:

```text
Your Application
      │
      │ HTTPS/API
      ▼
Cloud Service
      │
      ▼
Result
```

You don't move your entire application into the cloud service.

You simply **call the service**.

### Therefore:

> **Responses API approach = API consumption**

---

# 5. Approach 2 — Hosted Application Deployment

The second approach is different.

Instead of keeping your entire agent application outside OCI, you **deploy the agent application onto OCI**.

You can still build the agent using frameworks you already learned:

* LangChain
* LangGraph
* OpenAI Agents SDK
* Other supported frameworks

The basic architecture becomes:

```text
Your Agent Code
      ↓
Container
      ↓
OCI
      ↓
Managed Agent Application
      ↓
HTTP Endpoint
      ↓
Users / Other Agents / Applications
```

Here OCI is not merely providing the model.

OCI also hosts the **agent application itself**.

---

# 6. Why Containerize the Agent?

Suppose your agent contains:

```text
agent.py
requirements.txt
Python dependencies
configuration
framework
tools
```

You need a consistent environment in which the application can run.

A **Docker container** packages the application and its dependencies together.

Conceptually:

```text
Your Agent
   +
Dependencies
   +
Runtime
   ↓
Docker Image
```

This image can then be deployed to OCI.

---

# 7. Complete Deployment Process

The lesson describes a sequence of steps.

Remember this order:

```text
1. Build
2. Containerize
3. Push
4. Create Application
5. Create Deployment
6. Get Endpoint
7. Serve Requests
```

Let's go through each one.

---

# 8. Step 1 — Develop the Agent Locally

First, build and test your agent on your local machine.

You can use frameworks such as:

```text
LangChain
LangGraph
OpenAI Agents SDK
Other frameworks
```

Example:

```text
User
 ↓
Your Agent
 ↓
LLM
 ↓
Tools
 ↓
Final Answer
```

At this stage you're mainly focused on:

* Agent behavior
* Prompts/instructions
* Tools
* Handoffs
* Guardrails
* Testing

---

# 9. Step 2 — Containerize the Agent

Once your agent works, package it into a container.

You create a **Docker image** containing:

* Agent code
* Dependencies
* Required runtime environment

Conceptually:

```text
agent.py
requirements.txt
Dockerfile
other code
     │
     ▼
Docker Build
     │
     ▼
Docker Image
```

The Docker image becomes a portable package for your application.

---

# 10. Step 3 — Upload Image to OCIR

OCI provides a managed container registry called:

**OCIR = Oracle Cloud Infrastructure Registry**

You push your Docker image to OCIR.

```text
Local Docker Image
       │
       │ push
       ▼
      OCIR
       │
       ▼
Container Image Stored
```

Now OCI can retrieve your agent image when deploying it.

---

# 11. Step 4 — Create a Generative AI Application

The lesson introduces a concept called a **Generative AI Application**.

Think of this as a **container/context for your deployed agent application**.

It is where you configure application-level concerns such as:

* Scaling
* Storage
* Networking
* Authentication

Mental model:

```text
Generative AI Application
        │
        ├── Scaling
        ├── Storage
        ├── Networking
        ├── Authentication
        │
        └── Deployments
```

---

# 12. Step 5 — Create a Deployment

Inside the Generative AI Application, you create a **deployment**.

You select the container image that you uploaded to OCIR.

```text
OCIR
 │
 │ container image
 ▼
Generative AI Application
 │
 ▼
Deployment
```

The deployment is the running version of your agent application.

---

# 13. Application vs Deployment

This distinction is important.

### Application

Think:

> **The overall package/context for the application.**

It handles things such as:

* Scaling
* Networking
* Storage
* Authentication

### Deployment

Think:

> **The actual deployed instance/version of your agent.**

It uses your container image and serves requests.

Simple analogy:

```text
Application = Restaurant
Deployment  = Running kitchen/service
```

The application provides the environment/configuration.

The deployment is what actually runs your containerized agent.

---

# 14. Step 6 — OCI Provides an HTTP Endpoint

Once the application/deployment is provisioned, OCI provides an **HTTP endpoint**.

For example, conceptually:

```text
https://your-agent.example.com
```

Your clients can then send requests to that endpoint.

```text
Client
   │
   │ HTTP request
   ▼
OCI Agent Endpoint
   │
   ▼
Your Agent
   │
   ▼
Response
```

---

# 15. Who Can Call the Endpoint?

The endpoint can be used by:

### Users

```text
User
 ↓
Application
 ↓
Agent Endpoint
```

### Applications

```text
Enterprise App
 ↓
Agent Endpoint
```

### Other agents

This is especially useful for multi-agent systems.

```text
Agent A
   ↓
HTTP
   ↓
Agent B
```

So one deployed agent can become a service that other systems call.

---

# 16. Full Hosted Deployment Architecture

Put all the steps together:

```text
                    DEVELOPMENT
                         │
                         ▼
                  Build Agent
                         │
                         ▼
                 Docker Container
                         │
                         ▼
                    Docker Image
                         │
                         │ push
                         ▼
                       OCIR
                         │
                         │ pull image
                         ▼
          ┌────────────────────────────┐
          │ Generative AI Application  │
          │                            │
          │ Scaling                    │
          │ Networking                │
          │ Storage                   │
          │ Authentication            │
          │                            │
          │   ┌────────────────────┐   │
          │   │    Deployment      │   │
          │   │                    │   │
          │   │ Your Agent         │   │
          │   │ Container          │   │
          │   └─────────┬──────────┘   │
          └─────────────┼──────────────┘
                        │
                        ▼
                  HTTP Endpoint
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
           Users     Apps       Agents
```

---

# 17. Approach 1 vs Approach 2

This is the most important comparison from the lesson.

|                                       | Responses API              | Hosted Application               |
| ------------------------------------- | -------------------------- | -------------------------------- |
| Where agent application runs          | Wherever you choose        | OCI                              |
| How you use OCI                       | API                        | Managed deployment               |
| Your code                             | Runs in your environment   | Containerized and deployed       |
| OCI manages model infrastructure      | Yes                        | Yes                              |
| OCI manages agent application runtime | Mostly your responsibility | OCI-managed                      |
| Container required                    | Not necessarily            | Yes, according to this workflow  |
| OCI endpoint                          | API endpoint you call      | Endpoint for your deployed agent |
| Main idea                             | API consumption            | Managed application deployment   |

---

# 18. The Simplest Difference

If you remember nothing else, remember this:

### Approach 1

> **"I run my agent. OCI gives me AI capabilities."**

```text
MY APP → OCI API
```

### Approach 2

> **"I give OCI my containerized agent. OCI runs the agent for me."**

```text
MY AGENT → OCI HOSTED DEPLOYMENT
```

---

# 19. Local Development → Production

The second approach gives you a clear development-to-production path.

### Local

```text
Laptop
 ↓
Python
 ↓
Agent
```

### Package

```text
Agent
 ↓
Docker Image
```

### Registry

```text
Docker Image
 ↓
OCIR
```

### Deploy

```text
OCIR
 ↓
Generative AI Application
 ↓
Deployment
```

### Production

```text
Users / Apps / Agents
        ↓
   HTTP Endpoint
        ↓
  OCI Deployment
        ↓
   Your Agent
```

---

# 20. Why Is This Different From Just Calling an API?

Suppose you use the Responses API:

```text
Your Server
   ↓
OCI Responses API
   ↓
Model
```

Your server still exists outside OCI.

You are responsible for operating that server.

With hosted application deployment:

```text
Client
   ↓
OCI Endpoint
   ↓
OCI Runtime
   ↓
Your Agent Container
```

OCI is now responsible for more of the application runtime infrastructure.

According to the lesson, this includes concerns such as:

* Scaling
* Networking
* Authentication
* Endpoints
* Runtime infrastructure
* Production deployment

---

# 21. Connection to the Runtime Architecture Lesson

This lesson connects directly to what you learned previously about **runtime architecture**.

Earlier:

> **Agent logic = brain**

> **Runtime architecture = infrastructure that allows the brain to operate reliably**

Now we can map the two approaches.

### Approach 1 — You manage runtime

```text
Users
 ↓
Your API/server
 ↓
Your Agent
 ↓
OCI Responses API
```

You still need to think about your own:

* Server
* Scaling
* Networking
* Authentication
* Deployment
* Monitoring
* Reliability

### Approach 2 — OCI hosts the application

```text
Users
 ↓
OCI Endpoint
 ↓
OCI Managed Runtime
 ↓
Your Agent Container
 ↓
Models / Tools
```

More of the runtime infrastructure is handled by OCI.

---

# 22. Framework Independence

An important point:

The hosted deployment approach isn't limited to one agent framework.

You could build your agent using:

```text
LangChain
LangGraph
OpenAI Agents SDK
Other supported frameworks
```

The important step is:

```text
Framework
   ↓
Agent Application
   ↓
Containerize
   ↓
Deploy
```

So the framework defines your **agent logic**, while OCI provides the **deployment/runtime environment**.

---

# 23. When to Think About Each Approach

### Responses API approach

Think:

> "I already have an application/backend and just need OCI's AI capabilities."

Example:

```text
Existing Enterprise Backend
        ↓
OCI Responses API
        ↓
AI capability
```

This can be convenient when you want to retain control of your application's infrastructure.

---

### Hosted application approach

Think:

> "I have built an agent and want OCI to host it as a managed service."

Example:

```text
Agent
 ↓
Docker
 ↓
OCIR
 ↓
OCI Generative AI Application
 ↓
Deployment
 ↓
HTTP Endpoint
```

This is particularly relevant when moving from local experimentation toward a managed production deployment.

---

# 24. Interview Questions

### Q1. What are the two ways to build agents using OCI Enterprise AI Agents Service?

1. Build an agent using the OCI Responses API.
2. Deploy the agent as a hosted application on OCI.

---

### Q2. What is the main difference?

The primary difference is **where the agent application runs and who manages its runtime/orchestration infrastructure**.

---

### Q3. Does the Responses API require you to deploy your whole application on OCI?

No.

Your application can run on:

* Laptop
* VM
* Kubernetes
* Enterprise infrastructure
* Custom backend

and call OCI through the Responses API.

---

### Q4. What is OCIR?

**OCIR = Oracle Cloud Infrastructure Registry.**

It is OCI's managed container registry used to store container images.

---

### Q5. Why containerize the agent?

To package:

* Application code
* Dependencies
* Runtime environment

into a portable container image that can be deployed consistently.

---

### Q6. What is the deployment flow?

Memorize:

```text
Build
 ↓
Containerize
 ↓
Push to OCIR
 ↓
Create Generative AI Application
 ↓
Create Deployment
 ↓
OCI provides endpoint
 ↓
Serve requests
```

---

### Q7. What is a Generative AI Application?

In this lesson's deployment model, it acts as the application-level context/configuration around the hosted agent, including concerns such as:

* Scaling
* Storage
* Networking
* Authentication

---

### Q8. What is a Deployment?

The deployment uses the selected container image and runs the agent application so it can serve requests.

---

# 25. Final Revision Sheet

## Two OCI Agent Deployment Approaches

### 🟦 Approach 1 — Responses API

```text
Your Application
      ↓
OCI Responses API
      ↓
OCI AI Infrastructure
```

**Remember:**

> **You run the application; OCI provides the AI service.**

---

### 🟩 Approach 2 — Hosted Application

```text
Build Agent
     ↓
Dockerize
     ↓
Push to OCIR
     ↓
Create Generative AI Application
     ↓
Create Deployment
     ↓
HTTP Endpoint
     ↓
Users / Apps / Agents
```

**Remember:**

> **You package the agent; OCI hosts and manages the production application runtime.**

---

# 26. One-Line Mental Model

> **Responses API = "OCI, give my application AI capabilities."**

> **Hosted deployment = "OCI, run my agent application for me."**

And the complete production journey is:

```text
LOCAL AGENT
    ↓
CONTAINERIZE
    ↓
OCIR
    ↓
GENERATIVE AI APPLICATION
    ↓
DEPLOYMENT
    ↓
HTTP ENDPOINT
    ↓
PRODUCTION AGENT
```

That is the central concept of this lesson.
