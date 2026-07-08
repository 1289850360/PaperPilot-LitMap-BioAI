# Error Analysis

Prediction file: `experiments\outputs\benchmark_23_schema_v5\heuristic_predictions.csv`
Gold file: `evaluation\gold_23_paper_benchmark.csv`

## NeuralPLexer3: Accurate Biomolecular Complex Structure Prediction with Flow Models

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

## PLINDER: The protein-ligand interactions dataset and evaluation resource

### task

Unsupported predictions:
- Protein-ligand interactions (PLI) are foundational to small molecule drug design.

Missed gold values:
- protein-ligand interaction dataset curation
- leakage-controlled train/test split construction
- protein-ligand docking generalization evaluation

### datasets

Missed gold values:
- PLINDER
- PLINDER-NR
- PLINDER-PL50
- PLINDER-TIME

### models_or_methods

Missed gold values:
- PLINDER
- leakage-minimizing split generation
- protein/pocket/interaction/ligand-level similarity annotation
- paired apo and predicted structure annotation

### metrics

Unsupported predictions:
- PoseBusters checks
- inference time
- LDDT
- MAE

Missed gold values:
- protein/pocket/interaction/ligand similarity metrics
- leakage / train-test similarity
- test set quality

## EquiBind: Geometric Deep Learning for Drug Binding Structure Prediction

### task

Unsupported predictions:
- EQUIBIND: Geometric Deep Learning for Drug Binding Structure Prediction.

Missed gold values:
- drug-protein binding structure prediction
- blind protein-ligand docking
- receptor binding-location prediction
- ligand bound-pose and orientation prediction
- ligand torsion refinement

### datasets

Missed gold values:
- PDBBind v2020
- PDBBind time split

### models_or_methods

Missed gold values:
- EquiBind
- SE(3)-equivariant geometric deep learning
- direct-shot binding pose prediction
- keypoint-based rigid alignment
- von Mises torsion-angle conformer fitting

### metrics

Unsupported predictions:
- inference time

Missed gold values:
- Kabsch-RMSD
- percentage of predictions below 2 Å
- percentage of predictions below 5 Å
- RMSD percentiles

## DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking

### task

Missed gold values:
- protein-ligand binding pose prediction
- blind docking
- generative modeling of ligand poses
- confidence estimation for docking poses

### datasets

Missed gold values:
- PDBBind
- computationally folded protein structure evaluation setting

### models_or_methods

Unsupported predictions:
- pLDDT

Missed gold values:
- DiffDock
- diffusion generative model over ligand poses
- diffusion on translational, rotational and torsional degrees of freedom
- non-Euclidean manifold diffusion
- confidence model for pose ranking

### metrics

Unsupported predictions:
- success rate
- GPU memory
- mean RMSD
- runtime
- pLDDT
- Dice

Missed gold values:
- percentage of predictions below 2 Å
- percentage of predictions below 5 Å
- RMSD percentiles
- selective accuracy

## SE(3) Stochastic Flow Matching for Protein Backbone Generation / FoldFlow

### task

Unsupported predictions:
- The computational design of novel protein structures has the potential to impact numerous scientific disciplines greatly.

Missed gold values:
- protein backbone generation
- de novo protein structure generation
- unconditional protein backbone design
- generative modeling over SE(3)
- equilibrium conformation generation

### datasets

Unsupported predictions:
- CIFAR

Missed gold values:
- PDB subset / PDB-derived 22,248-protein training set
- BPTI molecular-dynamics trajectory evaluation set

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- continuous normalizing flow
- conditional flow matching
- Riemannian flow matching

Missed gold values:
- FoldFlow
- FoldFlow-Base
- FoldFlow-OT
- FoldFlow-SFM
- SE(3) stochastic flow matching
- Riemannian optimal transport
- simulation-free continuous-time dynamics
- stochastic continuous-time dynamics over SE(3)

### metrics

Missed gold values:
- designability
- scRMSD
- diversity / average pairwise TM-score
- iterations per second
- KL divergence for conformation sampling

## FrameFlow: Fast Protein Backbone Generation with SE(3) Flow Matching

### task

Unsupported predictions:
- Compared to FrameDiff, FrameFlow requires five times fewer sampling timesteps while achieving two fold better designability.

Missed gold values:
- protein backbone generation
- de novo protein design
- fast protein backbone sampling
- SE(3)-frame generation

### datasets

Missed gold values:
- SCOPe dataset

### models_or_methods

Unsupported predictions:
- conditional flow matching
- Riemannian flow matching

Missed gold values:
- FrameFlow
- SE(3) flow matching
- FrameDiff adaptation to flow matching
- FramePred architecture
- Invariant Point Attention
- self-conditioning
- SE(3) inference scheduler

### metrics

Missed gold values:
- designability
- diversity / structural clusters
- novelty / pdbTM
- sampling timesteps
- sampling speedup

## DiffBindFR: An SE(3) Equivariant Network for Flexible Protein-Ligand Docking

### task

Unsupported predictions:
- DiffBindFR: An SE(3) Equivariant Network for Flexible.

Missed gold values:
- flexible protein-ligand docking
- full-atom protein-ligand binding-structure prediction
- ligand binding-pose prediction
- protein pocket side-chain conformation prediction
- apo and AlphaFold2-structure-based docking

### datasets

Missed gold values:
- PDBBind v2020
- Apo dataset
- AlphaFold2 modeled structures

### models_or_methods

Missed gold values:
- DiffBindFR
- full-atom diffusion-based flexible docking
- SE(3)-equivariant network
- product-space diffusion over ligand rotation/translation/torsion and pocket side-chain torsions
- MDN scoring model

### metrics

Unsupported predictions:
- PoseBusters pass rate / physical validity
- success rate
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

Missed gold values:
- conditional protein backbone generation
- functional motif-conditioned protein design
- scaffold diversity improvement

### datasets

Missed gold values:
- benchmark of 24 biologically meaningful motifs
- PDB monomer training set

### models_or_methods

Unsupported predictions:
- Riemannian flow matching

Missed gold values:
- FrameFlow for motif scaffolding
- SE(3) flow matching
- motif amortization
- motif guidance
- conditional score estimation
- motif data augmentation

### metrics

Unsupported predictions:
- inference time
- success rate
- RMSD < 2 Å success rate

Missed gold values:
- designability / solved motifs
- number of unique designable motif-scaffolds
- scaffold diversity
- motif RMSD
- self-consistency RMSD / scRMSD

## Deep Confident Steps to New Pockets: Strategies for Docking Generalization / DockGen

### task

Unsupported predictions:
- Accurate blind docking has the potential to lead to new biological breakthroughs, but for this promise to be realized, docking methods must generalize well across the proteome.

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

Missed gold values:
- DockGen benchmark construction
- Confidence Bootstrapping
- DiffDock scaling/retraining strategy
- synthetic data strategy

### metrics

Unsupported predictions:
- inference time
- success rate
- runtime

Missed gold values:
- ligand RMSD
- binding-site similarity
- BLOSUM62 similarity
- harmonic mean similarity
- train-test leakage / contamination
- generalization performance

## FlowMol: Mixed Continuous and Categorical Flow Matching for 3D De Novo Molecule Generation

### task

Unsupported predictions:
- Deep generative models that produce novel molecular structures have the potential to facilitate chemical discovery.

Missed gold values:
- 3D de novo molecule generation
- joint generation of atom positions and atom/bond categorical variables
- unconditional molecular generation

### datasets

Missed gold values:
- QM9
- GEOM-Drugs

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- conditional flow matching
- Riemannian flow matching

Missed gold values:
- FlowMol
- SimplexFlow
- mixed continuous and categorical flow matching
- probability-simplex categorical flow
- GVP-based molecular generator
- flow matching with explicit hydrogens and formal charges

### metrics

Missed gold values:
- percent atoms stable
- percent molecules stable
- percent molecules valid
- Jensen-Shannon divergence of potential energy distributions

## FoldFlow-2: Sequence-Augmented SE(3)-Flow Matching for Conditional Protein Backbone Generation

### task

Unsupported predictions:
- To increase diversity and novelty of generated samples—crucial for de-novo drug design—we train FOLDFLOW-2 at scale on a new dataset that is an order of magnitude larger than PDB datasets of prior works, containing both known proteins in PDB and high-quality synthetic structures achieved through filtering.

Missed gold values:
- sequence-conditioned protein backbone generation
- conditional protein structure generation
- unconditional protein backbone generation
- equilibrium conformation sampling
- motif/scaffold conditional protein design

### datasets

Missed gold values:
- PDB
- filtered AlphaFold2 synthetic structures from SwissProt
- ATLAS molecular-dynamics trajectory evaluation set
- 24 single-chain motif scaffolding benchmark
- VHH nanobody scaffold design benchmark / Structural Antibody Database

### models_or_methods

Unsupported predictions:
- continuous normalizing flow
- Riemannian flow matching
- pLDDT

Missed gold values:
- FoldFlow-2
- sequence-augmented SE(3)-flow matching
- protein language model conditioning
- multi-modal fusion trunk
- geometric transformer decoder
- Reinforced Finetuning / ReFT

### metrics

Unsupported predictions:
- inference time
- RMSD < 2 Å success rate
- pLDDT

Missed gold values:
- designability
- diversity
- novelty
- scRMSD
- secondary-structure diversity
- motif scRMSD
- number of solved motif scaffolds
- pairwise RMSD Pearson correlation
- global RMSF Pearson correlation
- PCA W2 distance
- time per sample

## SemlaFlow: Efficient 3D Molecular Generation with Latent Attention and Equivariant Flow Matching

### task

Unsupported predictions:
- Current approaches, however, often suf- fer from very slow sampling times or generate molecules with poor chemical validity.

Missed gold values:
- unconditional 3D molecular generation
- joint molecular graph and 3D conformation generation
- efficient molecular sampling

### datasets

Unsupported predictions:
- PoseBusters

Missed gold values:
- QM9
- GEOM-Drugs

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- conditional flow matching

Missed gold values:
- Semla
- SemlaFlow
- scalable E(3)-equivariant message passing
- latent attention
- equivariant flow matching
- joint generation of atom types, coordinates, bond types and formal charges

### metrics

Unsupported predictions:
- inference time
- GPU memory

Missed gold values:
- atom stability
- molecule stability
- validity
- uniqueness
- novelty
- connectedness
- number of function evaluations / NFE
- distributional benchmark metrics

## AtomFlow: Design of Ligand-Binding Proteins with Atomic Flow Matching

### task

Unsupported predictions:
- DESIGN OF LIGAND-BINDING PROTEINS WITH ATOMIC.

Missed gold values:
- ligand-binding protein design
- protein backbone generation conditioned on a target molecule
- ligand conformation generation
- joint ligand-protein structure generation from a 2D molecular graph

### datasets

Unsupported predictions:
- PoseBusters
- CIFAR

Missed gold values:
- SCOPe
- RFDiffusionAA selected ligand evaluation set (FAD, SAM, IAI, OQO)
- extended ligand set

### models_or_methods

Unsupported predictions:
- harmonic self-conditioned flow matching
- conditional flow matching
- Riemannian flow matching

Missed gold values:
- AtomFlow
- atomic flow matching
- unified biotoken representation
- SE(3)-equivariant structure prediction network
- iterative ligand conformation and protein backbone generation

### metrics

Unsupported predictions:
- inference time
- TM-score

Missed gold values:
- self-consistency
- binding affinity
- diversity
- novelty
- scRMSD
- Vina score / binding score
- design success rate

## PocketFlow: Generalized Protein Pocket Generation with Prior-Informed Flow Matching

### task

Unsupported predictions:
- protein-ligand binding affinity prediction

Missed gold values:
- protein pocket generation
- ligand-binding protein pocket design
- generation of high-affinity and valid pockets
- generalized pocket design across small molecules, peptides and RNA

### datasets

Unsupported predictions:
- PDBBind

Missed gold values:
- CrossDocked
- small-molecule / peptide / RNA ligand benchmark sets

### models_or_methods

Unsupported predictions:
- Riemannian flow matching

Missed gold values:
- PocketFlow
- prior-informed flow matching
- protein-ligand interaction priors
- hydrogen-bond interaction modeling
- binding affinity guidance
- interaction geometry guidance
- multi-granularity guidance

### metrics

Unsupported predictions:
- MAE

Missed gold values:
- AAR / amino acid recovery
- Vina Score
- hydrogen-bond recovery
- interaction recovery
- binding affinity
- pocket validity
- ligand-modality generalization performance

## FLOWR: Flow Matching for Structure-Aware De Novo, Interaction- and Fragment-Based Ligand Generation

### task

Unsupported predictions:
- In addition, we introduce FLOWR.MULTI, a highly accurate multi-purpose model allowing for the targeted sampling of ligands that adhere to predefined interaction profiles and chemical substructures for fragment-based design without the need of re-training or any re-sampling strategies.

Missed gold values:
- structure-aware de novo ligand generation
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
- CrossDocked2020
- ligand-pocket co-crystal complexes
- protein-pocket ligand-generation benchmarks

### models_or_methods

Unsupported predictions:
- physics-inspired flow-based generative model
- conditional flow matching

Missed gold values:
- FLOWR
- FLOWR.MULTI
- continuous and categorical flow matching
- equivariant optimal transport
- protein pocket conditioning
- interaction-profile conditioning
- fragment/substructure conditioning

### metrics

Unsupported predictions:
- inference time
- sampling steps
- success rate
- mean RMSD
- PB-valid

Missed gold values:
- pose accuracy
- interaction recovery
- inference speedup
- Vina score
- diversity
- novelty
- uniqueness
- chemical validity
- fragment and interaction constraint satisfaction

## PoseBusters: AI-based docking methods fail to generate physically valid poses or generalise to novel sequences

### task

Unsupported predictions:
- PoseBusters: AI-based docking methods fail to.

Missed gold values:
- physical validity evaluation for protein-ligand docking
- docking-method benchmarking
- generalization assessment to novel sequences
- chemical and geometric consistency checking

### datasets

Unsupported predictions:
- Astex Diverse
- PDBBind 2020
- CASF

Missed gold values:
- PDBBind / protein-ligand docking benchmark collections

### models_or_methods

Missed gold values:
- PoseBusters
- PoseBusters test suite
- RDKit-based chemical validity checks
- post-prediction energy minimization evaluation protocol
- molecular-mechanics force-field minimization

### metrics

Unsupported predictions:
- PoseBusters checks

Missed gold values:
- ligand stereochemistry correctness
- aromatic ring planarity
- bond length validity
- bond angle validity
- intramolecular validity
- intermolecular steric clash checks
- physical plausibility
- generalization performance

## TANKBind: Trigonometry-Aware Neural Networks for Drug-Protein Binding Structure Prediction

### task

Unsupported predictions:
- protein pocket residue design for small-molecule binding
- joint residue-type and ligand-pose generation

Missed gold values:
- drug-protein binding structure prediction
- blind docking

### datasets

Missed gold values:
- PDBBind
- PDBBind 2019 time split

### models_or_methods

Missed gold values:
- TANKBind
- trigonometry-aware neural network
- protein functional block segmentation
- pairwise distance-map prediction
- contrastive losses with local-region negative sampling
- joint binding interaction and affinity optimization

### metrics

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
- PoseBusters

Missed gold values:
- Major Drug Target / MDT test set
- antibiotics benchmark
- Cryptosite dataset / cryptic-pocket case studies

### models_or_methods

Missed gold values:
- DynamicBind
- equivariant geometric diffusion network
- dynamic docking
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
- stringent success criterion (ligand RMSD < 2 Å and clash score < 0.35)
- pocket RMSD
- cLDDT

## Accurate Structure Prediction of Biomolecular Interactions with AlphaFold 3

### task

Unsupported predictions:
- Nature
- Vol 630
- 13 June 2024
- 493.

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
- pLDDT

Missed gold values:
- AlphaFold 3
- diffusion-based structure prediction model
- unified biomolecular interaction model
- Pairformer
- diffusion module
- cross-distillation strategy

### metrics

Unsupported predictions:
- PoseBusters validity
- inference time
- RMSD < 2 Å success rate
- PB-valid

Missed gold values:
- interface LDDT
- GDT
- confidence-ranked top sample accuracy
- RNA target accuracy
