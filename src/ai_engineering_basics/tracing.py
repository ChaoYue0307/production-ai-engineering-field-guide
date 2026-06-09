from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from time import perf_counter
from typing import Iterator
from uuid import uuid4


@dataclass
class TraceSpan:
    name: str
    span_id: str = field(default_factory=lambda: uuid4().hex)
    parent_id: str | None = None
    start_ms: float = field(default_factory=lambda: perf_counter() * 1000)
    end_ms: float | None = None
    attributes: dict[str, object] = field(default_factory=dict)
    error: str | None = None

    @property
    def duration_ms(self) -> float | None:
        if self.end_ms is None:
            return None
        return self.end_ms - self.start_ms

    def finish(self, *, error: Exception | None = None) -> None:
        self.end_ms = perf_counter() * 1000
        if error is not None:
            self.error = f"{type(error).__name__}: {error}"


class TraceRecorder:
    def __init__(self) -> None:
        self.spans: list[TraceSpan] = []
        self._stack: list[TraceSpan] = []

    @contextmanager
    def span(self, name: str, **attributes: object) -> Iterator[TraceSpan]:
        parent = self._stack[-1] if self._stack else None
        span = TraceSpan(name=name, parent_id=parent.span_id if parent else None)
        span.attributes.update(attributes)
        self.spans.append(span)
        self._stack.append(span)
        try:
            yield span
        except Exception as exc:
            span.finish(error=exc)
            raise
        else:
            span.finish()
        finally:
            self._stack.pop()

    def summary(self) -> list[dict[str, object]]:
        return [
            {
                "name": span.name,
                "duration_ms": round(span.duration_ms or 0, 2),
                "attributes": span.attributes,
                "error": span.error,
            }
            for span in self.spans
        ]
