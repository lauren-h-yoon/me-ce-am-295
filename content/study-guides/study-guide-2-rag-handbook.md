---
title: "Study Guide 2 RAG Handbook"
week: 0
doc_type: "study_guide"
access: "all_students"
agents: [all_student_agents]
source: "materials/Study Guides/Study_Guide_2_RAG_Handbook.docx"
source_hash: "ad0740c9aaae53dd"
normalized_at: "2026-08-19T11:55:16Z"
---
# Study Guide 2: RAG Implementation Handbook

**Course:** ME/CE 295 — AI Agents for Accelerating Scientific Discovery and Engineering Research  
**Author:** Manus AI

Retrieval-Augmented Generation (RAG) is a critical technique for grounding Large Language Models (LLMs) in factual, domain-specific data. Instead of relying on the LLM's internal (and potentially hallucinated) memory, RAG searches a curated database of documents (e.g., building codes, research papers) and provides the relevant excerpts to the LLM to formulate an answer.

This handbook outlines the complete pipeline for building a production-quality RAG system tailored for dense engineering documents.

## 1. Document Ingestion and Parsing

Engineering documents (PDFs) are notoriously difficult to parse because they contain multi-column layouts, complex mathematical equations, and dense tables. Standard text extractors often fail here.

### 1.1 Recommended Parsing Libraries

- **PyMuPDF (fitz):** Extremely fast, good for standard text extraction.

- **Unstructured (unstructured):** Excellent for identifying document elements (titles, narrative text, tables, images).

- **Nougat (Meta):** A vision-transformer model specifically designed to parse scientific PDFs into Markdown, preserving LaTeX equations.

### 1.2 Basic Extraction with PyMuPDF

import fitz \# PyMuPDF

def extract_text_from_pdf(pdf_path: str) -\> str:

doc = fitz.open(pdf_path)

full_text = ""

for page_num in range(len(doc)):

page = doc.load_page(page_num)

full_text += page.get_text("text") + "\n"

return full_text

\# Example usage

\# text = extract_text_from_pdf("ASCE_7_22.pdf")



## 2. Text Chunking Strategies

LLMs have a finite context window. We cannot pass an entire 500-page codebook into the prompt. We must split the text into smaller "chunks."

### 2.1 Recursive Character Text Splitting

This is the standard approach. It tries to split by paragraphs (\n\n), then sentences (\n), then words, ensuring chunks are semantically coherent.

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(

chunk_size=1000, \# Number of characters per chunk

chunk_overlap=200, \# Overlap prevents cutting sentences in half

length_function=len,

separators=\["\n\n", "\n", " ", ""\]

)

\# Assume 'document_text' is the string extracted from the PDF

\# chunks = text_splitter.create_documents(\[document_text\])

### 2.2 Semantic Chunking (Advanced)

For engineering standards, a section (e.g., "12.4 Seismic Load Effects") should ideally be kept together. Semantic chunking uses embeddings to detect shifts in topic and splits the text accordingly, rather than relying strictly on character counts.

## 3. Embeddings and Vector Databases

Once the text is chunked, we convert each chunk into a high-dimensional vector (an embedding) that captures its semantic meaning.

### 3.1 Choosing an Embedding Model

- **OpenAI text-embedding-3-small:** Fast, cheap, and highly performant (1536 dimensions).

- **HuggingFace all-MiniLM-L6-v2:** Open-source, runs locally, good for basic tasks (384 dimensions).

### 3.2 Setting up a Local Vector Store (ChromaDB)

ChromaDB is a lightweight, open-source vector database perfect for local development.

from langchain_community.vectorstores import Chroma

from langchain_openai import OpenAIEmbeddings

\# 1. Initialize the embedding model

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

\# 2. Create the vector database from our chunks

\# (Assuming 'chunks' is a list of Document objects from step 2)

vectorstore = Chroma.from_documents(

documents=chunks,

embedding=embedding_model,

persist_directory="./engineering_db" \# Saves to disk

)

\# To load an existing database later:

\# vectorstore = Chroma(persist_directory="./engineering_db", embedding_function=embedding_model)



## 4. Retrieval Strategies

When a user asks a question, we embed the question and search the vector database for the closest matching chunks.

### 4.1 Maximum Marginal Relevance (MMR)

Standard cosine similarity might return 5 chunks that all say the exact same thing. MMR optimizes for both **relevance** to the query and **diversity** among the retrieved chunks, giving the LLM a broader context.

# Create a retriever using MMR

retriever = vectorstore.as_retriever(

search_type="mmr",

search_kwargs={

"k": 5, \# Return 5 final documents

"fetch_k": 20, \# Fetch 20 initially, then select the 5 most diverse

"lambda_mult": 0.5 \# 1.0 = max relevance, 0.0 = max diversity

}

)

\# Test the retriever

\# query = "What is the redundancy factor for seismic design category D?"

\# retrieved_docs = retriever.invoke(query)



## 5. Generation and Grounding

Finally, we pass the retrieved chunks and the user's query to the LLM to generate an answer. We use a strict system prompt to prevent hallucination.

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.runnables import RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o", temperature=0)

\# Define a strict grounding prompt

template = """You are an expert structural engineer.

Answer the question based ONLY on the following retrieved context.

If the context does not contain the answer, say "I cannot answer this based on the provided documents."

Do not use outside knowledge. Always cite the section or page number if available in the context.

Context:

{context}

Question: {question}

"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):

return "\n\n".join(\[f"Excerpt:\n{d.page_content}" for d in docs\])

\# Build the LangChain pipeline (LCEL)

rag_chain = (

{"context": retriever \| format_docs, "question": RunnablePassthrough()}

\| prompt

\| llm

\| StrOutputParser()

)

\# Execute the chain

\# answer = rag_chain.invoke("What is the redundancy factor for seismic design category D?")

\# print(answer)



## 6. Evaluation Metrics

How do you know if your RAG system is actually good? In engineering, a wrong answer can be catastrophic.

1.  **Retrieval Accuracy (Hit@K):** Out of \$K\$ retrieved chunks, does at least one contain the actual answer? If the retriever fails, the LLM will fail.

2.  **Faithfulness (Hallucination Rate):** Does the LLM's generated answer logically follow from the retrieved chunks, or did it make something up? This is often evaluated using an "LLM-as-a-judge" framework (e.g., using the Ragas or TruLens libraries).

3.  **Answer Relevance:** Does the answer directly address the user's question without unnecessary rambling?
