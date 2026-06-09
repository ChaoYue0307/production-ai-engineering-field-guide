from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from time import time


def stable_cache_key(*parts: str) -> str:
    joined = "\x1f".join(parts)
    return sha256(joined.encode("utf-8")).hexdigest()


@dataclass
class CacheEntry:
    value: str
    created_at: float = field(default_factory=time)
    ttl_seconds: float | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def expired(self) -> bool:
        return self.ttl_seconds is not None and time() - self.created_at > self.ttl_seconds


class PromptCache:
    """Exact cache keyed by tenant, model, and full prompt."""

    def __init__(self) -> None:
        self._entries: dict[str, CacheEntry] = {}

    def make_key(self, *, tenant_id: str, model: str, prompt: str) -> str:
        return stable_cache_key(tenant_id, model, prompt)

    def get(self, key: str) -> str | None:
        entry = self._entries.get(key)
        if entry is None:
            return None
        if entry.expired():
            del self._entries[key]
            return None
        return entry.value

    def set(
        self,
        key: str,
        value: str,
        *,
        ttl_seconds: float | None = None,
        metadata: dict[str, str] | None = None,
    ) -> None:
        self._entries[key] = CacheEntry(value, ttl_seconds=ttl_seconds, metadata=metadata or {})


class SemanticCache:
    """Tiny semantic-cache teaching aid based on token overlap."""

    def __init__(self, threshold: float = 0.75) -> None:
        self.threshold = threshold
        self._entries: list[tuple[str, str, str, str]] = []

    def get(self, *, tenant_id: str, query: str) -> str | None:
        for entry_tenant, entry_query, answer, _source in self._entries:
            if entry_tenant != tenant_id:
                continue
            if jaccard_similarity(query, entry_query) >= self.threshold:
                return answer
        return None

    def set(self, *, tenant_id: str, query: str, answer: str, source: str = "model") -> None:
        self._entries.append((tenant_id, query, answer, source))


def jaccard_similarity(left: str, right: str) -> float:
    left_tokens = set(left.lower().split())
    right_tokens = set(right.lower().split())
    if not left_tokens and not right_tokens:
        return 1.0
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
