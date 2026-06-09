from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from ai_engineering_basics.models import FakeModelClient, LLMRequest, Message
from ai_engineering_basics.tracing import TraceRecorder


def main() -> None:
    recorder = TraceRecorder()
    client = FakeModelClient({"latency": "Latency has prefill and decode components."})
    request = LLMRequest(
        model="fake-teaching-model",
        messages=(
            Message("system", "Answer as a production AI engineer."),
            Message("user", "Explain why latency needs tracing."),
        ),
        metadata={"feature": "harness_lab", "tenant_id": "local"},
    )

    with recorder.span("llm.complete", model=request.model, feature="harness_lab"):
        response = client.complete(request)

    print("Response:", response.text)
    print("Tokens:", response.usage.total_tokens)
    print("Trace:", recorder.summary())


if __name__ == "__main__":
    main()
