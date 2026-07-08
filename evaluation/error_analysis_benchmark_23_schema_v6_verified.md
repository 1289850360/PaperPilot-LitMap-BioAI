# Error Analysis

Prediction file: `experiments\outputs\benchmark_23_schema_v6_verified\verified_predictions.csv`
Gold file: `evaluation\gold_23_paper_benchmark.csv`

## NeuralPLexer3: Accurate Biomolecular Complex Structure Prediction with Flow Models

### datasets

Missed gold values:
- PoseBusters-V2
- recent PDB bioassemblies / low-homology post-2023 PDB evaluation set

### models_or_methods

Unsupported predictions:
- AlphaFold 3
- PoseBusters
- DynamicBind
- AlphaFold3
- pairformer
- TANKBind
- DiffDock
- EquiBind
- PLINDER

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
- binding affinity
- steric clashes
- GPU memory
- runtime

Missed gold values:
- ligand stereochemistry accuracy
- LDDT

## FlowDock: Geometric Flow Matching for Generative Protein-Ligand Docking and Affinity Prediction

### datasets

Unsupported predictions:
- PoseBusters

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- generative flow matching model
- continuous normalizing flow
- equivariant flow matching
- harmonic prior
- AlphaFold 3
- PoseBusters
- DynamicBind
- TANKBind
- DiffDock
- EquiBind

Missed gold values:
- FlowDock
- hybrid structure-and-affinity prediction model
- apo-to-holo structure generation
- fine-tuned NeuralPLexer architecture
- VD-ODE sampler
- binding affinity head

### metrics

Unsupported predictions:
- binding affinity
- pocket RMSD

Missed gold values:
- binding pocket conformation RMSD
- Pearson correlation
- Spearman correlation
- CASP16 affinity-ranking position

## Harmonic Self-Conditioned Flow Matching for joint Multi-Ligand Docking and Binding Site Design

### datasets

Missed gold values:
- PDBBind time split
- Binding MOAD

### models_or_methods

Unsupported predictions:
- conditional flow matching
- Riemannian flow matching
- self-conditioning
- TANKBind
- DiffDock
- EquiBind

Missed gold values:
- harmonic self-conditioned flow matching
- joint discrete-continuous flow
- fake-ligand data augmentation
- invariant graph attention network

### metrics

Unsupported predictions:
- binding affinity
- inference time

Missed gold values:
- RMSD
- fraction of predictions with RMSD < 2 Å
- fraction of predictions with RMSD < 5 Å

## Composing Unbalanced Flows for Flexible Docking and Relaxation

### datasets

Missed gold values:
- PDBBind

### models_or_methods

Unsupported predictions:
- continuous normalizing flow
- conditional flow matching
- AlphaFold 3
- PoseBusters
- DynamicBind
- AlphaFold3
- DiffDock
- EquiBind

Missed gold values:
- Unbalanced Flow Matching
- manifold docking flow / manifold Unbalanced FM
- Euclidean relaxation flow / structure relaxation Unbalanced FM
- energy-based loss
- energy filtering
- SE(3) and side-chain torsion flow

### metrics

Unsupported predictions:
- intramolecular validity
- bond length validity
- PoseBusters validity
- bond angle validity
- chemical validity
- steric clashes
- diversity

Missed gold values:
- ligand RMSD
- median ligand RMSD
- percentage of all-atom RMSD < 1 Å
- PB-valid

## ForceFM: Enhancing Protein-Ligand Predictions through Force-Guided Flow Matching

### datasets

Missed gold values:
- PDBBind

### models_or_methods

Unsupported predictions:
- conditional flow matching
- force-guidance network
- PoseBusters
- DiffDock
- EquiBind
- DockGen

Missed gold values:
- energy-guided generation
- Vina-guided generation
- Glide-guided generation
- Gnina-guided generation
- RDKit ETKDG conformer initialization

### metrics

Unsupported predictions:
- steric clashes
- Vina score

Missed gold values:
- RMSD ≤ 2 Å success rate
- RMSD percentiles
- centroid distance
- mean centroid distance
- centroid distance ≤ 2 Å

## PLINDER: The protein-ligand interactions dataset and evaluation resource

### task

Unsupported predictions:
- protein-ligand binding pose prediction
- confidence-ranked ligand pose generation

Missed gold values:
- protein-ligand interaction dataset curation
- leakage-controlled train/test split construction
- protein-ligand docking generalization evaluation

### datasets

Missed gold values:
- PLINDER

### models_or_methods

Unsupported predictions:
- PoseBusters
- AlphaFold3
- DiffDock
- EquiBind
- DockGen

Missed gold values:
- leakage-minimizing split generation
- protein/pocket/interaction/ligand-level similarity annotation
- paired apo and predicted structure annotation

### metrics

Unsupported predictions:
- PoseBusters checks
- inference time
- clash score
- diversity
- Lipinski
- LDDT
- MAE

Missed gold values:
- protein/pocket/interaction/ligand similarity metrics
- leakage / train-test similarity

## EquiBind: Geometric Deep Learning for Drug Binding Structure Prediction

### task

Unsupported predictions:
- protein-ligand binding pose prediction
- direct-shot molecular docking
- rigid receptor blind docking

Missed gold values:
- drug-protein binding structure prediction
- blind protein-ligand docking
- receptor binding-location prediction
- ligand bound-pose and orientation prediction
- ligand torsion refinement

### datasets

Missed gold values:
- PDBBind time split
- PDBBind 2019 test set

### models_or_methods

Missed gold values:
- direct-shot binding pose prediction
- keypoint-based rigid alignment
- von Mises torsion-angle conformer fitting

### metrics

Unsupported predictions:
- inference time

Missed gold values:
- percentage of predictions below 2 Å
- percentage of predictions below 5 Å
- RMSD percentiles

## DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking

### task

Unsupported predictions:
- confidence-ranked ligand pose generation

Missed gold values:
- blind docking
- generative modeling of ligand poses
- confidence estimation for docking poses

### datasets

Missed gold values:
- PDBBind
- computationally folded protein structure evaluation setting

### models_or_methods

Unsupported predictions:
- TANKBind
- EquiBind

Missed gold values:
- diffusion generative model over ligand poses
- diffusion on translational, rotational and torsional degrees of freedom
- non-Euclidean manifold diffusion
- confidence model for pose ranking

### metrics

Unsupported predictions:
- steric clashes
- success rate
- pocket RMSD
- GPU memory
- mean RMSD
- runtime
- pLDDT
- Dice

Missed gold values:
- percentage of predictions below 2 Å
- percentage of predictions below 5 Å
- RMSD percentiles

## SE(3) Stochastic Flow Matching for Protein Backbone Generation / FoldFlow

### task

Unsupported predictions:
- simulation-free generative modeling on SE(3)

Missed gold values:
- de novo protein structure generation
- unconditional protein backbone design
- generative modeling over SE(3)
- equilibrium conformation generation

### datasets

Missed gold values:
- PDB subset / PDB-derived 22,248-protein training set
- BPTI molecular-dynamics trajectory evaluation set

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- continuous normalizing flow
- Invariant Point Attention
- equivariant flow matching
- conditional flow matching
- Riemannian flow matching
- FrameFlow

Missed gold values:
- FoldFlow
- simulation-free continuous-time dynamics
- stochastic continuous-time dynamics over SE(3)

### metrics

Unsupported predictions:
- average pairwise TM-score
- self-consistency
- connectedness
- max TM-score

Missed gold values:
- scRMSD
- iterations per second

## FrameFlow: Fast Protein Backbone Generation with SE(3) Flow Matching

### task

Unsupported predictions:
- protein structure generation
- SE(3)-equivariant flow matching for proteins

Missed gold values:
- de novo protein design
- fast protein backbone sampling
- SE(3)-frame generation

### models_or_methods

Unsupported predictions:
- equivariant flow matching
- conditional flow matching
- Riemannian flow matching
- FoldFlow

Missed gold values:
- SE(3) flow matching
- FrameDiff adaptation to flow matching
- SE(3) inference scheduler

### metrics

Unsupported predictions:
- structural clusters
- novelty

## DiffBindFR: An SE(3) Equivariant Network for Flexible Protein-Ligand Docking

### task

Missed gold values:
- full-atom protein-ligand binding-structure prediction
- apo and AlphaFold2-structure-based docking

### datasets

Missed gold values:
- PDBBind time split
- Apo dataset
- AlphaFold2 modeled structures

### models_or_methods

Unsupported predictions:
- PoseBusters
- TANKBind
- DiffDock
- EquiBind

Missed gold values:
- SE(3)-equivariant network
- product-space diffusion over ligand rotation/translation/torsion and pocket side-chain torsions
- MDN scoring model

### metrics

Unsupported predictions:
- PoseBusters pass rate / physical validity
- success rate
- pocket RMSD
- PB-valid

Missed gold values:
- centroid distance
- RMSD < 5 Å
- pocket side-chain RMSD
- PoseBusters validity
- steric clashes / physical plausibility
- runtime

## Improved Motif-Scaffolding with SE(3) Flow Matching

### task

Unsupported predictions:
- functional protein design

Missed gold values:
- functional motif-conditioned protein design
- scaffold diversity improvement

### datasets

Unsupported predictions:
- Structural Antibody Database

Missed gold values:
- benchmark of 24 biologically meaningful motifs
- PDB monomer training set

### models_or_methods

Unsupported predictions:
- equivariant flow matching
- Riemannian flow matching
- FoldFlow

Missed gold values:
- SE(3) flow matching
- conditional score estimation

### metrics

Unsupported predictions:
- average pairwise TM-score
- structural clusters
- inference time
- success rate
- novelty

Missed gold values:
- number of unique designable motif-scaffolds
- self-consistency RMSD / scRMSD
- TM-score-based clustering
- sampling speed

## Deep Confident Steps to New Pockets: Strategies for Docking Generalization / DockGen

### task

Unsupported predictions:
- protein-ligand docking generalization
- confidence-guided molecular docking

Missed gold values:
- blind docking generalization assessment
- protein binding-pocket benchmark construction
- docking to unseen protein classes
- confidence bootstrapping for diffusion docking

### datasets

Unsupported predictions:
- PoseBusters
- BindingDB
- ImageNet

Missed gold values:
- PDBBind
- DockGen benchmark

### models_or_methods

Unsupported predictions:
- PoseBusters
- TANKBind
- EquiBind

Missed gold values:
- synthetic data strategy

### metrics

Unsupported predictions:
- number of parameters
- diversity
- runtime

Missed gold values:
- ligand RMSD
- BLOSUM62 similarity
- train-test leakage / contamination
- generalization performance

## FlowMol: Mixed Continuous and Categorical Flow Matching for 3D De Novo Molecule Generation

### task

Unsupported predictions:
- atom-and-bond generation
- flow matching for molecule generation

Missed gold values:
- 3D de novo molecule generation
- joint generation of atom positions and atom/bond categorical variables
- unconditional molecular generation

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- equivariant flow matching
- conditional flow matching
- Riemannian flow matching

Missed gold values:
- probability-simplex categorical flow
- GVP-based molecular generator
- flow matching with explicit hydrogens and formal charges

### metrics

Unsupported predictions:
- validity

## FoldFlow-2: Sequence-Augmented SE(3)-Flow Matching for Conditional Protein Backbone Generation

### task

Unsupported predictions:
- inverse folding

Missed gold values:
- conditional protein structure generation
- equilibrium conformation sampling
- motif/scaffold conditional protein design

### datasets

Missed gold values:
- PDB
- filtered AlphaFold2 synthetic structures from SwissProt
- ATLAS molecular-dynamics trajectory evaluation set
- 24 single-chain motif scaffolding benchmark

### models_or_methods

Unsupported predictions:
- continuous normalizing flow
- Invariant Point Attention
- equivariant flow matching
- Riemannian flow matching
- FrameFlow
- pLDDT

Missed gold values:
- protein language model conditioning
- geometric transformer decoder

### metrics

Unsupported predictions:
- average pairwise TM-score
- self-consistency RMSD
- inference time
- motif RMSD

Missed gold values:
- scRMSD
- secondary-structure diversity
- number of solved motif scaffolds
- pairwise RMSD Pearson correlation
- global RMSF Pearson correlation
- PCA W2 distance
- time per sample

## SemlaFlow: Efficient 3D Molecular Generation with Latent Attention and Equivariant Flow Matching

### task

Unsupported predictions:
- molecular graph and geometry generation
- flow matching for molecule generation

Missed gold values:
- joint molecular graph and 3D conformation generation
- efficient molecular sampling

### datasets

Unsupported predictions:
- PoseBusters

Missed gold values:
- GEOM-Drugs

### models_or_methods

Unsupported predictions:
- mixed continuous and categorical flow matching
- harmonic self-conditioned flow matching
- conditional flow matching
- self-conditioning
- PoseBusters
- FrameFlow
- FoldFlow
- FlowMol

Missed gold values:
- Semla
- joint generation of atom types, coordinates, bond types and formal charges

### metrics

Unsupported predictions:
- inference time
- sampling steps
- strain energy
- GPU memory

Missed gold values:
- connectedness
- distributional benchmark metrics

## AtomFlow: Design of Ligand-Binding Proteins with Atomic Flow Matching

### task

Unsupported predictions:
- protein-ligand complex generation
- ligand conformation and protein backbone generation

Missed gold values:
- ligand-binding protein design
- protein backbone generation conditioned on a target molecule
- ligand conformation generation
- joint ligand-protein structure generation from a 2D molecular graph

### datasets

Unsupported predictions:
- PoseBusters

Missed gold values:
- RFDiffusionAA selected ligand evaluation set (FAD, SAM, IAI, OQO)
- extended ligand set

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- Invariant Point Attention
- equivariant flow matching
- conditional flow matching
- Riemannian flow matching
- AlphaFold 3
- PoseBusters
- FrameFlow

Missed gold values:
- SE(3)-equivariant structure prediction network
- iterative ligand conformation and protein backbone generation

### metrics

Unsupported predictions:
- inference time
- designability
- TM-score
- pdbTM

Missed gold values:
- scRMSD
- ligand RMSD
- design success rate

## PocketFlow: Generalized Protein Pocket Generation with Prior-Informed Flow Matching

### task

Unsupported predictions:
- structure-based drug design
- pocket-conditioned ligand generation
- protein-ligand interaction-guided molecule generation

Missed gold values:
- protein pocket generation
- ligand-binding protein pocket design
- generation of high-affinity and valid pockets
- generalized pocket design across small molecules, peptides and RNA

### datasets

Unsupported predictions:
- PDBBind

Missed gold values:
- small-molecule / peptide / RNA ligand benchmark sets

### models_or_methods

Unsupported predictions:
- Invariant Point Attention
- Riemannian flow matching
- self-conditioning
- AlphaFold 3
- AlphaFold3
- FrameFlow
- FoldFlow

Missed gold values:
- hydrogen-bond interaction modeling

### metrics

Unsupported predictions:
- amino acid recovery
- self-consistency
- steric clashes
- QED
- MAE

Missed gold values:
- hydrogen-bond recovery
- interaction recovery
- ligand-modality generalization performance

## FLOWR: Flow Matching for Structure-Aware De Novo, Interaction- and Fragment-Based Ligand Generation

### task

Unsupported predictions:
- pocket-conditioned molecule design

Missed gold values:
- protein-pocket-conditioned ligand generation
- interaction-conditioned ligand generation
- fragment-based ligand generation
- ligand optimization

### datasets

Unsupported predictions:
- PoseBusters
- PDBBind
- ChEMBL

Missed gold values:
- ligand-pocket co-crystal complexes
- protein-pocket ligand-generation benchmarks

### models_or_methods

Unsupported predictions:
- scalable E(3)-equivariant message passing
- fragment-based ligand generation
- equivariant flow matching
- conditional flow matching
- self-conditioning
- latent attention
- AlphaFold 3
- PoseBusters
- SemlaFlow
- PLINDER

Missed gold values:
- FLOWR
- equivariant optimal transport
- protein pocket conditioning
- interaction-profile conditioning
- fragment/substructure conditioning

### metrics

Unsupported predictions:
- binding affinity
- pocket validity
- inference time
- strain energy
- docking score
- success rate
- mean RMSD
- SA score
- Lipinski
- PB-valid
- QED

Missed gold values:
- pose accuracy
- inference speedup
- chemical validity
- fragment and interaction constraint satisfaction

## PoseBusters: AI-based docking methods fail to generate physically valid poses or generalise to novel sequences

### task

Unsupported predictions:
- physical validity assessment for generated ligand poses

Missed gold values:
- physical validity evaluation for protein-ligand docking
- docking-method benchmarking
- generalization assessment to novel sequences
- chemical and geometric consistency checking

### datasets

Unsupported predictions:
- Astex Diverse
- PDBBind 2019
- PDBBind 2020
- CASF

Missed gold values:
- PDBBind / protein-ligand docking benchmark collections

### models_or_methods

Unsupported predictions:
- trigonometry-aware neural network
- TANKBind
- EquiBind

Missed gold values:
- PoseBusters
- RDKit-based chemical validity checks
- post-prediction energy minimization evaluation protocol
- molecular-mechanics force-field minimization

### metrics

Unsupported predictions:
- PoseBusters checks
- chemical validity
- steric clashes

Missed gold values:
- ligand stereochemistry correctness
- aromatic ring planarity
- bond length validity
- bond angle validity
- intermolecular steric clash checks
- physical plausibility
- generalization performance

## TANKBind: Trigonometry-Aware Neural Networks for Drug-Protein Binding Structure Prediction

### task

Missed gold values:
- protein-ligand complex conformation prediction
- blind docking

### datasets

Missed gold values:
- PDBBind 2019 time split
- PDBBind affinity benchmark

### models_or_methods

Unsupported predictions:
- EquiBind

Missed gold values:
- trigonometry-aware neural network
- protein functional block segmentation
- pairwise distance-map prediction
- contrastive losses with local-region negative sampling
- joint binding interaction and affinity optimization

### metrics

Unsupported predictions:
- binding affinity

Missed gold values:
- RMSD percentiles
- percentage of predictions below 2 Å
- percentage of predictions below 5 Å
- number of parameters

## DynamicBind: Predicting Ligand-Specific Protein-Ligand Complex Structure with a Deep Equivariant Generative Model

### task

Unsupported predictions:
- https://doi.org/10.1038/s41467-024-45461-2.

Missed gold values:
- ligand-specific protein-ligand complex structure prediction
- flexible docking from unbound protein structures
- protein conformational change prediction
- cryptic pocket identification
- virtual screening

### datasets

Unsupported predictions:
- Major Drug Target
- PoseBusters

Missed gold values:
- antibiotics benchmark

### models_or_methods

Unsupported predictions:
- PoseBusters
- DiffDock

Missed gold values:
- equivariant geometric diffusion network
- ligand-specific conformational transition modeling
- smooth energy landscape construction
- cLDDT confidence/ranking module
- binding-affinity prediction module

### metrics

Unsupported predictions:
- success rate
- RMSD < 2 Å success rate
- RMSD < 5 Å success rate
- runtime

Missed gold values:
- ligand RMSD
- fraction of ligand RMSD < 2 Å
- fraction of ligand RMSD < 5 Å
- clash score
- cLDDT

## Accurate Structure Prediction of Biomolecular Interactions with AlphaFold 3

### task

Unsupported predictions:
- Nature
- Vol 630
- 13 June 2024

Missed gold values:
- biomolecular complex structure prediction
- protein-ligand interaction prediction
- protein-nucleic acid interaction prediction
- protein-protein and antibody-antigen interaction prediction
- prediction of complexes with ions and modified residues

### datasets

Unsupported predictions:
- MIMIC

Missed gold values:
- recent PDB evaluation set / RecentPDBEval
- PDB
- CCD-based ligand and modification evaluation sets

### models_or_methods

Unsupported predictions:
- PoseBusters
- TANKBind
- DiffDock
- EquiBind
- pLDDT

Missed gold values:
- diffusion-based structure prediction model
- unified biomolecular interaction model
- diffusion module
- cross-distillation strategy

### metrics

Unsupported predictions:
- PoseBusters validity
- interface accuracy
- inference time
- PB-valid
- novelty
- ipTM

Missed gold values:
- interface LDDT
- GDT
- confidence-ranked top sample accuracy
- RNA target accuracy
