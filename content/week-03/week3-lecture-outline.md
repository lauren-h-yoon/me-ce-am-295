---
title: "Week3 Lecture Outline"
week: 3
doc_type: "lecture_outline"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 3/Week3_Lecture_Outline.docx"
source_hash: "10ca5c28dc03937e"
normalized_at: "2026-08-19T11:55:19Z"
---
# Week 3 Lecture Outline: Agentic Frameworks and Multi-Agent Systems

**Format: Tuesday & Thursday lectures, 1:00–2:30 p.m. (2 × 90 minutes) + 5-hour at-home laboratory. Target Audience: Mechanical Engineering and Materials Science graduate students and senior undergraduates Prerequisites: Completion of Week 2; familiarity with API calls, Pydantic, and advanced prompting (CoT, ToT).**

*Delivery (Fall 2026): timeline blocks 0:00–1:30 are covered in the Tuesday session; blocks 1:30–3:00, including the laboratory briefing, in the Thursday session. The laboratory is completed at home (5 hours) before the following Tuesday.*

## Hour 1: The Anatomy of an AI Agent (0:00 - 0:50)

**0:00 - 0:10 \| Review and Week 3 Objectives**

- Recap of Week 2: Chain-of-Thought, structured outputs, and context windows.

- The limitation of static prompting: Why LLMs need agency to interact with engineering environments.

- Definition of an AI Agent: An LLM acting as a reasoning engine to drive external actions.

**0:10 - 0:25 \| Pillar 1: Planning and Task Decomposition**

- Breaking down complex engineering goals into actionable subtasks.

- The ReAct (Reasoning and Acting) paradigm: Interleaving thoughts, actions, and observations.

- Reflexion and self-correction: How agents learn from failed actions (e.g., a simulation crashing) without weight updates.

**0:25 - 0:40 \| Pillar 2: Memory Architectures**

- Short-term memory: Context windows and conversation history.

- Working memory: Intermediate state during task execution.

- Long-term memory: Persistent storage across sessions using databases and vector embeddings.

**0:40 - 0:50 \| Pillar 3: Tool Use (Function Calling)**

- How an LLM interacts with the outside world.

- Defining tools using schemas and docstrings.

- The mechanism of tool selection: How the model decides when to calculate a moment of inertia vs. when to query a database.

*10-Minute Break (0:50 - 1:00)*

## Hour 2: Single-Agent Frameworks in Practice (1:00 - 1:50)

**1:00 - 1:25 \| Introduction to LangChain and LangGraph**

- The ecosystem of agent development.

- Building a simple ReAct agent with create_agent().

- The @tool decorator in Python: Turning engineering functions into agent tools.

- Code example: An agent that computes beam deflections using a custom Python math tool.

**1:25 - 1:50 \| Implementing State and Memory in LangChain**

- Moving from stateless API calls to stateful agent sessions.

- Injecting conversation history into the agent's prompt.

- Debugging agent execution traces (e.g., using LangSmith) to understand the thought-action loop.

*10-Minute Break (1:50 - 2:00)*

## Hour 3: The Society of Mind: Multi-Agent Systems (2:00 - 2:50)

**2:00 - 2:15 \| Minsky's "Society of Mind" and Multi-Agent Philosophy**

- Marvin Minsky's theory: Intelligence emerges from the interaction of simple, specialized agents.

- Why single monolithic agents fail at complex engineering design.

- The necessity of specialized roles: Designer, Reviewer, and Manager.

**2:15 - 2:35 \| Multi-Agent Orchestration with AutoGen and CrewAI**

- **Microsoft AutoGen:** Conversational multi-agent systems where agents chat to solve problems and execute code.

- **CrewAI:** Role-based orchestration. Defining an agent's role, goal, and backstory.

- Example Workflow: A structural engineering crew where a "Designer Agent" sizes a column and a "Checker Agent" verifies it against buckling limits.

**2:35 - 2:50 \| Lab 3 Briefing: Building Your First Engineering Agent**

- Overview of Lab 3 tasks:

  - Part A: ReAct agent with a custom moment of inertia tool.

  - Part B: Adding memory for multi-step calculations.

  - Part C: A two-agent Designer/Checker system.

- Q&A and transition to the Lab session.

*End of Lecture (2:50 - 3:00 Buffer)*
