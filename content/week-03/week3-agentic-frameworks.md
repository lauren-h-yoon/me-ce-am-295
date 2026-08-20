---
title: "Week3 Agentic Frameworks"
week: 3
doc_type: "lecture_notes"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 3/Week3_Agentic_Frameworks.docx"
source_hash: "fdaaa96a45e28b8e"
normalized_at: "2026-08-19T11:55:19Z"
---
# ME/CE 295 --- Week 3 Lecture Notes

# Agentic Frameworks and Multi-Agent Systems

**California Institute of Technology --- Division of Engineering and Applied Science Course: ME/CE 295 --- AI Agents for Accelerating Scientific Discovery and Engineering Research Week: 3 of 10 Lectures: Tuesday & Thursday, 1:00–2:30 p.m. (2 × 1.5 hours) \| Laboratory: 5 hours, at-home (see separate lab handout)**

## Lecture Outline at a Glance

The following table summarizes the lecture structure, delivered as two 90-minute sessions: 0:00–1:30 on Tuesday and 1:30–3:00 (including the lab briefing) on Thursday. This session transitions from static prompt engineering to dynamic, autonomous systems capable of executing actions in engineering environments.

| **Time** | **Duration** | **Topic** | **Key Takeaway** |
|----|----|----|----|
| 0:00--0:10 | 10 min | Review and Week 3 Objectives | Moving from static prompts to autonomous agents |
| 0:10--0:25 | 15 min | Pillar 1: Planning and Task Decomposition | ReAct paradigm and Reflexion |
| 0:25--0:40 | 15 min | Pillar 2: Memory Architectures | Short-term, working, and long-term memory |
| 0:40--0:50 | 10 min | Pillar 3: Tool Use (Function Calling) | Interacting with the outside world via schemas |
| 0:50--1:00 | 10 min | *Break* |  |
| 1:00--1:25 | 25 min | Single-Agent Frameworks: LangChain | Building a ReAct agent with custom Python tools |
| 1:25--1:50 | 25 min | Implementing State and Memory | Managing conversation history and debugging |
| 1:50--2:00 | 10 min | *Break* |  |
| 2:00--2:15 | 15 min | Minsky's "Society of Mind" | The philosophy of emergent intelligence |
| 2:15--2:35 | 20 min | Multi-Agent Orchestration | AutoGen and CrewAI for role-based teams |
| 2:35--2:50 | 15 min | Lab 3 Briefing | Building a Designer/Checker agent system |
| 2:50--3:00 | 10 min | Q&A and Transition to Lab |  |

## Part I --- The Anatomy of an AI Agent

In the previous weeks, we treated Large Language Models (LLMs) as advanced calculators and data extractors. You provided a prompt, and the model returned an answer. However, this static paradigm is insufficient for complex engineering tasks, such as running a finite element analysis, parsing the error logs, adjusting the mesh, and re-running the simulation. To achieve this level of autonomy, we must wrap the LLM in an agentic framework. An AI agent is a system where an LLM acts as the central reasoning engine to drive external actions. Modern agent architectures rely on three foundational pillars: planning, memory, and tool use.

### 1. Planning and Task Decomposition

Complex engineering goals cannot be solved in a single forward pass of a neural network. They must be decomposed into manageable subtasks. The most influential framework for agent planning is the **ReAct (Reasoning and Acting)** paradigm, introduced by Yao et al. in 2022 [<u>1</u>](https://arxiv.org/abs/2210.03629). ReAct interleaves reasoning traces (thoughts) with task-specific actions. Instead of simply generating an answer, the model generates a "Thought" about what it needs to do, selects an "Action" to perform, receives an "Observation" from the environment, and then generates a new "Thought" based on that observation. This iterative loop allows the agent to induce, track, and update action plans while handling exceptions dynamically. Research demonstrated that ReAct agents outperformed traditional reinforcement learning methods by significant margins on interactive decision-making benchmarks [<u>1</u>](https://arxiv.org/abs/2210.03629).

Beyond basic planning, advanced agents employ self-correction mechanisms. The **Reflexion** framework, introduced by Shinn et al. in 2023, equips agents with the ability to learn from their mistakes through verbal reinforcement [<u>2</u>](https://arxiv.org/abs/2303.11366). If an agent attempts to execute a Python script to calculate beam deflection and the script crashes due to a syntax error, a Reflexion agent will analyze the traceback, generate a linguistic reflection on why the failure occurred, and store this reflection in its memory. In subsequent attempts, the agent uses this reflection to avoid repeating the same error. This process mimics human engineering intuition, allowing the system to improve its performance without requiring expensive weight updates to the underlying neural network.

### 2. Memory Architectures

An agent without memory is akin to an engineer with amnesia; it cannot learn from past interactions or maintain context over a long project. Agent memory is typically divided into three distinct architectures [<u>3</u>](https://www.ibm.com/think/topics/ai-agent-memory).

**Short-term memory** refers to the in-context learning capabilities of the model, bounded by its context window. This includes the immediate conversation history and the current prompt. It allows the agent to respond coherently to follow-up questions within a single session. **Working memory** acts as a temporary scratchpad where the agent stores intermediate variables, such as the parsed dimensions of a truss structure, before passing them to a simulation tool.

**Long-term memory** provides persistent storage across multiple sessions and days. Because it is impossible to fit an entire library of past projects into a single context window, long-term memory is often implemented using vector databases. When an agent encounters a new problem, it embeds the query and performs a similarity search against the vector database to retrieve relevant past experiences or reference documents. This architecture will be explored in depth during Week 4 when we build Retrieval-Augmented Generation (RAG) systems.

### 3. Tool Use (Function Calling)

The defining characteristic of an agent is its ability to affect the external world through **tool use**. Without tools, an LLM is confined to text generation. With tools, it can query databases, execute Python code, trigger API endpoints, and run proprietary engineering software.

Tools are provided to the agent as a list of JSON schemas. Each schema contains the name of the tool, a detailed natural language description of what the tool does, and the required input parameters defined via data validation libraries like Pydantic. When the LLM's reasoning engine determines that it needs external information—for example, the yield strength of A992 steel—it generates a structured JSON object requesting the get_material_properties tool. The agent framework intercepts this request, executes the corresponding Python function locally, and returns the result back to the LLM as an observation. The quality of an agent's performance is heavily dependent on the clarity of the tool descriptions; ambiguous docstrings will cause the model to select the wrong tool or hallucinate parameters.

## Part II --- Single-Agent Frameworks in Practice

To transition from theory to implementation, engineers rely on orchestration frameworks that handle the complex routing of prompts, tool executions, and memory management.

### 4. Introduction to LangChain and LangGraph

**LangChain** has emerged as the industry standard for building tool-augmented agents. It provides a highly modular architecture for connecting LLMs to external data sources and execution environments [<u>4</u>](https://python.langchain.com/docs/concepts/agents/). The framework abstracts away the boilerplate code required to maintain the ReAct loop.

In modern LangChain implementations, tools are defined using the @tool decorator in Python. By simply adding this decorator to a standard Python function and providing a descriptive docstring, the function is automatically converted into a schema that the LLM can understand. For example, an engineer can define a function that calculates the moment of inertia for various cross-sections, decorate it, and pass it to the agent initialization function. LangChain's underlying runtime, **LangGraph**, handles the stateful, cyclic execution of the agent, ensuring that the system can reliably loop between thoughts and actions until a final answer is reached [<u>4</u>](https://python.langchain.com/docs/concepts/agents/).

### 5. Implementing State and Memory

Stateless API calls are insufficient for engineering design workflows that require iterative refinement. LangChain provides mechanisms to inject state and memory into the agent loop. By maintaining a structured message history, the agent can recall that the user previously specified a "simply supported boundary condition" even when discussing the load cases several turns later.

Debugging these stateful systems can be challenging, as the agent may execute dozens of hidden steps before returning a final response to the user. Engineers utilize observability platforms like LangSmith to visualize the execution traces. These traces reveal the exact sequence of tools the agent attempted to use, the raw inputs it provided to those tools, and the errors it encountered, allowing the developer to refine the tool descriptions and system prompts.

## Part III --- The Society of Mind: Multi-Agent Systems

While single-agent systems are powerful for well-defined tasks, they struggle with open-ended, multi-domain engineering problems. A single prompt cannot effectively encompass the diverse expertise required to conceptualize, design, analyze, and review a complex structural system.

### 6. Minsky's Philosophy and Emergent Intelligence

In 1986, cognitive scientist Marvin Minsky published *The Society of Mind*, proposing that human intelligence is not the product of a single monolithic mechanism, but rather the emergent property of interactions between many simple, specialized "agents" operating within the brain [<u>5</u>](https://en.wikipedia.org/wiki/Society_of_Mind). Modern multi-agent AI systems embody this exact philosophy.

Instead of prompting one massive model to perform an entire structural design, engineers instantiate multiple specialized agents. One agent acts as the conceptual designer, another as the finite element analyst, and a third as the building code compliance reviewer. By restricting each agent's scope and providing them with specialized tools, the overall system achieves higher accuracy and exhibits complex problem-solving capabilities that no single agent could manage alone [<u>6</u>](https://arxiv.org/abs/2501.00000).

### 7. Multi-Agent Orchestration: AutoGen and CrewAI

Several frameworks have been developed to orchestrate these multi-agent interactions.

**Microsoft AutoGen** is an open-source framework designed around conversational agents [<u>7</u>](https://microsoft.github.io/autogen/). In AutoGen, agents collaborate by sending messages to one another. A typical setup involves an AssistantAgent that generates Python code to solve a problem, and a UserProxyAgent that executes the code in a secure local environment and reports the terminal output back to the assistant. This creates an autonomous loop of coding, testing, and debugging.

**CrewAI** takes a role-based approach, explicitly designed to mimic human engineering teams [<u>8</u>](https://docs.crewai.com/). In CrewAI, the developer defines specific agents with distinct roles, goals, and backstories. For example, a "Senior Structural Engineer" agent might be tasked with sizing a column, while a "Quality Assurance Reviewer" agent is tasked with aggressively critiquing the design against buckling limits. The framework allows developers to define sequential or hierarchical processes, ensuring that the design passes through the necessary review gates before the final output is delivered to the user.

## Assigned Reading for Week 3

| **Priority** | **Reference** | **Description** |
|----|----|----|
| **Required** | Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." *arXiv:2210.03629*. | The foundational paper defining the thought-action loop. |
| **Required** | Elrefaie, M. et al. (2025). "AI Agents in Engineering Design: A Multi-Agent Framework." | Application of multi-agent systems to mechanical design. |
| **Supplementary** | Shinn, N. et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." *arXiv:2303.11366*. | Framework for agent self-correction and reflection. |
| **Supplementary** | LangChain Documentation (2026). "Agents Concepts." | Technical guide on implementing tools and ReAct loops. |

## References

Part IV --- The Authority Problem: Instruction Hierarchy in Agentic Systems

The frameworks discussed above — AutoGen, CrewAI, LangGraph — solve the inter-agent coordination problem elegantly. A hub agent delegates to specialist spokes; a manager reviews worker outputs; a graph routes messages deterministically. However, none of these frameworks address a more fundamental challenge: what happens when a single agent receives contradictory instructions from multiple sources?

This is the instruction hierarchy problem, and recent research demonstrates that it is one of the most critical unsolved challenges in deploying reliable agentic systems for engineering.

1.  The Scale of the Problem

In April 2026, Zhang et al. at Johns Hopkins University published "Many-Tier Instruction Hierarchy in LLM Agents" (arXiv:2604.09443), introducing the ManyIH-Bench benchmark. The benchmark comprises 853 agentic tasks across 46 real-world agents, with up to 12 levels of conflicting instructions carrying different privilege levels. The results are sobering: even the best-performing frontier model (Claude Opus 4.6) achieved only 51.3% accuracy, while GPT-5.4 scored 39.5%. These same models score above 99% on simple two-tier evaluations (system prompt versus user prompt). The capability does not generalize. Models are not reasoning about authority — they are pattern-matching it.

The key finding is that accuracy degrades monotonically above 6 privilege tiers and collapses entirely above 8. This establishes a hard design constraint for practitioners: explicit authority hierarchies must be kept under 6 tiers, and models must never be expected to infer authority from context alone.

1.  Zones versus Hierarchy: Two Orthogonal Problems

It is essential to distinguish between two related but orthogonal governance mechanisms.

Action Authorization (Zones) answers the question: "Is this agent permitted to perform this action?" A zone-based system classifies actions by risk level. Green-zone actions (read a file, perform a calculation) proceed without approval. Yellow-zone actions (modify a design parameter, write to a shared database) require logging. Red-zone actions (send an email to a client, delete a file, publish results) require explicit human approval. This is access control — it gates what the agent can do, regardless of which instruction triggered the request.

Instruction Hierarchy answers a different question: "Which instruction should the agent follow when multiple instructions disagree?" A human directive (high authority) can authorize a red-zone action (high risk). A tool output (low authority) cannot. The zone gates the action; the hierarchy gates the instruction.

In Week 7, when we discuss sandboxing and code execution, we will revisit the zone concept in the context of action authorization. The instruction hierarchy is the complementary mechanism that determines whose voice the agent obeys.

1.  The 5-Tier Design Pattern

Based on the ManyIH paper finding that models can reliably handle up to 5-6 explicit tiers, practitioners have converged on a compressed priority table:

Priority P1 — Platform: Model safety layer, built-in constraints, tool schemas. Cannot be overridden. Not in developer control.

Priority P2 — Human-Live: The engineer real-time directive in this session. Always wins over everything below.

Priority P3 — Governance: Shared permissions, anti-patterns, settled project decisions. Overrides playbooks and memory. Only P2 can override.

Priority P4 — Playbook: Agent-specific instructions, domain boundaries. Overrides context. P2/P3 can override.

Priority P5 — Context: Memory files, tool outputs, search results, retrieved documents. Informs but never overrides.

Same-tier tiebreakers follow three rules: (1) more recent information beats older information; (2) more specific instructions beat more general ones; (3) observed facts beat inferred conclusions.

For the multi-agent systems built in this course — and particularly for the Self-Driving Laboratory workflows in Week 8 — the instruction hierarchy has direct practical consequences. Engineers must encode the priority table explicitly in the governance file that every agent inherits at session start, compress instruction sources into no more than 5 tiers, flag same-tier contradictions to the human operator rather than silently resolving them, and test for regression as prompts evolve over the project lifecycle.

## Part IV --- Coordination at Scale: From Demo to Production

### 11. When Central Orchestration Becomes a Bottleneck

The multi-agent systems introduced in Part III typically rely on a central coordinating layer (the "manager" agent) for task distribution. Early on this works well — providing a clear control point and making it easier to see how tasks are assigned.

However, as the system grows, that central layer accumulates responsibility. It must understand every agent, every tool, and every interaction pattern. Small changes elsewhere require corresponding changes in orchestration logic. What started as a simplifying abstraction gradually turns into a bottleneck — both in performance and in maintainability (Cognizant AI Lab, 2026).

**Key insight:** A single request might be interpreted differently by multiple agents, each operating with its own context and capabilities. The question of *who should act* is no longer something that can be answered cleanly in one place.

### 12. Adaptive Agent-Oriented Software Architecture (AAOSA)

An alternative to centralized orchestration is AAOSA — Adaptive Agent-Oriented Software Architecture — implemented in Cognizant's open-source **neuro-san** framework (Apache 2.0).

In AAOSA, coordination works differently:

- **Agents claim responsibility** rather than being assigned work

- Each agent evaluates incoming input and determines whether it can contribute

- Claims are combined into a coordinated response

- No single component "owns" coordination — it emerges from agent interactions

**Practical implications for scaling:**

- Adding a new agent does not require updating a central routing layer

- Agents remain modular and independently deployable

- Groups of agents can coordinate within their own scope while contributing to higher-level workflows

- Ambiguity is resolved collectively rather than forced into a single interpretation early

### 13. The Demo-to-Production Gap in Multi-Agent Systems

Research across production multi-agent systems demonstrates failure rates ranging from 41% to 86.7% (Zheng et al., 2026; Augment Code, 2026). The most common failure modes:

| **Failure Mode** | **Description** | **Root Cause** |
|----|----|----|
| Coordination breakdown | Agents misinterpret roles or duplicate work | Specification ambiguity |
| Context bloat | Full conversation histories passed between agents | No information filtering |
| Latency cascades | Sequential agent chains turn 3s demos into 30s delays | Lack of parallelism |
| State inconsistency | Agents work from cached data after updates | No single source of truth |

**The 79% Rule:** Research identifies specification ambiguity and unstructured coordination protocols as the source of 79% of production breakdowns (Augment Code, 2026).

**Solutions framework:**

1.  Treat specifications like API contracts (JSON schemas for everything)

2.  Explicit ownership boundaries per agent

3.  Automatic constraint validation

4.  Operating contracts with clear acceptance criteria and stop conditions

Updated Assigned Reading for Week 3

PriorityReferenceDescription

RequiredYao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." arXiv:2210.03629.The foundational paper defining the thought-action loop.

RequiredElrefaie, M. et al. (2025). "AI Agents in Engineering Design: A Multi-Agent Framework."Application of multi-agent systems to mechanical design.

RequiredZhang, J. et al. (2026). "Many-Tier Instruction Hierarchy in LLM Agents." arXiv:2604.09443.Benchmark demonstrating that frontier models fail at multi-tier instruction conflict resolution.

SupplementaryShinn, N. et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." arXiv:2303.11366.Framework for agent self-correction and reflection.

SupplementaryLangChain Documentation (2026). "Agents Concepts."Technical guide on implementing tools and ReAct loops.

RequiredCognizant AI Lab (2026). "Why Your Multi-Agent Network Works in Demo but Falls Apart in the Wild." Decision AI Bytes.Production challenges of multi-agent systems: coordination, integration, reliability, data control.

SupplementaryNeuro-san Documentation (2026). GitHub: cognizant-ai-labs/neuro-san (Apache 2.0).Open-source framework implementing AAOSA for scalable multi-agent coordination.

References

1.  Zhang, J., Li, T., Jurayj, W., Zhan, H., Van Durme, B., & Khashabi, D. (2026). "Many-Tier Instruction Hierarchy in LLM Agents." arXiv:2604.09443.

2.  Jost, K. (2026). "Your Agents Have an Authority Problem." Internal technical post on instruction hierarchy design patterns for multi-agent systems.
