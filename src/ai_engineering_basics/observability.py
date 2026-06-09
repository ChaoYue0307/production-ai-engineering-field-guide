from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class CostEvent:
    feature: str
    workflow: str
    tenant_id: str
    user_journey: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


class CostTracker:
    def __init__(self) -> None:
        self.events: list[CostEvent] = []

    def record(self, event: CostEvent) -> None:
        self.events.append(event)

    def by_dimension(self, dimension: str) -> dict[str, float]:
        totals: defaultdict[str, float] = defaultdict(float)
        for event in self.events:
            totals[str(getattr(event, dimension))] += event.cost_usd
        return dict(totals)


def estimate_cost(
    *,
    input_tokens: int,
    output_tokens: int,
    input_cost_per_1m: float,
    output_cost_per_1m: float,
) -> float:
    return (input_tokens / 1_000_000) * input_cost_per_1m + (
        output_tokens / 1_000_000
    ) * output_cost_per_1m
