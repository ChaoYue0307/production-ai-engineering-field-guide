from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LatencyEstimate:
    prefill_ms: float
    decode_ms: float

    @property
    def total_ms(self) -> float:
        return self.prefill_ms + self.decode_ms


def estimate_prefill_decode_latency(
    *,
    prompt_tokens: int,
    output_tokens: int,
    prefill_tokens_per_second: float,
    decode_tokens_per_second: float,
) -> LatencyEstimate:
    if prefill_tokens_per_second <= 0 or decode_tokens_per_second <= 0:
        raise ValueError("throughput values must be positive")
    return LatencyEstimate(
        prefill_ms=prompt_tokens / prefill_tokens_per_second * 1000,
        decode_ms=output_tokens / decode_tokens_per_second * 1000,
    )


def estimate_kv_cache_gib(
    *,
    layers: int,
    hidden_size: int,
    sequence_tokens: int,
    batch_size: int,
    bytes_per_value: int = 2,
) -> float:
    """Rough KV cache size for teaching: keys + values across layers."""

    bytes_total = layers * 2 * hidden_size * sequence_tokens * batch_size * bytes_per_value
    return bytes_total / 1024**3


def effective_tokens_per_second(
    *,
    batch_size: int,
    decode_tokens_per_second_per_request: float,
    batching_efficiency: float,
) -> float:
    if not 0 < batching_efficiency <= 1:
        raise ValueError("batching_efficiency must be within (0, 1]")
    return batch_size * decode_tokens_per_second_per_request * batching_efficiency


def quantization_risk(format_name: str) -> str:
    risks = {
        "int8": "Usually a good default; watch for math-heavy and rare-token regressions.",
        "int4": "Large memory win; higher risk for reasoning, tool args, and long-tail domains.",
        "fp8": "Strong serving format on supported hardware; calibration and kernels matter.",
        "awq": "Good weight-only approach for activation-aware compression; test domain quality.",
        "gptq": "Practical post-training quantization; quality depends on calibration data.",
    }
    return risks.get(format_name.lower(), "Unknown format; benchmark quality, latency, and memory.")
