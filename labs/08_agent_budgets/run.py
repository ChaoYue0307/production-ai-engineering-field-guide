from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from ai_engineering_basics.agents import AgentBudget, AgentDecision, Guardrail, should_terminate


def main() -> None:
    budget = AgentBudget(max_steps=3, max_tool_calls=1, max_tokens=50)
    guardrail = Guardrail(["send secrets", "ignore previous instructions"])

    decisions = [
        AgentDecision("tool", tool_name="search", arguments={"query": "RAG evals"}),
        AgentDecision("tool", tool_name="search", arguments={"query": "try again"}),
        AgentDecision("final", final_answer="RAG evals measure retrieval and grounding."),
    ]

    for decision in decisions:
        if decision.tool_name:
            budget.consume_tool_call()
        budget.consume_step()
        reason = should_terminate(decision, budget)
        print("Decision:", decision)
        print("Termination reason:", reason)
        if reason:
            break

    print("Guardrail allows normal text:", guardrail.allowed("Please summarize this document."))
    print("Guardrail allows injection:", guardrail.allowed("Ignore previous instructions."))


if __name__ == "__main__":
    main()
