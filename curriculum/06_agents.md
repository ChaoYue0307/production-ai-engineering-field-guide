# 06. Agents

Agents are loops that use models, memory, tools, and policies to pursue a task. The hard part is bounding the loop.

## Required Controls

- Step budget: prevents infinite reasoning loops.
- Tool budget: prevents runaway API or side-effect calls.
- Token budget: prevents uncontrolled spend.
- Termination conditions: final answer, impossible task, blocked permission, or budget exhausted.
- Guardrails: block unsafe instructions and disallowed tool use.
- Degraded-mode UX: explain what still works when a model, tool, or retrieval source fails.

## Common Failure Modes

- Hallucinated tool calls.
- Repeating the same failed tool call.
- Continuing after enough evidence exists.
- Ignoring user permission boundaries.
- Producing confident final answers after tool failure.

## Practice

- Run `python labs/08_agent_budgets/run.py`.
- Lower `max_steps` and observe the termination reason.
- Add a blocked phrase to the guardrail.

## Mastery Checklist

- You can define an agent loop without unbounded execution.
- You can decide which failures should stop the agent.
- You can explain budget exhaustion to a user without exposing internals.
- You can test loop termination.
