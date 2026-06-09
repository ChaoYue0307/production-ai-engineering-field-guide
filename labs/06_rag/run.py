from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from ai_engineering_basics.rag import (
    Document,
    KeywordRetriever,
    chunk_text,
    citation_coverage,
    rerank_by_overlap,
)


def main() -> None:
    docs = [
        Document(
            "doc-serving",
            "Continuous batching improves throughput by keeping accelerators busy as requests arrive.",
            {"freshness": "current"},
        ),
        Document(
            "doc-cache",
            "Prompt caching reuses stable prompt prefixes while semantic caching reuses similar answers.",
            {"freshness": "current"},
        ),
    ]
    chunks = [chunk for doc in docs for chunk in chunk_text(doc, max_words=12, overlap_words=2)]
    retriever = KeywordRetriever(chunks)

    query = "How does continuous batching improve throughput?"
    results = rerank_by_overlap(query, retriever.search(query, k=5), k=2)
    answer = "Continuous batching improves throughput by keeping accelerators busy."

    print("Retrieved:", [(result.chunk.chunk_id, round(result.score, 2)) for result in results])
    print("Citation coverage:", round(citation_coverage(answer, [r.chunk for r in results]), 2))


if __name__ == "__main__":
    main()
