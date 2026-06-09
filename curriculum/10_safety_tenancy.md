# 10. Safety And Tenancy

AI systems must preserve permission boundaries even when the model is persuasive, confused, or attacked.

## Prompt Injection Defense

Prompt injection is untrusted text trying to override instructions, exfiltrate secrets, or force unsafe tools. Defenses include:

- Treat retrieved documents as data, not instructions.
- Separate system policy from evidence.
- Filter or flag suspicious content.
- Require authorization outside the model.
- Restrict tools by user and tenant.
- Prefer explicit allowlists over broad capabilities.

## Multi-Tenant Isolation

Tenant safety must apply to retrieval, caches, traces, logs, tool calls, and generated context. A cache hit is only safe if the key includes the right isolation dimensions.

## Practice

- Run `python labs/10_safety_tenancy/run.py`.
- Add a cross-tenant document ID and verify it is filtered.
- Try an injection phrase and observe the detection result.

## Mastery Checklist

- You can prevent cross-user context contamination.
- You can explain cache safety in a multi-tenant system.
- You can separate model judgment from permission enforcement.
- You can test prompt injection handling.
