# Learning Guide

Use this repo as a practice system, not a reading list. The fastest path is to run code, break one assumption, add one check, and explain the tradeoff.

## The 7-Day Fast Track

| Time | Focus | Run | Ship |
| --- | --- | --- | --- |
| Day 1 | Harness and context | `python labs/01_harness_engineering/run.py` and `python labs/02_context_engineering/run.py` | A traced model request and priority-based context packing. |
| Day 2 | Caching and structured output | `python labs/03_caching/run.py` and `python labs/04_structured_outputs/run.py` | A tenant-safe cache key and schema failure you can explain. |
| Day 3 | Tools and agents | `python labs/05_tool_calling/run.py` and `python labs/08_agent_budgets/run.py` | A safe retry path and an agent termination rule. |
| Day 4 | RAG and evals | `python labs/06_rag/run.py` and `python labs/07_evals_observability/run.py` | One adversarial eval for stale retrieval, malformed JSON, or prompt injection. |
| Day 5 | Inference and safety | `python labs/09_inference_stack/run.py` and `python labs/10_safety_tenancy/run.py` | A latency/memory explanation and a blocked cross-tenant case. |
| Day 6-7 | Capstone | `python examples/capstone_assistant.py` and `pytest` | One capstone improvement and one regression test. |

## The Practice Loop

For every module:

1. Read the matching file in `curriculum/`.
2. Run the lab.
3. Change one assumption: a budget, schema, cache key, chunk size, route rule, or safety policy.
4. Run `pytest`.
5. Explain what broke and why.
6. Add one test or eval that catches the failure.

## Mastery Rubric

You understand a topic when you can do all six:

- Explain the concept, failure mode, and tradeoff in two minutes.
- Implement the pattern or point to the implementation in `src/ai_engineering_basics/`.
- Break the system in a controlled way.
- Measure the failure with a trace, eval, cost event, or test.
- Decide when the technique is the wrong tool.
- Recover safely with retry, repair, fallback, clarification, degradation, or termination.

## High-Quality Learning Rules

- Prefer small experiments over passive reading.
- Keep every module tied to one production failure mode.
- Write down the tradeoff after each lab: latency, quality, cost, reliability, or safety.
- Treat evals and tests as part of the learning, not as cleanup.
- Revisit the capstone after every two modules and improve one part of the system.

## Capstone Goal

By the end, you should be able to explain and modify a small AI assistant that combines:

- Model routing and fallback.
- Prompt-injection checks and tenant boundaries.
- Retrieval, reranking, context packing, and citations.
- Prompt caching and cache safety.
- Structured output validation.
- Tool contracts and idempotency.
- Agent budgets and termination.
- Traces, token/cost attribution, and regression evals.
