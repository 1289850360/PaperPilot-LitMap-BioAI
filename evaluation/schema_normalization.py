"""Schema-aware value normalization for PaperPilot evaluation.

These rules are intentionally conservative. They normalize spelling, aliases,
units, and common shorthand without turning related-but-distinct concepts into
the same benchmark value.
"""

from __future__ import annotations

import re


def canonicalize_value(field: str, value: str) -> str:
    normalized = normalize_text(value)
    if not normalized:
        return ""
    if field == "metrics":
        return canonicalize_metric(normalized)
    if field == "models_or_methods":
        return canonicalize_method(normalized)
    if field == "datasets":
        return canonicalize_dataset(normalized)
    if field == "task":
        return canonicalize_task(normalized)
    return normalized


def normalize_text(value: str) -> str:
    value = value.lower()
    value = value.replace("≤", "<=").replace("≥", ">=").replace("˚", "a").replace("å", "a")
    value = value.replace("angstrom", "a")
    value = re.sub(r"([<>]=?)\s*(\d+)\s*a\b", r"\1 \2 a", value)
    value = re.sub(r"[^a-z0-9<>=%/.+-]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def canonicalize_metric(value: str) -> str:
    if re.search(r"\b(pb valid|pb-valid|posebusters validity|posebusters valid|posebusters pass rate|posebusters checks|physical validity)\b", value):
        return "posebusters physical validity"
    if re.search(r"\bligand stereochemistry (accuracy|correctness)\b", value):
        return "ligand stereochemistry correctness"
    if "intramolecular validity" in value:
        return "intramolecular validity"
    if "intermolecular steric clash" in value or value == "steric clashes":
        return "intermolecular steric clash"
    if "bond length validity" in value:
        return "bond length validity"
    if "bond angle validity" in value:
        return "bond angle validity"
    if "aromatic ring planarity" in value:
        return "aromatic ring planarity"
    if re.search(r"\bfraction of ligand rmsd < 2\b|\bfraction of predictions with rmsd < 2\b|\bpercentage of ligand rmsd < 2\b|\brmsd (<=|<) 2\b", value):
        return "ligand rmsd under 2 success rate"
    if re.search(r"\bfraction of ligand rmsd < 5\b|\bfraction of predictions with rmsd < 5\b|\brmsd (<=|<) 5\b", value):
        return "ligand rmsd under 5 success rate"
    if re.search(r"\bcentroid distance (<=|<) 2\b", value):
        return "centroid distance under 2"
    if re.search(r"\bcentroid distance (<=|<) 5\b", value):
        return "centroid distance under 5"
    if "mean centroid distance" in value:
        return "mean centroid distance"
    if "centroid distance" in value:
        return "centroid distance"
    if "median ligand rmsd" in value:
        return "median ligand rmsd"
    if "mean rmsd" in value:
        return "mean rmsd"
    if "ligand rmsd" in value:
        return "ligand rmsd"
    if "pocket all atom rmsd" in value or "pocket side chain rmsd" in value or "pocket rmsd" in value:
        return "pocket rmsd"
    if "binding pocket conformation rmsd" in value:
        return "binding pocket conformation rmsd"
    if "motif scrmsd" in value or "motif rmsd" in value:
        return "motif rmsd"
    if value == "rmsd":
        return "rmsd"
    if "cpu memory" in value:
        return "cpu memory"
    if "gpu memory" in value:
        return "gpu memory"
    if re.search(r"\binference time\b|\bprediction speed\b|\bruntime\b|\baverage runtime\b|\bsampling speed\b|\btime per sample\b", value):
        return "runtime speed"
    if "number of sampling steps" in value or "sampling steps" in value or "sampling timesteps" in value:
        return "sampling steps"
    if "success rate" in value and "rmsd" not in value:
        return "success rate"
    if "auroc" in value or value == "auc":
        return "auroc"
    if "auprc" in value:
        return "auprc"
    if "pearson correlation" in value:
        return "pearson correlation"
    if "spearman correlation" in value:
        return "spearman correlation"
    if "rmse" in value:
        return "rmse"
    if "mae" in value:
        return "mae"
    if "qed" in value:
        return "qed"
    if "sa score" in value:
        return "sa score"
    if "lipinski" in value:
        return "lipinski"
    if "vina score" in value:
        return "vina score"
    if "qvina score" in value:
        return "qvina score"
    if "docking score" in value:
        return "docking score"
    if "strain energy" in value:
        return "strain energy"
    if "tm score" in value or "tm-score" in value:
        return "tm score"
    if "max tm score" in value:
        return "max tm score"
    if "average pairwise tm score" in value:
        return "average pairwise tm score"
    if "plddt" in value:
        return "plddt"
    if "pdockq" in value:
        return "pdockq"
    if "dockq" in value:
        return "dockq"
    if "lddt" in value:
        return "lddt"
    if "clash score" in value:
        return "clash score"
    if "designability" in value:
        return "designability"
    if "diversity score" in value or value == "diversity":
        return "diversity"
    if "validity score" in value or value == "validity":
        return "validity"
    if "uniqueness" in value:
        return "uniqueness"
    if "novelty" in value:
        return "novelty"
    if "connectedness" in value:
        return "connectedness"
    return value


def canonicalize_method(value: str) -> str:
    if value in {"np3", "neuralplexer3", "neuralplexer3 / np3"}:
        return "neuralplexer3"
    if "confidence head" in value or "plddt structural confidence" in value:
        return "confidence head"
    if "binding affinity head" in value:
        return "binding affinity head"
    if "continuous normalizing flow" in value:
        return "continuous normalizing flow"
    if "conditional flow matching" in value:
        return "conditional flow matching"
    if "riemannian flow matching" in value:
        return "riemannian flow matching"
    if "geometric flow matching" in value:
        return "geometric flow matching"
    if "harmonic self conditioned flow matching" in value:
        return "harmonic self conditioned flow matching"
    if "unbalanced flow matching" in value or value == "ufm":
        return "unbalanced flow matching"
    if "force guided flow matching" in value:
        return "force guided flow matching"
    if "force guidance network" in value:
        return "force guidance network"
    if "energy guided generation" in value:
        return "energy guided generation"
    if "rdkit etkdg conformer initialization" in value or value == "rdkit etkdg":
        return "rdkit etkdg conformer initialization"
    if "vina guided generation" in value:
        return "vina guided generation"
    if "glide guided generation" in value:
        return "glide guided generation"
    if "gnina guided generation" in value:
        return "gnina guided generation"
    if "flow based encoder decoder structure prediction model" in value:
        return "flow based encoder decoder structure prediction model"
    if "hybrid structure and affinity prediction model" in value:
        return "hybrid structure and affinity prediction model"
    if "apo to holo structure generation" in value:
        return "apo to holo structure generation"
    if "fine tuned neuralplexer architecture" in value:
        return "fine tuned neuralplexer architecture"
    if "vd ode sampler" in value:
        return "vd ode sampler"
    if "leakage minimizing split generation" in value:
        return "leakage minimizing split generation"
    if "protein/pocket/interaction/ligand level similarity annotation" in value:
        return "protein pocket interaction ligand similarity annotation"
    if "paired apo and predicted structure annotation" in value:
        return "paired apo and predicted structure annotation"
    if "direct shot binding pose prediction" in value:
        return "direct shot binding pose prediction"
    if "keypoint based rigid alignment" in value:
        return "keypoint based rigid alignment"
    if "von mises torsion angle conformer fitting" in value:
        return "von mises torsion angle conformer fitting"
    if "fragment based ligand generation" in value:
        return "fragment based ligand generation"
    if "self conditioning" in value:
        return "self conditioning"
    return value


def canonicalize_dataset(value: str) -> str:
    if "posebusters" in value or "posebench" in value:
        return "posebusters"
    if "pdbbind 2020" in value or "pdbbind version 2020" in value:
        return "pdbbind 2020"
    if "pdbbind 2019" in value:
        return "pdbbind 2019"
    if "pdbbind time" in value:
        return "pdbbind time split"
    if value == "pdbbind":
        return "pdbbind"
    if "binding moad" in value:
        return "binding moad"
    if "plinder" in value:
        return "plinder"
    if "dockgen" in value:
        return "dockgen"
    if "casp15" in value:
        return "casp15"
    if "casp16" in value:
        return "casp16"
    return value


def canonicalize_task(value: str) -> str:
    if "drug protein binding structure prediction" in value:
        return "protein ligand binding structure prediction"
    if "protein ligand binding pose prediction" in value or "binding pose prediction" in value:
        return "protein ligand binding pose prediction"
    if "blind protein ligand docking" in value or "rigid receptor blind docking" in value:
        return "blind protein ligand docking"
    if "protein ligand docking" in value and "generalization" not in value:
        return "protein ligand docking"
    if "protein ligand docking generalization" in value:
        return "protein ligand docking generalization"
    if "molecular docking" in value:
        return "molecular docking"
    if "flow matching for molecule generation" in value or "3d molecular generation" in value:
        return "3d molecular generation"
    if "protein structure generation" in value or "protein backbone generation" in value:
        return "protein structure generation"
    return value
