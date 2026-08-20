---
title: "Study Guide 1 Python API Fundamentals"
week: 0
doc_type: "study_guide"
access: "all_students"
agents: [all_student_agents]
source: "materials/Study Guides/Study_Guide_1_Python_API_Fundamentals.docx"
source_hash: "11f3efa138cba4d1"
normalized_at: "2026-08-19T11:55:16Z"
---
# Study Guide 1: Python Environment and LLM API Fundamentals

**Course:** ME/CE 295 — AI Agents for Accelerating Scientific Discovery and Engineering Research  
**Author:** Manus AI

This guide provides the foundational software engineering skills required to build AI agents. It covers environment setup, secure API interactions, asynchronous programming, and structured data parsing—all critical for transitioning from web-based chat interfaces to programmatic, autonomous workflows.

## 1. Virtual Environments and Dependency Management

In scientific computing, managing dependencies is crucial for reproducibility. We will use uv or venv to isolate project environments.

### 1.1 Setting up a Virtual Environment

Open your terminal and navigate to your project directory. Create a new virtual environment:

# Using standard venv

python3 -m venv .venv

\# Activate the environment (Linux/macOS)

source .venv/bin/activate

\# Activate the environment (Windows)

.venv\Scripts\activate

### 1.2 Installing Core Packages

For this course, we rely on a standard stack of AI and data science libraries:

pip install openai anthropic langchain chromadb torch pydantic python-dotenv



Create a requirements.txt file to lock your dependencies:

pip freeze \> requirements.txt



## 2. API Authentication and Security

**Never hardcode API keys in your Python scripts.** If you commit a script with an active OpenAI key to GitHub, it will be revoked automatically, and your account may be compromised.

### 2.1 Using .env Files

Create a file named .env in your project root (and add it to your .gitignore!):

# .env

OPENAI_API_KEY="sk-proj-your-actual-api-key-here"

ANTHROPIC_API_KEY="sk-ant-your-actual-api-key-here"

### 2.2 Loading Keys in Python

Use the python-dotenv library to load these variables securely at runtime:

import os

from dotenv import load_dotenv

from openai import OpenAI

\# Load environment variables from .env file

load_dotenv()

\# The client will automatically look for OPENAI_API_KEY in the environment

client = OpenAI()



## 3. Basic API Calls and Rate Limiting

When building agents that process thousands of scientific papers or run iterative loops, you must handle API rate limits (HTTP 429 errors).

### 3.1 Synchronous API Call with Error Handling

We use the tenacity library (often pre-installed with LangChain) to implement exponential backoff. This ensures your agent pauses and retries if it hits a rate limit, rather than crashing.

from openai import OpenAI

from tenacity import retry, wait_exponential, stop_after_attempt

import openai

client = OpenAI()

@retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))

def get_completion_with_retry(prompt: str, system_prompt: str = "You are a helpful engineering assistant."):

try:

response = client.chat.completions.create(

model="gpt-4o",

messages=\[

{"role": "system", "content": system_prompt},

{"role": "user", "content": prompt}

\],

temperature=0.2 \# Low temperature for more deterministic, factual responses

)

return response.choices\[0\].message.content

except openai.RateLimitError as e:

print(f"Rate limit exceeded. Retrying... Error: {e}")

raise \# Tenacity catches this and retries

except Exception as e:

print(f"An unexpected error occurred: {e}")

raise

\# Example usage

result = get_completion_with_retry("What is the yield strength of A36 steel?")

print(result)



## 4. Asynchronous API Calls

If your agent needs to extract data from 100 abstracts, processing them sequentially might take 5 minutes. Using asynchronous calls (asyncio) allows you to process them concurrently in seconds.

### 4.1 Async Processing with AsyncOpenAI

import asyncio

from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def fetch_summary(abstract: str, index: int):

response = await async_client.chat.completions.create(

model="gpt-4o-mini",

messages=\[{"role": "user", "content": f"Summarize this in one sentence: {abstract}"}\]

)

return index, response.choices\[0\].message.content

async def process_batch(abstracts: list\[str\]):

\# Create a list of tasks

tasks = \[fetch_summary(abstract, i) for i, abstract in enumerate(abstracts)\]

\# Run all tasks concurrently

results = await asyncio.gather(\*tasks)

\# Sort by index to maintain original order

return \[res\[1\] for res in sorted(results, key=lambda x: x\[0\])\]

\# To run the async function in a standard Python script:

\# abstracts = \["Abstract 1 text...", "Abstract 2 text...", "Abstract 3 text..."\]

\# summaries = asyncio.run(process_batch(abstracts))



## 5. Structured Output Parsing with Pydantic

LLMs naturally output unstructured text. In engineering workflows, we need structured data (JSON, integers, floats) to pass into simulation tools like OpenSees or MATLAB. We enforce this using **Pydantic**.

### 5.1 Defining a Data Schema

Pydantic allows you to define strict data models with type hints. OpenAI's API supports "Structured Outputs," which guarantees the LLM will match your schema.

from pydantic import BaseModel, Field

from openai import OpenAI

client = OpenAI()

\# 1. Define the schema

class MaterialProperties(BaseModel):

material_name: str = Field(description="The name of the material")

yield_strength_mpa: float = Field(description="Yield strength in Megapascals")

youngs_modulus_gpa: float = Field(description="Young's modulus in Gigapascals")

is_isotropic: bool = Field(description="Whether the material is isotropic")

\# 2. Provide the unstructured text

abstract_text = """

We investigated a novel titanium alloy, Ti-6Al-4V.

Tensile testing revealed a yield strength of 880 MPa.

Acoustic measurements determined the elastic modulus to be approximately 114 GPa.

The material exhibits isotropic behavior under standard conditions.

"""

\# 3. Call the API with response_format

response = client.beta.chat.completions.parse(

model="gpt-4o",

messages=\[

{"role": "system", "content": "Extract the material properties from the text."},

{"role": "user", "content": abstract_text}

\],

response_format=MaterialProperties,

)

\# 4. Access the parsed, type-safe data

material = response.choices\[0\].message.parsed

print(f"Material: {material.material_name}")

print(f"Yield Strength: {material.yield_strength_mpa} MPa")

print(f"Type of yield_strength: {type(material.yield_strength_mpa)}") \# Will be \<class 'float'\>

### 5.2 Why this matters for Agents

When Agent A writes parameters for Agent B (the simulator), using Pydantic ensures Agent B never receives a string like "around 880 MPa" when it expects the float 880.0. This prevents runtime crashes in automated workflows.
