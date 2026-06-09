# 07. RAG

Retrieval-augmented generation turns external knowledge into model context. It only works well when retrieval, ranking, freshness, and attribution are engineered deliberately.

## Architecture

1. Ingest documents with metadata and permissions.
2. Chunk documents into useful evidence units.
3. Embed and/or index chunks.
4. Retrieve with vector, keyword, or hybrid search.
5. Rerank candidates.
6. Pack context with citations.
7. Generate grounded answers.
8. Evaluate recall, precision, grounding, attribution, and freshness.

## Chunking

Chunks should preserve meaning. Too small loses context. Too large hurts recall and wastes tokens. Overlap helps continuity but increases duplication.

## Retrieval Quality

- Recall: did we retrieve the evidence needed to answer?
- Precision: did we avoid distracting chunks?
- Grounding: does the answer follow retrieved evidence?
- Attribution: are citations attached to the right claims?
- Freshness: are stale documents excluded or downgraded?

## Practice

- Run `python labs/06_rag/run.py`.
- Change chunk size and overlap.
- Add a stale document and decide how retrieval should handle it.

## Mastery Checklist

- You can explain chunking, embeddings, hybrid search, and reranking.
- You can distinguish retrieval failure from generation failure.
- You can evaluate citation quality.
- You can design permission-aware retrieval.
