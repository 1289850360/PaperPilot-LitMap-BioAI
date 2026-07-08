# Seed Paper Set

This document records the first small paper set for PaperPilot experiments.

Theme:

```text
Flow matching and related generative models for biomolecular docking, protein-ligand structure prediction, and flexible docking.
```

The goal is to start with 5 papers, run the heuristic extractor, manually correct a gold CSV, and produce the first evaluation table.

## Current Local Papers

These are already on the local machine.

| ID | Paper | Local PDF |
|---|---|---|
| seed_001 | NeuralPLexer3: Accurate Biomolecular Complex Structure Prediction | `C:\Users\12898\Desktop\flow matching文献阅读\2412.10743v2.pdf` |
| seed_002 | Composing Unbalanced Flows for Flexible Docking and Relaxation | `C:\Users\12898\Desktop\flow matching文献阅读\ICLR-2025-composing-unbalanced-flows-for-flexible-docking-and-relaxation-Paper-Conference.pdf` |
| seed_003 | ForceFM: Enhancing Protein-Ligand Predictions through Force-Guided Flow Matching | `C:\Users\12898\Desktop\flow matching文献阅读\NeurIPS-2025-forcefm-enhancing-protein-ligand-predictions-through-force-guided-flow-matching-Paper-Conference.pdf` |

## Recommended Additions

### seed_004: FlowDock

Title:

```text
FlowDock: Geometric Flow Matching for Generative Protein-Ligand Docking and Affinity Prediction
```

Why include it:

- directly uses conditional flow matching
- focuses on protein-ligand docking
- includes affinity prediction
- reports benchmarks such as PoseBusters and DockGen-E
- provides source code, data, and pretrained models

Links:

- Abstract: <https://arxiv.org/abs/2412.10966>
- PDF: <https://arxiv.org/pdf/2412.10966>
- Suggested local filename: `FlowDock-2412.10966.pdf`

### seed_005: HarmonicFlow / FlowSite

Title:

```text
Harmonic Self-Conditioned Flow Matching for Multi-Ligand Docking and Binding Site Design
```

Why include it:

- ICML 2024 paper
- uses self-conditioned flow matching
- covers multi-ligand docking
- extends from docking to binding site design
- useful comparison point against newer flow matching docking papers

Links:

- Abstract: <https://arxiv.org/abs/2310.05764>
- PDF: <https://arxiv.org/pdf/2310.05764>
- Suggested local filename: `HarmonicFlow-2310.05764.pdf`

## Optional Later Addition

### Matcha

Title:

```text
Matcha: Multi-Stage Riemannian Flow Matching for Accurate and Physically Valid Molecular Docking
```

Why consider it later:

- very recent flow matching docking paper
- emphasizes physical validity and staged geometric refinement
- useful if the seed set expands beyond 5 papers

Links:

- Abstract: <https://arxiv.org/abs/2510.14586>
- PDF: <https://arxiv.org/pdf/2510.14586>

## Suggested First Experiment

1. Download `FlowDock-2412.10966.pdf`.
2. Download `HarmonicFlow-2310.05764.pdf`.
3. Save both PDFs into:

```text
C:\Users\12898\Desktop\flow matching文献阅读\
```

4. Update `experiments/flow_matching_seed_manifest.csv` if the filenames are different.
5. Run:

```powershell
python experiments\batch_extract.py --manifest experiments\flow_matching_seed_manifest.csv --out-dir experiments\outputs
```

6. Copy predictions into the evaluation folder:

```powershell
Copy-Item experiments\outputs\heuristic_predictions.csv evaluation\predictions.csv
Copy-Item evaluation\predictions.csv evaluation\gold.csv
```

7. Manually correct `evaluation\gold.csv`.
8. Score:

```powershell
python evaluation\score_extraction.py --pred evaluation\predictions.csv --gold evaluation\gold.csv
```
