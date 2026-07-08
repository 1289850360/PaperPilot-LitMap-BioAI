# Revised Gold Annotation Review

Source file:

```text
evaluation/gold_revised.csv
```

This file was copied from:

```text
C:\Users\12898\Downloads\flow_matching_gold_annotations_revised.csv
```

## Summary

The revised annotation file is substantially stronger than the first `gold_assisted.csv` draft.

Compared with the first assisted draft, it:

- uses more complete task descriptions
- separates training/evaluation datasets more carefully in notes
- captures paper-specific method components
- expands metrics beyond generic terms such as RMSD and accuracy
- includes useful `review_notes` for ambiguous cases

This is a good candidate for the first pilot gold file after final human confirmation.

## Current Score Against Heuristic Baseline

Command:

```powershell
python evaluation\score_extraction.py --pred evaluation\predictions.csv --gold evaluation\gold_revised.csv --fields task datasets models_or_methods metrics --out-dir evaluation\results_revised
```

Result:

```text
papers compared:       5
fields compared:       20
field-level accuracy:  80.0%
missing rate:          5.0%
hallucination rate:    68.4%
citation checks:       supported=19, missing=1
```

Per-field:

```text
task                   accuracy=40.0%  missing=0.0%   hallucination=60.0%
datasets               accuracy=80.0%  missing=20.0%  hallucination=0.0%
models_or_methods      accuracy=100.0% missing=0.0%   hallucination=100.0%
metrics                accuracy=100.0% missing=0.0%   hallucination=100.0%
```

## Interpretation

The heuristic extractor successfully finds many relevant method and metric terms, which explains the high field-level scores for `models_or_methods` and `metrics`.

However, the hallucination rate is still high because the current scoring script treats extra predicted values as unsupported if they do not appear in the gold field. This is useful for the workshop story:

> The heuristic baseline has broad recall but weak schema control, leading to over-extraction.

This motivates:

- schema-constrained extraction
- stronger method/dataset/metric typing
- citation verification
- LLM verifier or rule-based post-filtering

## Notes Before Treating as Final Gold

Recommended checks:

1. Decide whether training/augmentation sources such as `OpenProteinSet`, `OrbNet conformers`, and `PLINDER` should stay in `datasets` or be separated from evaluation benchmarks.
2. Decide whether baselines such as `product-space diffusion`, `EigenFold diffusion`, `DiffDock-Pocket`, `SMINA`, `GNINA`, `VINA`, and `AlphaFold3` should stay in `models_or_methods` or move to a future `baselines` field.
3. Keep semicolon-separated values if using the current scoring script; it supports both semicolon and ` | ` separators.
4. If this file is accepted, copy it to:

```text
evaluation/gold.csv
```

Then rerun:

```powershell
python evaluation\score_extraction.py --pred evaluation\predictions.csv --gold evaluation\gold.csv --fields task datasets models_or_methods metrics
```
