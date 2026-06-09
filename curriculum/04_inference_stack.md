# 04. Inference Stack

LLM latency and throughput are shaped by different phases of inference. Optimizing them requires knowing where the bottleneck lives.

## Prefill vs. Decode

Prefill processes the prompt in parallel. It is dominated by prompt length and benefits from faster attention kernels, prompt caching, and shorter context.

Decode generates output tokens sequentially. It is dominated by output length, batch scheduling, memory bandwidth, and KV cache pressure.

## KV Cache

The KV cache stores attention keys and values for previous tokens so decoding does not recompute the entire sequence. It improves speed but consumes memory proportional to layers, hidden size, sequence length, batch size, and precision.

At scale, serving systems manage:

- Eviction when memory pressure rises.
- Reuse for shared prefixes.
- Paging so long requests do not fragment memory.
- Isolation so cache state cannot leak across users.

## Throughput Techniques

- Continuous batching keeps the GPU busy by mixing requests as they arrive.
- Paged attention reduces memory fragmentation for long contexts.
- Speculative decoding drafts tokens with a smaller model and verifies them with a larger model.
- Quantization reduces memory and bandwidth but can hurt quality.
- Distillation trains a smaller model to imitate a larger one but can lose edge-case capability.

## Quantization Notes

INT8 is often low-risk. INT4 saves more memory but can hurt reasoning, tool arguments, rare languages, and domain-specific terminology. FP8 is attractive on supported hardware. AWQ and GPTQ are post-training approaches whose quality depends on calibration data.

## Practice

- Run `python labs/09_inference_stack/run.py`.
- Change prompt length and output length separately.
- Compare INT8 and INT4 risk notes.

## Mastery Checklist

- You can explain prefill and decode latency separately.
- You can estimate why long context creates KV memory pressure.
- You can compare batching, paged attention, speculative decoding, quantization, and distillation.
- You can name cases where quantization hurts quality.
