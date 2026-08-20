---
title: "Week4 RAG Literature Review"
week: 4
doc_type: "reference"
access: "all_students"
agents: [all_student_agents, literature_scout]
source: "materials/Week 4/Week4_RAG_Literature_Review.docx"
source_hash: "8936f5c0ee330a11"
normalized_at: "2026-08-19T11:55:19Z"
---
# ME/CE 295 --- Week 4 Lecture Notes

# Automating Literature Review with Retrieval-Augmented Generation

**California Institute of Technology --- Division of Engineering and Applied Science Course: ME/CE 295 --- AI Agents for Accelerating Scientific Discovery and Engineering Research Week: 4 of 10 Lectures: Tuesday & Thursday, 1:00–2:30 p.m. (2 × 1.5 hours) \| Laboratory: 5 hours, at-home (see separate lab handout)**

## Lecture Outline at a Glance

The following table summarizes the lecture structure, delivered as two 90-minute sessions: 0:00–1:30 on Tuesday and 1:30–3:00 (including the lab briefing) on Thursday. This session focuses on bridging the gap between large language models and external, proprietary engineering documents using Retrieval-Augmented Generation (RAG).

| **Time** | **Duration** | **Topic** | **Key Takeaway** |
|----|----|----|----|
| 0:00--0:10 | 10 min | Review and Week 4 Objectives | LLMs need external memory to read building codes |
| 0:10--0:25 | 15 min | Parsing Engineering Documents | Overcoming the PDF barrier for tables and math |
| 0:25--0:50 | 25 min | Chunking Strategies | Balancing granularity with context retention |
| 0:50--1:00 | 10 min | *Break* |  |
| 1:00--1:20 | 20 min | Vector Embeddings and Databases | Storing high-dimensional representations of text |
| 1:20--1:50 | 30 min | Advanced Retrieval Strategies | MMR, Hybrid Search, and Re-ranking |
| 1:50--2:00 | 10 min | *Break* |  |
| 2:00--2:20 | 20 min | The Grounding Problem | Forcing strict citations to prevent hallucinations |
| 2:20--2:35 | 15 min | Evaluating RAG Systems (RAGAS) | Quantifying faithfulness using LLMs as judges |
| 2:35--2:50 | 15 min | Lab 4 Briefing | Building an AISC Steel Manual compliance agent |
| 2:50--3:00 | 10 min | Q&A and Transition to Lab |  |

## Part I --- The Ingestion Pipeline

Large Language Models (LLMs) possess vast amounts of general knowledge, but they are frozen in time at their training cutoff and lack access to proprietary data. If a civil engineer asks an LLM to verify a connection design against the latest AISC Steel Construction Manual, the model cannot reliably answer from its internal weights alone. The solution is Retrieval-Augmented Generation (RAG). RAG systems intercept the user's query, search a database of documents for relevant information, and inject that information into the LLM's context window before generating an answer. The first step in this process is ingestion.

### 1. Parsing Engineering Documents

The vast majority of engineering literature—journal papers, building codes, and datasheets—is stored in the Portable Document Format (PDF). While PDFs are excellent for visual rendering, they are notoriously difficult for machines to read. As noted in recent literature, PDFs store diverse content including figures, tables, equations, and references, but they are not inherently machine-readable [<u>1</u>](https://arxiv.org/html/2505.04846v1).

When a basic text extractor processes a PDF, it often scrambles the reading order, destroys the layout of tables, and turns mathematical equations into gibberish. To build a robust RAG pipeline, engineers must use specialized parsing tools. **PyMuPDF** offers extremely fast text extraction but struggles with complex layouts. **Unstructured.io** provides advanced partitioning capabilities, using computer vision models to identify and preserve the structure of tables and lists. For academic papers heavily laden with mathematics, Meta's **Nougat** model performs Optical Character Recognition (OCR) specifically tuned to output LaTeX-formatted equations, ensuring that the semantic meaning of the math is preserved for the LLM.

### 2. Chunking Strategies

Once a document is parsed into clean text, it must be divided into smaller segments called "chunks." This is necessary because embedding models and LLMs have finite context windows. The challenge lies in finding the optimal chunk size: too small, and the chunk loses its surrounding context; too large, and the specific technical details become diluted in the embedding space [<u>2</u>](https://www.pinecone.io/learn/chunking-strategies/).

The most straightforward approach is **fixed-size chunking**, where the text is split into segments of a specific token count (e.g., 512 or 1024 tokens). However, this often slices sentences or paragraphs in half. A more refined method is **Recursive Character Splitting**, implemented in frameworks like LangChain. This strategy attempts to split text using a hierarchy of separators—first by double newlines to separate paragraphs, then by single newlines, then by spaces—ensuring that natural linguistic boundaries are respected [<u>2</u>](https://www.pinecone.io/learn/chunking-strategies/).

More advanced pipelines utilize **Semantic Chunking**. Instead of relying on character counts, semantic chunking groups sentences together and generates embeddings for each group. By calculating the semantic distance between adjacent groups, the system can detect when the topic shifts and place a chunk boundary exactly at that conceptual transition [<u>2</u>](https://www.pinecone.io/learn/chunking-strategies/). Furthermore, Anthropic recently introduced **Contextual Chunking**, where an LLM reads the entire document and generates a brief summary that is prepended to every individual chunk. This ensures that even a highly specific chunk containing a single equation retains the high-level context of the paper it came from [<u>2</u>](https://www.pinecone.io/learn/chunking-strategies/). Regardless of the strategy, implementing a chunk overlap (e.g., 10-20%) is critical to prevent information loss at the boundaries.

## Part II --- Embedding, Storage, and Retrieval

After the documents are chunked, they must be converted into a format that a computer can search efficiently. This is achieved through vector embeddings.

### 3. Vector Embeddings and Databases

An embedding model takes a chunk of text and maps it into a high-dimensional vector space (often consisting of 1,000 to 3,000 dimensions). In this space, chunks that share similar semantic meaning are located close to one another. For example, a chunk discussing "tensile yield strength" will be positioned near a chunk discussing "material failure limits," even if they do not share the exact same keywords.

These high-dimensional vectors are stored in specialized systems known as **Vector Databases**. The choice of database depends on the deployment environment. **ChromaDB** is an open-source, lightweight database that runs natively in Python, making it ideal for local prototyping and laboratory exercises. **FAISS**, developed by Meta, is a highly optimized library for extremely fast similarity search across massive datasets, though it lacks built-in persistence. For enterprise-scale production applications, managed cloud services like **Pinecone** offer robust infrastructure with advanced metadata filtering capabilities [<u>3</u>](https://medium.com/@priyaskulkarni/vector-databases-for-rag-faiss-vs-chroma-vs-pinecone-6797bd98277d).

### 4. Advanced Retrieval Strategies

When a user submits a query, the RAG system embeds the query using the same model and searches the vector database for the closest chunks. The most basic retrieval method is **Cosine Similarity**, which simply returns the top-k chunks with the highest similarity scores. However, this can lead to redundant results; if a building code repeats a warning across five consecutive paragraphs, cosine similarity might retrieve all five, starving the LLM of diverse context.

To solve this, engineers use **Maximum Marginal Relevance (MMR)**. MMR optimizes the retrieval process by balancing relevance with diversity. It selects the most relevant chunk first, but then penalizes subsequent chunks that are too similar to the ones already selected [<u>4</u>](https://www.linkedin.com/pulse/retrieval-augmented-generation-hybrid-retriever-pipelines-ghosh-8w1bc). This ensures that the LLM receives a comprehensive view of the topic.

Another critical enhancement is **Hybrid Search**. While semantic vector search is excellent for conceptual queries, it often fails at exact keyword matching. If an engineer queries the properties of a "W14x90" steel beam, a semantic search might retrieve chunks about "W14x99" or "W12x90" because they are conceptually similar. Hybrid search combines dense vector retrieval with sparse keyword retrieval (such as the BM25 algorithm), ensuring that exact part numbers and specific terminology are accurately located [<u>4</u>](https://www.linkedin.com/pulse/retrieval-augmented-generation-hybrid-retriever-pipelines-ghosh-8w1bc). Finally, the retrieved chunks can be passed through a **Re-ranking** model—a cross-encoder that scores the relevance of each chunk against the query with much higher accuracy than the initial fast retrieval step.

## Part III --- Grounding and Evaluation

Retrieving the correct information is only half the battle. The agent must then use that information accurately without fabricating details—a phenomenon known as hallucination.

### 5. The Grounding Problem

In a scientific or engineering context, hallucinations are unacceptable. If a RAG system invents a load combination factor that does not exist in the ASCE 7 standard, the resulting structural design could be catastrophic. To prevent this, the LLM's response must be strictly **grounded** in the retrieved context.

This is achieved through aggressive prompt engineering. The system prompt must explicitly instruct the model: *"Answer the user's question using ONLY the provided context. If the answer cannot be deduced from the context, you must state 'I do not have enough information'."* Furthermore, engineers use structured output schemas (via Pydantic) to force the LLM to provide inline citations for every claim it makes. By requiring the model to output a JSON object containing both the answer and the specific section number from the retrieved chunk, the system enforces traceability.

### 6. Evaluating RAG Systems with RAGAS

To iteratively improve a RAG pipeline, developers need quantitative metrics. The **RAGAS (Retrieval Augmented Generation Assessment)** framework provides a standardized suite of metrics for this purpose [<u>5</u>](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/).

The most critical metric for engineering applications is **Faithfulness**. Faithfulness measures how factually consistent the generated response is with the retrieved context, yielding a score between 0 and 1.

> "A response is considered faithful if all its claims can be supported by the retrieved context." [<u>5</u>](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/)

The calculation involves three steps:

1.  An LLM acts as a judge to break the generated response down into individual, atomic claims.

2.  The judge evaluates whether each claim can be logically inferred from the retrieved chunks.

3.  The final score is the ratio of supported claims to the total number of claims [<u>5</u>](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/).

Other important RAGAS metrics include **Context Precision** (did the retrieval system rank the most relevant chunks at the top?) and **Answer Relevance** (does the response directly address the user's original question without tangential rambling?). By systematically tracking these metrics, engineers can objectively determine whether switching from fixed-size chunking to semantic chunking actually improves the performance of their literature review agent.

## Assigned Reading for Week 4

| **Priority** | **Reference** | **Description** |
|----|----|----|
| **Required** | Asai, A. et al. (2026). "Synthesizing scientific literature with retrieval-augmented language models." *Nature*. | Comprehensive overview of applying RAG to scientific discovery. |
| **Required** | Pinecone Documentation (2025). "Chunking Strategies for LLM Applications." | Technical guide on fixed, recursive, and semantic chunking. |
| **Supplementary** | RAGAS Documentation (2026). "Faithfulness Metric." | Mathematical formulation and implementation of RAG evaluation. |
| **Supplementary** | Elasticsearch Labs (2024). "How to parse PDF tables in RAG." | Strategies for extracting structured data from engineering PDFs. |

## References
