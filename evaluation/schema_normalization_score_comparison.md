# Baseline Comparison

| Run | Papers | Fields | Field accuracy | Value precision | Value recall | Value F1 | Missing rate | Hallucination rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| curated_v2_raw | 23 | 92 | 96.2% | 85.0% | 62.9% | 72.3% | 1.1% | 41.8% |
| curated_v2_normalized | 23 | 92 | 96.2% | 85.5% | 64.2% | 73.3% | 1.1% | 42.9% |

## Source Files

- curated_v2_raw: `evaluation\results_benchmark_23_schema_v7_verified_curated_gold_v2\score_summary.json`
- curated_v2_normalized: `evaluation\results_benchmark_23_schema_v7_verified_curated_gold_v2_normalized\score_summary.json`

## Notes

- Higher field accuracy, value precision, value recall, and value F1 are better.
- Lower missing rate and hallucination rate are better.
- Direct LLM citation status is expected to be `unknown` unless a verifier is added.
