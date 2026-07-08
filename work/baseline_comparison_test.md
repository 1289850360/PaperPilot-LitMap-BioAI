# Baseline Comparison

| Run | Papers | Fields | Field accuracy | Value precision | Value recall | Value F1 | Missing rate | Hallucination rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| heuristic | 5 | 20 | 80.0% | 38.5% | 11.8% | 18.0% | 5.0% | 68.4% |

## Source Files

- heuristic: `evaluation\results\score_summary.json`

## Notes

- Higher field accuracy, value precision, value recall, and value F1 are better.
- Lower missing rate and hallucination rate are better.
- Direct LLM citation status is expected to be `unknown` unless a verifier is added.
