# Gold Refinement Report

This report summarizes a conservative automatic refinement pass over the 23-paper gold annotation file.

## Inputs

- Gold: `evaluation\gold_23_paper_benchmark.csv`
- Verified predictions: `experiments\outputs\benchmark_23_schema_v7_verified\verified_predictions.csv`
- Value audit: `evaluation\value_verifier_audit_benchmark_23_v7.csv`

## Outputs

- Revised gold candidate: `evaluation\gold_23_paper_benchmark_auto_refined_v1.csv`
- Human review queue: `evaluation\gold_refinement_candidates_v1.csv`

## Decision Counts

| Decision | Count |
|---|---:|
| add | 114 |
| review | 86 |
| reject | 0 |

## By Field

| Field | Add | Review | Reject |
|---|---:|---:|---:|
| task | 0 | 28 | 0 |
| datasets | 14 | 3 | 0 |
| models_or_methods | 29 | 38 | 0 |
| metrics | 71 | 17 | 0 |

## Curation Policy

- `add`: supported by the PDF and specific enough to be safely merged into the revised gold candidate.
- `review`: supported or weakly supported, but broad enough that a human should confirm whether it belongs in the schema.
- `reject`: unsupported by the PDF evidence verifier.

The revised gold file is still marked as needing final human review. It should be treated as a benchmark candidate, not a fully locked gold standard.

## Score Impact

The same `schema v7 + value verifier` predictions were scored against the original gold and the auto-refined gold candidate.

| Gold Version | Field Accuracy | Value Precision | Value Recall | Value F1 | Missing Rate | Hallucination Rate |
|---|---:|---:|---:|---:|---:|---:|
| original 23-paper gold | 91.8% | 58.8% | 54.2% | 56.4% | 1.1% | 74.7% |
| auto-refined gold v1 | 92.9% | 80.0% | 61.5% | 69.6% | 1.1% | 53.8% |

## Recommended Manual Review

Focus first on rows marked `review` in `evaluation/gold_refinement_candidates_v1.csv`.

Priority order:

1. `task`: decide whether the proposed task label is genuinely part of the paper's main contribution.
2. `models_or_methods`: separate the paper's own method/components from baselines, comparison methods, and related work.
3. `metrics`: decide whether generic labels such as `runtime`, `binding affinity`, `diversity`, and `success rate` should be normalized into more specific metric names.
