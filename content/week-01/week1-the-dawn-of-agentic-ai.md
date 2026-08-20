---
title: "Week1 The Dawn of Agentic AI"
week: 1
doc_type: "lecture_notes"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 1/Week1_The_Dawn_of_Agentic_AI.docx"
source_hash: "c9c314d960fc809f"
normalized_at: "2026-08-19T11:55:17Z"
---
# ME/CE 295 --- Week 1 Lecture Notes

# The Dawn of Agentic AI in Engineering

**California Institute of Technology --- Division of Engineering and Applied Science Course: ME/CE 295 --- AI Agents for Accelerating Scientific Discovery and Engineering Research Week: 1 of 10 Lectures: Tuesday & Thursday, 1:00–2:30 p.m. (2 × 1.5 hours) \| Laboratory: 5 hours, at-home (see separate lab handout)**

## Lecture Outline at a Glance

The following table summarizes the lecture structure, delivered as two 90-minute sessions: 0:00–1:30 on Tuesday and 1:30–3:00 (including the lab briefing) on Thursday. Each segment is designed to build on the previous one, moving from historical context through foundational mechanics to the frontier of autonomous AI systems.

| **Time** | **Duration** | **Topic** | **Key Takeaway** |
|----|----|----|----|
| 0:00--0:10 | 10 min | Introduction and Course Vision | Why engineers need AI agents, not just chatbots |
| 0:10--0:25 | 15 min | A Brief History of Language Models | From ELIZA (1966) to reasoning models (2025) |
| 0:25--0:50 | 25 min | How LLMs Actually Work | Tokenization, embeddings, self-attention, next-token prediction |
| 0:50--1:00 | 10 min | *Break* |  |
| 1:00--1:15 | 15 min | Setting Up the Engineering Workspace | Virtual environments, package managers, .env files |
| 1:15--1:30 | 15 min | What Is an API? | The restaurant analogy; HTTP, JSON, and endpoints |
| 1:30--1:50 | 20 min | The Art and Science of Prompt Engineering | Zero-shot, few-shot, and chain-of-thought prompting |
| 1:50--2:00 | 10 min | *Break* |  |
| 2:00--2:20 | 20 min | Defining the AI Agent | The four pillars: LLM core, memory, planning, tools |
| 2:20--2:40 | 20 min | Tool Use and Multi-Agent Systems | ReAct pattern; giving AI "hands" in the physical world |
| 2:40--2:50 | 10 min | The Frontier of Scientific Discovery | GNoME, self-driving labs, and the course roadmap |
| 2:50--3:00 | 10 min | Q&A and Homework 1 Briefing |  |

## Part I --- The Evolution of Intelligence and How LLMs Work

### 1. Introduction and Course Vision

Welcome to ME/CE 295. As graduate students in mechanical engineering and materials science, you are already intimately familiar with the computational tools that have driven our fields for the last fifty years: Finite Element Analysis (FEA), Computational Fluid Dynamics (CFD), and complex numerical solvers. These tools represent the automation of calculation. We are now standing at the precipice of a fundamentally different paradigm: the automation of scientific reasoning and engineering design through Agentic Artificial Intelligence.

This course is not about learning how to use a chatbot to write emails. It is about understanding Large Language Models (LLMs) as cognitive engines that can be embedded into complex, autonomous systems capable of reading building codes, writing and executing Python scripts to optimize structural designs, and orchestrating multi-physics simulations---all without human intervention. We are shifting our focus from merely computing answers to autonomously generating hypotheses, executing tests, and evaluating results.

> **Course Philosophy:** "Learn by building." Every concept introduced in lecture will be implemented in the lab session the same week. By Week 9, you will have constructed a fully autonomous AI agent that can perform a meaningful engineering research task.

### 2. A Brief History of Language Models

To understand where we are, we must understand how we got here. The evolution of natural language processing (NLP) is a journey spanning six decades, from rigid rules to fluid, emergent reasoning [<u>1</u>](https://toloka.ai/blog/history-of-llms/).

#### 2.1 The Early Days: Rules and Recurrence

In 1966, Joseph Weizenbaum at MIT developed **ELIZA**, the world's first chatbot. ELIZA operated on simple pattern matching and substitution rules. If a user typed "I am feeling sad," ELIZA would identify the "I am \[X\]" pattern and respond with "Why are you feeling \[X\]?" While it gave the illusion of understanding, it possessed zero comprehension of the meaning of the words it processed. For decades, the field of natural language processing struggled with the limitations of such rule-based systems.

A major breakthrough occurred in 1997 with the introduction of **Long Short-Term Memory (LSTM)** networks by Hochreiter and Schmidhuber. LSTMs are a type of Recurrent Neural Network (RNN) designed to process sequential data---text, speech, time series. Unlike simpler models, LSTMs could retain information over longer sequences, allowing them to understand that a word at the end of a paragraph was related to a word at the beginning. However, LSTMs processed data sequentially---one word at a time, left to right---which made them prohibitively slow to train on the massive datasets that would later prove essential.

Another landmark arrived in 2013 when Tomas Mikolov and colleagues at Google published **Word2Vec** [<u>2</u>](https://arxiv.org/abs/1301.3781). This model demonstrated that words could be represented as dense numerical vectors in a high-dimensional space, and that the geometric relationships between these vectors captured semantic meaning. The now-famous example, vector("King") - vector("Man") + vector("Woman") ≈ vector("Queen"), showed that mathematical operations on word representations could encode human-like analogical reasoning. Word2Vec laid the conceptual foundation for all modern embedding techniques.

#### 2.2 The Transformer Revolution (2017)

The modern AI era officially began with a single paper. In June 2017, a team of eight researchers at Google published *"Attention Is All You Need"* [<u>3</u>](https://arxiv.org/abs/1706.03762). This paper introduced the **Transformer architecture**, which completely discarded sequential processing in favor of a mechanism called **self-attention**.

Instead of reading a sentence word-by-word from left to right (as RNNs and LSTMs did), Transformers process all words in a sequence simultaneously. Every word can "attend" to every other word in the input, regardless of how far apart they are. This parallelization was revolutionary for two reasons. First, it allowed researchers to train models on massive clusters of GPUs, processing vast swaths of the internet in a fraction of the time it would take an RNN. Second, it solved the "long-range dependency" problem---the Transformer could easily connect a pronoun at the end of a document to a noun introduced in the first paragraph.

The following table summarizes the key architectural milestones:

| **Year** | **Model / Paper** | **Key Innovation** | **Parameters** |
|----|----|----|----|
| 1997 | LSTM (Hochreiter & Schmidhuber) | Gated memory cells for sequential data | ~Thousands |
| 2013 | Word2Vec (Mikolov et al.) | Words as dense vectors; semantic arithmetic | ~Millions |
| 2017 | Transformer (Vaswani et al.) | Self-attention; parallel processing of sequences | ~65 Million |
| 2018 | BERT (Google) | Bidirectional context understanding | 340 Million |
| 2018 | GPT-1 (OpenAI) | Generative pre-training on unlabeled text | 117 Million |
| 2020 | GPT-3 (OpenAI) | Few-shot learning; emergent task generalization | 175 Billion |
| 2023 | GPT-4 (OpenAI) | Multimodal input (text + images) | ~1.8 Trillion (est.) |
| 2024 | o1 (OpenAI) | Chain-of-thought reasoning via reinforcement learning | Undisclosed |
| 2025 | DeepSeek R1 | Open-source reasoning; trained for ~\$5M | 671 Billion (MoE) |

#### 2.3 The Scaling Era and Reasoning Models

Following the Transformer, the field entered what is now called the **Scaling Era**. Researchers discovered empirical "scaling laws" showing that model performance improves predictably as you increase three variables: the number of parameters, the volume of training data, and the amount of compute [<u>4</u>](https://arxiv.org/abs/2001.08361). OpenAI exploited this insight aggressively. GPT-1 (2018) had 117 million parameters. GPT-2 (2019) had 1.5 billion. GPT-3 (2020) had 175 billion and demonstrated "few-shot learning"---the ability to perform tasks it was never explicitly trained to do, simply by being provided a few examples in the prompt.

The release of **ChatGPT** in November 2022 brought this technology to the masses, reaching 100 million users in two months---the fastest-growing consumer application in history at the time [<u>1</u>](https://toloka.ai/blog/history-of-llms/). However, the most profound shift for engineering applications occurred between 2024 and 2025, with the advent of **Reasoning Models**. OpenAI's **o1** (September 2024) was trained using reinforcement learning to generate hidden "chains of thought" before producing a final answer. On the 2024 AIME mathematics competition, GPT-4o solved only 12% of problems, while o1 achieved 74% with a single attempt [<u>1</u>](https://toloka.ai/blog/history-of-llms/). In January 2025, the Chinese lab DeepSeek released **R1**, an open-source reasoning model that matched o1's performance at a fraction of the cost, demonstrating that reasoning capabilities can emerge purely from reinforcement learning without any human-labeled reasoning examples [<u>1</u>](https://toloka.ai/blog/history-of-llms/).

### 3. Demystifying the Black Box: How LLMs Actually Work

As engineers, we cannot treat AI as magic. We must understand its mechanics. The operation of an LLM can be broken down into four fundamental concepts, each building on the last.

#### 3.1 Tokenization: The Atomic Units of Text

An LLM does not read English. It reads numbers. The first step in processing any text is **Tokenization**---the process of splitting a string of text into discrete subword units called **tokens**. Modern tokenizers use algorithms like Byte-Pair Encoding (BPE) to learn the most statistically efficient way to decompose text.

For example, the word "Thermodynamics" might be split into three tokens: \["Thermo", "dynam", "ics"\]. Common words like "the" or "is" are typically single tokens, while rare or technical terms are broken into subword pieces. Each token is assigned a unique integer ID from the model's vocabulary (typically 50,000 to 100,000 entries).

A standard rule of thumb is that **1 token ≈ 0.75 English words**. When you hear that a model has a "context window of 128,000 tokens," it means it can hold roughly 96,000 words---approximately a 300-page book---in its working memory at one time.

> **Engineering Intuition:** Think of tokenization as meshing in FEA. Just as you discretize a continuous geometry into finite elements before computation, a tokenizer discretizes continuous text into discrete units before the neural network can process it.

#### 3.2 Embeddings: Meaning as Geometry

Once text is tokenized into integer IDs, these IDs are mapped to high-dimensional vectors called **Embeddings**. An embedding is a learned, dense numerical representation of a token's meaning.

Imagine a simplified 3D coordinate system where the x-axis represents "royalty," the y-axis represents "gender," and the z-axis represents "age." In this space, the vector for "King" and "Queen" would be close together on the royalty axis but separated on the gender axis. The vector for "Prince" would be close to "King" on royalty but offset on the age axis.

Modern LLMs use embedding spaces with **thousands of dimensions** (e.g., GPT-4 uses 12,288 dimensions). In this massive geometric space, semantic meaning is encoded as spatial relationships. The model learns during training that the vector for "stress" is geometrically close to "strain" and "Young's modulus" in engineering contexts, but close to "anxiety" and "cortisol" in biomedical contexts. The specific position of a token's embedding vector shifts based on the surrounding context, which is precisely what the self-attention mechanism computes.

> **Engineering Intuition:** Embeddings are analogous to a material's position in Ashby charts. Just as you plot materials by their Young's modulus vs. density to reveal clusters (metals, ceramics, polymers), embeddings plot words in a high-dimensional space where proximity reveals semantic clusters.

#### 3.3 Self-Attention: Context Is Everything

The heart of the Transformer architecture is the **Self-Attention mechanism** [<u>3</u>](https://arxiv.org/abs/1706.03762). Consider the sentence:

> "The crane lifted the steel beam because **it** was heavy."

What does the word "it" refer to? The crane or the beam? A human resolves this ambiguity instantly using contextual reasoning. Self-attention allows the model to do the same thing, computationally.

For every token in the input sequence, the self-attention layer computes three vectors: a **Query (Q)**, a **Key (K)**, and a **Value (V)**. These are obtained by multiplying the token's embedding by three learned weight matrices. The attention score between any two tokens is calculated as the dot product of one token's Query with the other token's Key. A high dot product means those two tokens are highly relevant to each other.

When processing the token "it," the self-attention mechanism computes attention scores against every other token in the sentence. It assigns a high score to "beam" and "heavy" (because the model has learned from billions of sentences that "it" in this grammatical structure refers to the subject of the "because" clause). The representation of "it" is then updated to be a weighted sum of all the Value vectors, with the weights determined by the attention scores. In effect, the meaning of "it" is dynamically rewritten to incorporate the context of "steel beam."

A Transformer model contains many such attention "heads" operating in parallel (e.g., GPT-3 has 96 heads per layer across 96 layers), each learning to attend to different types of relationships---syntactic, semantic, positional, and more.

#### 3.4 Next-Token Prediction: The Engine of Generation

Fundamentally, an LLM is a massive statistical engine trained to perform one deceptively simple task: **Next-Token Prediction**.

Given a sequence of tokens (your prompt), the model passes them through dozens of Transformer layers, applying self-attention and feed-forward computations at each layer. The final output is a **probability distribution over the entire vocabulary** for what the next token should be.

If the prompt is "Newton's third law states that for every action, there is an equal and opposite...", the model calculates that the token "reaction" has a probability approaching 100%. It selects "reaction," appends it to the sequence, and runs the entire process again to predict the token after that. This is called **autoregressive generation**---each new token is conditioned on all previously generated tokens.

The profound insight is that the illusion of intelligence, creativity, and even mathematical reasoning emerges entirely from the sheer scale of the data the model has consumed (trillions of tokens from books, papers, code repositories, and websites) and the complexity of the statistical relationships it has learned across its billions of parameters. When a model "solves" a differential equation, it is not performing symbolic algebra. It is predicting the sequence of tokens that statistically follows a differential equation prompt, based on having seen thousands of solved examples during training.

## Part II --- Bridging the Gap: Environments, APIs, and the Agentic Frontier

### 4. Setting Up the Engineering Workspace

To build AI agents, we must move out of web browsers and into proper software development environments. While you may have written MATLAB scripts or basic Python code for previous courses, building agentic systems requires a more structured approach to managing software dependencies and secrets.

#### 4.1 The Virtual Environment

When you install Python packages (like numpy or scipy), they are installed globally on your computer by default. However, AI libraries are updated at a blistering pace---the openai Python library has had over 30 major releases in the past two years. If Project A requires langchain version 0.1 and Project B requires langchain version 0.3, a global installation will cause one of your projects to break.

The solution is a **Virtual Environment**. Created using Python's built-in venv module or the conda package manager, a virtual environment is an isolated, self-contained directory that houses a specific Python interpreter and a specific set of packages. When you "activate" a virtual environment, any package you install via pip is contained entirely within that project folder. When you deactivate it, your system returns to its default state.

This ensures **reproducibility**---a critical requirement for scientific research. You can share a requirements.txt file listing every package and its exact version, and a collaborator on the other side of the world can recreate your exact software environment in seconds.

#### 4.2 Managing Secrets: The .env File

When writing code that interacts with commercial AI models, you will be issued an **API key**---a long string of characters (e.g., sk-proj-abc123...) that acts simultaneously as your password and your billing account. **Never hardcode your API key directly into your Python script.** If you upload that script to GitHub, automated bots will scrape your key within seconds and use it to run up thousands of dollars in charges against your account.

Instead, we use a **.env (dotenv) file**. This is a plain text file stored locally on your machine that contains your secrets:

OPENAI_API_KEY=sk-proj-abc123...

ANTHROPIC_API_KEY=sk-ant-xyz789...



In your Python code, you use the python-dotenv library to load these variables into memory at runtime. The .env file must always be added to your .gitignore file to ensure it is never committed to version control. This is a non-negotiable security practice.

### 5. What Is an API? (Explained for Engineers)

If you want to use ChatGPT, you open a web browser, type in a box, and read the response on screen. But how does a Python script---running headlessly on a server---talk to an LLM? It uses an **API (Application Programming Interface)** [<u>5</u>](https://aws.amazon.com/what-is/api/).

#### 5.1 The Restaurant Analogy

An API is a standardized mechanism that allows two distinct software systems to communicate with each other. The classic analogy is a restaurant:

| **Restaurant Component** | **Software Equivalent** | **Role** |
|----|----|----|
| **You (the diner)** | Your Python script (the **Client**) | Knows what it wants but cannot cook |
| **The Menu** | The API specification (endpoints, parameters) | Defines what you are allowed to request |
| **The Waiter** | The HTTP protocol (the **API**) | Carries your structured order to the kitchen and brings back the result |
| **The Kitchen** | OpenAI's servers (the **Server**) | Has the ingredients (compute, model weights) to prepare the response |
| **The Bill** | Token-based pricing | You pay per item (token) consumed |

You never see the kitchen. You never touch the ingredients. You interact only through the standardized interface of the menu and the waiter. This abstraction is precisely what an API provides.

#### 5.2 Anatomy of an API Call

In technical terms, an API call to an LLM involves four components:

1.  **The Endpoint:** A URL that specifies which service you are requesting (e.g., https://api.openai.com/v1/chat/completions).

2.  **The Headers:** Metadata sent with the request, including your API key for authentication.

3.  **The Request Body (JSON):** A structured data payload containing your prompt, the model name, and configuration parameters like temperature (which controls randomness).

4.  **The Response Body (JSON):** The structured data returned by the server, containing the model's generated text, token usage counts, and metadata.

**JSON (JavaScript Object Notation)** is the lingua franca of APIs. It is a lightweight, human-readable format for structuring data as key-value pairs. For example:

{

"model": "gpt-4.1",

"messages": \[

{"role": "system", "content": "You are a structural engineering assistant."},

{"role": "user", "content": "What is the moment of inertia of a rectangular cross-section?"}

\],

"temperature": 0.2

}



The server processes this request, runs the prompt through the LLM, and returns a response containing the generated text. Crucially, **APIs charge by the token**. You pay a fraction of a cent for every token you send (input tokens) and every token the model generates (output tokens). Understanding token economics is essential for building cost-effective agents.

### 6. The Art and Science of Prompt Engineering

When interacting with an LLM through an API, the text you send is your **prompt**. Prompt engineering is not a dark art; it is essentially programming in natural language [<u>6</u>](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api). The quality of the output is directly and measurably determined by the quality of the input.

#### 6.1 Zero-Shot vs. Few-Shot Prompting

**Zero-shot prompting** means asking the model to perform a task without providing any examples. For instance: "Classify the following concrete failure mode: spalling near the rebar layer." The model relies entirely on its pre-trained knowledge to generate a response.

**Few-shot prompting** means providing the model with several examples of the desired input-output mapping before presenting the actual task. For instance:

Example 1: "Cracking along the tension face of a beam" -\> Flexural Failure

Example 2: "Diagonal cracks near the support" -\> Shear Failure

Example 3: "Spalling near the rebar layer" -\> ?



By providing examples, you are leveraging the self-attention mechanism to help the model recognize the pattern and format you expect. Few-shot prompting consistently and significantly outperforms zero-shot prompting on structured tasks.

#### 6.2 Chain-of-Thought (CoT) Prompting

For engineering mathematics, standard prompting often fails. If you ask an LLM to calculate the deflection of a simply supported beam under a point load, it might attempt to jump directly to the final numerical answer and get it wrong.

**Chain-of-Thought (CoT) prompting** involves explicitly instructing the model to "think step-by-step" or "show your work." By forcing the model to generate the intermediate mathematical steps---the formula, the variable substitution, the unit conversion, the arithmetic---you are giving the model more tokens of "thinking time." Each generated intermediate token becomes part of the context window, guiding the next-token prediction toward the correct final result. Research has shown that CoT prompting can improve mathematical reasoning accuracy by 20--40% on standard benchmarks [<u>7</u>](https://arxiv.org/abs/2201.11903).

#### 6.3 Structuring Outputs for Engineering Pipelines

A critical skill for this course is instructing the model to return its output in a structured format---typically **JSON**---rather than free-form prose. If your agent needs to extract material properties from a research paper and feed them into a simulation script, you need the output to be machine-readable:

Respond ONLY with a JSON object in the following format:

{

"material": "\<name\>",

"youngs_modulus_GPa": \<number\>,

"yield_strength_MPa": \<number\>,

"density_kg_m3": \<number\>

}



This transforms the LLM from a conversational partner into a structured data extraction engine---a far more powerful role in an engineering workflow.

### 7. From Chatbots to Autonomous Agents

The final conceptual leap for this week is understanding the difference between a chatbot and an AI agent [<u>8</u>](https://www.ibm.com/think/topics/ai-agents) [<u>9</u>](https://www.salesforce.com/agentforce/ai-agent-vs-chatbot/).

#### 7.1 The Limitations of Chatbots

A chatbot is **reactive**. It sits idle until a user provides a prompt. It generates a single text response and then returns to an idle state. If it makes a mathematical error in its response, it does not know it made an error unless the user explicitly points it out. It is confined entirely to the text domain---it cannot run code, access databases, or interact with the physical world.

#### 7.2 The Four Pillars of an AI Agent

An **AI Agent** is **proactive**. It is an autonomous system designed to achieve a specific goal by observing its environment, making decisions, and taking actions. An agent is built on four pillars:

| **Pillar** | **Description** | **Engineering Example** |
|----|----|----|
| **LLM Core** | The "brain" responsible for reasoning, planning, and language comprehension | Interprets the goal: "Optimize this truss for minimum weight" |
| **Memory** | Short-term (conversation history) and long-term (vector database of documents) context retention | Remembers the AISC Steel Manual specifications retrieved earlier |
| **Planning** | The ability to decompose a complex goal into a sequence of manageable sub-tasks | Breaks the goal into: (1) define loads, (2) parameterize geometry, (3) write FEA script, (4) run optimization loop |
| **Tools** | External capabilities the agent can invoke: code execution, web search, database queries, simulation software | Executes a Python script that calls an FEA solver and reads the output |

#### 7.3 The ReAct Pattern: Reason + Act

The most common and foundational architecture for building agents is the **ReAct (Reason + Act) pattern** [<u>10</u>](https://arxiv.org/abs/2210.03629). When given a goal, the agent enters a loop:

**Step 1 --- Reason:** The LLM analyzes the current state and decides what to do next. *("I need to calculate the area moment of inertia for this W-shape. I should write a Python function.")*

**Step 2 --- Act:** The LLM generates a specific command to invoke a tool. *("Execute the following Python code: I = (b \* h\*\*3) / 12...")*

**Step 3 --- Observe:** The tool executes in the environment, and the output (or error message) is fed back into the LLM's context window. *("Output: I = 4.526e-05 m^4")*

**Step 4 --- Repeat:** The LLM reads the observation, updates its reasoning, and takes the next action. The loop continues until the agent determines that the original goal has been achieved, at which point it returns the final result to the user.

This loop is the fundamental mechanism that transforms a passive text generator into an active problem-solving system. When the Python script throws an error, the agent reads the traceback, reasons about the bug, writes a corrected script, and tries again---all without human intervention.

#### 7.4 Multi-Agent Systems

A single agent can be powerful, but complex engineering tasks often benefit from **Multi-Agent Systems**---architectures where several specialized agents collaborate. For example, a structural design workflow might involve:

1.  An **Engineer Agent** that writes Python code to perform calculations.

2.  A **Reviewer Agent** that checks the Engineer's code and results against design standards.

3.  A **User Proxy Agent** that executes the code in a sandboxed environment and returns the output.

These agents communicate through structured messages, debating and refining the solution iteratively. We will implement multi-agent systems in Week 3 of this course using multi-agent frameworks.

### 8. The Frontier of Scientific Discovery

We conclude this week's lecture by looking at the frontier---the real-world applications that motivate this entire course.

In November 2023, Google DeepMind published a landmark paper in *Nature* describing **GNoME (Graph Networks for Materials Exploration)**, an AI system that discovered 2.2 million new stable crystal structures---an order-of-magnitude expansion in the number of stable materials known to humanity [<u>11</u>](https://www.nature.com/articles/s41586-023-06735-9). This was not a chatbot answering questions about materials; it was an autonomous system that generated candidate structures, predicted their stability using graph neural networks, and validated the results against density functional theory calculations.

In the autonomous laboratory space, researchers are building **self-driving laboratories** where AI agents design experiments, robotic systems execute them, and the AI analyzes the results to design the next round of experiments---closing the loop entirely [<u>12</u>](https://royalsocietypublishing.org/rsos/article/12/7/250646/235354). In civil engineering, AI agents are being deployed to automatically check structural designs against building codes, dramatically reducing the time and cost of compliance review [<u>13</u>](https://aecmag.com/features/ai-agents-for-civil-engineers/).

These are not science fiction scenarios. They are published, peer-reviewed results from the last two years. This course will give you the foundational skills to build such systems.

## Assigned Reading for Week 1

| **Priority** | **Reference** | **Description** |
|----|----|----|
| **Required** | Wei, J. et al. (2025). "From AI for Science to Agentic Science: A Survey on Autonomous Scientific Discovery." arXiv:2508.14111 | Sections 1–4 (autonomy levels, five core capabilities, discovery workflow) + the materials-science domain section. |
| **Required** | OpenAI (2024). "Best Practices for Prompt Engineering." | Practical guide to structuring prompts for the OpenAI API. |
| **Supplementary** | Vaswani, A. et al. (2017). "Attention Is All You Need." *NeurIPS*. | The original Transformer paper. Focus on Sections 1--3. |
| **Supplementary** | Alammar, J. (2018). "The Illustrated Transformer." *jalammar.github.io* | Excellent visual walkthrough of the self-attention mechanism. |
| Supplementary | Gridach, M. et al. (2025). "Agentic AI for Scientific Discovery: A Survey." ICLR 2025 Workshop on Agentic AI (arXiv:2503.08979) | The first major survey of the field; historical framing. |
| Supplementary | Bisht, H., Kumar, V., Jablonka, K. M., Mausam, and Krishnan, N. M. A. (2026). "Agentic AI Scientists Are Not Built for Autonomous Scientific Discovery." arXiv:2605.08956 | Critical counterpoint — read before believing the demos. |

## References
