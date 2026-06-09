from __future__ import annotations

from dataclasses import dataclass


PROMPT_INJECTION_MARKERS = (
    "ignore previous instructions",
    "developer message",
    "system prompt",
    "exfiltrate",
    "send secrets",
)


@dataclass(frozen=True)
class TenantContext:
    tenant_id: str
    user_id: str
    allowed_doc_ids: frozenset[str]


def detect_prompt_injection(text: str) -> list[str]:
    lowered = text.lower()
    return [marker for marker in PROMPT_INJECTION_MARKERS if marker in lowered]


def filter_authorized_documents(
    doc_ids: list[str],
    tenant_context: TenantContext,
) -> list[str]:
    return [doc_id for doc_id in doc_ids if doc_id in tenant_context.allowed_doc_ids]


def assert_same_tenant(*tenant_ids: str) -> None:
    if len(set(tenant_ids)) > 1:
        raise PermissionError(f"Cross-tenant access blocked: {sorted(set(tenant_ids))}")
