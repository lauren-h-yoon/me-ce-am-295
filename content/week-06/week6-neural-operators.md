---
title: "Week6 Neural Operators"
week: 6
doc_type: "lecture_notes"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 6/Week6_Neural_Operators.docx"
source_hash: "2ef9f9f421ec8633"
normalized_at: "2026-08-19T11:55:20Z"
---
# ME/CE 295 --- Week 6 Lecture Notes

# AI-Driven Simulation Acceleration and Surrogate Modeling

**California Institute of Technology --- Division of Engineering and Applied Science Course: ME/CE 295 --- AI Agents for Accelerating Scientific Discovery and Engineering Research Week: 6 of 10 Lectures: Tuesday & Thursday, 1:00–2:30 p.m. (2 × 1.5 hours) \| Laboratory: 5 hours, at-home (see separate lab handout)**

## Lecture Outline at a Glance

The following table summarizes the lecture structure, delivered as two 90-minute sessions: 0:00–1:30 on Tuesday and 1:30–3:00 (including the lab briefing) on Thursday. This session moves beyond solving single physical instances to learning families of solutions, enabling real-time engineering design optimization.

| **Time** | **Duration** | **Topic** | **Key Takeaway** |
|----|----|----|----|
| 0:00--0:10 | 10 min | Review and Week 6 Objectives | Moving from single PDE instances to families of PDEs |
| 0:10--0:30 | 20 min | Introduction to Surrogate Modeling | Bypassing the FEA bottleneck in design loops |
| 0:30--0:50 | 20 min | The DeepONet Architecture | Branch-Trunk networks for operator learning |
| 0:50--1:00 | 10 min | *Break* |  |
| 1:00--1:25 | 25 min | The Fourier Neural Operator (FNO) | Global convolutions in the spectral domain |
| 1:25--1:50 | 25 min | Resolution Invariance | Zero-shot super-resolution for fluid dynamics |
| 1:50--2:00 | 10 min | *Break* |  |
| 2:00--2:30 | 30 min | Graph Neural Networks (GNNs) | Modeling irregular meshes and truss structures |
| 2:30--2:50 | 20 min | Lab 6 Briefing | Training FNOs for structural and fluid mechanics |
| 2:50--3:00 | 10 min | Q&A and Transition to Lab |  |

## Part I --- From PINNs to Operator Learning

In Week 5, we explored Physics-Informed Neural Networks (PINNs) as a mesh-free method for solving Partial Differential Equations (PDEs). While PINNs are mathematically elegant, they suffer from a severe practical limitation: a standard PINN is trained to solve exactly *one* instance of a PDE. If an engineer changes the boundary conditions, alters the initial state, or modifies the geometry of the domain, the PINN must be completely retrained from scratch.

### 1. The Need for Surrogate Modeling

In real-world engineering workflows, such as aerodynamic shape optimization for an airfoil or topology optimization for a bridge truss, the design loop requires evaluating thousands of slightly different configurations. Running a high-fidelity Computational Fluid Dynamics (CFD) or Finite Element Analysis (FEA) solver for every iteration can take weeks on a supercomputer.

To accelerate this process, engineers use **Surrogate Models**—data-driven algorithms trained on a dataset of offline, high-fidelity simulation results. Once trained, the surrogate model replaces the traditional solver inside the optimization loop. While a CFD simulation might take hours to converge, a neural surrogate model can predict the resulting flow field in milliseconds, enabling real-time design exploration and active learning workflows [<u>1</u>](https://arxiv.org/abs/2502.09692).

### 2. The DeepONet Architecture

To build these surrogates, we must shift our perspective from learning a function (mapping a coordinate \$x\$ to a value \$u\$) to learning an **Operator** (mapping an input *function* to an output *function*). For example, mapping any arbitrary initial temperature distribution to the temperature distribution at time \$t\$.

In 2021, Lu et al. introduced the Deep Operator Network (**DeepONet**), grounded in the Universal Approximation Theorem for Operators [<u>2</u>](https://www.nature.com/articles/s42256-021-00302-5). DeepONet achieves this mapping through a unique dual-network architecture:

- **The Branch Net:** This sub-network ingests the input function (such as the initial condition or boundary shape), which is discretized at a fixed set of sensor locations. It outputs a set of latent coefficients.

- **The Trunk Net:** This sub-network ingests the continuous query coordinates (e.g., spatial location \$x, y\$ and time \$t\$) where the solution is desired. It outputs a set of continuous basis functions.

The final prediction of the DeepONet is computed as the dot product between the outputs of the branch and trunk networks. This architecture allows DeepONet to handle highly irregular geometries and non-uniform grids, making it a highly flexible surrogate model for complex engineering tasks [<u>2</u>](https://www.nature.com/articles/s42256-021-00302-5).

## Part II --- The Fourier Neural Operator (FNO)

While DeepONet is highly flexible, modeling complex, high-frequency phenomena like turbulent fluid flow requires an architecture specifically designed to handle continuous spatial fields efficiently.

### 3. Architecture of the FNO

Standard Convolutional Neural Networks (CNNs) are the workhorses of computer vision. However, CNN filters are strictly local—they excel at finding sharp edges in discrete pixel grids. PDE solutions, conversely, are continuous, global functions. A local CNN kernel struggles to capture the long-range physical dependencies inherent in fluid dynamics or structural mechanics.

To solve this, Li et al. (2020) introduced the **Fourier Neural Operator (FNO)** [<u>3</u>](https://arxiv.org/abs/2010.08895). The FNO bypasses local spatial convolutions by performing convolutions in the frequency domain. The architecture consists of three main stages:

1.  **Lifting Layer:** A local linear transformation maps the input function to a higher-dimensional channel space.

2.  **Fourier Layers:** The core of the FNO. In each Fourier layer:

    - The data is transformed into the spectral domain using the Fast Fourier Transform (FFT).

    - A learnable linear transformation is applied to the lower-frequency Fourier modes. Crucially, the higher-frequency modes are truncated to zero, acting as a low-pass filter that regularizes the learning process.

    - The data is transformed back to the spatial domain using the Inverse FFT.

    - A local spatial bias is added, and a non-linear activation function (like GeLU) is applied. The spatial activation is vital, as it helps recover the high-frequency details and non-periodic boundary behaviors that were truncated in the spectral domain [<u>4</u>](https://zongyi-li.github.io/blog/2020/fourier-pde/).

3.  **Projection Layer:** A final linear transformation projects the high-dimensional data back to the desired output physical quantities (e.g., pressure, velocity, or stress).

### 4. Resolution Invariance and Super-Resolution

The most profound advantage of the FNO is **resolution invariance**. Because the learnable parameters (the weights applied to the Fourier modes) are defined in the continuous spectral domain rather than on a discrete spatial grid, the trained model is entirely independent of the mesh resolution [<u>3</u>](https://arxiv.org/abs/2010.08895).

This enables **zero-shot super-resolution**. An engineer can train an FNO on low-resolution CFD data (e.g., a \$64 \times 64\$ grid) to save computational costs during training. Once deployed, that exact same FNO can be evaluated on a dense \$256 \times 256\$ grid, yielding high-fidelity predictions without any retraining [<u>3</u>](https://arxiv.org/abs/2010.08895). In benchmarking studies, FNOs have demonstrated the ability to solve the Navier-Stokes equations up to 1,000 times faster than traditional numerical solvers while maintaining state-of-the-art accuracy [<u>4</u>](https://zongyi-li.github.io/blog/2020/fourier-pde/).

## Part III --- Graph Neural Networks for Structural Systems

While FNOs are unparalleled for continuous fields on regular grids (like fluid flow in a rectangular domain), many engineering problems involve highly irregular geometries, discrete components, or particle-based systems.

### 5. Graph Neural Network (GNN) Surrogates

For problems like predicting the stress distribution in a complex 3D space frame or optimizing the topology of a truss bridge, **Graph Neural Networks (GNNs)** are the optimal surrogate architecture [<u>5</u>](https://www.sciencedirect.com/science/article/pii/S2352012423018003).

In a GNN, the physical system is represented as a mathematical graph:

- **Nodes** represent the joints, finite elements, or fluid particles.

- **Edges** represent the physical connectivity, structural members, or spatial proximity between nodes.

GNNs operate on a "message-passing" paradigm. During each layer of the network, every node aggregates physical state information (such as forces, displacements, or material properties) from its connected neighbors. This allows the network to learn how local forces propagate through the global structure. Recent applications in structural engineering have demonstrated that GNNs can serve as highly accurate surrogate models for multi-objective design optimization, allowing optimization algorithms to explore thousands of structural configurations in seconds [<u>5</u>](https://www.sciencedirect.com/science/article/pii/S2352012423018003).

## Assigned Reading for Week 6

| **Priority** | **Reference** | **Description** |
|----|----|----|
| **Required** | Li, Z. et al. (2020). "Fourier Neural Operator for Parametric Partial Differential Equations." *ICLR*. | The foundational paper introducing the FNO architecture and zero-shot super-resolution. |
| **Required** | Lu, L. et al. (2021). "Learning nonlinear operators via DeepONet..." *Nature Machine Intelligence*. | Comprehensive introduction to the Branch-Trunk architecture for operator learning. |
| **Supplementary** | Li, Z. (2020). "Fourier Neural Operator." *Zongyi Li Blog*. | A practical, intuitive breakdown of the Fourier layer mechanics. |
| **Supplementary** | Nourian, N. et al. (2023). "Design optimization of truss structures using a GNN-based surrogate model." *Algorithms*. | Application of GNNs to structural engineering design loops. |

## References
