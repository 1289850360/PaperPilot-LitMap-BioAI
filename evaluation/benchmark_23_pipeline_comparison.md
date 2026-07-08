# Baseline Comparison

| Run | Papers | Fields | Field accuracy | Value precision | Value recall | Value F1 | Missing rate | Hallucination rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| schema_v5 | 23 | 92 | 66.3% | 60.5% | 33.1% | 42.8% | 12.0% | 70.4% |
| schema_v5_verified | 23 | 92 | 66.3% | 63.8% | 32.4% | 43.0% | 14.1% | 68.4% |
| schema_v6 | 23 | 92 | 92.4% | 50.6% | 55.2% | 52.8% | 0.0% | 79.3% |
| schema_v6_verified | 23 | 92 | 91.8% | 53.5% | 54.0% | 53.7% | 1.1% | 75.8% |
| schema_v7 | 23 | 92 | 92.4% | 55.5% | 55.4% | 55.4% | 0.0% | 78.3% |
| schema_v7_verified | 23 | 92 | 91.8% | 58.8% | 54.2% | 56.4% | 1.1% | 74.7% |

## Source Files

- schema_v5: `evaluation\results_benchmark_23_schema_v5\score_summary.json`
- schema_v5_verified: `evaluation\results_benchmark_23_schema_v5_verified\score_summary.json`
- schema_v6: `evaluation\results_benchmark_23_schema_v6\score_summary.json`
- schema_v6_verified: `evaluation\results_benchmark_23_schema_v6_verified\score_summary.json`
- schema_v7: `evaluation\results_benchmark_23_schema_v7\score_summary.json`
- schema_v7_verified: `evaluation\results_benchmark_23_schema_v7_verified\score_summary.json`

## Notes

- Higher field accuracy, value precision, value recall, and value F1 are better.
- Lower missing rate and hallucination rate are better.
- Direct LLM citation status is expected to be `unknown` unless a verifier is added.
