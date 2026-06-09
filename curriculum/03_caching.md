# 03. Caching

Caching lowers latency and cost, but it can return stale, unsafe, or cross-tenant data if designed casually.

## Prompt Caching

Prompt caching is exact or provider-assisted reuse of repeated prompt prefixes. It is strong when many requests share stable instructions, policies, or documents.

Strengths:

- Predictable correctness.
- Good for repeated system prompts and long static context.
- Lower safety risk when keys include tenant and policy version.

Weaknesses:

- Misses paraphrases.
- Sensitive to tiny prompt changes.
- Needs careful invalidation when policy or retrieved facts change.

## Semantic Caching

Semantic caching reuses answers for similar queries. It can save more cost but carries more correctness risk.

Use it for low-risk, stable, read-only answers. Avoid it for permissions, account data, fresh facts, legal/medical advice, or tool actions.

## Practice

- Run `python labs/03_caching/run.py`.
- Try removing tenant IDs from cache keys and explain the failure.
- Add TTLs for facts that can go stale.

## Mastery Checklist

- You can compare prompt caching and semantic caching.
- You can define safe cache keys.
- You can explain freshness, invalidation, and tenant isolation.
- You can identify when caching should be disabled.
