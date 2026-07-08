# Error Analysis

Prediction file: `experiments\outputs\schema_heuristic_v3\heuristic_predictions.csv`
Gold file: `evaluation\gold.csv`

## NeuralPLexer3: Accurate Biomolecular Complex Structure Prediction with Flow Models

### task

Unsupported predictions:
- generalized biomolecular complex structure prediction

Missed gold values:
- protein-ligand complex structure prediction
- confidence estimation for predicted biomolecular complexes

### datasets

Missed gold values:
- recent PDB bioassemblies / low-homology post-2023 PDB evaluation set

### models_or_methods

Unsupported predictions:
- conditional flow matching

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
- joint residue-type and ligand-pose generation
- blind self-docking
- cross-domain docking generalization evaluation
- confidence estimation for predicted biomolecular complexes

Missed gold values:
- apo-to-holo protein-ligand structure generation

### datasets

Unsupported predictions:
- PoseBusters

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- self-conditioned flow matching
- generative flow matching model
- continuous normalizing flow
- harmonic prior

Missed gold values:
- FlowDock
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
- binding pose prediction

Missed gold values:
- multi-ligand docking
- 3D protein-ligand binding structure generation
- joint residue-type and ligand-pose generation

### datasets

Missed gold values:
- PDBBind time split
- Binding MOAD

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- conditional flow matching
- Riemannian flow matching

Missed gold values:
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
- cross-domain docking generalization evaluation

Missed gold values:
- flexible protein-ligand docking
- pocket-based flexible docking
- apo-to-holo conformational change modeling
- generation of energetically favorable / physically valid docking poses

### datasets

Missed gold values:
- PDBBind

### models_or_methods

Unsupported predictions:
- continuous normalizing flow
- conditional flow matching

Missed gold values:
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

Missed gold values:
- molecular docking
- blind self-docking
- cross-domain docking generalization evaluation

### datasets

Missed gold values:
- PDBBind

### models_or_methods

Unsupported predictions:
- conditional flow matching
- Riemannian flow matching
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
