from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentBudget:
    max_steps: int
    max_tool_calls: int
    max_tokens: int
    steps_used: int = 0
    tool_calls_used: int = 0
    tokens_used: int = 0

    def consume_step(self) -> None:
        self.steps_used += 1

    def consume_tool_call(self) -> None:
        self.tool_calls_used += 1

    def consume_tokens(self, tokens: int) -> None:
        self.tokens_used += tokens

    def termination_reason(self) -> str | None:
        if self.steps_used >= self.max_steps:
            return "step_budget_exhausted"
        if self.tool_calls_used >= self.max_tool_calls:
            return "tool_budget_exhausted"
        if self.tokens_used >= self.max_tokens:
            return "token_budget_exhausted"
        return None


@dataclass(frozen=True)
class AgentDecision:
    action: str
    tool_name: str | None = None
    arguments: dict[str, object] | None = None
    final_answer: str | None = None


class Guardrail:
    def __init__(self, blocked_phrases: list[str]) -> None:
        self.blocked_phrases = [phrase.lower() for phrase in blocked_phrases]

    def allowed(self, text: str) -> bool:
        lowered = text.lower()
        return not any(phrase in lowered for phrase in self.blocked_phrases)


def should_terminate(decision: AgentDecision, budget: AgentBudget) -> str | None:
    if decision.action == "final":
        return "final_answer"
    return budget.termination_reason()
