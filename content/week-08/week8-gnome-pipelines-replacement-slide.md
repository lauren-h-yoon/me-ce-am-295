---
title: "Week8 GNoME Pipelines REPLACEMENT Slide"
week: 8
doc_type: "lecture_slides"
access: "all_students"
agents: [all_student_agents, concept_tutor]
source: "materials/Week 8/Week8_GNoME_Pipelines_REPLACEMENT_Slide.pptx"
source_hash: "97d29a165e7c6b0f"
normalized_at: "2026-08-19T11:55:20Z"
---
## Slide 1

WEEK 8 · REPLACEMENT SLIDE (ORIGINAL DECK SLIDE IS BLANK)

GNoME's Two Discovery Pipelines

Structural pipeline

Start from known crystal structures; substitute elements using learned chemical-similarity rules; relax candidates with DFT; feed results back to retrain the GNN. Explores near known structural families.

Compositional pipeline

Start from chemical formulas only (no structure assumed); random structure search seeded by composition; GNN filters candidates before expensive DFT. Explores farther from known materials.

Active-learning loop: every DFT verification — success or failure — becomes training data. Six rounds grew hit rates from <10% to >80% (structural) and ~33% (compositional).

Merchant et al., Nature 624:80–85 (2023) — Ref_10. Novelty caveats: see the Week 8 critiques supplement slide (Ref_22, Ref_23).
