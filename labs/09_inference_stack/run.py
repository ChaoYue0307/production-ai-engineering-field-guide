from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from ai_engineering_basics.inference import (
    effective_tokens_per_second,
    estimate_kv_cache_gib,
    estimate_prefill_decode_latency,
    quantization_risk,
)


def main() -> None:
    latency = estimate_prefill_decode_latency(
        prompt_tokens=8_000,
        output_tokens=500,
        prefill_tokens_per_second=20_000,
        decode_tokens_per_second=80,
    )
    kv_gib = estimate_kv_cache_gib(
        layers=32,
        hidden_size=4096,
        sequence_tokens=8_500,
        batch_size=16,
        bytes_per_value=2,
    )
    throughput = effective_tokens_per_second(
        batch_size=16,
        decode_tokens_per_second_per_request=80,
        batching_efficiency=0.72,
    )

    print("Prefill ms:", round(latency.prefill_ms, 2))
    print("Decode ms:", round(latency.decode_ms, 2))
    print("Total ms:", round(latency.total_ms, 2))
    print("KV cache GiB:", round(kv_gib, 2))
    print("Continuous batching effective tok/s:", round(throughput, 2))
    print("INT4 risk:", quantization_risk("int4"))


if __name__ == "__main__":
    main()
