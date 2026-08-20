---
title: "Week 9 Slides"
week: 9
doc_type: "lecture_slides"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 9/ME_CE_295_Week_9_Slides.pptx"
source_hash: "c1e0d9c955492f58"
normalized_at: "2026-08-19T11:55:21Z"
---
## Slide 1

ME/CE 295 · WEEK 9 OF 10 · TUESDAY NOV 24 (SINGLE SESSION — THANKSGIVING WEEK)

Evaluation, Reliability,
and Deployment

From “it works in the demo” to evidence of reliability — hallucination, calibration, behavioral testing, and the production-readiness checklist.

California Institute of Technology · Division of Engineering and Applied Science

## Slide 2

PART I

Hallucination in Safety-Critical Contexts

In creative writing, hallucination is a quirk. In engineering, it is a safety hazard: models generate highly confident, entirely fabricated outputs.

Fabricated standards provisions

Confidently citing “ASCE 7-22 §12.8.4.5” for a seismic parameter — a subsection that does not exist.

Impossible material properties

A Young’s modulus for steel off by an order of magnitude, in authoritative formatting.

Flawed arithmetic

Correct beam-deflection setup; failed arithmetic.

MITIGATIONS

Neuro-symbolic checking — LLM reasoning paired with deterministic, rule-based verification against digitized codes and standards.

Multi-agent review (Week 3) — a Reviewer agent independently verifies the Designer agent’s math and citations.

Grounded retrieval (Week 4) — answers must cite retrieved sources, never free-recalled provisions.

## Slide 3

PART II

Uncertainty Quantification and Calibration

If an agent recommends a flange thickness for an aerospace bracket, the engineer must know how confident the model is — and whether that confidence means anything.

Token-level probability

How certain was the model about each next token? Low-probability regions flag uncertain claims.

Consistency-based UQ

Prompt repeatedly at high temperature. Wildly different dimensions each run = high uncertainty.

Calibration

“90% confident this beam will not yield” must be right 90% of the time. Overconfidence is the most dangerous property a tool can have.

Rule of thumb: an uncalibrated confidence number is decoration, not information. Demand calibration curves before trusting stated confidence.

## Slide 4

PART III

Behavioral Testing of Stochastic Agent Systems

Single-output testing fails for multi-agent systems: non-determinism compounds across agents, and one routing change cascades into a different action sequence. Reliability is a property of behavior over many runs.

The surface-correctness trap: a system can produce plausible answers while quietly missing constraints. Catch it by observing behavior across many runs, locating failure clusters, and tracing how changes propagate.

## Slide 5

PART IV

Data Control in Deployed Agent Systems

How data is handled must be decoupled from how agents reason about it. Production agents touch structured, proprietary, and sensitive data that must never be pasted into a prompt.

The protected-channel pattern

Pass sensitive fields between agents outside the model context (e.g., the sly_data pattern): data flows become explicit and auditable, sensitive fields never enter prompts or reasoning traces, and governance is built into the architecture rather than bolted on.

ENGINEERING EXAMPLES

Proprietary material compositions in a materials-discovery workflow

Confidential experimental results before publication

Cost and supplier data in optimization agents

Export-controlled geometry or performance data in simulation pipelines

## Slide 6

PART V

The Production-Readiness Checklist

1 · Coordination architecture

Single bottleneck? Can agents be added without rewiring orchestration? Bounded responsibilities with explicit ownership?

2 · Integration audit

Tools behind a consistent interface (MCP — Weeks 3, 8) or one-off connectors? What happens on unexpected tool errors?

3 · Behavioral testing

20+ runs on critical cases; failure modes documented and classified; traces observable; process vs. output failures distinguishable.

4 · Data-flow mapping

Sensitive fields identified and protected; per-agent permissions explicit; flows auditable.

5 · Operating contracts

Machine-enforceable definition of “done”; stop conditions against infinite loops; violations escalate to humans.

## Slide 7

LAB 9 · 5 HOURS, AT-HOME · DUE BEFORE TUE DEC 1

Reliability Audit of Your Own Capstone System

a)  Define 3–5 critical test cases for your capstone agent system.

b)  Execute each 20+ times, capturing agent communication traces.

c)  Classify failures: process vs. output; syntax vs. runtime vs. physically implausible (Week 7 taxonomy).

d)  Apply the five-part production-readiness checklist and document the gaps.

Deliverable: a 1–2 page reliability report appended to your capstone repository.

Checkpoint (hour 2): first test case executed 20 times with traces captured.

No class Thursday (Thanksgiving). Quiz 9 online. No deadlines Nov 25–29. Next week: ethics, professional practice, and final presentations.
