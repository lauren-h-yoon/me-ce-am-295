---
title: "Week8 Lecture Outline"
week: 8
doc_type: "lecture_outline"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 8/Week8_Lecture_Outline.docx"
source_hash: "1d568f796c6612de"
normalized_at: "2026-08-19T11:55:20Z"
---
# Week 8 Lecture Outline: Generative Design, Materials Discovery, and Autonomous Laboratories

**Format: Tuesday & Thursday lectures, 1:00–2:30 p.m. (2 × 90 minutes) + 5-hour at-home laboratory. Target Audience: Mechanical Engineering and Materials Science graduate students and senior undergraduates Prerequisites: Completion of Weeks 1-7; understanding of GNNs and multi-agent systems.**

*Delivery (Fall 2026): timeline blocks 0:00–1:30 are covered in the Tuesday session; blocks 1:30–3:00, including the laboratory briefing, in the Thursday session. The laboratory is completed at home (5 hours) before the following Tuesday.*

## Hour 1: Generative Design and the Materials Bottleneck (0:00 - 0:50)

**0:00 - 0:10 \| Review and Week 8 Objectives**

- Recap of Week 7: Autonomous code generation and data analysis.

- The grand challenge of engineering: The materials bottleneck.

- Introduction to the frontier of AI-driven scientific discovery.

**0:10 - 0:30 \| Topology Optimization vs. Generative Design**

- Topology Optimization: Finding the single optimal material distribution for a given constraint set.

- Generative Design: Using AI to explore a vast design space of multiple viable alternatives.

- Deep Generative Design: Integrating topology optimization with generative models (GANs, VAEs).

**0:30 - 0:50 \| The GNoME Breakthrough**

- The scale of the chemical space and the limitations of human intuition.

- DeepMind's Graph Networks for Materials Exploration (GNoME).

- How GNoME discovered 2.2 million new crystal structures, expanding the known stable materials by nearly 10x.

- Structural vs. compositional pipelines for materials discovery.

*10-Minute Break (0:50 - 1:00)*

## Hour 2: The Rise of Self-Driving Laboratories (1:00 - 1:50)

**1:00 - 1:20 \| What is a Self-Driving Laboratory (SDL)?**

- Definition: Systems combining AI and laboratory automation to perform research autonomously.

- The closed-loop architecture: Hypothesis generation \$\rightarrow\$ Experimental design \$\rightarrow\$ Robotic execution \$\rightarrow\$ Data analysis \$\rightarrow\$ Hypothesis updating.

- Historical context: From the Robot Scientist "Adam" (2009) to modern SDLs.

**1:20 - 1:50 \| Case Studies in Autonomous Experimentation**

- The A-Lab at Berkeley: Synthesizing GNoME's predicted materials autonomously (41 of 58 success rate in 17 days).

- The Acceleration Consortium (University of Toronto) and Argonne National Lab platforms.

- Cloud Labs: Democratizing access to experimental hardware via API.

*10-Minute Break (1:50 - 2:00)*

## Hour 3: Multi-Agent Workflows and Lab Briefing (2:00 - 2:50)

**2:00 - 2:30 \| Multi-Agent Orchestration in SDLs**

- How different AI agents collaborate in an SDL.

- The "Scientist" agent (proposing experiments based on literature/data).

- The "Simulator/Executor" agent (running physical or simulated experiments).

- The "Analyst" agent (evaluating results and feeding back to the Scientist).

**2:30 - 2:50 \| Lab 8 Briefing: Simulated Autonomous Laboratory**

- Overview of Lab 8 tasks:

  - Building a simulated SDL for high-performance concrete mix design.

  - Setting up the multi-agent system (Scientist, Simulator, Analyst).

  - Implementing the convergence loop to optimize compressive strength and workability.

- Q&A and transition to the Lab session.

*End of Lecture (2:50 - 3:00 Buffer)*

2:35 - 2:50 \| Reading the Claims Critically (Fall 2026 addition) — Cheetham & Seshadri (Ref_22) on GNoME novelty; Leeman et al. (Ref_23) on the A-Lab’s 41-of-58 claim; verification as the bridge to Week 9. Supplementary: MatterGen (Ref_27), Tom et al. SDL review (Ref_37).
