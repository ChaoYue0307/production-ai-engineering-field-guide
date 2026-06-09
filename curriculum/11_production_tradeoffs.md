# 11. Production Tradeoffs

AI engineering is choosing tradeoffs across latency, quality, cost, and reliability across the full stack.

## Tool Choice Tradeoffs

- Fine-tuning: good for style, narrow behavior, and domain adaptation; wrong for frequently changing facts or permissions.
- In-context learning: fast to iterate; wrong when prompts become huge, brittle, or expensive.
- RAG: good for fresh external knowledge; wrong when retrieval quality is poor or the task requires learned behavior.
- Distillation: good for cost and latency; wrong when rare edge cases from the teacher matter.
- Quantization: good for serving efficiency; wrong when quality regressions are unacceptable or unmeasured.

## Failure Modes To Design For

- Hallucinated tool calls.
- Malformed JSON.
- Stale retrieval.
- Runaway agents.
- Silent eval regressions.
- Cache contamination.
- Fallback models that lack required capabilities.
- Degraded UX that hides important uncertainty.

## Practice

- Run the capstone example in `examples/capstone_assistant.py`.
- Break one dependency and observe the fallback behavior.
- Add an eval that catches the failure before it reaches a user.

## Mastery Checklist

- You can justify model routing and fallback logic.
- You can identify the wrong tool for a problem.
- You can reason about latency, quality, cost, and reliability together.
- You can describe production failure modes and the guardrails that catch them.
