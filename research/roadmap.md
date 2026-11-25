# Roadmap

0. **Reproducible primitives:** T000 gradient accumulation and I000 INT8 dot product; smoke tests and formal-equivalence harness. No PPBA ranking before validated measurement.
1. **Compute tiles:** Training: BF16/FP32 accumulate, FP8, forward/backward GEMM, optimizer. Inference: INT4/INT8/FP8/FP4 GEMM/GEMV, attention, quantization, accuracy. Define rounding and exceptional-value behavior.
2. **System architecture:** SRAM hierarchy, DMA, NoC, host interface, dataflow, compiler/runtime, memory capacity and bandwidth; train-to-quality and inference latency/throughput/quality.
3. **Physical implementation:** version-pinned RTL-to-GDSII flow, documented PDK and signoff limitations. Establish fixed benchmark corners and workloads, area and power evidence.
4. **Prototype:** FPGA board demo; independent MPW quote and design-review go/no-go; small test chip plus PCB, bring-up firmware, silicon test vectors and measurement plans.
5. **Productization:** foundry-qualified PDK and signoff, DFT/ATE, package and board, characterization, reliability/qualification, yield and volume-cost quotes, driver/toolchain, target-market requirements. No production claim until supported by evidence.
