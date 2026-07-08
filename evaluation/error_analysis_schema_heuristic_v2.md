# Error Analysis

Prediction file: `experiments\outputs\schema_heuristic_v2\heuristic_predictions.csv`
Gold file: `evaluation\gold.csv`

## NeuralPLexer3: Accurate Biomolecular Complex Structure Prediction with Flow Models

### task

Missed gold values:
- protein-ligand complex structure prediction
- biomolecular interaction structure prediction
- ligand-induced conformational change prediction
- confidence estimation for predicted biomolecular complexes

### datasets

Unsupported predictions:
- PoseBusters Benchmark

Missed gold values:
- recent PDB bioassemblies / low-homology post-2023 PDB evaluation set

### models_or_methods

Unsupported predictions:
- conditional flow matching
- graph neural network
- NeuralPLexer3
- DiffDock

Missed gold values:
- continuous normalizing flow
- flow-based encoder-decoder structure prediction model
- informative globular polymer prior
- confidence module

### metrics

Unsupported predictions:
- sequence recovery
- sampling steps
- GPU memory
- runtime

Missed gold values:
- ligand stereochemistry accuracy
- LDDT
- ConfBench score
- pocket_fident
- bb_LDDT

## FlowDock: Geometric Flow Matching for Generative Protein-Ligand Docking and Affinity Prediction

### task

Unsupported predictions:
- flexible protein-ligand docking
- binding pose prediction

Missed gold values:
- apo-to-holo protein-ligand structure generation

### datasets

Unsupported predictions:
- PoseBusters Benchmark

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- self-conditioned flow matching
- generative flow matching model
- continuous normalizing flow
- Unbalanced Flow Matching
- optimal transport

Missed gold values:
- FlowDock
- deep geometric generative model
- hybrid structure-and-affinity prediction model
- apo-to-holo structure generation
- ESMFold protein prior
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
- protein pocket residue design for small-molecule binding
- joint residue-type and ligand-pose generation

### datasets

Missed gold values:
- PDBBind version 2020
- PDBBind time split
- Binding MOAD

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- conditional flow matching
- Riemannian flow matching
- graph neural network
- optimal transport

Missed gold values:
- harmonic prior
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

Missed gold values:
- flexible protein-ligand docking
- pocket-based flexible docking
- apo-to-holo conformational change modeling
- generation of energetically favorable / physically valid docking poses

### datasets

Unsupported predictions:
- PoseBusters Benchmark

Missed gold values:
- PDBBind

### models_or_methods

Unsupported predictions:
- continuous normalizing flow
- conditional flow matching
- optimal transport
- DiffDock
- ESMFold

Missed gold values:
- manifold docking flow / manifold Unbalanced FM
- Euclidean relaxation flow / structure relaxation Unbalanced FM
- confidence discriminator
- energy-based loss
- flat-bottom potential
- energy filtering
- SE(3) and side-chain torsion flow

### metrics

Unsupported predictions:
- PoseBusters validity
- inference time

Missed gold values:
- ligand RMSD
- pocket all-atom RMSD / AA-RMSD
- percentage of all-atom RMSD < 1 Å
- PoseBusters checks
- PB-valid
- proportion of energetically favorable poses

## ForceFM: Enhancing Protein-Ligand Predictions through Force-Guided Flow Matching

### task

Missed gold values:
- molecular docking
- low-energy ligand pose generation
- blind self-docking
- cross-domain docking generalization evaluation

### datasets

Missed gold values:
- PDBBind

### models_or_methods

Unsupported predictions:
- conditional flow matching
- Riemannian flow matching
- optimal transport
- DiffDock

Missed gold values:
- force-guidance network / force model
- energy-guided generation
- Vina-guided generation
- Glide-guided generation
- Gnina-guided generation
- RDKit ETKDG conformer initialization

### metrics

Missed gold values:
- mean RMSD
- RMSD ≤ 2 Å success rate
- RMSD percentiles
- centroid distance
- mean centroid distance
- centroid distance ≤ 2 Å
- PoseBusters pass rate / physical validity
- inference cost
