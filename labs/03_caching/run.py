from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from ai_engineering_basics.caching import PromptCache, SemanticCache


def main() -> None:
    prompt_cache = PromptCache()
    prompt = "Explain prompt caching vs semantic caching."

    key = prompt_cache.make_key(tenant_id="tenant-a", model="fake", prompt=prompt)
    prompt_cache.set(key, "Prompt caching reuses exact prompts or prefixes.")

    same_tenant_hit = prompt_cache.get(key)
    other_tenant_key = prompt_cache.make_key(tenant_id="tenant-b", model="fake", prompt=prompt)
    other_tenant_hit = prompt_cache.get(other_tenant_key)

    semantic_cache = SemanticCache(threshold=0.5)
    semantic_cache.set(
        tenant_id="tenant-a",
        query="How does prompt caching compare to semantic caching?",
        answer="Prompt caching is exact; semantic caching reuses similar queries.",
    )

    print("Prompt cache same-tenant hit:", same_tenant_hit)
    print("Prompt cache cross-tenant hit:", other_tenant_hit)
    print(
        "Semantic cache paraphrase hit:",
        semantic_cache.get(tenant_id="tenant-a", query="Compare semantic caching and prompt caching"),
    )


if __name__ == "__main__":
    main()
