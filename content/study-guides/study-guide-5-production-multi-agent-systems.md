---
title: "Study Guide 5 Production Multi Agent Systems"
week: 0
doc_type: "study_guide"
access: "all_students"
agents: [all_student_agents]
source: "materials/Study Guides/Study_Guide_5_Production_Multi_Agent_Systems.docx"
source_hash: "63f16790daed0963"
normalized_at: "2026-08-19T11:55:16Z"
---
# Study Guide 5: Production Multi-Agent Systems

# *Companion guide to Week 9 (Evaluation, Reliability & Deployment) and Lab 9 (the reliability audit of your capstone system). Primary neutral sources: Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (MAST, NeurIPS 2025) — Ref_25; tau-bench (Yao et al.) — Ref_33; the MCP specification — Ref_19. Framework examples in this guide (neuro-san, sly_data, AAOSA — "Adaptive Agent-Oriented Software Architecture") are one vendor's implementation of these ideas; the concepts, not the framework, are examinable.*

**ME/CE 295 — AI Agents for Accelerating Scientific Discovery and Engineering Research**

**California Institute of Technology — Division of Engineering and Applied Science**

## Overview

This study guide covers the transition from prototype multi-agent systems to production-ready deployments. It synthesizes concepts from Weeks 3, 7, 8, and 9 into a practical reference for building agent systems that work reliably in real engineering and research environments.

**Primary Source:** Cognizant AI Lab (2026). "Why Your Multi-Agent Network Works in Demo but Falls Apart in the Wild." *Decision AI Bytes.*

## 1. Coordination Patterns

### Centralized Orchestration (Default Pattern)

- **How it works:** A single "manager" agent routes all tasks to specialist agents

- **Pros:** Clear control point, easy to reason about when small

- **Cons:** Accumulates responsibility; becomes bottleneck; every change requires updating the central layer

- **When to use:** Systems with \<5 agents and well-defined task boundaries

### Decentralized Coordination (AAOSA Pattern)

- **How it works:** Agents evaluate input and *claim* responsibility for parts they can handle

- **Pros:** Modular, scalable, no single point of failure

- **Cons:** Harder to predict behavior, requires clear capability descriptions per agent

- **When to use:** Systems that need to scale, evolve, or handle ambiguous inputs

- **Framework:** neuro-san (Apache 2.0, Cognizant AI Labs)

### Comparison Table

| Aspect             | Centralized                  | Decentralized (AAOSA)   |
|--------------------|------------------------------|-------------------------|
| Adding agents      | Requires orchestrator update | Plug-and-play           |
| Failure mode       | Single point of failure      | Graceful degradation    |
| Ambiguity handling | Forced early resolution      | Collective resolution   |
| Debugging          | Trace through one point      | Trace emergent behavior |
| Scale limit        | ~10 agents before bottleneck | Hundreds of agents      |

## 2. The Model Context Protocol (MCP)

### What MCP Solves

Integration logic fragments as systems grow. Each tool has its own interface, auth model, and data format. MCP provides a **consistent interface layer** so agents interact with all tools uniformly.

### Key Concepts

- **Tool registration:** Tools declare their capabilities in a standard schema

- **Uniform access:** Agents use the same protocol regardless of underlying implementation

- **Discovery:** Agents can find available tools at runtime

- **Composability:** Tools can be combined without custom glue code

### MCP vs. Ad-Hoc Integration

| Dimension               | Ad-Hoc                    | MCP                |
|-------------------------|---------------------------|--------------------|
| Adding 1st tool         | Same effort               | Same effort        |
| Adding 10th tool        | 10x effort + interactions | Linear effort      |
| Changing a tool's API   | Update every consumer     | Update one adapter |
| Agent discovering tools | Hard-coded knowledge      | Runtime discovery  |
| Testing                 | Mock each connector       | Mock the protocol  |

## 3. Behavioral Testing Methodology

### Why Traditional Testing Fails

Traditional software testing asserts: *given input X, output must equal Y*. Multi-agent systems break this because:

- LLMs are non-deterministic (same prompt → different reasoning paths)

- Variability compounds across multiple agents

- Surface-level correctness ≠ process correctness

### The Behavioral Testing Framework

**Step 1: Define behavioral properties (not just outputs)**

- Does the system use the correct tools in the correct order?

- Does it respect constraints and stop conditions?

- Does it escalate appropriately when uncertain?

**Step 2: Run repeatedly (statistical evaluation)**

- Minimum 20-50 runs per critical test case

- Measure: success rate, consistency, latency distribution, failure clustering

**Step 3: Classify failures**

- **Output failure:** Wrong answer, but correct process

- **Process failure:** Right answer (by luck), wrong process

- **Cascade failure:** One agent's error propagates through the system

- **Silent failure:** Plausible output, constraint violated

**Step 4: Monitor continuously**

- Track behavioral metrics over time (not just accuracy)

- Alert on process deviations, not just output errors

- Regression testing: does adding/changing an agent degrade existing behaviors?

## 4. Data Isolation Patterns

### The sly_data Pattern

**Problem:** Production agents need access to real data (proprietary, sensitive, structured) but cannot safely pass it through LLM reasoning.

**Solution:** A protected channel that passes data *between* agents without exposing it *to* the model.

┌─────────────┐ reasoning ┌─────────────┐

│ Agent A │ ──────────────── │ Agent B │

│ │ │ │

│ sly_data │ ═══════════════\> │ sly_data │

│ (protected)│ direct pass │ (protected)│

└─────────────┘ └─────────────┘

**Properties:**

- Data never appears in prompts or LLM context

- Agents reason *about* data abstractly while operating *on* it precisely

- Audit trail shows what data moved where

- Compliance built into architecture

### When to Use Data Isolation

| Data Type | Isolation Needed? | Pattern |
|----|----|----|
| Public reference data | No | Pass directly |
| Internal experimental results | Maybe | Tag sensitivity level |
| Patient/subject data | Yes | sly_data + access control |
| Proprietary compositions | Yes | sly_data + audit log |
| Financial/cost data | Yes | sly_data + role-based access |

## 5. Prototype-to-Production Checklist

### Phase 1: Working Prototype (Vibe Coding)

- System produces correct output for happy-path inputs

- Basic agent communication established

- Core tools connected

### Phase 2: Robustness Testing

- Run 50+ times on varied inputs

- Document failure modes and rates

- Test tool failures (timeout, unexpected response, unavailability)

- Test coordination failures (agents disagree, duplicate work, infinite loops)

- Measure latency distribution (not just average)

### Phase 3: Production Hardening

- Operating contracts defined for every agent (acceptance criteria + stop conditions)

- Data flows mapped and sensitive data isolated

- Observability: can trace any decision back to its source

- Integration layer standardized (MCP or equivalent)

- Graceful degradation: system handles partial failures

- Human escalation paths defined and tested

### Phase 4: Deployment & Monitoring

- Behavioral metrics dashboard (not just accuracy)

- Alerting on process deviations

- Regression test suite for agent changes

- Capacity planning: latency impact of adding agents

- Documentation: system architecture, data flows, failure modes

## Key Vocabulary

| Term | Definition |
|----|----|
| **AAOSA** | Adaptive Agent-Oriented Software Architecture — decentralized coordination where agents claim tasks |
| **MCP** | Model Context Protocol — standardized interface for agent-tool communication |
| **sly_data** | Protected data channel between agents that bypasses LLM reasoning |
| **Operating contract** | Explicit definition of acceptance criteria and stop conditions for an agent workflow |
| **Behavioral testing** | Statistical evaluation of system behavior across many runs |
| **Vibe coding** | Building systems by describing intent in natural language and iteratively refining |
| **Coordination bottleneck** | When a central orchestrator accumulates too much responsibility |
| **Surface correctness** | System appears correct but violates process constraints |

## Recommended Reading

1.  Cognizant AI Lab (2026). "Why Your Multi-Agent Network Works in Demo but Falls Apart in the Wild." *Decision AI Bytes.*

2.  Cognizant AI Lab (2026). "Vibe Coding Agentic Networks You Can Actually Deploy with neuro-san." *Decision AI Bytes.*

3.  Cognizant AI Lab (2026). "Introducing Agentic AI 101." *Decision AI Bytes.*

4.  neuro-san GitHub repository: https://github.com/cognizant-ai-labs/neuro-san (Apache 2.0)

5.  Augment Code (2026). "Multi-Agent AI Systems: Why They Fail and How to Fix Coordination Issues."

6.  MIT (2025). "State of AI in Business Report."

## Practice Problems

1.  **Architecture Decision:** You are building a multi-agent system for autonomous materials characterization. The system has 12 specialized agents (XRD analysis, SEM imaging, tensile testing, etc.). Would you use centralized orchestration or AAOSA? Justify with at least 3 criteria.

2.  **Failure Classification:** A multi-agent literature review system returns a plausible summary but cites 2 papers that don't exist. Classify this failure (output, process, cascade, or silent) and explain why.

3.  **Data Isolation Design:** Design the data flow for a multi-agent drug discovery pipeline that must handle patient genetic data, proprietary compound structures, and published literature. Which data requires sly_data channels?

4.  **Behavioral Test Design:** Write a behavioral test specification for a 3-agent structural design system (Designer → Analyzer → Reviewer). What properties should you test beyond "correct final design"?

5.  **MCP Integration:** You have a lab with 5 instruments, each with different APIs (REST, gRPC, serial, file-based, MQTT). Sketch an MCP-based architecture that lets any agent access any instrument through a uniform interface.
