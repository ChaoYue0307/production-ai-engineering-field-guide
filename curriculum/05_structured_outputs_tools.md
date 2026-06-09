# 05. Structured Outputs And Tools

Structured output is a contract, not a hope. Tool calling is a distributed system boundary, not just a model feature.

## Structured Output Failure Modes

- The model returns prose around JSON.
- Required fields are missing.
- Types are wrong.
- Enums contain unsupported values.
- The schema is valid but semantically unsafe.

Production systems use validation, repair, fallback, and explicit failure states.

## Tool Calling Reliability

Every tool needs:

- A name and narrow purpose.
- A schema for arguments.
- Runtime validation.
- Authorization checks.
- Idempotency for retries.
- Clear success and error shapes.

## Practice

- Run `python labs/04_structured_outputs/run.py`.
- Run `python labs/05_tool_calling/run.py`.
- Add a new enum field and watch validation fail before repair.
- Add an idempotency key and retry the same tool call.

## Mastery Checklist

- You can build a schema validation and repair loop.
- You can reject hallucinated tool names.
- You can explain why argument validation must happen outside the model.
- You can make a tool safe to retry.
