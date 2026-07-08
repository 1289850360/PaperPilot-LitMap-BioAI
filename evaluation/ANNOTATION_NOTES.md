# Assisted Gold Annotation Notes

This file documents the first AI-assisted annotation pass for the 5-paper flow-matching seed set.

Important:

- `evaluation/gold_assisted.csv` is a draft, not final gold.
- The project author should review and correct it before using it as a gold standard in a workshop paper.
- The first pilot evaluation focuses on four fields: `task`, `datasets`, `models_or_methods`, and `metrics`.

## Annotation Protocol

### task

Annotate the main scientific or engineering task solved by the paper.

Good examples:

- protein-ligand docking
- biomolecular complex structure prediction
- binding site design
- protein-ligand affinity prediction
- structure relaxation

Do not annotate generic motivations such as "drug discovery" unless the paper frames it as the direct task.

### datasets

Annotate named datasets, benchmarks, benchmark splits, or evaluation collections.

Good examples:

- PDBBind
- PDBBind-E
- PoseBusters Benchmark
- DockGen-E
- Binding MOAD
- CASP16 ligand category

Do not annotate tools or baselines as datasets.

### models_or_methods

Annotate the proposed method and important method families used by the paper.

Good examples:

- FlowDock
- ForceFM
- FLEXDOCK
- HarmonicFlow
- FlowSite
- conditional flow matching
- self-conditioned flow matching
- force-guided flow matching

Baselines can be included only if they are central to the experimental comparison.

### metrics

Annotate evaluation metrics and success criteria.

Good examples:

- RMSD
- centroid distance
- TM-score
- DockQ
- LDDT
- Pearson correlation
- Spearman correlation
- RMSE
- MAE
- PoseBusters validity
- sequence recovery
- BLOSUM score

Do not include method names as metrics.

## Paper-Level Draft Annotations

### paper_001: NeuralPLexer3

Task:

- biomolecular complex structure prediction
- protein-ligand complex structure prediction
- biomolecular interaction structure prediction

Datasets / benchmarks:

- PoseBusters
- newly developed biomolecular interaction benchmarks

Methods:

- NeuralPLexer3
- physics-inspired flow-based generative model
- flow matching
- continuous normalizing flow
- encoder-decoder structure prediction model

Metrics:

- RMSD
- PoseBusters validity
- success rate
- TM-score
- DockQ
- LDDT
- stereochemistry accuracy

Review notes:

- Check whether any named benchmark datasets besides PoseBusters should be added.
- The paper discusses multiple biomolecular interaction types, so task may be broader than ligand docking.

### paper_002: FlowDock

Task:

- flexible protein-ligand docking
- protein-ligand affinity prediction
- multi-ligand docking

Datasets / benchmarks:

- PDBBind-E
- PDBBind 2020
- PoseBusters Benchmark
- DockGen-E
- CASP16 ligand category

Methods:

- FlowDock
- conditional flow matching
- geometric generative model
- affinity prediction head
- apo-to-holo structure generation

Metrics:

- blind docking success rate
- RMSD
- centroid distance
- TM-score
- pLDDT
- Pearson correlation
- Spearman correlation
- RMSE
- MAE

Review notes:

- Confirm whether CASP16 should be treated as a dataset/benchmark or as an external evaluation track.

### paper_003: HarmonicFlow / FlowSite

Task:

- multi-ligand docking
- binding site design
- protein pocket residue design for small-molecule binding

Datasets / benchmarks:

- PDBBind version 2020
- Binding MOAD
- PDBBind time split
- PDBBind sequence similarity split
- Binding MOAD sequence similarity split

Methods:

- HarmonicFlow
- FlowSite
- harmonic self-conditioned flow matching
- self-conditioned flow matching
- product-space diffusion baseline
- EigenFold diffusion baseline

Metrics:

- RMSD
- fraction of predictions with RMSD below 2 angstrom
- fraction of predictions with RMSD below 5 angstrom
- median RMSD
- sequence recovery
- BLOSUM score
- runtime

Review notes:

- Decide whether product-space diffusion and EigenFold diffusion should remain under `models_or_methods` or be moved to `baselines` in a full 8-field annotation.

### paper_004: Composing Unbalanced Flows

Task:

- flexible protein-ligand docking
- structure relaxation
- modeling protein flexibility
- generating energetically favorable docking poses

Datasets / benchmarks:

- PDBBind
- PoseBusters
- PDBBind ESMFold docking benchmark

Methods:

- Unbalanced Flow Matching
- Flow Matching
- FLEXDOCK
- manifold docking flow
- relaxation flow
- DiffDock-Pocket baseline

Metrics:

- ligand RMSD
- pocket all-atom RMSD
- percentage RMSD below 1 angstrom
- percentage RMSD below 2 angstrom
- PoseBusters checks
- proportion of energetically favorable poses

Review notes:

- DiffDock-Pocket is a baseline; for the 4-field pilot it is included under methods, but a full annotation should move it to `baselines`.

### paper_005: ForceFM

Task:

- protein-ligand docking
- binding pose prediction
- physically plausible ligand conformation generation

Datasets / benchmarks:

- PDBBind
- DockGen

Methods:

- ForceFM
- force-guided flow matching
- force guidance network
- Molecular Docking via Manifold Flow Matching
- energy-guided generation
- Vina
- Glide
- Gnina
- Confscore

Metrics:

- RMSD
- percentage RMSD below 2 angstrom
- centroid distance
- percentage centroid distance below 2 angstrom
- PoseBusters validity
- docking score
- inference cost

Review notes:

- Vina, Glide, Gnina, and Confscore are force/energy guidance functions in this paper. If using a strict schema, they may be better represented under `baselines` or `auxiliary scoring functions`.

## First Pilot Score

Using:

```powershell
python evaluation\score_extraction.py --pred evaluation\predictions.csv --gold evaluation\gold_assisted.csv --fields task datasets models_or_methods metrics
```

Current result:

- papers compared: 5
- fields compared: 20
- field-level accuracy: 75.0%
- missing rate: 5.0%
- hallucination rate: 73.7%

Interpretation:

- The heuristic extractor can find many relevant terms.
- It misses some datasets, especially for NeuralPLexer3.
- It over-extracts broad method and metric terms, which increases the hallucination rate under the current strict scoring rule.
- This is useful for the workshop story because it motivates stronger schema constraints and citation verification.
