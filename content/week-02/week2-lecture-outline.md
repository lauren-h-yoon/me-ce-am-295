---
title: "Week2 Lecture Outline"
week: 2
doc_type: "lecture_outline"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 2/Week2_Lecture_Outline.docx"
source_hash: "85a305ee849b8279"
normalized_at: "2026-08-19T11:55:18Z"
---
# Week 2 Lecture Outline: Foundations of LLMs and Advanced Prompt Engineering

**Format: Tuesday & Thursday lectures, 1:00–2:30 p.m. (2 × 90 minutes) + 5-hour at-home laboratory. Target Audience: Mechanical Engineering and Materials Science graduate students and senior undergraduates Prerequisites: Completion of Week 1; basic understanding of API calls and Python virtual environments.**

*Delivery (Fall 2026): timeline blocks 0:00–1:30 are covered in the Tuesday session; blocks 1:30–3:00, including the laboratory briefing, in the Thursday session. The laboratory is completed at home (5 hours) before the following Tuesday.*

## Hour 1: The Engine Under the Hood: Transformer Mechanics (0:00 - 0:50)

**0:00 - 0:10 \| Review and Week 2 Objectives**

- Recap of Week 1: Tokenization, embeddings, and the ReAct loop.

- The goal for today: Moving from black-box API calls to rigorous, deterministic engineering workflows.

**0:10 - 0:30 \| Deep Dive into Self-Attention**

- The mechanics of Query (Q), Key (K), and Value (V) matrices.

- Multi-head attention: How models capture different semantic and syntactic relationships simultaneously.

- Positional encoding: How the model understands word order without sequential processing.

**0:30 - 0:40 \| Context Windows and Scaling Limits**

- The \$O(n^2)\$ computational complexity of self-attention.

- "Lost in the middle" phenomenon: Why models sometimes ignore information in the center of a large document.

- Practical implications: Feeding entire building codes (e.g., ASCE 7) into a 1M token context window.

**0:40 - 0:50 \| Emergent Abilities and Sampling Parameters**

- What are "emergent abilities"? (e.g., multi-step arithmetic appearing suddenly at scale).

- Controlling the model: Temperature (\$T\$), Top-\$p\$, and Top-\$k\$.

- Engineering rules of thumb: \$T=0\$ for deterministic math and data extraction; \$T=0.7\$ for creative design ideation.

*10-Minute Break (0:50 - 1:00)*

## Hour 2: Advanced Prompting for Engineering Reasoning (1:00 - 1:50)

**1:00 - 1:20 \| Chain-of-Thought (CoT) Prompting**

- Why standard zero-shot prompting fails at engineering mathematics.

- The theory behind CoT: Generating intermediate tokens as a form of "computational scratchpad."

- Example: Prompting an LLM to calculate the deflection of a simply supported beam step-by-step.

**1:20 - 1:35 \| Self-Consistency**

- The concept of running multiple CoT paths in parallel.

- Majority voting: Treating language model outputs probabilistically.

- Application: Reducing variance and catching arithmetic hallucinations in structural load calculations.

**1:35 - 1:50 \| Tree-of-Thoughts (ToT) and Search Algorithms**

- Extending CoT to a tree structure: Exploring multiple design paths.

- Implementing breadth-first or depth-first search over language model thoughts.

- Example: Exploring different truss topologies before committing to a final design.

*10-Minute Break (1:50 - 2:00)*

## Hour 3: Structured Outputs and Data Extraction (2:00 - 2:50)

**2:00 - 2:20 \| The Necessity of Structured Data**

- Why natural language prose is useless for automated simulation pipelines.

- The transition from JSON mode to guaranteed Structured Outputs.

- Introduction to JSON Schema and why it matters for API communication.

**2:20 - 2:40 \| Implementing Structured Outputs with Pydantic**

- What is Pydantic? Data validation and settings management using Python type hints.

- Defining a BaseModel for material properties (Young's modulus, yield strength, density).

- Passing the Pydantic schema to the OpenAI API using the response_format parameter.

- Combining CoT with Structured Outputs (e.g., a schema containing a steps list and a final_answer field).

**2:40 - 2:50 \| Homework 1 Briefing: Material Property Extraction**

- Overview of Homework 1: Extracting material properties from 20 unstructured academic abstracts.

- Defining the evaluation metrics: Precision and recall.

- Q&A and transition to the Lab session.

*End of Lecture (2:50 - 3:00 Buffer)*
