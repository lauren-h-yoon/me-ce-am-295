---
title: "Week2 Foundations of LLMs"
week: 2
doc_type: "lecture_notes"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 2/Week2_Foundations_of_LLMs.docx"
source_hash: "8f8a960d3c523796"
normalized_at: "2026-08-19T11:55:18Z"
---
# ME/CE 295 --- Week 2 Lecture Notes

# Foundations of LLMs and Advanced Prompt Engineering

**California Institute of Technology --- Division of Engineering and Applied Science Course: ME/CE 295 --- AI Agents for Accelerating Scientific Discovery and Engineering Research Week: 2 of 10 Lectures: Tuesday & Thursday, 1:00–2:30 p.m. (2 × 1.5 hours) \| Laboratory: 5 hours, at-home (see separate lab handout)**

## Lecture Outline at a Glance

The following table summarizes the lecture structure, delivered as two 90-minute sessions: 0:00–1:30 on Tuesday and 1:30–3:00 (including the lab briefing) on Thursday. This session moves from the internal mechanics of Large Language Models (LLMs) to advanced prompt engineering techniques and structured data extraction for engineering workflows.

| **Time** | **Duration** | **Topic** | **Key Takeaway** |
|----|----|----|----|
| 0:00--0:10 | 10 min | Review and Week 2 Objectives | Moving from black-box APIs to rigorous workflows |
| 0:10--0:30 | 20 min | Deep Dive into Self-Attention | Query, Key, Value matrices and Multi-head attention |
| 0:30--0:40 | 10 min | Context Windows and Scaling Limits | The \$O(n^2)\$ complexity and "lost in the middle" |
| 0:40--0:50 | 10 min | Emergent Abilities and Sampling | Temperature, Top-\$p\$, and Top-\$k\$ parameters |
| 0:50--1:00 | 10 min | *Break* |  |
| 1:00--1:20 | 20 min | Chain-of-Thought (CoT) Prompting | Forcing models to generate a computational scratchpad |
| 1:20--1:35 | 15 min | Self-Consistency | Majority voting to reduce variance in calculations |
| 1:35--1:50 | 15 min | Tree-of-Thoughts (ToT) | Exploring multiple design paths via search algorithms |
| 1:50--2:00 | 10 min | *Break* |  |
| 2:00--2:20 | 20 min | The Necessity of Structured Data | Why natural language fails for simulation pipelines |
| 2:20--2:40 | 20 min | Structured Outputs with Pydantic | Defining schemas for the OpenAI API |
| 2:40--2:50 | 10 min | Homework 1 Briefing | Material property extraction assignment details |
| 2:50--3:00 | 10 min | Q&A and Transition to Lab |  |

## Part I --- The Engine Under the Hood: Transformer Mechanics

In Week 1, we introduced the high-level concepts of tokenization, embeddings, and the ReAct loop. This week, we move from treating Large Language Models (LLMs) as black-box APIs to understanding their internal mechanics. To build robust engineering workflows, you must understand the computational constraints and behaviors of the models you are orchestrating.

### 1. Deep Dive into Self-Attention

The core innovation of the Transformer architecture, introduced by Vaswani et al. in 2017, is the **self-attention mechanism** [<u>1</u>](https://arxiv.org/abs/1706.03762). Unlike earlier Recurrent Neural Networks (RNNs) that processed text sequentially, Transformers process all tokens in a sequence simultaneously. This is achieved through three learned matrices: Query (\$Q\$), Key (\$K\$), and Value (\$V\$).

You can conceptualize this using a database retrieval analogy:

- The **Query (\$Q\$)** is what a token is "looking for" in the surrounding context.

- The **Key (\$K\$)** is what a token "advertises" about itself to other tokens.

- The **Value (\$V\$)** is the actual semantic content the token contains.

For every token in a sequence, the model computes the dot product of its Query vector with the Key vectors of all other tokens. This dot product yields an **attention score**, representing the relevance of one word to another. The scores are normalized using a softmax function, and the token's final representation is updated as a weighted sum of the Value vectors of all tokens in the sequence.

Modern LLMs utilize **Multi-Head Attention**. Instead of computing a single set of \$Q\$, \$K\$, and \$V\$ matrices, the model computes multiple sets (or "heads") in parallel. For example, GPT-3 uses 96 attention heads per layer. This allows the model to simultaneously capture different types of relationships: one head might track grammatical syntax, another might track mathematical operators, and a third might track the physical properties of a material mentioned earlier in the text.

### 2. Positional Encoding

If the Transformer processes all tokens simultaneously, how does it know the order of the words? "The load acts on the beam" has a very different engineering meaning than "The beam acts on the load," yet the set of tokens is identical.

Because the self-attention mechanism itself has no inherent sense of sequence, Transformers inject order using **Positional Encodings**. Before the token embeddings are fed into the attention layers, a mathematical vector representing the token's position in the sequence is added to the embedding. Early models used alternating sine and cosine functions of different frequencies to encode position [<u>1</u>](https://arxiv.org/abs/1706.03762), while modern models often use learned positional embeddings or Rotary Position Embeddings (RoPE). This allows the model to differentiate between identical tokens based on their location in the prompt.

### 3. Context Windows and Scaling Limits

Every LLM has a hard limit on the amount of text it can process in a single request, known as the **context window**.

#### 3.1 The \$O(n^2)\$ Complexity Problem

The size of the context window is primarily constrained by the self-attention mechanism. Because every token must compute an attention score with every other token, the computational complexity and memory requirements scale quadratically with the sequence length, denoted as \$O(n^2)\$. If you double the length of your prompt, the memory required by the attention mechanism quadruples.

In recent years, breakthroughs in hardware optimization (such as FlashAttention) and sparse attention techniques have dramatically expanded context windows. While early models were limited to 2,048 tokens, modern models like GPT-4o and Gemini 1.5 Pro boast context windows of 128,000 to 2,000,000 tokens [<u>2</u>](https://developers.openai.com/api/docs/guides/structured-outputs/).

#### 3.2 The "Lost in the Middle" Phenomenon

A massive context window allows engineers to feed entire building codes, such as the 1,000-page ASCE 7 standard, directly into the model's prompt. However, researchers have identified a critical limitation known as the **"lost in the middle" phenomenon** [<u>3</u>](https://arxiv.org/abs/2307.03172).

When evaluating how well LLMs retrieve facts from long contexts, performance follows a U-shaped curve. Models are highly accurate at extracting information located at the very beginning or the very end of a long prompt. However, their accuracy degrades significantly when the relevant information is buried in the middle of the document. For engineering applications where missing a single load factor coefficient can lead to catastrophic design failure, you cannot rely solely on dumping massive documents into the context window. This necessitates the Retrieval-Augmented Generation (RAG) architectures we will build in Week 4.

### 4. Emergent Abilities and Sampling Parameters

As models scale in parameters and training data, they exhibit behaviors that were not explicitly programmed into them.

#### 4.1 Emergent Abilities

An **emergent ability** is defined as a capability that is not present in smaller models but appears suddenly and unpredictably when the model reaches a certain scale threshold [<u>4</u>](https://arxiv.org/abs/2206.07682). Examples of emergent abilities include multi-step arithmetic, transliteration, and the ability to write executable Python code.

For engineers, this means that smaller, open-source models running locally on your laptop may fail completely at structural analysis reasoning, while a massive frontier model will succeed, even though both share the exact same underlying Transformer architecture. The capability arises from the scale of the statistical relationships learned during training.

#### 4.2 Controlling the Output: Temperature and Sampling

When an LLM generates text, its final layer outputs a probability distribution over the entire vocabulary for the next token. You control how the model selects from this distribution using sampling parameters.

The most critical parameter is **Temperature (\$T\$)**, which scales the logits (raw output scores) before they are converted into probabilities via the softmax function [<u>5</u>](https://aws.amazon.com/what-is/api/).

- **\$T = 0\$ (Greedy Decoding):** The model deterministically selects the token with the highest probability. This results in highly repetitive, predictable text.

- **\$T = 1\$ (Standard Sampling):** The model samples from the true probability distribution.

- **\$T \> 1\$:** The distribution is flattened, increasing the probability of selecting less likely tokens, resulting in more "creative" or chaotic text.

Other parameters include **Top-\$p\$ (Nucleus Sampling)**, which restricts the model to sampling only from the smallest set of tokens whose cumulative probability exceeds the value \$p\$, and **Top-\$k\$**, which restricts sampling to the \$k\$ most probable tokens.

> **Engineering Rule of Thumb:** When using an LLM to extract numerical data from a research paper, write code, or perform deterministic mathematical reasoning, always set Temperature to 0. When using an LLM for brainstorming, hypothesis generation, or conceptual design exploration, set Temperature between 0.5 and 0.7 to encourage diverse outputs.

## Part II --- Advanced Prompting for Engineering Reasoning and Structured Outputs

### 5. Advanced Prompting for Engineering Reasoning

In Week 1, we introduced the basics of zero-shot and few-shot prompting. While these are sufficient for simple text generation, they frequently fail when applied to the multi-step mathematical reasoning required in mechanical and civil engineering. To solve this, researchers have developed advanced prompting topologies that manipulate the model's autoregressive generation process.

#### 5.1 Chain-of-Thought (CoT) Prompting

If you ask an LLM, "Calculate the maximum deflection of a simply supported steel beam (W12x50) spanning 20 feet under a uniform load of 2 kips/ft," standard zero-shot prompting will often result in the model attempting to guess the final numerical answer directly. Because the model lacks the internal computational depth to perform complex algebra in a single forward pass, it will likely hallucinate an incorrect number.

**Chain-of-Thought (CoT) prompting**, introduced by Wei et al. in 2022, solves this by explicitly instructing the model to generate intermediate reasoning steps [<u>6</u>](https://arxiv.org/abs/2201.11903). By appending the phrase "Let's think step by step" to the prompt, or by providing few-shot examples that include detailed mathematical derivations, the model is forced to generate intermediate tokens.

These intermediate tokens act as a "computational scratchpad." Because LLMs are autoregressive---meaning each new token is conditioned on all previously generated tokens---the intermediate steps (e.g., extracting the moment of inertia from the W-shape designation, writing the formula \$\Delta = 5wL^4 / 384EI\$, performing the unit conversions) become part of the context window. This drastically narrows the probability distribution toward the correct final answer. Research shows CoT prompting improves performance on mathematical benchmarks by 20% to 40% [<u>6</u>](https://arxiv.org/abs/2201.11903).

#### 5.2 Self-Consistency

Even with CoT prompting, LLMs can still make arithmetic errors or take a flawed logical path. **Self-Consistency**, introduced by Wang et al. in 2022, mitigates this by treating language model outputs probabilistically rather than deterministically [<u>7</u>](https://arxiv.org/abs/2203.11171).

Instead of generating a single Chain-of-Thought response using a Temperature of 0, you set the Temperature slightly higher (e.g., 0.4) and prompt the model to generate multiple, diverse reasoning paths (e.g., 5 to 10 independent responses) for the same problem. You then apply a **majority vote** to the final answers.

If 8 out of 10 reasoning paths arrive at a deflection of 0.45 inches, but two paths hallucinate 0.90 inches due to a unit conversion error, the majority vote filters out the noise. This technique is highly effective for structural load calculations and risk assessments where variance reduction is critical.

#### 5.3 Tree-of-Thoughts (ToT)

Chain-of-Thought represents a single, linear progression of logic. However, complex engineering design is rarely linear; it involves exploring multiple alternatives, evaluating them, and backtracking if a path proves unviable.

**Tree-of-Thoughts (ToT)**, introduced by Yao et al. in 2023, extends CoT by maintaining a tree structure of intermediate thoughts [<u>8</u>](https://arxiv.org/abs/2305.10601). The LLM generates multiple possible next steps (branches), and then a separate prompt asks the LLM to evaluate the promise of each branch ("Is this truss topology viable given the load constraints?").

Using classical search algorithms like Breadth-First Search (BFS) or Depth-First Search (DFS) orchestrated by a Python script, the system explores the tree, pruning unpromising design paths and expanding promising ones. This framework transforms the LLM from a simple text generator into an active participant in design space exploration.

### 6. Structured Outputs and Data Extraction

The ultimate goal of this course is to build autonomous agents that interact with engineering software. An agent cannot feed a paragraph of natural language prose into an OpenSees or OpenFOAM simulation script. It requires structured, machine-readable data.

#### 6.1 The Transition to Guaranteed Schemas

Historically, engineers relied on "JSON mode" or strongly worded prompts ("Return ONLY valid JSON") to extract data. However, these methods were prone to errors: the model might omit a required key, hallucinate a new property, or wrap the JSON in markdown code blocks, causing the Python script to crash when it attempted to parse the string.

Modern APIs, such as the OpenAI API, now support **Structured Outputs** [<u>2</u>](https://developers.openai.com/api/docs/guides/structured-outputs/). This feature guarantees that the model's output will strictly adhere to a developer-defined JSON Schema. The API achieves this by modifying the model's token-generation probabilities at the lowest level, physically preventing it from generating a token that would violate the schema.

#### 6.2 Implementing Structured Outputs with Pydantic

In Python, the most robust way to define and validate these schemas is using **Pydantic**. Pydantic is a data validation library that uses standard Python type hints.

To extract material properties from an unstructured academic abstract, you define a Pydantic BaseModel:

from pydantic import BaseModel, Field

class MaterialProperties(BaseModel):

material_name: str = Field(description="The name of the material being tested.")

youngs_modulus_GPa: float = Field(description="Young's modulus in GPa.")

yield_strength_MPa: float = Field(description="Yield strength in MPa.")

density_kg_m3: float = Field(description="Density in kg/m^3.")



When you pass this Pydantic class to the OpenAI SDK using the response_format parameter, the SDK automatically translates the Python class into a strict JSON Schema. The model processes the unstructured abstract and returns a fully instantiated Python object.

response = client.beta.chat.completions.parse(

model="gpt-4o",

messages=\[

{"role": "system", "content": "Extract the material properties from the text."},

{"role": "user", "content": abstract_text}

\],

response_format=MaterialProperties

)

\# Access the data directly as object attributes

print(response.choices\[0\].message.parsed.youngs_modulus_GPa)

#### 6.3 Combining CoT with Structured Outputs

A powerful pattern for engineering agents is combining Chain-of-Thought reasoning with Structured Outputs. If you force the model to output *only* the final JSON data, it loses the "computational scratchpad" needed to reason accurately.

The solution is to define a Pydantic schema that includes a field for the reasoning steps *before* the final answer:

class BeamDeflectionCalculation(BaseModel):

reasoning_steps: list\[str\] = Field(description="Step-by-step mathematical derivation.")

maximum_deflection_inches: float = Field(description="The final calculated deflection.")



Because JSON is generated sequentially from top to bottom, the model will first generate the reasoning_steps array, utilizing its autoregressive properties to perform the math, before finally outputting the maximum_deflection_inches float. This ensures both high mathematical accuracy and perfect data structure for your downstream simulation pipeline.

## Assigned Reading for Week 2

| **Priority** | **Reference** | **Description** |
|----|----|----|
| **Required** | OpenAI (2024). "Structured model outputs" | Guide on using JSON mode and Pydantic with the OpenAI API. |
| **Required** | Wei, J. et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS*. | Foundational paper on CoT prompting. |
| **Supplementary** | Yao, S. et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." *arXiv:2305.10601*. | Extension of CoT for complex search spaces. |
| **Supplementary** | Liu, N. F. et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts." *arXiv:2307.03172*. | Analysis of context window limitations. |

## References
