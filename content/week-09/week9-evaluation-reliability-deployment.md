---
title: "Week9 Evaluation Reliability Deployment"
week: 9
doc_type: "lecture_notes"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 9/Week9_Evaluation_Reliability_Deployment.docx"
source_hash: "c52fb64ce30e6753"
normalized_at: "2026-08-19T11:55:21Z"
---
**ME/CE 295 — Week 9 Lecture Notes**

**Evaluation, Reliability, and Deployment**

California Institute of Technology — Division of Engineering and Applied Science. Course: AM/ME/CE 295 — AI Agents for Accelerating Scientific Discovery and Engineering Research. Week: 9 of 10. Lectures: Tuesday only this week (Nov 24) — Thursday is Thanksgiving. 1:00–2:30 p.m. \| Laboratory: 5 hours, at-home (reliability audit of your capstone system).

**Lecture Outline at a Glance**

A single 90-minute session this week. The center of gravity is the at-home laboratory, in which you run a structured reliability audit on your own capstone agent system one week before final presentations.

| **Time** | **Duration** | **Topic** | **Key Takeaway** |
|----|----|----|----|
| 0:00–0:05 | 5 min | Week 9 objectives | From "it works on my machine" to evidence of reliability |
| 0:05–0:25 | 20 min | Hallucination in safety-critical contexts | Fabricated code provisions and impossible physics are silent hazards |
| 0:25–0:45 | 20 min | Uncertainty quantification and calibration | "90% confident" must mean right 90% of the time |
| 0:45–1:05 | 20 min | Behavioral testing of stochastic systems | Reliability is a property of behavior over many runs, not one output |
| 1:05–1:20 | 15 min | Data control and the production-readiness checklist | Deployment is an architecture question, not a demo question |
| 1:20–1:30 | 10 min | Lab 9 briefing | Auditing your own capstone system |

**Part I — Hallucination in Safety-Critical Contexts**

In creative writing, an LLM hallucination is a quirky feature; in engineering, it is a potential safety hazard. Studies evaluating LLMs for static analysis have shown that models frequently generate highly confident but entirely fabricated outputs. Common engineering hallucinations include:

- **Fabricated regulatory or standards provisions:** An LLM might confidently cite "ASCE 7-22 Section 12.8.4.5" for a seismic parameter when that subsection does not exist.

- **Impossible material properties:** Generating a Young’s modulus for steel that is off by an order of magnitude, presented with authoritative formatting.

- **Flawed arithmetic:** Accurately setting up a beam-deflection equation but failing the arithmetic.

Mitigations include neuro-symbolic architectures that combine LLM reasoning with deterministic rule-based checking against digitized codes and standards, and multi-agent review (Week 3): a specialized Reviewer agent independently verifies the math and citations of the Designer agent.

**Part II — Uncertainty Quantification and Calibration**

If an agent recommends a flange thickness for an aerospace bracket, the engineer must know how confident the model is. UQ methods include token-level probability analysis and consistency-based methods: prompt the model multiple times at high temperature; if it returns wildly different dimensions each time, uncertainty is high.

Crucially, confidence must be calibrated: a model that states "I am 90% confident this beam will not yield" must be correct 90% of the time. Poorly calibrated overconfidence is the most dangerous property an engineering tool can have.

**Part III — Behavioral Reliability in Multi-Agent Systems**

In early development, reliability is judged by whether the system produces the correct output for a given input. This breaks down in multi-agent settings: LLMs are non-deterministic; with multiple agents, variability compounds; a slightly different routing decision cascades into a different sequence of actions; and a system can appear correct while failing to follow the intended process. Reliability in multi-agent systems is a property of behavior over time, not of individual outputs.

| **Testing dimension** | **What to measure** | **Minimum runs** |
|----|----|----|
| Consistency | Same input → same outcome (within tolerance) | 20–50 per test case |
| Accuracy | Correct outcomes across varied inputs | 100+ across input space |
| Process adherence | Correct sequence of actions, not just final result | Every run (traced) |
| Degradation patterns | Where and how failures cluster | Continuous monitoring |

**The surface-correctness trap:** A system may produce plausible answers while quietly missing important constraints. Catching this requires observing behavior across many runs, identifying where failures occur, and understanding how changes propagate.

**Part IV — Data Control in Deployed Agent Systems**

How data is handled must be decoupled from how agents reason about it. In production, agents work with structured, proprietary, or sensitive data that cannot simply be passed through a language model. A protected data channel between agents (e.g., the sly_data pattern) keeps sensitive fields out of prompts and reasoning traces, makes data flows explicit and auditable, and builds governance into the architecture. Engineering examples: proprietary material compositions in materials-discovery workflows, confidential experimental results before publication, and cost data in optimization agents.

**Part V — The Production-Readiness Checklist**

Before deploying any multi-agent system from this course into a real research environment:

- **1. Coordination architecture review.** Is there a single coordination bottleneck? Can new agents be added without modifying existing orchestration? Are responsibilities bounded with explicit ownership?

- **2. Integration audit.** Are tools connected via a consistent interface (MCP, Week 3/8) or one-off connectors? What happens when a tool returns an unexpected error?

- **3. Behavioral testing.** Has the system run 20+ times on critical test cases? Are failure modes documented and classified? Is there observability into agent communication traces?

- **4. Data-flow mapping.** Are sensitive fields identified, protected, and passed outside prompts? Are per-agent data permissions explicit and auditable?

- **5. Operating contracts.** Does every workflow have an explicit, machine-enforceable definition of "done"? Are stop conditions defined and constraint violations escalated to humans?

**Laboratory 9 (5 hours, at-home) — Reliability Audit of Your Capstone System**

Run a structured behavioral test suite on your own capstone agent system: (a) define 3–5 critical test cases; (b) execute each 20+ times, tracing agent communications; (c) classify failures (process vs. output; syntax vs. runtime vs. physically implausible results, per Week 7); (d) apply the production-readiness checklist and document the gaps. Deliverable: a 1–2 page reliability report appended to your capstone repository. Checkpoint (hour 2): first test case executed 20 times with traces captured.

**References**

Core reading: Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (MAST), NeurIPS 2025 — Ref_25; its 14-mode failure taxonomy and process-vs-output distinction underpin Parts III–V and Lab 9. Supplementary: tau-bench (Ref_33) for reproducible agent evaluation; MCP specification (Ref_19) for integration audits.
