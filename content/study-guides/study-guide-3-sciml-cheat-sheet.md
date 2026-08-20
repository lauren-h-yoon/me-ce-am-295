---
title: "Study Guide 3 SciML Cheat Sheet"
week: 0
doc_type: "study_guide"
access: "all_students"
agents: [all_student_agents]
source: "materials/Study Guides/Study_Guide_3_SciML_Cheat_Sheet.docx"
source_hash: "ae89a69f513cdef9"
normalized_at: "2026-08-19T11:55:16Z"
---
# Study Guide 3: Scientific Machine Learning (SciML) Cheat Sheet

**Course:** ME/CE 295 — AI Agents for Accelerating Scientific Discovery and Engineering Research  
**Author:** Manus AI

This cheat sheet provides a quick reference for implementing Physics-Informed Neural Networks (PINNs) and Neural Operators using PyTorch. These techniques allow us to bridge the gap between purely data-driven deep learning and physics-based computational mechanics.

## 1. Physics-Informed Neural Networks (PINNs)

A PINN is a standard feedforward neural network, but its loss function is heavily modified. Instead of just minimizing the error against training data, it also minimizes the residual of the governing Partial Differential Equation (PDE), as well as boundary and initial conditions.

### 1.1 The Mathematical Formulation

For a general PDE defined as \$\mathcal{N}\[u\](x, t) = 0\$, the total loss is:

\$\$ \mathcal{L}*{total} = w*{data}\mathcal{L}*{data} + w*{PDE}\mathcal{L}*{PDE} + w*{BC}\mathcal{L}*{BC} + w*{IC}\mathcal{L}\_{IC} \$\$

Where:

- \$\mathcal{L}\_{data}\$: Mean Squared Error (MSE) between predictions and known sensor/simulation data.

- \$\mathcal{L}\_{PDE}\$: MSE of the PDE residual (should be 0 everywhere in the domain).

- \$\mathcal{L}\_{BC}\$: MSE at the spatial boundaries.

- \$\mathcal{L}\_{IC}\$: MSE at \$t=0\$ (for transient problems).

- \$w_i\$: Loss weighting coefficients (often tuned dynamically during training).

### 1.2 Automatic Differentiation in PyTorch

The core mechanism of a PINN is using PyTorch's autograd to compute exact spatial and temporal derivatives of the network's output with respect to its inputs, bypassing the need for finite difference meshes.

import torch

import torch.nn as nn

\# Define a simple Multi-Layer Perceptron (MLP)

class PINN(nn.Module):

def \_\_init\_\_(self, layers):

super().\_\_init\_\_()

self.activation = nn.Tanh()

self.linears = nn.ModuleList(\[nn.Linear(layers\[i\], layers\[i+1\]) for i in range(len(layers)-1)\])

def forward(self, x, t):

\# Concatenate spatial and temporal inputs

inputs = torch.cat(\[x, t\], axis=1)

for i in range(len(self.linears)-1):

inputs = self.activation(self.linears\[i\](inputs))

return self.linears\[-1\](inputs)

\# Helper function to compute gradients

def compute_gradient(y, x):

"""

Computes dy/dx using PyTorch autograd.

x must have requires_grad=True before passing through the network.

"""

grad = torch.autograd.grad(

y, x,

grad_outputs=torch.ones_like(y),

create_graph=True, \# Crucial for computing higher-order derivatives

retain_graph=True

)\[0\]

return grad

### 1.3 Example: 1D Heat Equation Residual

Consider the 1D heat equation: \$\frac{\partial u}{\partial t} - \alpha \frac{\partial^2 u}{\partial x^2} = 0\$.

def heat_equation_loss(model, x_collocation, t_collocation, alpha=0.01):

\# 1. Ensure inputs track gradients

x_collocation.requires_grad\_(True)

t_collocation.requires_grad\_(True)

\# 2. Forward pass: predict temperature u(x,t)

u = model(x_collocation, t_collocation)

\# 3. Compute first derivatives

u_t = compute_gradient(u, t_collocation)

u_x = compute_gradient(u, x_collocation)

\# 4. Compute second derivative (d^2u/dx^2)

u_xx = compute_gradient(u_x, x_collocation)

\# 5. Compute the PDE residual

residual = u_t - alpha \* u_xx

\# 6. Return Mean Squared Error of the residual

loss_pde = torch.mean(residual\*\*2)

return loss_pde

### 1.4 Common Pitfalls in PINNs

1.  **Spectral Bias:** Neural networks struggle to learn high-frequency features. If your solution has sharp gradients (e.g., shockwaves, stress concentrations), standard PINNs will blur them. **Fix:** Use Fourier feature mappings or sinusoidal activation functions (SIRENs).

2.  **Loss Imbalance:** The gradients of \$\mathcal{L}*{PDE}\$ might be orders of magnitude larger than \$\mathcal{L}*{BC}\$, causing the network to ignore the boundary conditions. **Fix:** Use adaptive loss weighting algorithms (e.g., learning rate annealing or Neural Tangent Kernel weighting).

## 2. Neural Operators

While PINNs learn the solution to a *single* PDE instance, Neural Operators learn the mapping between *infinite-dimensional function spaces*. For example, mapping an initial velocity field directly to the velocity field at time \$t\$, or mapping a variable boundary geometry to a stress field.

### 2.1 The Fourier Neural Operator (FNO)

The FNO performs convolutions in the frequency domain. By transforming the input into Fourier space, multiplying by learnable weights, and transforming back, it achieves **resolution invariance**. You can train an FNO on a \$64 \times 64\$ mesh and evaluate it on a \$256 \times 256\$ mesh without retraining.

### 2.2 FNO Architecture (Conceptual)

1.  **Lift:** Project the input field \$a(x)\$ into a higher-dimensional channel space using a shallow MLP.

2.  **Iterate:** Apply multiple Fourier Layers. In each layer:

    - Apply a standard linear transform in physical space.

    - Apply an FFT, truncate high frequencies, multiply by learnable complex weights, and apply an Inverse FFT.

    - Add the two paths together and apply a non-linear activation (e.g., GeLU).

3.  **Project:** Map the high-dimensional representation back to the target output field \$u(x)\$.

### 2.3 PyTorch Implementation of a 1D Spectral Convolution

import torch

import torch.nn as nn

import torch.fft

class SpectralConv1d(nn.Module):

def \_\_init\_\_(self, in_channels, out_channels, modes):

super(SpectralConv1d, self).\_\_init\_\_()

self.in_channels = in_channels

self.out_channels = out_channels

self.modes = modes \# Number of Fourier modes to keep (truncation)

\# Learnable complex weights

self.weights = nn.Parameter(

torch.empty(in_channels, out_channels, modes, dtype=torch.cfloat)

)

nn.init.xavier_normal\_(self.weights)

def forward(self, x):

\# x shape: (batch, in_channels, num_grid_points)

batch_size = x.shape\[0\]

\# 1. Compute Fast Fourier Transform

x_ft = torch.fft.rfft(x)

\# 2. Multiply relevant Fourier modes

out_ft = torch.zeros(batch_size, self.out_channels, x.size(-1)//2 + 1,

device=x.device, dtype=torch.cfloat)

\# Einstein summation for efficient batched complex multiplication

out_ft\[:, :, :self.modes\] = torch.einsum(

"bix,iox-\>box",

x_ft\[:, :, :self.modes\],

self.weights

)

\# 3. Return to physical space via Inverse FFT

x_out = torch.fft.irfft(out_ft, n=x.size(-1))

return x_out

### 2.4 Why use FNOs in Engineering?

Once trained (which is computationally expensive), an FNO can evaluate a new PDE parameterization (e.g., a new airfoil shape or structural topology) in milliseconds. This makes them ideal surrogate models for real-time digital twins or inner-loop evaluations in generative design and topology optimization.

**Fall 2026 addendum — practical training recipes and honest expectations**

For systematic training recipes (Adam→L-BFGS scheduling, adaptive loss weighting, Fourier features, causality enforcement), see "An Expert's Guide to Training Physics-Informed Neural Networks" — Ref_36 in the course References folder. Calibrate expectations with McGreivy & Hakim (Nat. Mach. Intell. 2024, Ref_24): most published ML-beats-solver claims used weak baselines. Rule of thumb from Weeks 5–6: PINNs win at inverse problems and data fusion; classical FEA/CFD still wins most forward problems; neural operators (FNO/DeepONet) win when you must solve a family of parameterized problems fast.
