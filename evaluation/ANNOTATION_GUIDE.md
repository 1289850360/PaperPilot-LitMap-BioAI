# Annotation Guide

This guide defines how to annotate the PaperPilot flow-matching seed set.

It is inspired by scientific information extraction benchmarks such as SciREX and TDMSci:

- SciREX treats scientific IE as a document-level problem, where entities and relations may span multiple sections of a paper.
- TDMSci focuses on extracting Task, Dataset, and Metric entities from scientific literature.
- ORKG motivates turning paper contributions into structured, machine-actionable comparison units.

References:

- SciREX: <https://arxiv.org/abs/2005.00512>
- TDMSci: <https://arxiv.org/abs/2101.10273>
- Open Research Knowledge Graph: <https://arxiv.org/abs/1901.10816>

## Scope

The first pilot evaluation uses four fields:

- `task`
- `datasets`
- `models_or_methods`
- `metrics`

The later full schema should add:

- `baselines`
- `main_result`
- `limitations`
- `code_availability`
- `evidence_page`
- `evidence_text`

The stricter candidate schema is stored in:

```text
evaluation/gold_schema_v2.csv
```

It separates:

- `datasets` into `training_data`, `evaluation_benchmarks`, and `external_test_sets`
- `models_or_methods` into `proposed_method`, `method_components`, `baselines`, and `auxiliary_tools`

## General Rules

### Use Document-Level Evidence

Do not rely only on the abstract. Check:

- abstract
- introduction
- method overview
- experiment setup
- tables
- figure captions
- appendix experiment details

### Prefer Canonical Names

Use the paper's canonical terms when possible.

Examples:

- `FlowDock`
- `ForceFM`
- `FLEXDOCK`
- `HARMONICFLOW`
- `FLOWSITE`
- `PDBBind`
- `PoseBusters`
- `DockGen-E`

### Use Semicolon Separators

Current revised gold uses semicolons:

```text
PDBBind; PoseBusters; DockGen-E
```

The scoring script accepts both semicolons and ` | `, but semicolons should be preferred in manually edited gold files.

## Field Definitions

## task

Annotate the main scientific or engineering problem the paper solves.

Good examples:

- `protein-ligand docking`
- `flexible protein-ligand docking`
- `protein-ligand binding affinity prediction`
- `biomolecular complex structure prediction`
- `binding site design`
- `structure relaxation`
- `multi-ligand docking`

Do not include:

- generic motivation such as `drug discovery`, unless the paper directly frames it as the task
- evaluation metrics
- model names

Recommended granularity:

- Include 2-5 task phrases if the paper genuinely covers multiple related tasks.
- Keep one broad task plus one or two specific sub-tasks.

## datasets

Annotate named datasets, benchmarks, evaluation sets, or benchmark splits used in the paper.

Good examples:

- `PDBBind`
- `PDBBind-E`
- `PoseBusters Benchmark`
- `DockGen-E`
- `Binding MOAD`
- `CASP16 ligand category`
- `PDBBind sequence similarity split`

Borderline cases:

- Training or pretraining data can be included only if it is important to the paper's experimental setup.
- If included, explain in `review_notes` whether it is training data, augmentation data, or evaluation data.

Do not include:

- methods, models, or software tools
- metrics
- generic words such as `benchmark` without a name

Recommended future improvement:

Split this into:

- `training_data`
- `evaluation_benchmarks`
- `external_test_sets`

## models_or_methods

Annotate the proposed method, model family, and central technical components.

Good examples:

- `FlowDock`
- `ForceFM`
- `FLEXDOCK`
- `HARMONICFLOW`
- `FLOWSITE`
- `conditional flow matching`
- `force-guided flow matching`
- `unbalanced flow matching`
- `confidence head`
- `binding affinity head`

Borderline cases:

- Baselines can be included in this field during the 4-field pilot, but should move to `baselines` in the full schema.
- Auxiliary scoring or guidance functions can be included if they are part of the proposed method.

Do not include:

- datasets
- metrics
- broad background methods that are only mentioned in related work

Recommended future improvement:

Split this into:

- `proposed_method`
- `method_components`
- `baselines`
- `auxiliary_tools`

## metrics

Annotate evaluation metrics, success criteria, and reported evaluation measures.

Good examples:

- `RMSD`
- `ligand RMSD`
- `centroid distance`
- `PoseBusters validity`
- `PB-valid success rate`
- `TM-score`
- `DockQ`
- `LDDT`
- `pLDDT`
- `Pearson correlation`
- `Spearman correlation`
- `RMSE`
- `MAE`
- `sequence recovery`
- `BLOSUM score`
- `runtime`
- `memory usage`

Borderline cases:

- Thresholded criteria such as `RMSD <= 2 Å success rate` are acceptable as metrics because they are reported evaluation measures.
- Runtime and memory are acceptable if the paper reports them as efficiency metrics.

Do not include:

- model names
- datasets
- qualitative claims such as `better performance`

Recommended future improvement:

Split this into:

- `pose_metrics`
- `structure_metrics`
- `affinity_metrics`
- `validity_metrics`
- `efficiency_metrics`

## Gold vs Prediction

The gold file should be stricter than the system prediction.

Prediction may over-extract:

- generic method names
- related work baselines
- broad terms such as `accuracy`
- metrics mentioned only in passing

Gold should include:

- terms that are central to the paper
- terms used in experiments, tables, or main claims
- terms supported by source text

## Recommended Review Questions

For every item in gold, ask:

1. Is this term explicitly present in the paper?
2. Is it central enough to the paper's task, experiment, or method?
3. Is it in the correct field?
4. Would another annotator likely put it in the same field?
5. Should it move to a future field such as `baselines` or `training_data`?

## Current Pilot Decision

For the current 5-paper pilot:

- It is acceptable to keep training data and evaluation benchmarks together in `datasets`, if `review_notes` explains the distinction.
- It is acceptable to keep baselines and auxiliary tools in `models_or_methods`, if `review_notes` explains what should move later.
- The workshop write-up should state that this is a 4-field pilot schema and that the full schema will separate baselines, training data, and evaluation benchmarks.

For the next evaluation iteration:

- Use `evaluation/gold.csv` for 4-field baseline scoring.
- Use `evaluation/gold_schema_v2.csv` for analysis, full-schema design, and later model targets.
