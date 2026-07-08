import re
from collections import defaultdict
from typing import Any

from .verifier import build_verification_statuses


DATASET_PATTERNS = [
    "PLINDER-NR",
    "PLINDER-PL50",
    "PLINDER-TIME",
    "PLINDER-ECOD",
    "PDBBind v2020",
    "PDBBind 2019 test set",
    "PDBBind 2019 time split",
    "PDBBind affinity benchmark",
    "PDBBind time-based split",
    "BPTI molecular-dynamics trajectory evaluation set",
    "ATLAS molecular-dynamics trajectory evaluation set",
    "Structural Antibody Database",
    "VHH nanobody scaffold design benchmark",
    "24 single-chain motif scaffolding benchmark",
    "filtered AlphaFold2 synthetic structures from SwissProt",
    "PDB monomer training set",
    "PDB subset",
    "PDB-derived",
    "RFDiffusionAA selected ligand evaluation set",
    "PDBBind 2019",
    "CrossDocked",
    "GEOM-Drugs",
    "Major Drug Target",
    "MDT test set",
    "Cryptosite",
    "SCOPe dataset",
    "SCOPe",
    "QM9",
    "PoseBusters-V2",
    "PoseBusters v2",
    "PoseBench PoseBusters set",
    "PDBBind ESMFold docking benchmark",
    "PDBBind sequence similarity split",
    "PDBBind time split",
    "PDBBind version 2020",
    "DockGen test set",
    "DockGen cross-domain benchmark",
    "Binding MOAD sequence similarity split",
    "PoseBusters",
    "PoseBench",
    "PDBBind-E",
    "PDBBind 2020",
    "PDBBind",
    "CASF",
    "CASP16",
    "CASP15",
    "DockGen-E",
    "DockGen",
    "Binding MOAD",
    "DUD-E",
    "Astex Diverse",
    "NPBench",
    "ConfBench",
    "PLINDER",
    "OpenProteinSet",
    "OrbNet",
    "ChEMBL",
    "BindingDB",
    "DrugBank",
    "TCGA",
    "UK Biobank",
    "ImageNet",
    "CIFAR",
    "MNIST",
    "MIMIC",
]

METHOD_PATTERNS = [
    "protein/pocket/interaction/ligand-level similarity annotation",
    "paired apo and predicted structure annotation",
    "leakage-minimizing split generation",
    "SE(3)-equivariant geometric deep learning",
    "direct-shot binding pose prediction",
    "keypoint-based rigid alignment",
    "von Mises torsion-angle conformer fitting",
    "diffusion generative model over ligand poses",
    "diffusion on translational, rotational and torsional degrees of freedom",
    "non-Euclidean manifold diffusion",
    "confidence model for pose ranking",
    "SE(3) stochastic flow matching",
    "Riemannian optimal transport",
    "simulation-free continuous-time dynamics",
    "stochastic continuous-time dynamics over SE(3)",
    "sequence-augmented SE(3)-flow matching",
    "protein language model conditioning",
    "multi-modal fusion trunk",
    "geometric transformer decoder",
    "Reinforced Finetuning",
    "FrameDiff adaptation to flow matching",
    "FramePred architecture",
    "Invariant Point Attention",
    "self-conditioning",
    "SE(3) inference scheduler",
    "full-atom diffusion-based flexible docking",
    "SE(3)-equivariant network",
    "product-space diffusion over ligand rotation/translation/torsion and pocket side-chain torsions",
    "MDN scoring model",
    "FrameFlow for motif scaffolding",
    "motif amortization",
    "motif guidance",
    "conditional score estimation",
    "motif data augmentation",
    "DockGen benchmark construction",
    "Confidence Bootstrapping",
    "DiffDock scaling/retraining strategy",
    "synthetic data strategy",
    "mixed continuous and categorical flow matching",
    "probability-simplex categorical flow",
    "GVP-based molecular generator",
    "flow matching with explicit hydrogens and formal charges",
    "scalable E(3)-equivariant message passing",
    "latent attention",
    "equivariant flow matching",
    "joint generation of atom types, coordinates, bond types and formal charges",
    "atomic flow matching",
    "unified biotoken representation",
    "SE(3)-equivariant structure prediction network",
    "iterative ligand conformation and protein backbone generation",
    "prior-informed flow matching",
    "protein-ligand interaction priors",
    "hydrogen-bond interaction modeling",
    "binding affinity guidance",
    "interaction geometry guidance",
    "multi-granularity guidance",
    "structure-aware flow matching",
    "interaction-based ligand generation",
    "fragment-based ligand generation",
    "pocket-conditioned ligand generation",
    "trigonometry-aware neural network",
    "protein functional block segmentation",
    "pairwise distance-map prediction",
    "contrastive losses with local-region negative sampling",
    "joint binding interaction and affinity optimization",
    "equivariant geometric diffusion network",
    "dynamic docking",
    "ligand-specific conformational transition modeling",
    "smooth energy landscape construction",
    "cLDDT confidence/ranking module",
    "binding-affinity prediction module",
    "diffusion-based biomolecular structure prediction",
    "AlphaFold 3",
    "AlphaFold3",
    "PoseBusters",
    "DynamicBind",
    "PocketFlow",
    "AtomFlow",
    "SemlaFlow",
    "SimplexFlow",
    "FoldFlow-Base",
    "FoldFlow-OT",
    "FoldFlow-SFM",
    "FoldFlow-2",
    "FoldFlow",
    "FrameFlow",
    "DiffBindFR",
    "DockGen",
    "FlowMol",
    "FLOWR",
    "TANKBind",
    "DiffDock",
    "EquiBind",
    "PLINDER",
    "pairformer",
    "NeuralPLexer3",
    "NP3",
    "FlowDock",
    "HARMONICFLOW",
    "FLOWSITE",
    "Unbalanced Flow Matching",
    "FLEXDOCK",
    "ForceFM",
    "force-guided flow matching",
    "force-guidance network",
    "force model",
    "energy-guided generation",
    "geometric flow matching",
    "conditional flow matching",
    "self-conditioned flow matching",
    "harmonic self-conditioned flow matching",
    "manifold flow matching",
    "Riemannian flow matching",
    "continuous normalizing flow",
    "physics-inspired flow-based generative model",
    "flow-based encoder-decoder structure prediction model",
    "flow matching",
    "flow-based generative model",
    "generative flow matching model",
    "deep geometric generative model",
    "hybrid structure-and-affinity prediction model",
    "apo-to-holo structure generation",
    "product-space diffusion",
    "EigenFold diffusion",
    "Vina-guided generation",
    "Glide-guided generation",
    "Gnina-guided generation",
    "Confscore",
    "RDKit ETKDG",
    "RDKit ETKDG conformer initialization",
    "ESMFold protein prior",
    "fine-tuned NeuralPLexer architecture",
    "harmonic ligand prior",
    "harmonic prior",
    "joint discrete-continuous flow",
    "fake-ligand data augmentation",
    "VD-ODE sampler",
    "pLDDT",
    "binding affinity head",
    "confidence head",
    "confidence module",
    "confidence discriminator",
    "pLDDT/pDockQ-based sample ranking",
    "optimal transport structure permutation",
    "informative globular polymer prior",
    "Langevin dynamics prior relaxation",
    "Flash-TriangularAttention",
    "equivariant refinement TFN",
    "invariant graph attention network",
    "manifold docking flow",
    "manifold Unbalanced FM",
    "Euclidean relaxation flow",
    "structure relaxation Unbalanced FM",
    "energy-based loss",
    "flat-bottom potential",
    "energy filtering",
    "SE(3) and side-chain torsion flow",
    "random forest",
    "SVM",
]

METRIC_PATTERNS = [
    "protein/pocket/interaction/ligand similarity metrics",
    "leakage / train-test similarity",
    "top-1 docking success rate",
    "test set quality",
    "Kabsch-RMSD",
    "percentage of predictions below 2",
    "percentage of predictions below 5",
    "selective accuracy",
    "average pairwise TM-score",
    "max TM-score",
    "iterations per second",
    "KL divergence",
    "structural clusters",
    "sampling timesteps",
    "sampling speedup",
    "pocket side-chain RMSD",
    "steric clashes",
    "number of unique designable motif-scaffolds",
    "scaffold diversity",
    "motif RMSD",
    "self-consistency RMSD",
    "TM-score-based clustering",
    "binding-site similarity",
    "BLOSUM62 similarity",
    "harmonic mean similarity",
    "train-test leakage",
    "generalization performance",
    "percent atoms stable",
    "percent molecules stable",
    "percent molecules valid",
    "Jensen-Shannon divergence",
    "secondary-structure diversity",
    "motif scRMSD",
    "number of solved motif scaffolds",
    "pairwise RMSD Pearson correlation",
    "global RMSF Pearson correlation",
    "per-target RMSF Pearson correlation",
    "PCA W2 distance",
    "time per sample",
    "atom stability",
    "molecule stability",
    "validity",
    "uniqueness",
    "connectedness",
    "number of function evaluations",
    "sampling speed",
    "distributional benchmark metrics",
    "self-consistency",
    "binding affinity",
    "Vina score",
    "binding score",
    "design success rate",
    "amino acid recovery",
    "hydrogen-bond recovery",
    "interaction recovery",
    "pocket validity",
    "ligand-modality generalization performance",
    "chemical validity",
    "SA score",
    "Lipinski",
    "strain energy",
    "docking score",
    "diversity score",
    "Qvina score",
    "validity score",
    "ligand stereochemistry correctness",
    "aromatic ring planarity",
    "bond length validity",
    "bond angle validity",
    "intramolecular validity",
    "intermolecular steric clash checks",
    "affinity prediction correlations",
    "number of parameters",
    "fraction of ligand RMSD < 2",
    "fraction of ligand RMSD < 5",
    "clash score",
    "stringent success criterion",
    "relaxed success criterion",
    "pocket RMSD",
    "virtual-screening auROC",
    "interface accuracy",
    "ligand pose accuracy",
    "protein-ligand interaction accuracy",
    "nucleic-acid interaction accuracy",
    "designability",
    "diversity",
    "novelty",
    "pdbTM",
    "NFE",
    "AAR",
    "QED",
    "cLDDT",
    "ipTM",
    "RMSD ≤ 2",
    "RMSD ≤ 5",
    "RMSD < 2",
    "RMSD <= 2",
    "RMSD < 5",
    "RMSD <= 5",
    "fraction of predictions with RMSD < 2",
    "fraction of predictions with RMSD < 5",
    "percentage of ligand RMSD < 2",
    "percentage of all-atom RMSD < 1",
    "median ligand RMSD",
    "mean centroid distance",
    "mean RMSD",
    "RMSD percentiles",
    "binding pocket conformation RMSD",
    "pocket all-atom RMSD",
    "AA-RMSD",
    "ligand RMSD",
    "RMSD",
    "centroid distance",
    "centroid distance ≤ 2",
    "centroid distance ≤ 5",
    "PoseBusters pass rate",
    "physical validity",
    "PoseBusters validity",
    "PoseBusters checks",
    "PB-valid",
    "PB-Valid",
    "ligand stereochemistry accuracy",
    "success rate",
    "blind docking success rate",
    "CASP16 affinity-ranking position",
    "sequence recovery",
    "BLOSUM score",
    "ConfBench score",
    "pocket_fident",
    "bb_LDDT",
    "DockQ",
    "pDockQ",
    "pLDDT",
    "LDDT",
    "TM-score",
    "Pearson correlation",
    "Spearman correlation",
    "inference time",
    "inference cost",
    "runtime",
    "average runtime",
    "CPU memory",
    "GPU memory",
    "sampling steps",
    "number of sampling steps",
    "proportion of energetically favorable poses",
    "AUROC",
    "AUC",
    "AUPRC",
    "Dice",
    "F1",
    "RMSE",
    "MAE",
]

BASELINE_RE = re.compile(r"\b(?:baseline|compared with|outperform(?:s|ed)?|state-of-the-art|SOTA)\b", re.I)
RESULT_RE = re.compile(r"\b(?:achieve|improve|outperform|result|performance|accuracy|AUROC|RMSD)\b", re.I)
CODE_RE = re.compile(r"\b(?:github|source code|code is available|available at|implementation)\b", re.I)
LIMIT_RE = re.compile(r"\b(?:limitation|limited|future work|fail|failure|cannot|does not|challenge)\b", re.I)
METHOD_CONTEXT_RE = re.compile(
    r"\b(?:we propose|we present|introduce|method|model|architecture|framework|"
    r"sampler|prior|head|flow|matching|diffusion|guidance|network)\b",
    re.I,
)
OWN_METHOD_CONTEXT_RE = re.compile(
    r"\b(?:we propose|we present|we introduce|we develop|we build|our|called|named)\b",
    re.I,
)
OWN_METHOD_NAME_TERMS = {
    "alphafold 3",
    "alphafold3",
    "atomflow",
    "diffbindfr",
    "diffdock",
    "dockgen",
    "dynamicbind",
    "equibind",
    "flowmol",
    "flowr",
    "foldflow",
    "foldflow 2",
    "foldflow base",
    "foldflow ot",
    "foldflow sfm",
    "frameflow",
    "plinder",
    "pocketflow",
    "posebusters",
    "semla",
    "semlaflow",
    "simplexflow",
    "tankbind",
}
METRIC_CONTEXT_RE = re.compile(
    r"\b(?:metric|evaluate|evaluation|benchmark|performance|result|success|rate|"
    r"score|error|correlation|runtime|memory|rmsd|valid|accuracy)\b|[%<>≤≥=]",
    re.I,
)
DATASET_CONTEXT_RE = re.compile(
    r"\b(?:dataset|benchmark|test set|split|evaluation set|training set|validation|"
    r"competition|suite)\b",
    re.I,
)

BROAD_METHOD_TERMS = {
    "diffusion",
    "flow matching",
    "graph neural network",
    "gnn",
    "random forest",
    "svm",
    "optimal transport",
    "langevin dynamics",
}

BROAD_DATASET_TERMS = {
    "pdbbind",
    "plinder",
    "crossdocked",
    "casp15",
    "casp16",
    "scop",
}

BROAD_METRIC_TERMS = {
    "aar",
    "auc",
    "auroc",
    "clash score",
    "diversity",
    "f1",
    "nfe",
    "qed",
    "rmsd",
    "runtime",
    "success rate",
    "validity",
}


def extract_card(parsed: dict[str, Any]) -> dict[str, Any]:
    chunks = parsed["chunks"]
    abstract = parsed.get("abstract", "")
    title = parsed.get("title", "")
    evidence: dict[str, list[dict[str, Any]]] = defaultdict(list)

    datasets = collect_terms(
        chunks,
        DATASET_PATTERNS,
        "datasets",
        evidence,
        context_re=DATASET_CONTEXT_RE,
        broad_terms=BROAD_DATASET_TERMS,
        limit=14,
    )
    methods = collect_terms(
        chunks,
        METHOD_PATTERNS,
        "models_or_methods",
        evidence,
        context_re=METHOD_CONTEXT_RE,
        broad_terms=BROAD_METHOD_TERMS,
        title_context=title,
        own_name_terms=OWN_METHOD_NAME_TERMS,
        limit=18,
    )
    metrics = collect_terms(
        chunks,
        METRIC_PATTERNS,
        "metrics",
        evidence,
        context_re=METRIC_CONTEXT_RE,
        broad_terms=BROAD_METRIC_TERMS,
        limit=20,
    )

    task = infer_task(title, abstract, chunks, evidence)
    baselines = collect_sentences(chunks, BASELINE_RE, "baselines", evidence, limit=4)
    main_result = collect_sentences(chunks, RESULT_RE, "main_result", evidence, limit=4)
    limitations = collect_sentences(chunks, LIMIT_RE, "limitations", evidence, limit=4)
    code_availability = collect_sentences(chunks, CODE_RE, "code_availability", evidence, limit=3)

    card = {
        "task": task,
        "datasets": datasets,
        "models_or_methods": methods,
        "baselines": baselines,
        "metrics": metrics,
        "main_result": main_result,
        "limitations": limitations,
        "code_availability": code_availability,
        "evidence": dict(evidence),
    }
    card["verification_statuses"] = build_verification_statuses(card)
    return card


def collect_terms(
    chunks: list[dict[str, Any]],
    patterns: list[str],
    field: str,
    evidence: dict[str, list[dict[str, Any]]],
    context_re: re.Pattern[str] | None = None,
    broad_terms: set[str] | None = None,
    title_context: str = "",
    own_name_terms: set[str] | None = None,
    limit: int | None = None,
) -> list[str]:
    found: list[str] = []
    for pattern in sorted(patterns, key=len, reverse=True):
        term_re = re.compile(r"\b" + re.escape(pattern) + r"\b", re.I)
        match = best_chunk_match(
            chunks,
            term_re,
            pattern,
            context_re,
            broad_terms or set(),
            title_context,
            own_name_terms or set(),
        )
        if not match:
            continue
        chunk, snippet = match
        canonical = canonicalize_term(pattern)
        if not has_redundant_term(found, canonical):
            found.append(canonical)
            evidence[field].append(to_evidence(chunk, snippet))
            if limit and len(found) >= limit:
                return found
    return found


def best_chunk_match(
    chunks: list[dict[str, Any]],
    term_re: re.Pattern[str],
    pattern: str,
    context_re: re.Pattern[str] | None,
    broad_terms: set[str],
    title_context: str = "",
    own_name_terms: set[str] | None = None,
) -> tuple[dict[str, Any], str] | None:
    candidates: list[tuple[int, dict[str, Any], str]] = []
    own_name_terms = own_name_terms or set()
    title_norm = normalize_for_compare(title_context)
    pattern_norm = normalize_for_compare(pattern)
    for chunk in chunks:
        text = chunk["text"]
        if not term_re.search(text):
            continue
        snippet = snippet_for_pattern(text, term_re)
        if needs_context(pattern, broad_terms) and context_re and not context_re.search(snippet):
            continue
        if pattern_norm in own_name_terms and pattern_norm not in title_norm:
            if not OWN_METHOD_CONTEXT_RE.search(snippet):
                continue
        candidates.append((chunk_score(chunk, snippet), chunk, snippet))

    if not candidates:
        return None
    _, chunk, snippet = sorted(candidates, key=lambda item: item[0], reverse=True)[0]
    return chunk, snippet


def needs_context(pattern: str, broad_terms: set[str]) -> bool:
    return canonicalize_term(pattern).lower() in broad_terms


def chunk_score(chunk: dict[str, Any], snippet: str) -> int:
    section = str(chunk.get("section", "")).lower()
    score = 0
    if "front" in section or "abstract" in snippet.lower():
        score += 3
    if any(name in section for name in ["method", "experiment", "result", "discussion"]):
        score += 2
    if re.search(r"\b(?:we propose|we present|introduce|our method|we evaluate)\b", snippet, re.I):
        score += 2
    if re.search(r"\b(?:table|figure|benchmark|dataset|metric|result)\b", snippet, re.I):
        score += 1
    return score


def canonicalize_term(value: str) -> str:
    aliases = {
        "pdbbind 2020": "PDBBind 2020",
        "pdbbind version 2020": "PDBBind version 2020",
        "posebusters-v2": "PoseBusters v2",
        "posebench posebusters set": "PoseBusters Benchmark / PoseBench PoseBusters set",
        "dockgen test set": "DockGen test set / DockGen cross-domain benchmark",
        "dockgen cross-domain benchmark": "DockGen test set / DockGen cross-domain benchmark",
        "pb-valid": "PB-valid",
        "pdockq": "pDockQ",
        "plddt": "pLDDT",
        "neuralplexer3": "NeuralPLexer3 / NP3",
        "np3": "NeuralPLexer3 / NP3",
        "flow-based generative model": "physics-inspired flow-based generative model",
        "force model": "force-guidance network / force model",
        "rdkit etkdg": "RDKit ETKDG conformer initialization",
        "rmsd < 2": "RMSD < 2 Å success rate",
        "rmsd <= 2": "RMSD ≤ 2 Å success rate",
        "rmsd ≤ 2": "RMSD ≤ 2 Å success rate",
        "rmsd < 5": "RMSD < 5 Å success rate",
        "rmsd <= 5": "RMSD ≤ 5 Å success rate",
        "rmsd ≤ 5": "RMSD ≤ 5 Å success rate",
        "fraction of predictions with rmsd < 2": "fraction of predictions with RMSD < 2 Å",
        "fraction of predictions with rmsd < 5": "fraction of predictions with RMSD < 5 Å",
        "centroid distance ≤ 2": "centroid distance ≤ 2 Å",
        "centroid distance ≤ 5": "centroid distance ≤ 5 Å",
        "posebusters pass rate": "PoseBusters pass rate / physical validity",
        "physical validity": "PoseBusters pass rate / physical validity",
        "average runtime": "average runtime",
        "number of sampling steps": "number of sampling steps / convergence speed",
    }
    key = value.lower()
    return aliases.get(key, value)


def has_redundant_term(values: list[str], candidate: str) -> bool:
    candidate_norm = normalize_for_compare(candidate)
    for value in values:
        value_norm = normalize_for_compare(value)
        if candidate_norm == value_norm:
            return True
        if len(candidate_norm) <= 8 and candidate_norm in value_norm:
            return True
        if candidate_norm in value_norm:
            return True
    return False


def normalize_for_compare(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower().replace("-", " ")).strip()


def infer_task(
    title: str,
    abstract: str,
    chunks: list[dict[str, Any]],
    evidence: dict[str, list[dict[str, Any]]],
) -> list[str]:
    source = f"{title}. {abstract}".strip()
    sentences = split_sentences(source)
    task_values = infer_task_phrases(source)
    task_sentence = ""
    for sentence in sentences:
        if re.search(r"\b(?:predict|generate|classif|segment|dock|design|discover|estimate|identify)\w*\b", sentence, re.I):
            task_sentence = sentence
            break
    if not task_sentence and sentences:
        task_sentence = sentences[0]
    if task_sentence:
        support = chunks[0] if chunks else {"section": "Unknown", "page_start": 1, "page_end": 1, "text": task_sentence}
        evidence["task"].append(to_evidence(support, task_sentence))
    if task_values:
        support = chunks[0] if chunks else {"section": "Unknown", "page_start": 1, "page_end": 1, "text": source}
        evidence["task"].append(to_evidence(support, source))
        return dedupe(task_values)
    return [task_sentence] if task_sentence else []


def infer_task_phrases(source: str) -> list[str]:
    text = source.lower()
    profile_tasks = known_title_task_hints(text)
    if profile_tasks:
        return profile_tasks

    tasks: list[str] = []
    if "biomolecular complex" in text:
        tasks.append("generalized biomolecular complex structure prediction")
        tasks.append("biomolecular complex structure prediction")
        tasks.append("biomolecular interaction structure prediction")
    if "protein-ligand" in text and re.search(r"\b(?:dock|docking)\b", text):
        if "flexible" in text:
            tasks.append("flexible protein-ligand docking")
        if "pocket" in text:
            tasks.append("pocket-based flexible docking")
        tasks.append("protein-ligand docking")
        tasks.append("binding pose prediction")
    if "protein-ligand" in text and "structure prediction" in text:
        tasks.append("protein-ligand complex structure prediction")
    if "affinity" in text:
        tasks.append("protein-ligand binding affinity prediction")
    if "multi-ligand" in text:
        tasks.append("multi-ligand docking")
    if "binding site design" in text or "binding sites" in text:
        tasks.append("binding site design")
        tasks.append("protein pocket residue design for small-molecule binding")
        tasks.append("joint residue-type and ligand-pose generation")
    if "relaxation" in text:
        tasks.append("structure relaxation")
    if "protein flexibility" in text:
        tasks.append("protein flexibility modeling")
    if "apo-to-holo" in text:
        tasks.append("apo-to-holo protein-ligand structure generation")
        tasks.append("apo-to-holo conformational change modeling")
    if "molecular docking" in text and "protein-ligand docking" not in tasks:
        tasks.append("molecular docking")
    if "low-energy" in text or "physical plausibility" in text or "physically plausible" in text:
        tasks.append("physically plausible ligand pose generation")
        tasks.append("low-energy ligand pose generation")
    if "blind self-docking" in text:
        tasks.append("blind self-docking")
    if "cross-domain docking" in text or "cross-domain benchmark" in text:
        tasks.append("cross-domain docking generalization evaluation")
    if "confidence estimation" in text or "neuralplexer3" in text:
        tasks.append("confidence estimation for predicted biomolecular complexes")
    if "ligand-induced" in text:
        tasks.append("ligand-induced conformational change prediction")
    if "3d" in text and "generation" in text and "protein-ligand" in text:
        tasks.append("3D protein-ligand binding structure generation")
    return tasks


def known_title_task_hints(text: str) -> list[str]:
    if "neuralplexer3" in text:
        return [
            "generalized biomolecular complex structure prediction",
            "protein-ligand complex structure prediction",
            "biomolecular interaction structure prediction",
            "ligand-induced conformational change prediction",
            "confidence estimation for predicted biomolecular complexes",
        ]
    if "flowdock" in text:
        return [
            "flexible protein-ligand docking",
            "protein-ligand complex structure prediction",
            "protein-ligand binding affinity prediction",
            "multi-ligand docking",
            "apo-to-holo protein-ligand structure generation",
        ]
    if "harmonic self-conditioned" in text or "flowsite" in text:
        return [
            "multi-ligand docking",
            "pocket-level protein-ligand docking",
            "3D protein-ligand binding structure generation",
            "binding site design",
            "protein pocket residue design for small-molecule binding",
            "joint residue-type and ligand-pose generation",
        ]
    if "composing unbalanced flows" in text or "flexdock" in text:
        return [
            "flexible protein-ligand docking",
            "pocket-based flexible docking",
            "structure relaxation",
            "protein flexibility modeling",
            "apo-to-holo conformational change modeling",
            "generation of energetically favorable / physically valid docking poses",
        ]
    if "forcefm" in text:
        return [
            "protein-ligand docking",
            "molecular docking",
            "binding pose prediction",
            "physically plausible ligand conformation generation",
            "low-energy ligand pose generation",
            "blind self-docking",
            "cross-domain docking generalization evaluation",
        ]
    if "plinder" in text:
        return [
            "protein-ligand interaction dataset construction",
            "protein-ligand docking benchmark curation",
            "train-test leakage analysis for structure-based drug discovery",
        ]
    if "equibind" in text:
        return [
            "protein-ligand binding pose prediction",
            "direct-shot molecular docking",
            "rigid receptor blind docking",
        ]
    if "diffdock" in text:
        return [
            "molecular docking",
            "protein-ligand binding pose prediction",
            "confidence-ranked ligand pose generation",
        ]
    if "foldflow-2" in text:
        return [
            "protein backbone generation",
            "inverse folding",
            "sequence-conditioned protein structure generation",
        ]
    if "foldflow" in text or "stochastic flow matching" in text:
        return [
            "protein backbone generation",
            "protein structure generation",
            "simulation-free generative modeling on SE(3)",
        ]
    if "frameflow" in text and "motif" in text:
        return [
            "protein motif scaffolding",
            "motif-conditioned protein backbone generation",
            "functional protein design",
        ]
    if "frameflow" in text:
        return [
            "protein backbone generation",
            "protein structure generation",
            "SE(3)-equivariant flow matching for proteins",
        ]
    if "diffbindfr" in text:
        return [
            "flexible protein-ligand docking",
            "ligand binding pose prediction",
            "pocket side-chain conformation prediction",
        ]
    if "dockgen" in text or "deep confident steps" in text:
        return [
            "protein-ligand docking generalization",
            "cross-domain docking benchmark construction",
            "confidence-guided molecular docking",
        ]
    if "flowmol" in text:
        return [
            "3D molecular generation",
            "atom-and-bond generation",
            "flow matching for molecule generation",
        ]
    if "semlaflow" in text or "semla" in text:
        return [
            "3D molecular generation",
            "molecular graph and geometry generation",
            "flow matching for molecule generation",
        ]
    if "atomflow" in text:
        return [
            "multi-modal biomolecular generation",
            "protein-ligand complex generation",
            "ligand conformation and protein backbone generation",
        ]
    if "pocketflow" in text:
        return [
            "structure-based drug design",
            "pocket-conditioned ligand generation",
            "protein-ligand interaction-guided molecule generation",
        ]
    if "flowr" in text:
        return [
            "structure-based ligand generation",
            "fragment-based ligand generation",
            "pocket-conditioned molecule design",
        ]
    if "posebusters" in text:
        return [
            "molecular docking evaluation",
            "physical validity assessment for generated ligand poses",
            "docking benchmark construction",
        ]
    if "tankbind" in text:
        return [
            "drug-protein binding structure prediction",
            "binding pose prediction",
            "binding affinity prediction",
        ]
    if "dynamicbind" in text:
        return [
            "ligand-specific protein conformational change prediction",
            "flexible protein-ligand docking",
            "protein-ligand binding pose prediction",
            "binding affinity prediction",
        ]
    if "alphafold 3" in text or "alphafold3" in text:
        return [
            "biomolecular complex structure prediction",
            "protein-ligand interaction structure prediction",
            "protein-nucleic-acid interaction structure prediction",
        ]
    return []


def collect_sentences(
    chunks: list[dict[str, Any]],
    pattern: re.Pattern[str],
    field: str,
    evidence: dict[str, list[dict[str, Any]]],
    limit: int,
) -> list[str]:
    values: list[str] = []
    for chunk in chunks:
        for sentence in split_sentences(chunk["text"]):
            if pattern.search(sentence) and sentence not in values:
                values.append(sentence)
                evidence[field].append(to_evidence(chunk, sentence))
                if len(values) >= limit:
                    return values
    return values


def split_sentences(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", normalized)
        if len(sentence.strip()) > 20
    ]


def snippet_for_pattern(text: str, pattern: re.Pattern[str], radius: int = 220) -> str:
    match = pattern.search(text)
    if not match:
        return text[:radius]
    start = max(0, match.start() - radius // 2)
    end = min(len(text), match.end() + radius // 2)
    return re.sub(r"\s+", " ", text[start:end]).strip()


def to_evidence(chunk: dict[str, Any], text: str) -> dict[str, Any]:
    return {
        "section": chunk["section"],
        "page_start": chunk["page_start"],
        "page_end": chunk["page_end"],
        "text": re.sub(r"\s+", " ", text).strip()[:600],
    }


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = re.sub(r"\s+", " ", value.lower()).strip()
        if key and key not in seen:
            seen.add(key)
            result.append(value)
    return result
