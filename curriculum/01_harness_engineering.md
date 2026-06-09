# 01. Harness Engineering

Prompt engineering asks, "What text should I send?" Harness engineering asks, "How do I make model behavior reproducible, observable, testable, and safe to change?"

## Mental Model

A production LLM call should be a typed workflow:

1. Build a request from inputs, policy, context, and metadata.
2. Send it through a model client interface.
3. Record traces, tokens, latency, cost, model version, and errors.
4. Validate the response before it reaches users or tools.
5. Regression test the behavior whenever prompts, models, tools, or retrieval change.

## Practice

- Run `python labs/01_harness_engineering/run.py`.
- Add a canned fake response and assert its token usage.
- Add trace attributes for `feature`, `tenant_id`, and `workflow`.

## Mastery Checklist

- You can explain why a prompt string alone is not a production interface.
- You can replace a real model with a deterministic fake in tests.
- You can trace one request from user input to response validation.
- You can add a regression test before changing prompt behavior.
