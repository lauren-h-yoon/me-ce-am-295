---
title: "Week7 Lecture Outline"
week: 7
doc_type: "lecture_outline"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 7/Week7_Lecture_Outline.docx"
source_hash: "40ba952bae820c8a"
normalized_at: "2026-08-19T11:55:20Z"
---
# Week 7 Lecture Outline: LLM-Driven Code Generation and Autonomous Data Analysis

**Format: Tuesday & Thursday lectures, 1:00–2:30 p.m. (2 × 90 minutes) + 5-hour at-home laboratory. Target Audience: Mechanical Engineering and Materials Science graduate students and senior undergraduates Prerequisites: Completion of Week 6; familiarity with Python, APIs, and basic FEA/CFD concepts.**

*Delivery (Fall 2026): timeline blocks 0:00–1:30 are covered in the Tuesday session; blocks 1:30–3:00, including the laboratory briefing, in the Thursday session. The laboratory is completed at home (5 hours) before the following Tuesday.*

## Hour 1: The Code Generation Paradigm (0:00 - 0:50)

**0:00 - 0:10 \| Review and Week 7 Objectives**

- Recap of Week 6: Surrogate modeling and Neural Operators.

- The shift from training AI to *solve* physics, to using AI to *orchestrate* traditional physics solvers.

- Introduction to the "Agentic Workflow" for simulation.

**0:10 - 0:30 \| Reframing Structural Analysis**

- The limitation of pure text generation: Why LLMs fail at directly calculating structural responses (hallucinations, lack of precision).

- The solution: Reframing structural analysis from an open-ended text task to a structured code generation task.

- Case Study: The OpenSeesPy framework (Liang et al., 2025). Translating natural language descriptions of 2D frames into executable FEA scripts.

**0:30 - 0:50 \| Domain-Specific Code Generation**

- Prompt engineering for code: The three-layer architecture (Data Layer, Model Layer, Output Layer).

- In-Context Learning (ICL): Providing the LLM with templates of correct simulation scripts.

- State-of-the-art frameworks: ModSolAgent for Abaqus, OpenFOAMGPT for CFD.

*10-Minute Break (0:50 - 1:00)*

## Hour 2: Execution, Feedback, and Autonomous Debugging (1:00 - 1:50)

**1:00 - 1:25 \| The Execution-Feedback Loop**

- The reality of LLM code: The first draft rarely runs perfectly.

- Building the loop: Generate \$\rightarrow\$ Execute \$\rightarrow\$ Capture Error \$\rightarrow\$ Feed Back \$\rightarrow\$ Regenerate.

- Sandboxed execution: Why we must isolate AI-generated code (Docker containers, resource limits).

**1:25 - 1:50 \| Autonomous Error Correction**

- Types of simulation errors: Syntax errors, runtime crashes, convergence failures, and physically implausible results.

- The "self-healing" paradigm: Teaching the LLM to read stack traces and debug its own code.

- Setting retry limits and fallback mechanisms to prevent infinite loops.

*10-Minute Break (1:50 - 2:00)*

## Hour 3: Data Analysis Pipelines and Lab Briefing (2:00 - 2:50)

**2:00 - 2:30 \| Autonomous Data Analysis and Visualization**

- Moving beyond simulation setup to post-processing.

- LLM-driven data pipelines: Ingesting raw experimental/simulation data and generating Pandas/Matplotlib code.

- Multi-stage pipelines (e.g., LIDA): Summarization \$\rightarrow\$ Goal Setting \$\rightarrow\$ Visualization Generation.

- Ensuring statistical correctness and appropriate test selection.

**2:30 - 2:50 \| Lab 7 Briefing: Building an OpenSeesPy Agent**

- Overview of Lab 7 tasks:

  - Part A: Build an agent that translates a text description of a 2D truss into an OpenSeesPy script.

  - Part B: Implement the Python try/except feedback loop to catch and fix OpenSees errors.

  - Part C: Extend the agent to automatically extract nodal displacements and plot the deformed shape.

- Q&A and transition to the Lab session.

*End of Lecture (2:50 - 3:00 Buffer)*
