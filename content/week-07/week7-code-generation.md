---
title: "Week7 Code Generation"
week: 7
doc_type: "lecture_notes"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 7/Week7_Code_Generation.docx"
source_hash: "143af5dda234bbe4"
normalized_at: "2026-08-19T11:55:20Z"
---
# ME/CE 295 --- Week 7 Lecture Notes

# LLM-Driven Code Generation and Autonomous Data Analysis

**California Institute of Technology --- Division of Engineering and Applied Science Course: ME/CE 295 --- AI Agents for Accelerating Scientific Discovery and Engineering Research Week: 7 of 10 Lectures: Tuesday & Thursday, 1:00–2:30 p.m. (2 × 1.5 hours) \| Laboratory: 5 hours, at-home (see separate lab handout)**

## Lecture Outline at a Glance

The following table summarizes the lecture structure, delivered as two 90-minute sessions: 0:00–1:30 on Tuesday and 1:30–3:00 (including the lab briefing) on Thursday. This session bridges the gap between natural language reasoning and deterministic engineering software, teaching students how to build agents that write, execute, and debug simulation code.

| **Time** | **Duration** | **Topic** | **Key Takeaway** |
|----|----|----|----|
| 0:00--0:10 | 10 min | Review and Week 7 Objectives | Moving from text generation to executable engineering scripts |
| 0:10--0:30 | 20 min | Reframing Structural Analysis | Why LLMs must write code instead of calculating math directly |
| 0:30--0:50 | 20 min | Domain-Specific Code Generation | Prompting strategies for OpenSees, Abaqus, and OpenFOAM |
| 0:50--1:00 | 10 min | *Break* |  |
| 1:00--1:25 | 25 min | The Execution-Feedback Loop | The core architecture of autonomous coding agents |
| 1:25--1:50 | 25 min | Autonomous Error Correction | Sandboxing, reading stack traces, and self-healing code |
| 1:50--2:00 | 10 min | *Break* |  |
| 2:00--2:30 | 30 min | Data Analysis Pipelines | Automating post-processing, statistics, and visualization |
| 2:30--2:50 | 20 min | Lab 7 Briefing | Building an autonomous OpenSeesPy agent from scratch |
| 2:50--3:00 | 10 min | Q&A and Transition to Lab |  |

## Part I --- The Code Generation Paradigm

In the previous weeks, we explored how AI can be trained to approximate physics via Scientific Machine Learning (PINNs and Neural Operators). However, replacing traditional solvers is not the only way to accelerate engineering. Often, the most practical application of AI is to act as an orchestrator—an intelligent agent that drives existing, highly trusted simulation software.

### 1. Reframing Structural Analysis

A fundamental limitation of Large Language Models is their unreliability with complex, deterministic mathematics. If you ask an LLM to calculate the internal forces of a highly indeterminate 2D frame under a complex load combination, it will likely hallucinate the final numbers, even if it understands the underlying theory. LLMs lack the precision, consistency, and reliability required for direct structural analysis.

To solve this, researchers have successfully reframed structural analysis from an open-ended text generation task to a **structured code generation task** [<u>1</u>](https://arxiv.org/abs/2504.09754). Instead of asking the LLM for the answer, we ask the LLM to write a Python script for a trusted solver (like OpenSeesPy or Abaqus) that will compute the answer. The LLM handles the semantics (interpreting the geometry, materials, and loads from a natural language prompt) and the syntax (writing the API calls), while the traditional Finite Element Analysis (FEA) solver handles the deterministic math.

### 2. Domain-Specific Code Generation

Generating code for specialized engineering software requires a carefully designed architecture. A state-of-the-art framework typically consists of three layers [<u>1</u>](https://arxiv.org/abs/2504.09754):

- **The Data Layer:** This handles prompt engineering. It translates the user's natural language description of the structure into a structured prompt. Crucially, this layer utilizes In-Context Learning (ICL) by providing the LLM with template scripts and API documentation for the target software.

- **The Model Layer:** The LLM itself (e.g., GPT-4o, Claude 3.5 Sonnet) processes the prompt and generates the simulation script.

- **The Output Layer:** The system saves the generated code to a file and executes it within the target environment.

Recent studies have shown that frontier models like GPT-4o can achieve up to 100% accuracy in generating correct OpenSeesPy scripts for standard structural analysis word problems, significantly outperforming earlier models and open-source alternatives [<u>1</u>](https://arxiv.org/abs/2504.09754). Similar frameworks, such as OpenFOAMGPT for Computational Fluid Dynamics (CFD) [<u>2</u>](https://ui.adsabs.harvard.edu/abs/2025PhFl...37c5120P/abstract) and ModSolAgent for Abaqus [<u>3</u>](https://www.researchgate.net/publication/403069552_ModSolAgent_Automated_Finite_Element_Code_Generation_for_Abaqus_via_LLM-Based_Agent), have demonstrated high success rates in automating complex simulation setups.

## Part II --- Execution, Feedback, and Autonomous Debugging

Generating code is only the first step. In practice, the first draft of an LLM-generated simulation script rarely runs perfectly. It may contain syntax errors, reference non-existent API methods, or fail to converge during the numerical solution. To build a truly autonomous agent, we must implement an execution-feedback loop.

### 3. The Execution-Feedback Loop

The core pattern of an autonomous coding agent is the **Generate \$\rightarrow\$ Execute \$\rightarrow\$ Capture \$\rightarrow\$ Feed Back \$\rightarrow\$ Regenerate** loop.

When the LLM generates a script, the agent executes it in a secure environment. If the execution fails, the agent intercepts the standard error (stderr) output—the stack trace. Instead of presenting this error to the human user, the agent feeds the exact error message back into the LLM with a prompt like: *"Your previous code failed with the following error. Analyze the stack trace, explain the bug, and provide the corrected code."*

This creates a "self-healing" paradigm. The LLM reads its own errors and iterates until the code runs successfully. To prevent infinite loops, these systems are typically constrained by a maximum retry limit (usually 3 to 5 iterations).

### 4. Sandboxing and Error Classification

Executing AI-generated code on a host machine presents significant security and stability risks. A hallucinated script could accidentally delete files, consume infinite memory, or execute malicious commands. Therefore, it is a strict best practice to execute LLM-generated code within a **Sandbox**—typically an isolated Docker container with strict resource limits (CPU, memory, and network access) [<u>4</u>](https://arxiv.org/abs/2512.12806).

When building these loops, engineers must classify and handle different types of errors:

- **Syntax and API Errors:** Easily caught by the Python interpreter and easily fixed by the LLM.

- **Runtime Errors:** Issues like dividing by zero or singular stiffness matrices.

- **Physical Implausibility:** The most dangerous "silent" errors. The code runs without crashing, but the results violate physics (e.g., a cantilever beam deflecting upward under gravity). Advanced agents employ "Critic" sub-agents that review the output data against physical heuristics before accepting the result.

## Part III --- Autonomous Data Analysis Pipelines

Beyond setting up simulations, LLMs excel at automating the post-processing and analysis of engineering data. Whether the data comes from a physical experiment (e.g., a tensile test) or a massive CFD simulation, the analysis pipeline can be fully automated.

### 5. LLM-Driven Visualization and Reporting

Data analysis agents follow a multi-stage pipeline [<u>5</u>](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0317084):

1.  **Data Ingestion and Summarization:** The agent reads the raw CSV or JSON files and generates a statistical summary of the dataset's structure.

2.  **Goal Setting:** Based on the user's prompt (e.g., "Compare the ductility of the three steel samples"), the agent determines which statistical tests and visualizations are appropriate.

3.  **Code Generation:** The agent writes Pandas and Matplotlib/Seaborn code to clean the data, perform the analysis, and generate plots.

4.  **Execution and Reporting:** The agent runs the code, saves the visualizations, and drafts a comprehensive Markdown or PDF report interpreting the results.

The primary challenge in autonomous data analysis is ensuring statistical correctness. LLMs can sometimes apply inappropriate statistical tests if the data distribution assumptions (e.g., normality) are not explicitly checked by the generated code [<u>5</u>](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0317084). Therefore, robust data agents are prompted to explicitly write code that tests assumptions before applying analytical models.

## Assigned Reading for Week 7

| **Priority** | **Reference** | **Description** |
|----|----|----|
| **Required** | Liang, H. et al. (2025). "Integrating Large Language Models for Automated Structural Analysis." *arXiv*. | A comprehensive framework for using LLMs to generate OpenSeesPy scripts for 2D frame analysis. |
| **Required** | Pandey, S. et al. (2025). "A retrieval-augmented large language model (LLM) agent for OpenFOAM." *Physics of Fluids*. | Application of LLM agents to CFD simulation setup and execution. |
| **Supplementary** | Jansen, J. A. et al. (2025). "Leveraging large language models for data analysis automation." *PLoS ONE*. | Detailed review of LLM capabilities in exploratory data analysis and visualization. |

## From Vibe Coding to System Design

### The Prototype-to-Production Gap

Over the past year, a fundamental shift has occurred in how AI systems are built. Instead of starting with architecture, APIs, and orchestration logic, developers can now start with **intent** — describing what they want, refining through iteration, and watching a working system take shape. This approach, known as *vibe coding*, has made it possible to stand up agent-based workflows in a fraction of the time it used to take (Cognizant AI Lab, 2026).

**What vibe coding enables:**

- Describe a system in plain language → structured network of agents with defined responsibilities

- Generate working prototypes without committing to rigid architecture upfront

- Rapidly iterate on communication paths, tools, and agent roles

**What vibe coding does NOT solve:**

- The system works once. Then it works again, slightly differently.

- A new edge case appears, a tool behaves unexpectedly, or an agent routes a task in an unintended way.

- Nothing is obviously broken, but the system is no longer something you can fully reason about.

### The Transition Point

The moment agent networks start interacting with real tools, real data, and real usage patterns, a different set of constraints appears:

1.  **Coordination complexity** — grows non-linearly with agent count (~200ms with 2 agents → \>4s with 8+ agents)

2.  **Integration fragmentation** — each new tool adds bespoke connectors, scattered across prompts and scripts

3.  **Non-deterministic behavior** — same input produces different reasoning paths across runs

4.  **Data handling** — real data introduces sensitivity, access control, and state consistency requirements

### Design Principle: Continuity from Prototype to Production

The goal is that the system you *create* is the system you continue to *develop, test, and run* — without rebuilding from scratch. This requires:

- **Structural refinement** over prompt editing — shaping how the system is composed, not just what it says

- **Repeated testing** — running networks multiple times to understand behavioral consistency

- **Real integrations** — grounding in actual tools and services, not placeholder logic

- **Visibility** — tracing how agents communicate so decisions can be understood and refined

### Lab Exercise Extension

Take the code generation agent from the earlier lab exercise and apply the prototype-to-production lens:

1.  Run the agent 10 times on the same input — measure output consistency

2.  Introduce a deliberate tool failure — observe cascading effects

3.  Add a second agent — observe coordination overhead

4.  Document the "demo → production" gaps you discover

**New References:**

- Cognizant AI Lab (2026). "Why Your Multi-Agent Network Works in Demo but Falls Apart in the Wild." *Decision AI Bytes.*

- Cognizant AI Lab (2026). "Vibe Coding Agentic Networks You Can Actually Deploy with neuro-san." *Decision AI Bytes.*

## References
