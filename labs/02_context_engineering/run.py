from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from ai_engineering_basics.context import ContextBlock, build_messages, pack_context


def main() -> None:
    blocks = [
        ContextBlock("policy", "Never expose secrets. Cite factual claims.", priority=100, source="system"),
        ContextBlock("fresh_doc", "Paged attention reduces KV cache fragmentation.", 80, "docs"),
        ContextBlock("chat_history", "The user is learning AI engineering basics.", 50, "memory"),
        ContextBlock("noisy_note", "A random unrelated note about cooking pasta.", 5, "notes"),
    ]

    packed = pack_context(blocks, token_budget=22)
    messages = build_messages(
        system_prompt="You are a concise AI engineering tutor.",
        user_request="Explain paged attention.",
        context_blocks=packed,
    )

    print("Packed blocks:", [block.name for block in packed])
    print("Final user message:\n", messages[-1].content)


if __name__ == "__main__":
    main()
