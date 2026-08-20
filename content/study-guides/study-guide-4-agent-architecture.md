---
title: "Study Guide 4 Agent Architecture"
week: 0
doc_type: "study_guide"
access: "all_students"
agents: [all_student_agents]
source: "materials/Study Guides/Study_Guide_4_Agent_Architecture.docx"
source_hash: "28b0107792702cd3"
normalized_at: "2026-08-19T11:55:16Z"
---
# Study Guide 4: Agent Architecture Patterns

**Course:** ME/CE 295 — AI Agents for Accelerating Scientific Discovery and Engineering Research  
**Author:** Manus AI

An "Agent" is not just an LLM. An LLM is a stateless text-completion engine. An Agent is a system that wraps an LLM with **Memory**, **Planning**, and **Tools**, allowing it to interact with the environment (e.g., a file system, an API, or a simulation software) over multiple steps to achieve a goal.

This guide outlines the primary architectural patterns used to build AI agents for engineering workflows.

## 1. The ReAct Pattern (Reasoning + Acting)

The ReAct (Reason + Act) pattern forces the LLM to explicitly write out its thought process before deciding on an action. This prevents the model from hallucinating tool inputs and allows for complex, multi-step problem solving.

### 1.1 The ReAct Loop

1.  **Thought:** The agent analyzes the current state and decides what to do next.

2.  **Action:** The agent selects a tool and provides the arguments.

3.  **Observation:** The tool executes and returns the result to the agent. *(Repeat until the goal is achieved)*

### 1.2 Implementation with LangChain

In this example, we give the agent a custom tool to calculate the moment of inertia for a rectangular beam.

from langchain_openai import ChatOpenAI

from langchain.agents import create_react_agent, AgentExecutor

from langchain.tools import tool

from langchain_core.prompts import PromptTemplate

\# 1. Define a custom engineering tool

@tool

def calculate_moment_of_inertia(width: float, height: float) -\> float:

"""

Calculates the area moment of inertia (I) for a solid rectangular cross-section.

Args:

width: The width of the base (b)

height: The height of the section (h)

Returns:

The moment of inertia (I = b\*h^3 / 12)

"""

return (width \* (height \*\* 3)) / 12.0

tools = \[calculate_moment_of_inertia\]

\# 2. Define the ReAct prompt template

template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer

Thought: you should always think about what to do

Action: the action to take, should be one of \[{tool_names}\]

Action Input: the input to the action

Observation: the result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer

Final Answer: the final answer to the original input question

Begin!

Question: {input}

Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)

\# 3. Initialize the agent and executor

llm = ChatOpenAI(model="gpt-4o", temperature=0)

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

\# 4. Run the agent

\# response = agent_executor.invoke({"input": "What is the moment of inertia for a beam with width 200mm and height 400mm?"})



## 2. The Reflection Pattern (Self-Correction)

LLMs often make mistakes when generating code (e.g., OpenSees Tcl scripts or Python simulation scripts). The Reflection pattern pairs a "Generator" agent with a "Critic" agent (or uses the same agent in a second pass) to review and correct the output.

### 2.1 The Code-Execution-Correction Loop

For engineering simulations, the best "Critic" is the compiler or the simulation engine itself.

1.  **Generate:** Agent writes the simulation script (e.g., model.py).

2.  **Execute:** A Python subprocess tool runs python model.py.

3.  **Reflect:** If the script crashes, the error traceback (Observation) is fed back to the Agent.

4.  **Correct:** The Agent reads the traceback, identifies the syntax or logical error, and rewrites the script.

### 2.2 System Prompt for a Coding Agent

You are an expert computational mechanics engineer writing OpenSeesPy scripts.

Write the script to solve the user's problem.

If you receive an error traceback from a previous execution, analyze the error.

Identify exactly which line caused the failure and why.

Then, provide the fully corrected script. Do not omit any parts of the code.



## 3. Multi-Agent Systems (AutoGen)

For complex engineering tasks, a single agent can become overwhelmed by conflicting instructions (e.g., "be creative in design" vs. "be strictly compliant with building codes"). Multi-agent systems assign distinct personas to different agents and let them converse.

### 3.1 The AutoGen Framework

Microsoft's AutoGen framework is excellent for this. You define agents and set up a "Group Chat."

import autogen

config_list = \[{"model": "gpt-4o", "api_key": "your-api-key"}\]

\# 1. Define the User Proxy (can execute code)

user_proxy = autogen.UserProxyAgent(

name="User_Proxy",

system_message="A human admin. Executes code written by the Engineer.",

code_execution_config={"work_dir": "simulation_workspace", "use_docker": False},

human_input_mode="NEVER"

)

\# 2. Define the Engineer (writes the simulation)

engineer = autogen.AssistantAgent(

name="Structural_Engineer",

system_message="""You are a structural engineer.

Write Python code using the \`openseespy\` library to model the structure requested.

Ensure the code saves the nodal displacements to a file.""",

llm_config={"config_list": config_list}

)

\# 3. Define the Reviewer (checks the results)

reviewer = autogen.AssistantAgent(

name="Code_Reviewer",

system_message="""You are a senior code reviewer.

Review the Engineer's code for physical realism and boundary condition correctness.

If the code is correct, say 'APPROVED'. If not, explain the flaw.""",

llm_config={"config_list": config_list}

)

\# 4. Initiate the chat

\# groupchat = autogen.GroupChat(agents=\[user_proxy, engineer, reviewer\], messages=\[\], max_round=10)

\# manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

\# user_proxy.initiate_chat(manager, message="Model a 2D cantilever beam with a point load of 10kN at the free end.")

### 3.2 Why Multi-Agent?

In the example above, the Structural_Engineer focuses purely on translating physics to code, while the Code_Reviewer acts as a safeguard against hallucinated boundary conditions or unrealistic material properties. The User_Proxy provides the actual computational environment to test the code. This mirrors a real-world engineering firm's workflow.
