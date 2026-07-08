# Issues and Decisions for `gold_revised.csv`

This document reviews `evaluation/gold_revised.csv`.

Overall conclusion:

```text
gold_revised.csv is strong enough for a first pilot evaluation, but it should be described as a 4-field pilot gold schema rather than a final full benchmark schema.
```

## High-Priority Issues

### 1. Dataset Field Mixes Evaluation Benchmarks and Training/Augmentation Sources

Examples:

- `PLINDER`
- `OpenProteinSet`
- `OrbNet conformers`
- `PDBBind time split`
- `PDBBind sequence similarity split`

This is not necessarily wrong, but it needs a rule.

Recommended decision for the pilot:

- Keep them if they are important to the paper.
- Explain in `review_notes` whether they are evaluation benchmarks, training data, curation sources, or augmentation sources.

Recommended decision for the full schema:

- Split `datasets` into:
  - `training_data`
  - `evaluation_benchmarks`
  - `external_test_sets`

### 2. `models_or_methods` Mixes Proposed Methods, Components, Baselines, and Tools

Examples:

- `product-space diffusion baseline`
- `EigenFold diffusion baseline`
- `DiffDock-Pocket`
- `VINA`
- `GNINA`
- `AlphaFold3`
- `RDKit ETKDG conformer initialization`

Recommended decision for the pilot:

- Keep these in `models_or_methods` only if they are central to the paper's method or experimental comparison.
- Use `review_notes` to mark which ones should move to a future `baselines` field.

Recommended decision for the full schema:

- Split into:
  - `proposed_method`
  - `method_components`
  - `baselines`
  - `auxiliary_tools`

### 3. Gold Is More Complete Than the Current Prediction Schema

The revised gold includes many fine-grained method components and metrics. This is good for human annotation, but the current heuristic extractor was not designed to extract this level of detail.

Effect:

- field-level accuracy is still usable
- hallucination rate is inflated because predictions often include extra broad terms or miss fine-grained distinctions

Recommended decision:

- Use the current score as a baseline result, not as a final system quality claim.
- In the workshop text, describe the heuristic extractor as a high-recall baseline with weak schema control.

## Medium-Priority Issues

### 4. `paper_title` Column Does Not Match the Prediction CSV's `title` Column

Current revised gold uses:

```text
paper_title
```

Prediction CSV uses:

```text
title
```

This is okay because the scoring script matches rows by `paper_id`. Still, for consistency, the final `gold.csv` should probably include `title`.

Recommended decision:

- Before finalizing, create a normalized `gold.csv` with columns matching `evaluation/predictions.csv`.

### 5. Semicolon Separators Are Fine, But Should Be Declared

The revised gold uses semicolons:

```text
PDBBind; PoseBusters; DockGen-E
```

The original PaperPilot export uses:

```text
PDBBind | PoseBusters | DockGen-E
```

The scorer supports both. This is fine.

Recommended decision:

- Use semicolons in manually edited gold files.
- Mention this in `evaluation/ANNOTATION_GUIDE.md`.

### 6. Some Metrics Are Composite Measures

Examples:

- `RMSD ≤ 2 Å and PB-Valid success rate`
- `PB-valid and ligand RMSD < 2 Å`
- `TM-score and RMSD apo-to-holo training filters`

These are valid if they are reported as evaluation criteria. But they mix metric names with thresholds or filtering criteria.

Recommended decision:

- Keep thresholded criteria when the paper reports them as a success metric.
- Move training filters out of `metrics` in a stricter future schema.

## Paper-Specific Notes

### paper_001: NeuralPLexer3

Strength:

- revised annotation correctly broadens the task beyond ligand docking.

Potential issue:

- `PLINDER`, `OpenProteinSet`, and `OrbNet conformers` are not all evaluation benchmarks. The current review note handles this well.

Decision:

- Accept for pilot if notes remain.

### paper_002: FlowDock

Strength:

- captures both docking and affinity prediction.
- includes resource metrics such as runtime and memory.

Potential issue:

- `generalized unbalanced flow matching` should be checked carefully. If it is inherited from related methodology rather than central to FlowDock, keep it only if explicitly used in the model.

Decision:

- Accept for pilot; optionally review this one phrase.

### paper_003: HarmonicFlow / FlowSite

Strength:

- correctly captures that the paper covers both docking and binding site design.

Potential issue:

- `product-space diffusion baseline` and `EigenFold diffusion baseline` are baselines, not proposed methods.

Decision:

- Accept for 4-field pilot.
- Move to `baselines` in full schema.

### paper_004: Composing Unbalanced Flows

Strength:

- good task granularity.
- metrics are specific and useful.

Potential issue:

- Some comparison methods are only in review notes, not in `models_or_methods`; this is actually cleaner for the 4-field pilot.

Decision:

- Accept for pilot.

### paper_005: ForceFM

Strength:

- correctly treats Vina, Glide, Gnina, and Confscore as guidance/scoring functions rather than metrics.

Potential issue:

- `PoseBuster benchmark` should probably be normalized to `PoseBusters Benchmark`.

Decision:

- Normalize spelling in final `gold.csv`.

## Recommended Next Action

Create a normalized final gold file:

```text
evaluation/gold.csv
```

Recommended changes:

1. Rename `paper_title` to `title`.
2. Keep all four annotated fields.
3. Keep `review_notes`.
4. Normalize `PoseBuster benchmark` to `PoseBusters Benchmark`.
5. Add empty columns for the future full schema if useful:
   - `baselines`
   - `main_result`
   - `limitations`
   - `code_availability`

Then rerun:

```powershell
python evaluation\score_extraction.py --pred evaluation\predictions.csv --gold evaluation\gold.csv --fields task datasets models_or_methods metrics
```
