import re
from typing import Any


CARD_FIELD_KEYS = [
    "task",
    "datasets",
    "models_or_methods",
    "baselines",
    "metrics",
    "main_result",
    "limitations",
    "code_availability",
]

VERIFICATION_STATUSES = {"supported", "weak", "unsupported", "missing"}


def build_verification_statuses(card: dict[str, Any]) -> dict[str, str]:
    evidence = card.get("evidence", {})
    return {
        field: verify_field(card.get(field, []), evidence.get(field, []))
        for field in CARD_FIELD_KEYS
    }


def verify_field(values: list[str], evidence_items: list[dict[str, Any]]) -> str:
    clean_values = [value.strip() for value in values if value.strip()]
    if not clean_values:
        return "missing"
    if not evidence_items:
        return "unsupported"

    evidence_text = " ".join(str(item.get("text", "")) for item in evidence_items)
    evidence_norm = normalize(evidence_text)
    if not evidence_norm:
        return "unsupported"

    supported = 0
    weak = 0
    for value in clean_values:
        match_level = match_value_to_evidence(value, evidence_norm)
        if match_level == "supported":
            supported += 1
        elif match_level == "weak":
            weak += 1

    if supported == len(clean_values):
        return "supported"
    if supported or weak:
        return "weak"
    return "unsupported"


def match_value_to_evidence(value: str, evidence_norm: str) -> str:
    value_norm = normalize(value)
    if not value_norm:
        return "unsupported"

    if value_norm in evidence_norm:
        return "supported"

    value_tokens = meaningful_tokens(value_norm)
    if not value_tokens:
        return "unsupported"

    evidence_tokens = set(meaningful_tokens(evidence_norm))
    overlap = len(value_tokens & evidence_tokens) / len(value_tokens)

    if overlap >= 0.75:
        return "supported"
    if overlap >= 0.35:
        return "weak"
    return "unsupported"


def meaningful_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.split(r"\s+", value)
        if len(token) >= 3 and token not in {"the", "and", "for", "with", "from", "this", "that"}
    }


def normalize(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()
