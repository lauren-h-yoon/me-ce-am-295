---
title: "Week5 SciML PINNs"
week: 5
doc_type: "lecture_notes"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 5/Week5_SciML_PINNs.docx"
source_hash: "7ad766f9a62ac0af"
normalized_at: "2026-08-19T11:55:20Z"
---
# ME/CE 295 --- Week 5 Lecture Notes

# Scientific Machine Learning and Physics-Informed Neural Networks

**California Institute of Technology --- Division of Engineering and Applied Science Course: ME/CE 295 --- AI Agents for Accelerating Scientific Discovery and Engineering Research Week: 5 of 10 Lectures: Tuesday & Thursday, 1:00–2:30 p.m. (2 × 1.5 hours) \| Laboratory: 5 hours, at-home (see separate lab handout)**

## Lecture Outline at a Glance

The following table summarizes the lecture structure, delivered as two 90-minute sessions: 0:00–1:30 on Tuesday and 1:30–3:00 (including the lab briefing) on Thursday. This session transitions the course from text-based agentic workflows to continuous physical modeling, introducing the core concepts of Scientific Machine Learning (SciML).

| **Time** | **Duration** | **Topic** | **Key Takeaway** |
|----|----|----|----|
| 0:00--0:10 | 10 min | Review and Week 5 Objectives | Transitioning from text to physical equations |
| 0:10--0:25 | 15 min | Limitations of Purely Data-Driven Models | Why standard NNs fail in engineering physics |
| 0:25--0:50 | 25 min | The PINN Paradigm | NNs as mesh-free universal function approximators |
| 0:50--1:00 | 10 min | *Break* |  |
| 1:00--1:25 | 25 min | The Composite Loss Function | Encoding PDEs, BCs, and ICs as soft constraints |
| 1:25--1:50 | 25 min | Automatic Differentiation in PyTorch | Computing exact spatial and temporal derivatives |
| 1:50--2:00 | 10 min | *Break* |  |
| 2:00--2:20 | 20 min | Spectral Bias and Training Instabilities | Overcoming the neural network frequency principle |
| 2:20--2:35 | 15 min | Engineering Applications | Solid mechanics, fluid dynamics, and inverse problems |
| 2:35--2:50 | 15 min | Lab 5 Briefing | Solving the 1D heat and beam equations from scratch |
| 2:50--3:00 | 10 min | Q&A and Transition to Lab |  |

## Part I --- The Limits of Data and the Promise of Physics

For the past four weeks, we have explored how Large Language Models (LLMs) can process text, write code, and synthesize engineering literature. However, mechanical and civil engineering fundamentally deal with the continuous physical world—stress fields in a steel beam, heat conduction in a composite material, or fluid flow around a bridge pier. To apply AI to these domains, we must transition to Scientific Machine Learning (SciML).

### 1. Limitations of Purely Data-Driven Models

Traditional deep learning models, such as Convolutional Neural Networks (CNNs) or standard Multi-Layer Perceptrons (MLPs), have achieved remarkable success in computer vision and natural language processing. However, when applied to computational mechanics, they exhibit severe limitations [<u>1</u>](https://www.mdpi.com/2673-2688/5/3/74).

First, purely data-driven models are "black boxes" that do not inherently understand physical laws. If trained to predict the temperature distribution in a rod based solely on sensor data, a standard NN might predict a temperature profile that violates the conservation of energy. Second, these models suffer from catastrophic extrapolation failures. While they interpolate well within the bounds of their training data, they cannot reliably predict outcomes for boundary conditions or material properties they have never seen. Finally, engineering faces a severe data scarcity problem. Unlike the internet, which provides trillions of text tokens for LLMs, generating high-fidelity physical data requires expensive physical experiments or computationally exhaustive Finite Element Analysis (FEA) simulations taking days to run on supercomputers [<u>1</u>](https://www.mdpi.com/2673-2688/5/3/74).

### 2. The PINN Paradigm

To overcome these limitations, Raissi, Perdikaris, and Karniadakis introduced Physics-Informed Neural Networks (PINNs) in 2019 [<u>2</u>](https://www.sciencedirect.com/science/article/abs/pii/S0021999118307125). The core innovation of PINNs is that they do not rely solely on labeled data; instead, they integrate the governing Partial Differential Equations (PDEs) directly into the neural network's training process.

In a PINN, the neural network acts as a universal function approximator for the solution of the PDE. For example, to solve a spatio-temporal problem, the network takes spatial coordinates (\$x, y, z\$) and time (\$t\$) as inputs, and outputs the physical quantities of interest, such as temperature (\$T\$) or displacement (\$u, v, w\$). Because the neural network is a continuous, differentiable mathematical function, it can be evaluated at any point in the domain without the need for a discrete finite element mesh. This makes PINNs a fundamentally mesh-free approach to computational mechanics [<u>2</u>](https://www.sciencedirect.com/science/article/abs/pii/S0021999118307125).

## Part II --- Mathematical Formulation and Automatic Differentiation

The magic of PINNs lies in how the physics are enforced during the training loop. Rather than hard-coding the equations into the architecture, PINNs enforce physics through the loss function.

### 3. The Composite Loss Function

In a standard neural network, the loss function simply measures the Mean Squared Error (MSE) between the network's predictions and the ground-truth data. In a PINN, the loss function is a composite of multiple terms, each representing a different physical constraint [<u>1</u>](https://www.mdpi.com/2673-2688/5/3/74):

\$L\_{total} = \lambda\_{data} L\_{data} + \lambda\_{pde} L\_{pde} + \lambda\_{bc} L\_{bc} + \lambda\_{ic} L\_{ic}\$

- **\$L\_{data}\$**: The error against any available empirical sensor data (if solving a purely forward problem, this term may be zero).

- **\$L\_{pde}\$**: The residual of the governing partial differential equation evaluated at random "collocation points" sampled throughout the domain.

- **\$L\_{bc}\$**: The error at the spatial boundaries of the domain (Boundary Conditions).

- **\$L\_{ic}\$**: The error at \$t=0\$ (Initial Conditions).

The weighting coefficients (\$\lambda\$) balance the importance of each term. Because the physics are enforced as penalties in the loss function rather than strict mathematical guarantees, PINNs are said to use "soft constraints" [<u>1</u>](https://www.mdpi.com/2673-2688/5/3/74).

### 4. Automatic Differentiation (AD)

To compute the PDE residual (\$L\_{pde}\$), the network must calculate the derivatives of its output with respect to its inputs. For example, the 1D transient heat equation is governed by:

\$\frac{\partial u}{\partial t} - \alpha \frac{\partial^2 u}{\partial x^2} = 0\$

Where \$u\$ is temperature and \$\alpha\$ is thermal diffusivity. To evaluate this, the PINN must compute the first derivative with respect to time (\$\frac{\partial u}{\partial t}\$) and the second spatial derivative (\$\frac{\partial^2 u}{\partial x^2}\$).

Traditional numerical solvers use finite differences, which introduce truncation errors and require a grid. PINNs, however, use Automatic Differentiation (AD)—the same algorithmic engine that powers backpropagation in PyTorch and TensorFlow [<u>2</u>](https://www.sciencedirect.com/science/article/abs/pii/S0021999118307125). AD applies the chain rule of calculus exactly through the computational graph of the neural network, yielding exact derivatives up to machine precision. In PyTorch, this is achieved using the torch.autograd.grad() function, allowing the network to evaluate the PDE residual \$r = \frac{\partial u}{\partial t} - \alpha \frac{\partial^2 u}{\partial x^2}\$ at thousands of randomly sampled collocation points.

## Part III --- Training Challenges and Engineering Applications

While the formulation of PINNs is elegant, training them in practice presents significant optimization challenges that engineers must navigate.

### 5. Spectral Bias and Training Instabilities

Neural networks suffer from a phenomenon known as the "F-Principle" or Spectral Bias: they inherently learn low-frequency functions much faster than high-frequency functions [<u>3</u>](https://www.sciencedirect.com/science/article/pii/S0360835225008502). If an engineering problem involves sharp gradients, shock waves, or multi-scale phenomena (e.g., turbulence in fluid dynamics or stress concentrations around a crack tip), a standard PINN will struggle to resolve the high-frequency details, resulting in an overly smoothed, inaccurate solution [<u>3</u>](https://www.sciencedirect.com/science/article/pii/S0360835225008502).

To mitigate spectral bias, researchers employ several techniques. Fourier feature embeddings map the input coordinates into a higher-dimensional periodic space before passing them to the network, forcing the network to "see" higher frequencies. Additionally, adaptive activation functions and multi-scale network architectures are used to capture localized phenomena.

Another major challenge is loss imbalance. During training, the gradients from the boundary condition loss (\$L\_{bc}\$) might be orders of magnitude larger than the gradients from the PDE residual (\$L\_{pde}\$), causing the network to perfectly satisfy the boundaries while ignoring the physics in the interior domain. Advanced training strategies utilize adaptive learning rate annealing to dynamically balance the \$\lambda\$ weights during training, and often employ a two-phase optimization strategy: starting with the Adam optimizer for robust global search, followed by the L-BFGS optimizer (a second-order method) to achieve precise local convergence [<u>1</u>](https://www.mdpi.com/2673-2688/5/3/74).

### 6. Engineering Applications

PINNs have rapidly become a pillar of modern computational engineering. Their applications span multiple domains:

- **Solid Mechanics:** Solving the Euler-Bernoulli beam equation or full 3D linear elasticity equations to predict stress and strain fields in complex geometries without meshing.

- **Fluid Dynamics:** Solving the Navier-Stokes equations to model incompressible fluid flow. PINNs can even infer continuous pressure fields from discrete velocity measurements.

- **Inverse Problems:** This is perhaps the most powerful application of PINNs. If an engineer has sparse displacement data from a vibrating bridge, a PINN can ingest that data (\$L\_{data}\$) and use the physics equations (\$L\_{pde}\$) to work backward and infer the unknown material properties (e.g., Young's modulus) or identify the location of structural damage [<u>2</u>](https://www.sciencedirect.com/science/article/abs/pii/S0021999118307125).

By bridging the gap between deep learning and classical physics, PINNs offer a powerful new tool for engineers to simulate, optimize, and monitor physical systems.

## Assigned Reading for Week 5

| **Priority** | **Reference** | **Description** |
|----|----|----|
| **Required** | Raissi, M., Perdikaris, P., and Karniadakis, G. E. (2019). "Physics-informed neural networks..." *Journal of Computational Physics*. | The foundational paper introducing the PINN framework and AD for PDE residuals. |
| **Required** | Karniadakis, G. E. et al. (2021). "Physics-informed machine learning." *Nature Reviews Physics*. | A comprehensive review of the SciML landscape and PINN applications. |
| **Supplementary** | Farea, A. et al. (2024). "Understanding Physics-Informed Neural Networks..." *MDPI AI*. | Detailed breakdown of loss formulations, training challenges, and future trends. |

## Connecting PINNs to Multi-Agent System Design: Operating Contracts

A powerful conceptual parallel exists between Physics-Informed Neural Networks and the design of reliable multi-agent AI systems.

**The shared principle:** Both PINNs and production multi-agent systems achieve reliability by *imposing structural constraints on otherwise unconstrained systems.*

| **Domain** | **Unconstrained System** | **Constraint Mechanism** | **Result** |
|----|----|----|----|
| Scientific ML | Neural network (universal approximator) | Physics loss terms (PDEs, boundary conditions) | Physically plausible predictions |
| Multi-Agent AI | LLM agents (non-deterministic) | Operating contracts (acceptance criteria, stop conditions) | Predictable system behavior |

**Key insight from production multi-agent systems (Cognizant AI Lab, 2026):**

Just as a PINN without physics constraints can produce any smooth function (including physically impossible ones), a multi-agent system without operating contracts can produce plausible-looking outputs while quietly failing to follow intended processes or missing important constraints.

**Operating contracts** for agents mirror boundary conditions for PINNs:

- **Acceptance criteria** → What does "done" look like? (analogous to target solution values)

- **Stop conditions** → When should the agent halt? (analogous to convergence criteria)

- **Constraint enforcement** → Runtime validation that agents stay within bounds (analogous to physics loss terms)

This parallel will be revisited in Week 9 when we discuss behavioral reliability testing for multi-agent systems.

**New Reference:**

- Cognizant AI Lab (2026). "Why Your Multi-Agent Network Works in Demo but Falls Apart in the Wild." *Decision AI Bytes.*

## References
