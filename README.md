# AI Engineering Basics

A Python-first learning repo for becoming a production-minded AI engineer. It is both a curriculum and a runnable lab environment: each topic includes a mental model, exercises, and small pieces of code you can inspect, test, and extend.

The emphasis is harness engineering, context engineering, reliability, observability, retrieval, cost, safety, and inference tradeoffs rather than prompt tricks alone.

Start with the [Learning Guide](LEARNING_GUIDE.md) if you want the fastest path through the material. It gives you a 7-day plan, a practice loop, and a mastery rubric for knowing when a concept has actually stuck.

## Web Learning Guide

Browse the interactive learning webpage:

[Production AI Engineering Field Guide](https://chaoyue0307.github.io/production-ai-engineering-field-guide/)

The webpage includes the roadmap, filterable module cards, copyable practice commands, progress checkboxes, and the capstone assistant flow.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

Run a lab:

```bash
python labs/01_harness_engineering/run.py
python labs/06_rag/run.py
```

The default code uses deterministic fake model clients, so you can learn without paid APIs. Copy `.env.example` to `.env` later if you want to adapt the interfaces to real providers.

Open the webpage locally:

```bash
open site/index.html
```

## Learning Path

1. Harness engineering: reproducible requests, typed responses, traces, and tests.
2. Context engineering: structured messages, packing, retrieval insertion, and truncation.
3. Caching: prompt caching, semantic caching, tenant scoping, freshness, and invalidation.
4. Inference stack: KV cache, prefill vs. decode, batching, paged attention, speculative decoding, quantization, and distillation.
5. Structured output: schemas, validation, repair loops, fallback chains, and failure handling.
6. Tool calling: tool contracts, argument validation, idempotency, and hallucinated call prevention.
7. Agents: loop budgets, tool budgets, guardrails, termination conditions, and degraded-mode UX.
8. RAG: chunking, embeddings/search, hybrid retrieval, reranking, freshness, grounding, attribution, and citations.
9. Evals: golden sets, adversarial tests, regression tests, LLM-as-judge, and human review.
10. Observability and cost: traces, spans, tokens, latency, errors, drift, and attribution by feature, workflow, tenant, and journey.
11. Safety and tenancy: prompt injection defense, data leakage prevention, permission boundaries, cache safety, and context contamination prevention.
12. Production tradeoffs: latency, quality, cost, reliability, routing, fallback, and failure modes.

## Repo Map

- `curriculum/`: concept notes, exercises, and mastery checklists.
- `labs/`: runnable scripts for hands-on practice.
- `src/ai_engineering_basics/`: reusable primitives used by the labs.
- `evals/`: example golden sets and adversarial cases.
- `examples/`: small end-to-end demos that combine multiple concepts.
- `tests/`: regression tests for the learning primitives.

## How To Master A Module

For each module:

1. Read the note in `curriculum/`.
2. Run the matching lab in `labs/`.
3. Change one assumption, such as a budget, schema, chunk size, or fallback rule.
4. Run `pytest`.
5. Explain the tradeoff in your own words.
6. Add one new test case that would catch a realistic production failure.

The quality bar is simple: for each topic, you should be able to explain it, implement it, break it, measure the failure, decide when it is the wrong tool, and recover safely.

## Capstone Target

By the end, you should be able to build and explain a small production-style AI assistant with:

- A typed model harness and trace logs.
- Context packing and retrieval.
- Prompt and semantic cache safety.
- Structured output validation and repair.
- Tool contracts and idempotent execution.
- Agent budgets and termination rules.
- Golden-set and adversarial evals.
- Cost attribution and latency reporting.
- Tenant isolation and prompt-injection checks.
- Graceful model fallback and degraded-mode UX.
