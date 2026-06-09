# 09. Observability And Cost

LLM observability should be a first-class discipline. Without traces, spans, tokens, latency, errors, and drift signals, failures look random and costs are impossible to explain.

## What To Record

- Trace ID and span hierarchy.
- Model, provider, version, and route decision.
- Prompt, completion, and total tokens.
- Latency by step: retrieval, model, tools, validation, repair.
- Error type and fallback path.
- Safety decisions and blocked actions.
- Cost attributed to feature, workflow, tenant, and user journey.

## Drift Signals

Watch for:

- Rising validation failures.
- Longer outputs.
- Lower retrieval citation coverage.
- Higher fallback rate.
- More tool errors.
- Golden-set score drops.

## Practice

- Run `python labs/07_evals_observability/run.py`.
- Add cost attribution by tenant.
- Add a span around schema validation.

## Mastery Checklist

- You can inspect a trace and identify the expensive step.
- You can attribute cost beyond model name.
- You can define alerts for quality and reliability drift.
- You can explain why aggregate token cost is not enough.
