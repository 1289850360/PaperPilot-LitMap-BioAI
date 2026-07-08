# Baseline Comparison

| Run | Papers | Fields | Field accuracy | Value precision | Value recall | Value F1 | Missing rate | Hallucination rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| seed_5_schema_v5 | 5 | 20 | 100.0% | 85.2% | 71.2% | 77.6% | 0.0% | 35.0% |
| benchmark_23_schema_v5 | 23 | 92 | 66.3% | 60.5% | 33.1% | 42.8% | 12.0% | 70.4% |

## Source Files

- seed_5_schema_v5: `evaluation\results_schema_heuristic_v5\score_summary.json`
- benchmark_23_schema_v5: `evaluation\results_benchmark_23_schema_v5\score_summary.json`

## Notes

- Higher field accuracy, value precision, value recall, and value F1 are better.
- Lower missing rate and hallucination rate are better.
- Direct LLM citation status is expected to be `unknown` unless a verifier is added.
