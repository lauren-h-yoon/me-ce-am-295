---
title: "Week1 Lecture Outline"
week: 1
doc_type: "lecture_outline"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 1/Week1_Lecture_Outline.docx"
source_hash: "a2c08c44166b9a83"
normalized_at: "2026-08-19T11:55:16Z"
---
# Week 1 Lecture Outline: The Dawn of Agentic AI in Engineering

**Format: Tuesday & Thursday lectures, 1:00–2:30 p.m. (2 × 90 minutes) + 5-hour at-home laboratory. Target Audience: Mechanical Engineering and Materials Science graduate students and senior undergraduates Prerequisites: Basic coding fundamentals (e.g., MATLAB, basic Python syntax). No prior knowledge of APIs, LLM architecture, or advanced software environments.**

*Delivery (Fall 2026): timeline blocks 0:00–1:30 are covered in the Tuesday session; blocks 1:30–3:00, including the laboratory briefing, in the Thursday session. The laboratory is completed at home (5 hours) before the following Tuesday.*

## Hour 1: The Evolution of Intelligence and How LLMs Work (0:00 - 0:50)

**0:00 - 0:10 \| Introduction & Course Vision**

- Welcome to ME/CE 295.

- The shift from numerical simulation (FEA/CFD) to AI-accelerated discovery.

- Why engineers need to understand AI agents: moving beyond chatbots to autonomous problem-solving.

**0:10 - 0:25 \| A Brief History of Language Models**

- The early days: ELIZA (1966) and pattern matching.

- The neural network era: RNNs and LSTMs (1997) for sequential data.

- The breakthrough: "Attention Is All You Need" (Vaswani et al., 2017) and the Transformer architecture.

- The scaling era: From GPT-1 to GPT-4, and the rise of reasoning models (o1, DeepSeek R1).

**0:25 - 0:50 \| Demystifying the Black Box: How LLMs Actually Work**

- **Tokenization:** Breaking text into subwords (e.g., "Thermodynamics" -\> "Thermo", "dynamics").

- **Embeddings:** Mapping tokens to high-dimensional vectors. Semantic meaning as geometry (e.g., King - Man + Woman = Queen).

- **Self-Attention:** The core mechanism. How words provide context to other words in a sentence.

- **Next-Token Prediction:** The fundamental objective function. How predicting the next word leads to emergent reasoning capabilities.

*10-Minute Break (0:50 - 1:00)*

## Hour 2: Bridging the Gap - Environments, APIs, and Prompting (1:00 - 1:50)

**1:00 - 1:15 \| Setting Up the Engineering Workspace**

- The concept of a Virtual Environment (venv, conda): Why isolation matters for engineering projects.

- Package managers (pip) and dependencies.

- Managing secrets: Introduction to .env files. Why we never hardcode API keys.

**1:15 - 1:30 \| What is an API? (Explained for Engineers)**

- The Restaurant Analogy: Client (You) -\> API (Menu/Waiter) -\> Server (Kitchen).

- HTTP requests, JSON payloads, and endpoints.

- Transitioning from web interfaces (ChatGPT) to programmatic access (OpenAI API).

- The concept of API cost: pricing per token.

**1:30 - 1:50 \| The Art and Science of Prompt Engineering**

- Why prompting is essentially programming in natural language.

- Zero-shot vs. Few-shot prompting.

- Chain-of-Thought (CoT) prompting: Forcing the model to show its mathematical steps.

- Structuring outputs: Asking for JSON to integrate with engineering pipelines.

*10-Minute Break (1:50 - 2:00)*

## Hour 3: From Chatbots to Autonomous Agents (2:00 - 2:50)

**2:00 - 2:20 \| Defining the AI Agent**

- What separates an Agent from a Chatbot? (Proactivity vs. Reactivity).

- The Four Pillars of an Agent: LLM Core, Memory, Planning, and Tools.

- The ReAct Pattern: Reason -\> Act -\> Observe -\> Repeat.

**2:20 - 2:40 \| Tool Use: Giving AI Hands in the Real World**

- How an LLM executes code, queries databases, or runs simulations.

- Example: An agent that writes a Python script to calculate the moment of inertia, runs it, and reads the output.

- The concept of multi-agent systems (e.g., an Engineer agent and a Reviewer agent).

**2:40 - 2:50 \| The Frontier of Scientific Discovery**

- Real-world examples: Agentic AI in materials discovery (Google GNoME) and self-driving laboratories.

- What we will build in this course: Automated literature reviews, RAG systems for building codes, and autonomous design optimizers.

- Q&A and Homework 1 Briefing.

*End of Lecture (2:50 - 3:00 Buffer)*
