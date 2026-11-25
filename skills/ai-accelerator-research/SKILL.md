---
name: ai-accelerator-research
description: "Evaluate AI training and inference accelerator architectures, memory and dataflow bottlenecks, workload quality, PPBA and manufacturing tradeoffs."
---

# AI accelerator research

Use for a user's requested AI accelerator architecture or benchmark question.

1. Specify training or inference workloads, quality target, precision, batch/sequence, memory capacity, interconnect and latency requirements.
2. Estimate compute and bytes moved; use a roofline-style bound min(peak compute, bandwidth × arithmetic intensity) with consistent units and realistic utilization. Separate prefill/decode or forward/backward/optimizer.
3. Compare dataflows, SRAM tiling, NoC, quantization, accumulation, scheduling and host costs. State latency, accuracy and capacity tradeoffs.
4. Measure useful workload performance, energy and area in matched scenarios. Training uses time-to-quality and cost; inference uses tokens/s, TTFT, TPOT and quality. Peak TOPS alone is not evidence.
5. Record model and hardware provenance, toolchain, PDK/PVT, system boundary and cost/yield assumptions. Separate analytic estimates, RTL simulation, synthesis, P&R, signoff and real silicon.

Return a falsifiable hypothesis, benchmark plan, evidence and uncertainty. Optional [public research status](https://github.com/rtl-ai/silicon-arena/blob/main/research/STATUS.md) and [manufacturing gates](https://github.com/rtl-ai/silicon-arena/blob/main/research/manufacturing.md). No automatic research enrollment, credential use, posting or spending.
