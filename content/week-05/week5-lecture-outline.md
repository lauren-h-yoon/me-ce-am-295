---
title: "Week5 Lecture Outline"
week: 5
doc_type: "lecture_outline"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 5/Week5_Lecture_Outline.docx"
source_hash: "0974b33ab3ec5230"
normalized_at: "2026-08-19T11:55:19Z"
---
# Week 5 Lecture Outline: Scientific Machine Learning and Physics-Informed Neural Networks

**Format: Tuesday & Thursday lectures, 1:00–2:30 p.m. (2 × 90 minutes) + 5-hour at-home laboratory. Target Audience: Mechanical Engineering and Materials Science graduate students and senior undergraduates Prerequisites: Completion of Week 4; familiarity with PyTorch basics, differential equations, and calculus.**

*Delivery (Fall 2026): timeline blocks 0:00–1:30 are covered in the Tuesday session; blocks 1:30–3:00, including the laboratory briefing, in the Thursday session. The laboratory is completed at home (5 hours) before the following Tuesday.*

## Hour 1: The Limits of Data and the Promise of Physics (0:00 - 0:50)

**0:00 - 0:10 \| Review and Week 5 Objectives**

- Recap of Week 4: RAG and extracting information from external documents.

- The shift from discrete text processing to continuous physical modeling.

- Introduction to Scientific Machine Learning (SciML).

**0:10 - 0:25 \| Limitations of Purely Data-Driven Models in Engineering**

- The "black box" problem: Lack of interpretability and violation of conservation laws (mass, momentum, energy).

- The extrapolation failure: Why standard neural networks fail catastrophically outside their training distribution.

- The data scarcity problem in engineering: Experimental data is expensive, and high-fidelity simulations take days.

**0:25 - 0:50 \| The PINN Paradigm**

- Introduction to Physics-Informed Neural Networks (PINNs) (Raissi et al., 2019).

- The core concept: Using neural networks as universal function approximators for PDE solutions.

- Mesh-free modeling: Bypassing the traditional finite element mesh generation process.

*10-Minute Break (0:50 - 1:00)*

## Hour 2: Mathematical Formulation and Automatic Differentiation (1:00 - 1:50)

**1:00 - 1:25 \| The Composite Loss Function**

- Formulating the soft constraints: \$L = \lambda\_{data} L\_{data} + \lambda\_{pde} L\_{pde} + \lambda\_{bc} L\_{bc} + \lambda\_{ic} L\_{ic}\$.

- Understanding collocation points: Sampling the spatio-temporal domain without a mesh.

- Forward problems (solving PDEs) vs. Inverse problems (discovering material properties from data).

**1:25 - 1:50 \| Automatic Differentiation (AD) in PyTorch**

- How AD computes exact derivatives (not finite differences) through the computational graph.

- Step-by-step AD for the 1D Heat Equation: Computing \$\frac{\partial u}{\partial t}\$ and \$\frac{\partial^2 u}{\partial x^2}\$.

- Encoding the PDE residual into the loss function.

*10-Minute Break (1:50 - 2:00)*

## Hour 3: Training Challenges, Advanced Techniques, and Lab Briefing (2:00 - 2:50)

**2:00 - 2:20 \| Spectral Bias and Training Instabilities**

- The F-Principle (Frequency Principle): Why neural networks learn low frequencies first and struggle with sharp gradients.

- Loss imbalance: When the boundary condition loss dominates the PDE residual loss.

- Mitigation strategies: Adaptive loss weighting, Fourier feature embeddings, and two-phase training (Adam + L-BFGS).

**2:20 - 2:35 \| Engineering Applications of PINNs**

- Solid mechanics: Predicting stress/strain fields in linear elasticity.

- Fluid dynamics: Solving the Navier-Stokes and Burgers' equations.

- Structural health monitoring: Identifying damage from vibration data via inverse PINNs.

**2:35 - 2:50 \| Lab 5 Briefing: Implementing PINNs from Scratch**

- Overview of Lab 5 tasks:

  - Part A: Solving the 1D steady-state heat equation in a composite rod.

  - Part B: Solving the Euler-Bernoulli beam equation for a cantilever beam under distributed load.

- Q&A and transition to the Lab session.

*End of Lecture (2:50 - 3:00 Buffer)*
