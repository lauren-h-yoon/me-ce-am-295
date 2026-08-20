---
title: "Syllabus Fall2026 v2 CD"
week: 0
doc_type: "syllabus"
access: "all_students"
agents: [syllabus_agent, all_student_agents]
source: "materials/ME_CE_295_Syllabus_Fall2026_v2_CD.docx"
source_hash: "679d6ce80dcc627e"
normalized_at: "2026-08-19T11:55:13Z"
---
**AM/ME/CE 295: AI Agents for Accelerating Scientific  
Discovery and Engineering Research**

Course Syllabus – Fall 2026

Mechanical and Civil Engineering Department, California Institute of Technology

**Course Instructor**

Chiara Daraio

Contact Information (GT 349, x8515, daraio@caltech.edu)

Office Hours: Open-door policy, by appointment, and via the course Slack channel

**Teaching Assistants**

TBD

Contact Information (TBD)

Office Hours: TBD. The course also provides a 24/7 AI teaching-assistant system on Slack (see Course Website below); human TAs remain the escalation path for anything the AI TAs cannot resolve.

**Course Description (as seen in the Caltech catalogue)**

9 units (3-5-1); first term. The course introduces the use of agentic artificial intelligence for scientific discovery and engineering research, for students in mechanical engineering and materials science. AI systems capable of reasoning, planning, and autonomous decision-making are transforming how researchers perform literature reviews, generate hypotheses, run simulations, and analyze results. The course covers the architecture of large language models and advanced prompt engineering; the construction of autonomous agent workflows with modern frameworks; retrieval-augmented generation for literature and standards; scientific machine learning (physics-informed neural networks and neural operators) as surrogate models for expensive simulations; LLM-driven code generation for simulation software; and generative design, materials discovery, and self-driving laboratories. The course culminates in the design of multi-agent systems that autonomously propose, execute, and evaluate engineering simulations. Every concept introduced in lecture is reinforced through a hands-on at-home laboratory. Prerequisites: graduate standing or senior standing in ME, MS, or a related field; proficiency in Python; prior coursework in numerical methods or computational mechanics. Instructor: Daraio.

**Course Welcome**

Welcome to AM/ME/CE 295. This course teaches you to build teams of AI agents that accelerate your own research — from automating literature reviews, to training physics-informed surrogate models, to orchestrating multi-agent systems that write, run, and debug simulations autonomously. The pedagogical philosophy is learning by building: lectures introduce each concept with analogies drawn from mechanics and materials science, and the weekly at-home laboratory immediately turns it into working code. By the end of the term each student will have a portfolio of functional AI agent systems and a capstone project that integrates an LLM with a domain-specific computational tool from their own research area.

**Learning Outcomes**

By the end of this course, students will be able to:

- Explain the architecture of LLMs, including tokenization, attention, and the role of memory, planning, and tool use in agentic systems

- Construct Retrieval-Augmented Generation (RAG) pipelines to automate literature reviews and extract structured data from technical documents and standards

- Implement Physics-Informed Neural Networks (PINNs) and Fourier Neural Operators (FNOs) as surrogate models that accelerate engineering simulations

- Develop AI agents capable of autonomous code generation to drive simulation software programmatically

- Design and orchestrate end-to-end multi-agent workflows to solve open-ended mechanical engineering and materials optimization problems

- Critically evaluate the reliability, reproducibility, safety, and ethical implications of deploying AI agents in autonomous research

**Required Text**

There is no required textbook. Required and supplementary readings (survey papers, landmark research articles, and framework documentation) are assigned per week; the full reading list is posted on the course website as a downloadable PDF "List of References." Five self-contained study guides (Python/LLM API fundamentals, RAG implementation, scientific machine learning, agent architecture patterns, and evaluation/production of multi-agent systems) are distributed via the course GitHub repository.

**Course Website and Learning Management System**

Online course resources (lecture notes, slides, lab notebooks, study guides, and the reading list) are hosted on the course website and GitHub repository; announcements and Q&A run on the course Slack workspace, which includes the AI teaching-assistant bot. Links and access instructions are distributed by email before the first lecture. Environment-setup materials are public so that students adding the course late (add deadline: October 16) can catch up in one evening.

**Assessment Rubric**

Bi-weekly Assignments (4): 40%

Final Project (capstone): 30%

Final Exam (3-hour practical, December 9–11 window): 30%

**Assignments.** Students complete four practical coding assignments, released and due as shown in the Lecture Schedule. All submissions are via the course GitHub Classroom. Grading criteria include correctness, code quality, documentation, and the accompanying brief report.

**Final Project.** Students work independently or in 2-person teams, and inform the TA of team composition together with a 1-page project proposal by October 30, 2026 (Week 5). Each student/team designs and executes an end-to-end AI agent workflow tailored to their research domain, integrating an LLM-based agent with at least one domain-specific computational tool. Deliverables: (1) a public GitHub repository with a reproducible environment; (2) a 4-page paper in IEEE conference format, due December 4, 2026; and (3) a 10-minute presentation followed by 5 minutes of questions during the final lecture slot on December 3, 2026. Grading: technical depth 30%, reproducibility 20%, results and analysis 25%, presentation and writing 15%, novelty and ambition 10%. For questions concerning the project, please contact the TA.

**Final Exam.** Three-hour, open-book, practical programming examination on personal laptops with internet access, scheduled in the December final-examination window. Students may consult any course materials, documentation, and AI tools. The exam tests the ability to diagnose, fix, and extend a partially completed AI agent system under time pressure.

**Honor Code**

No member of the Caltech community shall take unfair advantage of any other member of the Caltech community.

**Collaboration Policy**

**Turning in homework:** All assignments are submitted via the course GitHub Classroom by 11:59 p.m. Pacific on the due date.

**Late policy:** Each student has a budget of 3 late days for the quarter. A late day extends a deadline by 24 hours; no more than 2 late days may be applied to a single assignment. After the budget is exhausted, late submissions receive a 20% penalty per day. No deadlines fall during the Thanksgiving break (November 25–29). For special circumstances, please consult the instructor.

**AI use policy:** Students are encouraged to use AI tools (LLMs, coding assistants) as part of their workflow — this is the subject of the course. However, all submitted work must include an "AI Use Declaration" appendix that transparently documents which AI tools were used, for what purpose, and what modifications were made to AI-generated outputs. Undeclared use of AI to generate substantial portions of written reports is treated as an academic integrity violation under the Caltech Honor Code.

**Collaboration:** Homework assignments are individual unless otherwise stated; the capstone project may be completed individually or in pairs. Discussion of concepts and debugging strategies with classmates is encouraged; sharing of code is not permitted for individual assignments. You may not use class materials (notes, homework, exams) from previous years.

**Software and compute:** All laboratories can be completed on a standard laptop. For work requiring GPU access, students may use Caltech shared computing clusters or cloud notebooks. API costs for LLM providers are covered by a course-provided key with a per-student spending cap.

**Accessibility**

In the case of a documented disability, please contact Caltech Accessibility Services for Students (CASS) to coordinate any special accommodations.

**Lecture Schedule**

Lectures: Tuesdays and Thursdays, 1:00–2:30 p.m. Instruction begins September 28 and ends December 4, 2026. Each week releases a 5-hour at-home laboratory on Thursday, with checkpoint questions due before the following Tuesday; weekly quizzes are taken online at the end of each content week (Weeks 1–9).

| **Week** | **Date** | **Lecture Topic** | **Homework Due** |
|----|----|----|----|
| 1 | 9.29 | The AI revolution in science and engineering; from expert systems to foundation models; LLM basics |  |
| 1 | 10.1 | APIs and structured output; prompting fundamentals; what makes an "agent" | Lab 1 out |
| 2 | 10.6 | Transformer architecture: attention, tokenization, context windows, sampling | HW 1 out |
| 2 | 10.8 | Advanced prompting: chain-of-thought, self-consistency, structured outputs; prompting vs. reasoning models |  |
| 3 | 10.13 | Agent anatomy: memory, planning, tool use; the Model Context Protocol (MCP) |  |
| 3 | 10.15 | Multi-agent systems and frameworks; instruction hierarchy; Designer/Checker pattern | (Add deadline 10.16) |
| 4 | 10.20 | RAG I: document ingestion, parsing, chunking, embeddings, vector stores |  |
| 4 | 10.22 | RAG II: retrieval strategies, grounding, evaluation; RAG vs. long context | HW 1 due 10.23; HW 2 out |
| 5 | 10.27 | Scientific machine learning: limits of data-driven models; PINN formulation |  |
| 5 | 10.29 | PINN training in practice; failure modes; when PINNs beat classical solvers (and when not) | Capstone proposal due 10.30 |
| 6 | 11.3 | Neural operators: DeepONet, FNO, resolution invariance |  |
| 6 | 11.5 | GNN surrogates; choosing a solver: PINN vs. FNO vs. GNN vs. FEA | HW 2 due 11.6; HW 3 out |
| 7 | 11.10 | LLM-driven code generation; error taxonomy for generated simulation code |  |
| 7 | 11.12 | Execution-feedback loops; sandboxing; autonomous data analysis |  |
| 8 | 11.17 | Generative design and materials discovery; GNoME and the synthesizability debate |  |
| 8 | 11.19 | Self-driving laboratories; Bayesian-optimization intuition; Scientist/Simulator/Analyst pattern | HW 3 due 11.20; HW 4 out |
| 9 | 11.24 | Evaluation, reliability, and deployment: uncertainty quantification, calibration, hallucination mitigation, behavioral testing |  |
| 9 | 11.26 | Thanksgiving (Institute holiday) — no class |  |
| 10 | 12.1 | Ethics, professional practice, and the future of human–AI collaboration; course synthesis | HW 4 due 12.1 |
| 10 | 12.3 | Final project presentations and peer review | Capstone paper due 12.4 |
| — | 12.9–11 | Final examination (3-hour practical), scheduled by the Registrar |  |

**Weekly Program: Lectures and At-Home Laboratories**

Each week comprises two 1.5-hour lectures (Tuesday: concepts; Thursday: methods and lab briefing) and a 5-hour at-home computational laboratory with stated checkpoints. Labs are supported by skeleton code, pinned dependency versions, and the AI TA Lab Coach on Slack as the first line of support, with escalation to human TAs.

**Week 1 — The AI Revolution in Science and Engineering**

**Lectures.** Lectures trace the evolution from early expert systems and finite-element automation to foundation models and autonomous AI co-scientists (AI Co-Scientist, FutureHouse, the AI Scientist), and survey how agentic AI is transforming mechanical engineering and materials research. The Thursday session introduces LLM APIs, structured output parsing, and system vs. user prompts.

**Laboratory.** Lab 1: configure the computational environment (Python, API keys, course repository); first LLM API calls; extract structured material properties from a research abstract.

**Week 2 — Foundations of LLMs and Advanced Prompt Engineering**

**Lectures.** The Transformer architecture: self-attention, tokenization, context windows, and sampling parameters. Advanced prompting for scientific reasoning: chain-of-thought, self-consistency, tree-of-thoughts, few-shot learning with structured examples, and when explicit prompting still matters in the era of native reasoning models.

**Laboratory.** Lab 2: systematically benchmark prompt strategies against known analytical solutions; convert natural-language descriptions of a truss into a validated JSON representation.

**Week 3 — Agentic Frameworks and Multi-Agent Systems**

**Lectures.** What distinguishes an agent from an LLM call: memory, planning, and tool use, including the Model Context Protocol (MCP) as the standard interface between agents and engineering tools. Single- vs. multi-agent architectures, instruction hierarchy, and role-based agent teams.

**Laboratory.** Lab 3: build a ReAct agent with a custom cross-section-property tool; add session memory; extend to a two-agent Designer/Checker system that verifies designs against load requirements.

**Week 4 — Automating Literature Review with RAG**

**Lectures.** The complete RAG pipeline: document ingestion and parsing (equations and tables), chunking, embedding models, vector databases, retrieval strategies (similarity, MMR, hybrid), grounding and citation faithfulness, and evaluation. When to use RAG vs. long-context vs. agentic search.

**Laboratory.** Lab 4: build a RAG system over an engineering corpus (materials handbooks/standards and open-access papers); answer natural-language questions with inline citations; evaluate faithfulness on a provided question set. The 1-hour study block this week is a mandatory PyTorch primer preparing Week 5.

**Week 5 — Scientific Machine Learning and PINNs**

**Lectures.** Limits of purely data-driven models (extrapolation, conservation-law violations, data scarcity) and the PINN formulation: PDE residuals, boundary and initial conditions as soft constraints via automatic differentiation. Applications in heat conduction, elasticity, and fluids; training pathologies; where PINNs excel (inverse problems, data fusion) and where classical solvers remain superior.

**Laboratory.** Lab 5: implement PINNs in PyTorch (skeleton code provided): 1D steady-state heat equation in a composite rod; Euler–Bernoulli cantilever under distributed load, compared against analytical and FEM references.

**Week 6 — Neural Operators and Surrogate Modeling**

**Lectures.** From solving one PDE to learning families of PDEs: neural operators. DeepONet and the Fourier Neural Operator; resolution invariance and its limits; GNN-based surrogates for irregular geometries; how surrogates replace or augment FEA/CFD in design loops; surrogate failure modes. Pre-reading: the PINN vs. PINO comparison note.

**Laboratory.** Lab 6 (choose a track): train an FNO to predict the von Mises stress field in a plate with parametric hole geometry (structures) or vorticity fields for Navier–Stokes (fluids); benchmark inference speed against a traditional solver.

**Week 7 — LLM-Driven Code Generation and Autonomous Data Analysis**

**Lectures.** How agents write, execute, and debug simulation code: prompt-to-input-file generation for domain software, the taxonomy of errors (syntax, runtime, and physically implausible results as silent failures), execution-feedback loops, sandboxing, and autonomous data-analysis pipelines.

**Laboratory.** Lab 7 (choose a track): an agent that generates and self-debugs a structural analysis script from a natural-language specification (structures), or an agent that automates a tensile-test data pipeline — extracting modulus, yield, and UTS from raw data files — and produces plots and a report (materials).

**Week 8 — Generative Design, Materials Discovery, and Autonomous Laboratories**

**Lectures.** Generative design vs. topology optimization; deep learning for materials discovery (GNoME) and the synthesizability debate; self-driving laboratories: closed-loop platforms where agents propose experiments, robots execute them, and results feed back into planning; Bayesian optimization as the decision engine.

**Laboratory.** Lab 8: build a simulated self-driving laboratory as a multi-agent system — a Scientist agent proposes candidate compositions (alloy, electrolyte, or composite layup; concrete mix available as an alternative track), a Simulator agent evaluates them with a provided predictive model, and an Analyst agent scores results and closes the loop; analyze convergence.

**Week 9 — Evaluation, Reliability, and Deployment (single lecture; Thanksgiving week)**

**Lectures.** Hallucination in safety-critical engineering contexts; calibration and uncertainty quantification; behavioral and statistical testing of stochastic agent systems; the prototype-to-production gap and a production-readiness checklist.

**Laboratory.** Lab 9: run a 20+-repetition behavioral test suite and failure-mode classification on your own capstone agent system — a structured reliability audit one week before presentations.

**Week 10 — Ethics, Professional Practice, and the Future**

**Lectures.** Reproducibility and AI; intellectual property and authorship when AI systems contribute to research; the evolving regulatory landscape; research integrity, export control, and physical safety of autonomous laboratories; the future of human–AI collaboration. Thursday: final project presentations and structured peer code review.

**Laboratory.** Lab 10: capstone polish and a reproducibility pass on the project repository (can it be cloned and run by a peer with minimal setup?).

**Bi-weekly Assignments**

| **\#** | **Topic** | **Out** | **Due** |
|----|----|----|----|
| 1 | Prompt engineering and structured data extraction: a system prompt + Python pipeline that extracts material properties (Young’s modulus, Poisson’s ratio, yield strength, UTS, density) from 20 unstructured abstracts into a validated JSON schema; report precision/recall against ground truth | Oct 6 | Oct 23 |
| 2 | RAG system for engineering document compliance: a retrieval-augmented chatbot answering 30 compliance questions from an engineering standard/handbook corpus, returning section and page of the source; report Hit@5 and faithfulness | Oct 22 | Nov 6 |
| 3 | Physics-informed surrogate: train a PINN for steady-state temperature in a 2D two-material composite plate with an internal heat source; 2-page IEEE-format report comparing accuracy (relative L2 error) and inference time against an FEM reference | Nov 5 | Nov 20 |
| 4 | Multi-agent simulation system: a dual-agent Script-Writer/Debugger-Reviewer system that generates and autonomously corrects a structural analysis script until it runs (≤5 iterations); submit conversation log, final script, and orchestration code | Nov 19 | Dec 1 |

*This syllabus is based on the preliminary Caltech 2026–27 academic calendar; dates will be re-verified against the final registrar calendar.*
