from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    input: str
    expected_terms: tuple[str, ...]
    forbidden_terms: tuple[str, ...] = ()
    metadata: dict[str, str] | None = None


@dataclass(frozen=True)
class EvalResult:
    case_id: str
    passed: bool
    score: float
    reasons: tuple[str, ...]


class EvalRunner:
    def __init__(self, generate: Callable[[str], str]) -> None:
        self.generate = generate

    def run(self, cases: list[EvalCase]) -> list[EvalResult]:
        return [score_case(case, self.generate(case.input)) for case in cases]


def score_case(case: EvalCase, output: str) -> EvalResult:
    lowered = output.lower()
    expected_hits = [term for term in case.expected_terms if term.lower() in lowered]
    forbidden_hits = [term for term in case.forbidden_terms if term.lower() in lowered]
    expected_score = len(expected_hits) / len(case.expected_terms) if case.expected_terms else 1.0
    penalty = 0.25 * len(forbidden_hits)
    score = max(0.0, expected_score - penalty)
    reasons: list[str] = []
    if len(expected_hits) < len(case.expected_terms):
        missing = sorted(set(case.expected_terms) - set(expected_hits))
        reasons.append(f"Missing expected terms: {missing}")
    if forbidden_hits:
        reasons.append(f"Included forbidden terms: {forbidden_hits}")
    return EvalResult(case_id=case.case_id, passed=score >= 1.0, score=score, reasons=tuple(reasons))


def aggregate(results: list[EvalResult]) -> dict[str, float]:
    if not results:
        return {"pass_rate": 0.0, "mean_score": 0.0}
    return {
        "pass_rate": sum(result.passed for result in results) / len(results),
        "mean_score": sum(result.score for result in results) / len(results),
    }
