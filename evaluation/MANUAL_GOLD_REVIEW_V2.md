# Manual Gold Review v2

This pass manually reviews only `task` and `models_or_methods` values that were previously marked as `review`.

## Inputs

- Starting gold: `evaluation\gold_23_paper_benchmark_auto_refined_v1.csv`
- Review queue: `evaluation\gold_refinement_candidates_v1.csv`

## Outputs

- Revised gold v2: `evaluation\gold_23_paper_benchmark_curated_v2.csv`
- Decision log: `evaluation\manual_gold_review_v2_decisions.csv`

## Summary

| Manual decision | Count |
|---|---:|
| accept | 27 |
| reject | 39 |

## Acceptance Policy

- Accept task values when they describe the paper's main research problem or an explicitly claimed capability.
- Accept method values when they are part of the paper's own model, training objective, or core pipeline.
- Reject baseline names, datasets, metrics, related-work citations, bibliography hits, journal metadata, and overly broad field labels.

## Accepted Values

| Paper | Field | Value |
|---|---|---|
| paper_002 | models_or_methods | continuous normalizing flow |
| paper_005 | models_or_methods | conditional flow matching |
| paper_007 | task | protein-ligand binding pose prediction |
| paper_007 | task | direct-shot molecular docking |
| paper_007 | task | rigid receptor blind docking |
| paper_008 | task | confidence-ranked ligand pose generation |
| paper_010 | task | protein structure generation |
| paper_010 | models_or_methods | conditional flow matching |
| paper_012 | task | functional protein design |
| paper_013 | task | protein-ligand docking generalization |
| paper_013 | task | confidence-guided molecular docking |
| paper_014 | task | atom-and-bond generation |
| paper_014 | task | flow matching for molecule generation |
| paper_015 | task | inverse folding |
| paper_016 | task | molecular graph and geometry generation |
| paper_016 | task | flow matching for molecule generation |
| paper_016 | models_or_methods | conditional flow matching |
| paper_018 | task | protein-ligand complex generation |
| paper_018 | task | ligand conformation and protein backbone generation |
| paper_018 | models_or_methods | Riemannian flow matching |
| paper_019 | task | pocket-conditioned ligand generation |
| paper_019 | task | protein-ligand interaction-guided molecule generation |
| paper_019 | models_or_methods | self-conditioning |
| paper_020 | task | pocket-conditioned molecule design |
| paper_020 | models_or_methods | fragment-based ligand generation |
| paper_021 | task | physical validity assessment for generated ligand poses |
| paper_024 | models_or_methods | confidence head |
