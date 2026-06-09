from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


@dataclass(frozen=True)
class LLMRequest:
    model: str
    messages: tuple[Message, ...]
    temperature: float = 0.0
    max_tokens: int = 512
    metadata: Mapping[str, str] = field(default_factory=dict)

    def prompt_text(self) -> str:
        return "\n".join(f"{message.role}: {message.content}" for message in self.messages)


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    usage: TokenUsage
    finish_reason: str = "stop"
    metadata: Mapping[str, str] = field(default_factory=dict)


class ModelClient(Protocol):
    def complete(self, request: LLMRequest) -> LLMResponse:
        """Return a model response for a typed request."""


class FakeModelClient:
    """Deterministic model client for local labs and tests."""

    def __init__(self, canned_responses: Mapping[str, str] | None = None) -> None:
        self.canned_responses = dict(canned_responses or {})
        self.requests: list[LLMRequest] = []

    def complete(self, request: LLMRequest) -> LLMResponse:
        self.requests.append(request)
        prompt = request.prompt_text()
        text = self._lookup_response(prompt, request.messages)
        return LLMResponse(
            text=text,
            model=request.model,
            usage=TokenUsage(
                prompt_tokens=count_tokens(prompt),
                completion_tokens=count_tokens(text),
            ),
            metadata={"client": "fake"},
        )

    def _lookup_response(self, prompt: str, messages: Sequence[Message]) -> str:
        for key, response in self.canned_responses.items():
            if key in prompt:
                return response
        latest_user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        return f"Fake response: {latest_user[:160]}"


def count_tokens(text: str) -> int:
    """Cheap approximation for labs; real systems should use provider tokenizers."""

    return len(text.split())
