# Error Analysis

Prediction file: `experiments\outputs\schema_heuristic_v4\heuristic_predictions.csv`
Gold file: `evaluation\gold.csv`

## NeuralPLexer3: Accurate Biomolecular Complex Structure Prediction with Flow Models

### task

Unsupported predictions:
- generalized biomolecular complex structure prediction

### datasets

Missed gold values:
- recent PDB bioassemblies / low-homology post-2023 PDB evaluation set

### models_or_methods

Missed gold values:
- continuous normalizing flow
- flow-based encoder-decoder structure prediction model
- informative globular polymer prior
- Langevin dynamics prior relaxation

### metrics

Unsupported predictions:
- number of sampling steps / convergence speed
- pocket all-atom RMSD
- PoseBusters pass rate / physical validity
- sequence recovery
- GPU memory

Missed gold values:
- ligand stereochemistry accuracy
- LDDT
- TM-score
- pLDDT
- pDockQ
- bb_LDDT

## FlowDock: Geometric Flow Matching for Generative Protein-Ligand Docking and Affinity Prediction

### task

Unsupported predictions:
- flexible protein-ligand docking
- pocket-based flexible docking
- binding pose prediction

### datasets

Unsupported predictions:
- PoseBusters

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- generative flow matching model
- continuous normalizing flow
- harmonic prior

Missed gold values:
- hybrid structure-and-affinity prediction model
- apo-to-holo structure generation
- fine-tuned NeuralPLexer architecture
- VD-ODE sampler
- binding affinity head

### metrics

Missed gold values:
- binding pocket conformation RMSD
- Pearson correlation
- Spearman correlation
- CASP16 affinity-ranking position

## Harmonic Self-Conditioned Flow Matching for joint Multi-Ligand Docking and Binding Site Design

### task

Unsupported predictions:
- pocket-level protein-ligand docking
- pocket-based flexible docking
- binding pose prediction

### datasets

Missed gold values:
- PDBBind time split
- Binding MOAD

### models_or_methods

Unsupported predictions:
- conditional flow matching
- Riemannian flow matching

Missed gold values:
- harmonic self-conditioned flow matching
- joint discrete-continuous flow
- fake-ligand data augmentation
- invariant graph attention network

### metrics

Unsupported predictions:
- inference time
- Dice

Missed gold values:
- RMSD
- fraction of predictions with RMSD < 2 Å
- fraction of predictions with RMSD < 5 Å

## Composing Unbalanced Flows for Flexible Docking and Relaxation

### task

Unsupported predictions:
- molecular docking

### datasets

Missed gold values:
- PDBBind

### models_or_methods

Unsupported predictions:
- continuous normalizing flow
- conditional flow matching

Missed gold values:
- Unbalanced Flow Matching
- manifold docking flow / manifold Unbalanced FM
- Euclidean relaxation flow / structure relaxation Unbalanced FM
- SE(3) and side-chain torsion flow

### metrics

Unsupported predictions:
- PoseBusters validity
- inference time
- RMSD < 2 Å success rate

Missed gold values:
- ligand RMSD
- median ligand RMSD
- percentage of all-atom RMSD < 1 Å
- PB-valid

## ForceFM: Enhancing Protein-Ligand Predictions through Force-Guided Flow Matching

### task

Unsupported predictions:
- physically plausible ligand pose generation

### datasets

Missed gold values:
- PDBBind

### models_or_methods

Unsupported predictions:
- conditional flow matching
- force-guidance network

Missed gold values:
- energy-guided generation
- Vina-guided generation
- Glide-guided generation
- Gnina-guided generation
- RDKit ETKDG conformer initialization

### metrics

Missed gold values:
- RMSD ≤ 2 Å success rate
- RMSD percentiles
- centroid distance
- mean centroid distance
- centroid distance ≤ 2 Å
