from __future__ import annotations

from dataclasses import dataclass
from math import log


@dataclass(frozen=True)
class Document:
    doc_id: str
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float


def chunk_text(document: Document, *, max_words: int = 80, overlap_words: int = 10) -> list[Chunk]:
    words = document.text.split()
    if max_words <= overlap_words:
        raise ValueError("max_words must be greater than overlap_words")
    chunks: list[Chunk] = []
    step = max_words - overlap_words
    for index, start in enumerate(range(0, len(words), step)):
        chunk_words = words[start : start + max_words]
        if not chunk_words:
            continue
        chunks.append(
            Chunk(
                chunk_id=f"{document.doc_id}:{index}",
                doc_id=document.doc_id,
                text=" ".join(chunk_words),
                metadata=document.metadata,
            )
        )
        if start + max_words >= len(words):
            break
    return chunks


class KeywordRetriever:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks

    def search(self, query: str, *, k: int = 3) -> list[SearchResult]:
        query_terms = set(query.lower().split())
        results: list[SearchResult] = []
        for chunk in self.chunks:
            terms = set(chunk.text.lower().split())
            overlap = len(query_terms & terms)
            if overlap:
                score = overlap * idf_bonus(query_terms, self.chunks)
                results.append(SearchResult(chunk=chunk, score=score))
        return sorted(results, key=lambda result: result.score, reverse=True)[:k]


def rerank_by_overlap(query: str, results: list[SearchResult], *, k: int = 3) -> list[SearchResult]:
    query_terms = set(query.lower().split())
    reranked = [
        SearchResult(
            chunk=result.chunk,
            score=result.score + len(query_terms & set(result.chunk.text.lower().split())) * 0.25,
        )
        for result in results
    ]
    return sorted(reranked, key=lambda result: result.score, reverse=True)[:k]


def citation_coverage(answer: str, cited_chunks: list[Chunk]) -> float:
    answer_terms = set(answer.lower().split())
    cited_terms = set()
    for chunk in cited_chunks:
        cited_terms.update(chunk.text.lower().split())
    if not answer_terms:
        return 1.0
    return len(answer_terms & cited_terms) / len(answer_terms)


def idf_bonus(query_terms: set[str], chunks: list[Chunk]) -> float:
    if not chunks:
        return 1.0
    bonus = 0.0
    for term in query_terms:
        containing = sum(1 for chunk in chunks if term in set(chunk.text.lower().split()))
        if containing:
            bonus += log(1 + len(chunks) / containing)
    return max(1.0, bonus)
