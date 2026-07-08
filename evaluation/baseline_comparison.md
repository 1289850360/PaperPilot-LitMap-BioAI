# Baseline Comparison

| Run | Papers | Fields | Field accuracy | Value precision | Value recall | Value F1 | Missing rate | Hallucination rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| heuristic_v1 | 5 | 20 | 80.0% | 38.5% | 11.8% | 18.0% | 5.0% | 68.4% |
| schema_v2 | 5 | 20 | 100.0% | 70.5% | 54.7% | 61.6% | 0.0% | 60.0% |
| schema_v3 | 5 | 20 | 100.0% | 75.2% | 64.1% | 69.2% | 0.0% | 50.0% |
| schema_v4 | 5 | 20 | 100.0% | 80.1% | 71.2% | 75.4% | 0.0% | 50.0% |
| schema_v5 | 5 | 20 | 100.0% | 85.2% | 71.2% | 77.6% | 0.0% | 35.0% |

## Source Files

- heuristic_v1: `evaluation\results\score_summary.json`
- schema_v2: `evaluation\results_schema_heuristic_v2\score_summary.json`
- schema_v3: `evaluation\results_schema_heuristic_v3\score_summary.json`
- schema_v4: `evaluation\results_schema_heuristic_v4\score_summary.json`
- schema_v5: `evaluation\results_schema_heuristic_v5\score_summary.json`

## Notes

- Higher field accuracy, value precision, value recall, and value F1 are better.
- Lower missing rate and hallucination rate are better.
- Direct LLM citation status is expected to be `unknown` unless a verifier is added.
