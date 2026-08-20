---
title: "Week6 Lecture Outline"
week: 6
doc_type: "lecture_outline"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 6/Week6_Lecture_Outline.docx"
source_hash: "849226ad353dd633"
normalized_at: "2026-08-19T11:55:20Z"
---
# Week 6 Lecture Outline: AI-Driven Simulation Acceleration and Surrogate Modeling

**Format: Tuesday & Thursday lectures, 1:00–2:30 p.m. (2 × 90 minutes) + 5-hour at-home laboratory. Target Audience: Mechanical Engineering and Materials Science graduate students and senior undergraduates Prerequisites: Completion of Week 5; understanding of PINNs, PDE residuals, and basic spectral analysis.**

*Delivery (Fall 2026): timeline blocks 0:00–1:30 are covered in the Tuesday session; blocks 1:30–3:00, including the laboratory briefing, in the Thursday session. The laboratory is completed at home (5 hours) before the following Tuesday.*

## Hour 1: From PINNs to Operator Learning (0:00 - 0:50)

**0:00 - 0:10 \| Review and Week 6 Objectives**

- Recap of Week 5: PINNs as mesh-free solvers for single PDE instances.

- The limitation of PINNs: Changing a boundary condition or geometry requires retraining the entire network.

- The goal for Week 6: Learning families of PDEs to replace traditional solvers in design loops.

**0:10 - 0:30 \| Introduction to Surrogate Modeling**

- What is a surrogate model? A data-driven approximation of a computationally expensive high-fidelity simulation (FEA/CFD).

- The traditional design optimization bottleneck: Hours per iteration.

- The surrogate paradigm: Training on offline data to enable millisecond-level inference for real-time design exploration.

**0:30 - 0:50 \| The DeepONet Architecture**

- Learning mappings between function spaces rather than finite-dimensional vectors.

- The Universal Approximation Theorem for Operators (Chen & Chen, 1995; Lu et al., 2021).

- The Branch-Trunk architecture:

  - Branch net: Processes the input function (e.g., initial condition) sampled at fixed sensors.

  - Trunk net: Processes the continuous query coordinates \$(x, y, t)\$.

  - The dot product output mechanism.

*10-Minute Break (0:50 - 1:00)*

## Hour 2: The Fourier Neural Operator (FNO) (1:00 - 1:50)

**1:00 - 1:25 \| The Architecture of FNO**

- Why CNNs fail for PDEs: Local filters vs. the global nature of continuous physical fields.

- The FNO pipeline: Lifting layer \$\rightarrow\$ Fourier Layers \$\rightarrow\$ Projection layer.

- Deep dive into the Fourier Layer:

  1.  Fast Fourier Transform (FFT) to the spectral domain.

  2.  Learnable linear transformation on the truncated lower frequency modes.

  3.  Inverse FFT back to the spatial domain.

  4.  Addition of spatial bias and non-linear activation (GeLU).

**1:25 - 1:50 \| Resolution Invariance and Zero-Shot Super-Resolution**

- The breakthrough of FNO (Li et al., 2020): Parameters are learned in the continuous Fourier space.

- Training on a coarse grid (\$64 \times 64\$) and evaluating on a fine grid (\$256 \times 256\$) without retraining.

- Achieving 1000x speedups over traditional Navier-Stokes solvers.

*10-Minute Break (1:50 - 2:00)*

## Hour 3: Graph Neural Networks and Lab Briefing (2:00 - 2:50)

**2:00 - 2:30 \| Graph Neural Networks (GNNs) in Structural Engineering**

- When regular grids fail: Complex truss structures, irregular meshes, and particle-based simulations.

- Representing structures as graphs: Nodes (joints/elements) and Edges (connectivity).

- The message-passing paradigm: Aggregating physical state information from neighboring nodes.

- Case studies: Multi-objective topology optimization and rapid stress prediction.

**2:30 - 2:50 \| Lab 6 Briefing: Training an FNO**

- Overview of Lab 6 tasks (Track-based):

  - Structural Track: Train an FNO to predict von Mises stress fields in plates with parametric hole geometries under tension.

  - Fluid Track: Train an FNO to predict vorticity fields for the 2D Navier-Stokes equations.

<!-- -->

- Benchmarking inference speed against the provided traditional solver.

- Q&A and transition to the Lab session.

*End of Lecture (2:50 - 3:00 Buffer)*
