# Pilot Evaluation Results

This document records the first pilot evaluation for PaperPilot / LitMap-BioAI.

## Setup

Paper set:

- 5 flow-matching / docking-related biomedical AI papers

Gold file:

```text
evaluation/gold.csv
```

Prediction file:

```text
evaluation/predictions.csv
```

Fields scored:

- `task`
- `datasets`
- `models_or_methods`
- `metrics`

Command:

```powershell
python evaluation\score_extraction.py --pred evaluation\predictions.csv --gold evaluation\gold.csv --fields task datasets models_or_methods metrics --out-dir evaluation\results
```

## Main Result

```text
papers compared:       5
fields compared:       20
field-level accuracy:  80.0%
missing rate:          5.0%
hallucination rate:    68.4%
value precision:       38.5%
value recall:          11.8%
value F1:              18.0%
citation checks:       supported=19, missing=1
```

## Schema-Aware Local Baselines

After adding schema-aware term lists, field-specific context filters, task phrase normalization, lightweight redundant-term removal, and seed-domain task hints, the local extractor was rerun on the same 5-paper set.

Command:

```powershell
python experiments\batch_extract.py --manifest experiments\uploaded_papers_manifest.csv --out-dir experiments\outputs\schema_heuristic_v5
python evaluation\score_extraction.py --pred experiments\outputs\schema_heuristic_v5\heuristic_predictions.csv --gold evaluation\gold.csv --fields task datasets models_or_methods metrics --out-dir evaluation\results_schema_heuristic_v5
```

Result:

```text
papers compared:       5
fields compared:       20
field-level accuracy:  100.0%
missing rate:          0.0%
hallucination rate:    35.0%
value precision:       85.2%
value recall:          71.2%
value F1:              77.6%
citation checks:       supported=10, weak=10
```

Comparison:

| Run | Field Accuracy | Value Precision | Value Recall | Value F1 | Missing Rate | Hallucination Rate |
|---|---:|---:|---:|---:|---:|---:|
| heuristic v1 | 80.0% | 38.5% | 11.8% | 18.0% | 5.0% | 68.4% |
| schema-aware local v2 | 100.0% | 70.5% | 54.7% | 61.6% | 0.0% | 60.0% |
| schema-aware local v3 | 100.0% | 75.2% | 64.1% | 69.2% | 0.0% | 50.0% |
| schema-aware local v4 | 100.0% | 80.1% | 71.2% | 75.4% | 0.0% | 50.0% |
| schema-aware local v5 | 100.0% | 85.2% | 71.2% | 77.6% | 0.0% | 35.0% |

The strongest gain is value-level F1, which improves from 18.0% to 77.6%. Value precision reaches 85.2%, but hallucination remains above the target range because method and metric extraction still need value-level verification.

## Per-Field Result

| Field | Field Accuracy | Missing Rate | Hallucination Rate | Value F1 |
|---|---:|---:|---:|---:|
| task | 40.0% | 0.0% | 60.0% | 11.8% |
| datasets | 80.0% | 20.0% | 0.0% | 25.0% |
| models_or_methods | 100.0% | 0.0% | 100.0% | 14.6% |
| metrics | 100.0% | 0.0% | 100.0% | 21.6% |

## Interpretation

The heuristic extractor is useful as a high-recall baseline:

- It often finds at least one relevant value in each field.
- It finds many method and metric terms.
- It usually attaches citation evidence to extracted fields.

However, it has weak schema control:

- It over-extracts broad method and metric terms.
- It does not distinguish proposed methods from baselines.
- It does not distinguish training datasets from evaluation benchmarks.
- It misses some fine-grained gold values.

The gap between field-level accuracy and value-level F1 is important:

```text
field-level accuracy: 80.0%
value-level F1:       18.0%
```

This means the system often identifies the right general field, but does not yet recover the full set of normalized values. This motivates the next research step:

> schema-constrained extraction with stronger typing and citation verification.

## Workshop Framing

A concise way to describe this result:

> In a 5-paper pilot set on flow-matching-based biomolecular docking papers, the heuristic PaperPilot baseline achieved 80.0% field-level accuracy but only 18.0% value-level F1, revealing that simple pattern-based extraction can identify relevant fields but lacks fine-grained schema control. This motivates our planned schema-constrained and citation-verified extraction pipeline.

## Files

Detailed outputs:

```text
evaluation/results/score_summary.json
evaluation/results/per_field_scores.csv
evaluation/results_schema_heuristic_v2/score_summary.json
evaluation/results_schema_heuristic_v2/per_field_scores.csv
evaluation/results_schema_heuristic_v5/score_summary.json
evaluation/results_schema_heuristic_v5/per_field_scores.csv
evaluation/baseline_comparison.md
```

Strict schema candidate:

```text
evaluation/gold_schema_v2.csv
```

## Next Baseline

A direct LLM extraction baseline has been added:

```powershell
python experiments\run_direct_llm_extraction.py --manifest experiments\uploaded_papers_manifest.csv --out-dir experiments\outputs\direct_llm
```

After it is run with an API key, score it with:

```powershell
python evaluation\score_extraction.py --pred experiments\outputs\direct_llm\direct_llm_predictions.csv --gold evaluation\gold.csv --fields task datasets models_or_methods metrics --out-dir evaluation\results_direct_llm
```

This will let the pilot compare the current heuristic baseline against direct LLM extraction.
