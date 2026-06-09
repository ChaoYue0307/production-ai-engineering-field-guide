from __future__ import annotations

from dataclasses import dataclass

from ai_engineering_basics.models import Message, count_tokens


@dataclass(frozen=True)
class ContextBlock:
    name: str
    content: str
    priority: int
    source: str


def pack_context(blocks: list[ContextBlock], *, token_budget: int) -> list[ContextBlock]:
    packed: list[ContextBlock] = []
    used = 0
    for block in sorted(blocks, key=lambda item: item.priority, reverse=True):
        cost = count_tokens(block.content)
        if used + cost <= token_budget:
            packed.append(block)
            used += cost
    return packed


def build_messages(
    *,
    system_prompt: str,
    user_request: str,
    context_blocks: list[ContextBlock],
) -> tuple[Message, ...]:
    context_text = "\n\n".join(
        f"[{block.name} from {block.source}]\n{block.content}" for block in context_blocks
    )
    return (
        Message("system", system_prompt),
        Message("user", f"Context:\n{context_text}\n\nRequest:\n{user_request}"),
    )
