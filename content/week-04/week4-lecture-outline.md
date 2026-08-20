---
title: "Week4 Lecture Outline"
week: 4
doc_type: "lecture_outline"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 4/Week4_Lecture_Outline.docx"
source_hash: "5acbf2bf55e4f78c"
normalized_at: "2026-08-19T11:55:19Z"
---
# Week 4 Lecture Outline: Automating Literature Review with Retrieval-Augmented Generation

**Format: Tuesday & Thursday lectures, 1:00–2:30 p.m. (2 × 90 minutes) + 5-hour at-home laboratory. Target Audience: Mechanical Engineering and Materials Science graduate students and senior undergraduates Prerequisites: Completion of Week 3; familiarity with vector embeddings and basic API calls.**

*Delivery (Fall 2026): timeline blocks 0:00–1:30 are covered in the Tuesday session; blocks 1:30–3:00, including the laboratory briefing, in the Thursday session. The laboratory is completed at home (5 hours) before the following Tuesday.*

## Hour 1: The Ingestion Pipeline (0:00 - 0:50)

**0:00 - 0:10 \| Review and Week 4 Objectives**

- Recap of Week 3: Agent memory architectures and the limitations of context windows.

- The challenge: How do we get an LLM to read the 800-page AISC Steel Construction Manual without hallucinating?

- Introduction to Retrieval-Augmented Generation (RAG).

**0:10 - 0:25 \| Parsing Engineering Documents**

- Why PDFs are the enemy of LLMs: Loss of structural semantics, tables, and equations.

- Overview of parsing tools: PyMuPDF (fast text), Unstructured.io (tables), and Nougat (Meta's OCR for academic math).

- Best practices for preserving document hierarchy.

**0:25 - 0:50 \| Chunking Strategies**

- The "Goldilocks" problem of chunk size: Too small loses context, too large dilutes the embedding.

- Fixed-size chunking vs. Recursive Character Splitting (LangChain's RecursiveCharacterTextSplitter).

- Advanced methods: Semantic chunking (splitting on topic shifts) and Contextual chunking (Anthropic's approach).

- The importance of chunk overlap for maintaining boundary context.

*10-Minute Break (0:50 - 1:00)*

## Hour 2: Embedding, Storage, and Retrieval (1:00 - 1:50)

**1:00 - 1:20 \| Vector Embeddings and Databases**

- What is an embedding? Mapping text to high-dimensional space.

- Comparing embedding models: OpenAI's text-embedding-3-small vs. open-source Sentence-Transformers.

- Vector Databases: When to use ChromaDB (local prototyping), FAISS (high-speed similarity search), and Pinecone (managed production).

**1:20 - 1:50 \| Advanced Retrieval Strategies**

- Basic top-k cosine similarity and its failure modes (e.g., retrieving five identical chunks).

- Maximum Marginal Relevance (MMR): Balancing relevance with diversity to capture different sections of a building code.

- Hybrid Search: Combining dense vector search (semantic) with sparse BM25 (keyword matching) for exact part numbers (e.g., "W14x90").

- Re-ranking: Using cross-encoders to refine the retrieved set before passing it to the LLM.

*10-Minute Break (1:50 - 2:00)*

## Hour 3: Grounding, Evaluation, and Lab Briefing (2:00 - 2:50)

**2:00 - 2:20 \| The Grounding Problem: Fighting Hallucinations**

- Why RAG systems hallucinate: The LLM's prior knowledge vs. the retrieved context.

- Prompt engineering for strict grounding: "Answer ONLY using the provided context. If the answer is not present, state 'I don't know'."

- Forcing inline citations (e.g., \[ASCE 7, Section 12.8\]) using Pydantic structured outputs.

**2:20 - 2:35 \| Evaluating RAG Systems (RAGAS)**

- You can't improve what you can't measure.

- Introduction to the RAGAS framework.

- Deep dive into the **Faithfulness** metric: Calculating the ratio of supported claims to total claims using an LLM-as-a-judge.

- Other metrics: Context Precision (did we retrieve the right chunks?) and Answer Relevance.

**2:35 - 2:50 \| Lab 4 Briefing: Building a Building Code Assistant**

- Overview of Lab 4 tasks:

  - Part A: Ingesting the AISC Steel Manual into ChromaDB.

  - Part B: Implementing a LangChain retrieval chain with MMR.

  - Part C: Evaluating the system's faithfulness on 30 compliance questions.

- Q&A and transition to the Lab session.

*End of Lecture (2:50 - 3:00 Buffer)*
