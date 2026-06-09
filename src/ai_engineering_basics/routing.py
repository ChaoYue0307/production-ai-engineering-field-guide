from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelProfile:
    name: str
    quality: float
    cost_per_1k_tokens: float
    p95_latency_ms: float
    supports_tools: bool = True
    supports_json: bool = True
    available: bool = True


@dataclass(frozen=True)
class RouteRequest:
    needs_tools: bool = False
    needs_json: bool = False
    max_cost_per_1k_tokens: float | None = None
    max_p95_latency_ms: float | None = None
    min_quality: float = 0.0


class ModelRouter:
    def __init__(self, profiles: Iterable[ModelProfile]) -> None:
        self.profiles = list(profiles)

    def choose(self, request: RouteRequest) -> ModelProfile | None:
        candidates = [profile for profile in self.profiles if profile.available]
        if request.needs_tools:
            candidates = [profile for profile in candidates if profile.supports_tools]
        if request.needs_json:
            candidates = [profile for profile in candidates if profile.supports_json]
        if request.max_cost_per_1k_tokens is not None:
            candidates = [
                profile
                for profile in candidates
                if profile.cost_per_1k_tokens <= request.max_cost_per_1k_tokens
            ]
        if request.max_p95_latency_ms is not None:
            candidates = [
                profile for profile in candidates if profile.p95_latency_ms <= request.max_p95_latency_ms
            ]
        candidates = [profile for profile in candidates if profile.quality >= request.min_quality]
        return min(candidates, key=lambda p: (p.cost_per_1k_tokens, p.p95_latency_ms)) if candidates else None

    def fallback_chain(self, preferred: str) -> list[ModelProfile]:
        available = [profile for profile in self.profiles if profile.available]
        preferred_profiles = [profile for profile in available if profile.name == preferred]
        rest = sorted(
            [profile for profile in available if profile.name != preferred],
            key=lambda p: (-p.quality, p.cost_per_1k_tokens, p.p95_latency_ms),
        )
        return preferred_profiles + rest
