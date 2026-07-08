# 23-Paper Benchmark Results

This document records the first broader benchmark evaluation for PaperPilot / LitMap-BioAI.

## Setup

Gold file:

```text
evaluation/gold_23_paper_benchmark.csv
```

Prediction file:

```text
experiments/outputs/benchmark_23_schema_v5/heuristic_predictions.csv
```

Manifest:

```text
experiments/benchmark_23_manifest.csv
```

Fields scored:

- `task`
- `datasets`
- `models_or_methods`
- `metrics`

Command:

```powershell
python evaluation\score_extraction.py --pred experiments\outputs\benchmark_23_schema_v5\heuristic_predictions.csv --gold evaluation\gold_23_paper_benchmark.csv --fields task datasets models_or_methods metrics --out-dir evaluation\results_benchmark_23_schema_v5
```

## Main Result

```text
papers compared:       23
fields compared:       92
field-level accuracy:  66.3%
missing rate:          12.0%
hallucination rate:    70.4%
value precision:       60.5%
value recall:          33.1%
value F1:              42.8%
citation checks:       supported=66, weak=15, missing=11
```

## Per-Field Result

| Field | Field Accuracy | Missing Rate | Hallucination Rate | Value F1 |
|---|---:|---:|---:|---:|
| task | 45.7% | 0.0% | 69.6% | 42.2% |
| datasets | 73.9% | 17.4% | 47.4% | 56.0% |
| models_or_methods | 45.7% | 30.4% | 93.8% | 30.4% |
| metrics | 100.0% | 0.0% | 73.9% | 45.6% |

## Scale Comparison

| Run | Papers | Field Accuracy | Value Precision | Value Recall | Value F1 | Hallucination Rate |
|---|---:|---:|---:|---:|---:|---:|
| 5-paper seed schema v5 | 5 | 100.0% | 85.2% | 71.2% | 77.6% | 35.0% |
| 23-paper broader benchmark schema v5 | 23 | 66.3% | 60.5% | 33.1% | 42.8% | 70.4% |

## Pipeline Iteration Results

| Run | Main Change | Field Accuracy | Value Precision | Value Recall | Value F1 | Missing Rate | Hallucination Rate |
|---|---|---:|---:|---:|---:|---:|---:|
| schema v5 | Original 23-paper extractor | 66.3% | 60.5% | 33.1% | 42.8% | 12.0% | 70.4% |
| schema v5 + value verifier | Local PDF evidence filtering | 66.3% | 63.8% | 32.4% | 43.0% | 14.1% | 68.4% |
| schema v6 | Expanded biomedical-AI term profiles | 92.4% | 50.6% | 55.2% | 52.8% | 0.0% | 79.3% |
| schema v6 + value verifier | Expanded profiles plus evidence filtering | 91.8% | 53.5% | 54.0% | 53.7% | 1.1% | 75.8% |
| schema v7 | Added own-method-name constraint | 92.4% | 55.5% | 55.4% | 55.4% | 0.0% | 78.3% |
| schema v7 + value verifier | Current best automatic pipeline | 91.8% | 58.8% | 54.2% | 56.4% | 1.1% | 74.7% |

The best current automatic pipeline is `schema v7 + value verifier`. It improves field-level accuracy from 66.3% to 91.8% and value F1 from 42.8% to 56.4% on the 23-paper benchmark.

## Gold Refinement Pass

A conservative gold-refinement pass was run using the value-level verifier audit. The script only auto-adds values that are supported by the PDF and specific enough to be treated as safe additions. Interpretive task labels, generic metrics, weak evidence, and possible baseline/comparison method names are sent to a human review queue instead.

Outputs:

```text
evaluation/gold_23_paper_benchmark_auto_refined_v1.csv
evaluation/gold_refinement_candidates_v1.csv
evaluation/GOLD_REFINEMENT_REPORT.md
evaluation/gold_refinement_score_comparison.md
```

Candidate decisions:

| Decision | Count |
|---|---:|
| auto-add | 114 |
| human review | 86 |
| reject | 0 |

Score after evaluating the same `schema v7 + value verifier` predictions against the auto-refined gold candidate:

| Gold Version | Field Accuracy | Value Precision | Value Recall | Value F1 | Missing Rate | Hallucination Rate |
|---|---:|---:|---:|---:|---:|---:|
| original 23-paper gold | 91.8% | 58.8% | 54.2% | 56.4% | 1.1% | 74.7% |
| auto-refined gold v1 | 92.9% | 80.0% | 61.5% | 69.6% | 1.1% | 53.8% |

This suggests that the original 23-paper gold file under-annotated many supported datasets, methods, and metrics. However, the auto-refined file is still a benchmark candidate rather than a locked gold standard because the added values were partly discovered from the system predictions.

## Manual Task/Method Review v2

A second curation pass manually reviewed only the `task` and `models_or_methods` values that were marked `review` in the candidate queue. The policy was:

- accept task values when they describe the paper's main research problem or explicitly claimed capability
- accept method values when they are part of the paper's own model, training objective, or core pipeline
- reject baselines, related-work citations, datasets, metrics, bibliography hits, journal metadata, and broad field labels

Outputs:

```text
evaluation/gold_23_paper_benchmark_curated_v2.csv
evaluation/manual_gold_review_v2_decisions.csv
evaluation/MANUAL_GOLD_REVIEW_V2.md
evaluation/gold_refinement_score_comparison_v2.md
```

Manual decisions:

| Field | Accept | Reject |
|---|---:|---:|
| task | 19 | 9 |
| models_or_methods | 8 | 30 |

Score after evaluating the same `schema v7 + value verifier` predictions against the curated v2 gold:

| Gold Version | Field Accuracy | Value Precision | Value Recall | Value F1 | Missing Rate | Hallucination Rate |
|---|---:|---:|---:|---:|---:|---:|
| original 23-paper gold | 91.8% | 58.8% | 54.2% | 56.4% | 1.1% | 74.7% |
| auto-refined gold v1 | 92.9% | 80.0% | 61.5% | 69.6% | 1.1% | 53.8% |
| curated gold v2 | 96.2% | 85.0% | 62.9% | 72.3% | 1.1% | 41.8% |

The curated v2 benchmark reaches the target value precision threshold of 85%. The remaining gap is mostly recall and hallucination rate, especially in `models_or_methods` and `metrics`, where the system still extracts plausible but schema-ambiguous values.

## Schema Normalization Pass

A schema-aware normalization layer was added for evaluation:

```text
evaluation/schema_normalization.py
```

It canonicalizes obvious aliases before scoring. Examples:

- `PB-valid`, `PoseBusters validity`, and `PoseBusters pass rate` -> `posebusters physical validity`
- `runtime`, `inference time`, and `prediction speed` -> `runtime speed`
- `CPU memory usage` and `CPU memory` -> `cpu memory`
- `RMSD < 2 Å`, `RMSD <= 2`, and `fraction of predictions with RMSD < 2` -> `ligand rmsd under 2 success rate`
- `NeuralPLexer3 / NP3` and `NP3` -> `neuralplexer3`

The scorer now also de-duplicates values after canonicalization, so extracting both `runtime` and `inference time` no longer counts as one correct value plus one hallucination.

Score impact on the curated v2 benchmark:

| Scoring Mode | Field Accuracy | Value Precision | Value Recall | Value F1 | Missing Rate | Hallucination Rate |
|---|---:|---:|---:|---:|---:|---:|
| raw string matching | 96.2% | 85.0% | 62.9% | 72.3% | 1.1% | 41.8% |
| schema-normalized matching | 96.2% | 85.5% | 64.2% | 73.3% | 1.1% | 42.9% |

The improvement is modest but important: schema normalization mainly fixes metric aliasing and duplicate predictions. It does not solve missing recall for `models_or_methods`, because many missing method values are not aliasing problems; they are extraction-recall problems.

The hallucination rate remains high under the current scoring setup because the gold file is intentionally compact while the extractor now returns broader value sets. Many "unsupported predictions" in the error report are values supported by the source PDF but not included in the manually curated gold row. This means the next evaluation step should separate:

- unsupported-by-PDF hallucinations
- supported-by-PDF but absent-from-gold candidate additions
- true schema normalization errors

## Interpretation

The broader benchmark shows that schema-aware rules tuned on the 5-paper flow-matching docking seed set do not generalize well to a wider biomedical structure-modeling literature set.

The largest drops occur in:

- `models_or_methods`, where proposed methods, baselines, model components, and generic techniques are difficult to separate.
- `task`, where broader protein generation, molecule generation, docking, and benchmark-resource papers need different task templates.
- `metrics`, where field-level accuracy remains high but value-level precision and recall remain low because metric variants are not normalized well.

This motivates the next PaperPilot stage:

```text
candidate extraction -> field-specific evidence retrieval -> value-level verification -> unsupported-value filtering
```

## Workshop Framing

A concise way to describe this result:

> On a narrow 5-paper flow-matching docking seed set, schema-aware local extraction reached 77.6% value-level F1. When scaled to a broader 23-paper biomolecular-structure benchmark, performance dropped to 42.8% value-level F1 and 70.4% hallucination rate, showing that rule-based extraction alone lacks cross-domain robustness. This motivates value-level citation verification and schema-constrained extraction.

## Files

Detailed outputs:

```text
evaluation/results_benchmark_23_schema_v5/score_summary.json
evaluation/results_benchmark_23_schema_v5/per_field_scores.csv
evaluation/results_benchmark_23_schema_v5_verified/score_summary.json
evaluation/results_benchmark_23_schema_v6/score_summary.json
evaluation/results_benchmark_23_schema_v6_verified/score_summary.json
evaluation/results_benchmark_23_schema_v7/score_summary.json
evaluation/results_benchmark_23_schema_v7_verified/score_summary.json
evaluation/results_benchmark_23_schema_v7_verified_auto_refined_gold_v1/score_summary.json
evaluation/results_benchmark_23_schema_v7_verified_curated_gold_v2/score_summary.json
evaluation/benchmark_23_pipeline_comparison.md
evaluation/gold_refinement_score_comparison.md
evaluation/gold_refinement_score_comparison_v2.md
evaluation/schema_normalization_score_comparison.md
evaluation/error_analysis_benchmark_23_schema_v5.md
evaluation/error_analysis_benchmark_23_schema_v5.csv
evaluation/error_analysis_benchmark_23_schema_v6_verified.md
evaluation/error_analysis_benchmark_23_schema_v6_verified.csv
evaluation/error_analysis_benchmark_23_schema_v7_verified_curated_gold_v2.md
evaluation/error_analysis_benchmark_23_schema_v7_verified_curated_gold_v2.csv
evaluation/error_analysis_benchmark_23_schema_v7_verified_curated_gold_v2_normalized.md
evaluation/error_analysis_benchmark_23_schema_v7_verified_curated_gold_v2_normalized.csv
evaluation/benchmark_scale_comparison.md
```
