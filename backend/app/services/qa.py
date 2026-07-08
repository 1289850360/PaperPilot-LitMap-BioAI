import re
from collections import Counter
from typing import Any

from .extractor import split_sentences, to_evidence


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "were",
    "was",
    "are",
    "what",
    "which",
    "how",
    "does",
    "did",
    "paper",
    "论文",
    "什么",
    "哪些",
    "如何",
}


def answer_question(question: str, chunks: list[dict[str, Any]]) -> dict[str, Any]:
    ranked = rank_chunks(question, chunks)[:4]
    citations = [to_evidence(chunk, best_sentence(question, chunk["text"])) for chunk in ranked]

    if not ranked:
        return {
            "answer": "I could not find enough relevant evidence in this paper.",
            "citations": [],
        }

    answer_parts = []
    for citation in citations[:2]:
        page = citation["page_start"]
        answer_parts.append(f"{citation['text']} [p. {page}, {citation['section']}]")
    return {
        "answer": " ".join(answer_parts),
        "citations": citations,
    }


def rank_chunks(question: str, chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    query_terms = tokenize(question)
    if not query_terms:
        return chunks[:4]
    query_counter = Counter(query_terms)
    scored = []
    for chunk in chunks:
        chunk_counter = Counter(tokenize(chunk["text"]))
        score = sum(query_counter[term] * chunk_counter.get(term, 0) for term in query_counter)
        if score > 0:
            scored.append((score, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored]


def best_sentence(question: str, text: str) -> str:
    terms = set(tokenize(question))
    candidates = split_sentences(text)
    if not candidates:
        return text[:500]
    best = max(candidates, key=lambda sentence: len(terms.intersection(tokenize(sentence))))
    return best


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[\w\u4e00-\u9fff]+", text.lower())
    return [token for token in tokens if token not in STOPWORDS and len(token) > 1]
