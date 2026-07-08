# Batch 1 Annotation Review

## Summary

- Candidate rows: 19
- Included in benchmark: 18
- Excluded from benchmark: 1
- Rows needing final PDF check: 0

## Output Files

- Cleaned candidate gold: `evaluation\gold_batch1_candidate_cleaned.csv`
- Source copy: `evaluation\flow_matching_candidate_annotations_batch1_verified_v2.csv`

## Benchmark Scope

This batch is broader than the original 5-paper flow-matching docking seed set. It contains flow-matching models, non-flow docking baselines, dataset/evaluation resources, and docking validation suites.

Recommended framing:

> Batch 1 evaluates a broader flow-matching and biomolecular-structure literature set, including docking, protein generation, molecule generation, dataset resources, and non-flow baseline systems.

Do not describe this batch as only protein-ligand flow matching docking papers.

## Included Paper Types

- benchmark plus docking generalization method: 1
- dataset / evaluation resource: 1
- docking evaluation / validation suite paper: 1
- flow matching conditional protein design model: 1
- flow matching conditional protein generation model: 1
- flow matching ligand-binding protein design model: 1
- flow matching molecule generation model: 2
- flow matching pocket-conditioned ligand generation model: 1
- flow matching protein generation model: 2
- flow matching protein pocket generation model: 1
- non-flow biomolecular interaction prediction model: 1
- non-flow docking baseline / model paper: 2
- non-flow docking/affinity model paper: 1
- non-flow flexible docking baseline / model paper: 1
- non-flow flexible docking model paper: 1

## Excluded Rows

- paper_017: PoseBench: Benchmarking the Robustness of Pose Estimation Models under Corruptions (excluded; computer vision pose-estimation benchmark)

## Rows Needing PDF Check

- None

## Recommended Fixes Applied

- Kept the original candidate file unchanged.
- Created a cleaned candidate gold file using ` | ` as the value separator.
- Removed the excluded computer-vision PoseBench row from the cleaned gold file.
- Added `folder`, `paper_type`, `verification_status`, and `needs_pdf_check` metadata columns.
- Preserved `review_notes` so uncertain annotation decisions remain auditable.
- PDF-checked `paper_015` and `paper_022`, then applied targeted dataset/metric corrections.

## PDF Requirement

PDFs are not required for schema-level cleanup. PDFs are required before treating this as final gold, especially for rows marked `needs_pdf_check=yes`.
