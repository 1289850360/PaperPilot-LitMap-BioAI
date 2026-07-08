# Baseline Comparison

| Run | Papers | Fields | Field accuracy | Value precision | Value recall | Value F1 | Missing rate | Hallucination rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| original_gold | 23 | 92 | 91.8% | 58.8% | 54.2% | 56.4% | 1.1% | 74.7% |
| auto_refined_v1 | 23 | 92 | 92.9% | 80.0% | 61.5% | 69.6% | 1.1% | 53.8% |
| curated_v2 | 23 | 92 | 96.2% | 85.0% | 62.9% | 72.3% | 1.1% | 41.8% |

## Source Files

- original_gold: `evaluation\results_benchmark_23_schema_v7_verified\score_summary.json`
- auto_refined_v1: `evaluation\results_benchmark_23_schema_v7_verified_auto_refined_gold_v1\score_summary.json`
- curated_v2: `evaluation\results_benchmark_23_schema_v7_verified_curated_gold_v2\score_summary.json`

## Notes

- Higher field accuracy, value precision, value recall, and value F1 are better.
- Lower missing rate and hallucination rate are better.
- Direct LLM citation status is expected to be `unknown` unless a verifier is added.
