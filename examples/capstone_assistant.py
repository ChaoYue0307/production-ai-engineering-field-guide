from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ai_engineering_basics.agents import AgentBudget
from ai_engineering_basics.caching import PromptCache
from ai_engineering_basics.context import ContextBlock, build_messages, pack_context
from ai_engineering_basics.evals import EvalCase, EvalRunner, aggregate
from ai_engineering_basics.models import FakeModelClient, LLMRequest
from ai_engineering_basics.observability import CostEvent, CostTracker, estimate_cost
from ai_engineering_basics.rag import Document, KeywordRetriever, chunk_text
from ai_engineering_basics.routing import ModelProfile, ModelRouter, RouteRequest
from ai_engineering_basics.safety import TenantContext, detect_prompt_injection
from ai_engineering_basics.schemas import parse_json_object, validate_schema
from ai_engineering_basics.tracing import TraceRecorder


SCHEMA = {
    "type": "object",
    "required": ["answer", "citations"],
    "properties": {
        "answer": {"type": "string"},
        "citations": {"type": "array", "items": {"type": "string"}},
    },
}


def answer_question(question: str, tenant: TenantContext) -> dict[str, object]:
    trace = TraceRecorder()
    budget = AgentBudget(max_steps=4, max_tool_calls=2, max_tokens=1_000)
    cache = PromptCache()
    cost = CostTracker()
    router = ModelRouter(
        [
            ModelProfile("fake-large", quality=0.95, cost_per_1k_tokens=0.02, p95_latency_ms=900),
            ModelProfile("fake-small", quality=0.75, cost_per_1k_tokens=0.004, p95_latency_ms=250),
        ]
    )
    client = FakeModelClient(
        {
            "RAG": '{"answer":"RAG quality depends on retrieval recall, precision, grounding, and citations.","citations":["rag-guide:0"]}'
        }
    )

    injection_markers = detect_prompt_injection(question)
    if injection_markers:
        return {"ok": False, "error": "Prompt injection markers detected", "markers": injection_markers}

    with trace.span("route"):
        route = router.choose(RouteRequest(needs_json=True, max_p95_latency_ms=1_000, min_quality=0.7))
        if route is None:
            return {"ok": False, "error": "No model available"}

    docs = [
        Document(
            "rag-guide",
            "RAG evals should measure retrieval recall, precision, grounding, attribution, and citation quality.",
            {"tenant_id": tenant.tenant_id},
        )
    ]
    chunks = [chunk for doc in docs for chunk in chunk_text(doc, max_words=16, overlap_words=2)]
    retrieved = KeywordRetriever(chunks).search(question, k=2)
    context = [
        ContextBlock(
            name=result.chunk.chunk_id,
            content=result.chunk.text,
            priority=90,
            source=result.chunk.doc_id,
        )
        for result in retrieved
    ]
    messages = build_messages(
        system_prompt="Return JSON matching the schema. Cite retrieved chunks.",
        user_request=question,
        context_blocks=pack_context(context, token_budget=60),
    )
    request = LLMRequest(model=route.name, messages=messages, metadata={"tenant_id": tenant.tenant_id})
    cache_key = cache.make_key(tenant_id=tenant.tenant_id, model=request.model, prompt=request.prompt_text())

    with trace.span("llm.complete", model=request.model):
        cached = cache.get(cache_key)
        response_text = cached
        if response_text is None:
            response = client.complete(request)
            budget.consume_tokens(response.usage.total_tokens)
            response_text = response.text
            cache.set(cache_key, response_text, ttl_seconds=300)
            cost.record(
                CostEvent(
                    feature="capstone",
                    workflow="answer_question",
                    tenant_id=tenant.tenant_id,
                    user_journey="learning",
                    model=request.model,
                    input_tokens=response.usage.prompt_tokens,
                    output_tokens=response.usage.completion_tokens,
                    cost_usd=estimate_cost(
                        input_tokens=response.usage.prompt_tokens,
                        output_tokens=response.usage.completion_tokens,
                        input_cost_per_1m=0.15,
                        output_cost_per_1m=0.60,
                    ),
                )
            )

    with trace.span("validate"):
        parsed = parse_json_object(response_text)
        if not parsed.ok:
            return {"ok": False, "error": "Malformed JSON", "trace": trace.summary()}
        validation = validate_schema(parsed.value, SCHEMA)
        if not validation.ok:
            return {"ok": False, "error": "Schema validation failed", "details": validation.errors}

    budget.consume_step()
    return {
        "ok": True,
        "answer": parsed.value,
        "trace": trace.summary(),
        "cost_by_feature": cost.by_dimension("feature"),
        "termination": budget.termination_reason() or "completed",
    }


def main() -> None:
    tenant = TenantContext("tenant-a", "user-1", frozenset({"rag-guide"}))
    result = answer_question("What should RAG evals measure?", tenant)
    print(result)

    evals = EvalRunner(lambda prompt: str(answer_question(prompt, tenant))).run(
        [EvalCase("capstone-rag", "What should RAG evals measure?", ("recall", "precision", "citation"))]
    )
    print("Capstone eval:", aggregate(evals))


if __name__ == "__main__":
    main()
