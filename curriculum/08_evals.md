# 08. Evals

Evals are the regression tests of AI systems. They should be treated as production infrastructure, not a one-time benchmark.

## Eval Types

- Golden sets: known inputs with expected behavior.
- Regression tests: cases that previously failed or are business critical.
- Adversarial tests: prompt injection, malformed inputs, ambiguity, and edge cases.
- LLM-as-judge: scalable review for subjective criteria, with calibration.
- Human evals: high-trust review for important quality and safety questions.

## Metrics

Use metrics that match the workflow:

- Retrieval recall and precision.
- Groundedness and citation quality.
- Structured output validity.
- Tool-call accuracy.
- Task success.
- Latency and cost budgets.
- Safety violation rate.

## Practice

- Run `python labs/07_evals_observability/run.py`.
- Add one adversarial case from `evals/adversarial_cases.jsonl`.
- Change the generator so one golden case fails.

## Mastery Checklist

- You can create a golden set for a workflow.
- You can explain when LLM-as-judge is useful and when it is risky.
- You can catch silent regressions before deployment.
- You can separate quality, safety, cost, and latency evals.
