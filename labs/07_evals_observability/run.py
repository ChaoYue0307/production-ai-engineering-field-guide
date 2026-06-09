from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from ai_engineering_basics.evals import EvalCase, EvalRunner, aggregate
from ai_engineering_basics.observability import CostEvent, CostTracker, estimate_cost
from ai_engineering_basics.tracing import TraceRecorder


def generate(answer: str) -> str:
    if "cache" in answer.lower():
        return "Prompt caching is exact. Semantic caching reuses similar queries."
    return "Use traces to record latency, tokens, errors, and cost."


def main() -> None:
    trace = TraceRecorder()
    with trace.span("eval.run", dataset="golden"):
        cases = [
            EvalCase("cache-1", "Compare caches", ("prompt caching", "semantic caching")),
            EvalCase("obs-1", "What should traces record?", ("latency", "tokens", "cost")),
        ]
        results = EvalRunner(generate).run(cases)

    tracker = CostTracker()
    tracker.record(
        CostEvent(
            feature="evals",
            workflow="regression",
            tenant_id="local",
            user_journey="learning",
            model="fake",
            input_tokens=300,
            output_tokens=120,
            cost_usd=estimate_cost(
                input_tokens=300,
                output_tokens=120,
                input_cost_per_1m=0.15,
                output_cost_per_1m=0.60,
            ),
        )
    )

    print("Eval results:", results)
    print("Aggregate:", aggregate(results))
    print("Cost by feature:", tracker.by_dimension("feature"))
    print("Trace:", trace.summary())


if __name__ == "__main__":
    main()
