---
title: "Week6 GNN REPLACEMENT Slide"
week: 6
doc_type: "lecture_slides"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 6/Week6_GNN_REPLACEMENT_Slide.pptx"
source_hash: "3537b74886ed5bd6"
normalized_at: "2026-08-19T11:55:20Z"
---
## Slide 1

WEEK 6 · REPLACEMENT SLIDE (ORIGINAL DECK SLIDE IS BLANK)

Graph Neural Networks (GNNs) for Irregular Geometries

FNOs need regular grids. Real engineering meshes are graphs: nodes (joints, mesh vertices) and edges (members, element connectivity). GNNs learn directly on that structure.

Message passing

Each node aggregates information from its neighbors, layer by layer — like load redistribution propagating joint-to-joint through a truss.

Why engineers care

Mesh-native: works on the unstructured meshes FEA already uses. MeshGraphNets-style simulators predict deformation fields on arbitrary geometry.

Materials example

Lattice metamaterials ARE graphs: struts = edges, nodes = joints. GNN surrogates predict effective stiffness orders of magnitude faster than FEA.

Solver selection: regular grid + family of PDEs → FNO · single PDE instance or inverse problem → PINN · irregular mesh/graph → GNN · everything else → classical FEA/CFD.
