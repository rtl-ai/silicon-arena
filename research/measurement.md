# Measurement contract (draft v0)
Each candidate requires fixed task, precision, quality, interfaces, clocks, process, PVT corners, workload, benchmark and measurement boundary.
- Correctness is a hard gate: exact equivalence for exact kernels, specified numerical tolerances/quality for approximate kernels.
- Power: dynamic plus leakage at specified activity and operating point; include memory/interconnect/host boundary where relevant.
- Performance: useful throughput at stated batch and latency; training time to fixed quality, inference TTFT/TPOT and tokens/s. Report utilization.
- Bandwidth: useful on-/off-chip bytes/s and traffic volume, bottleneck and capacity; distinguish theoretical from measured.
- Area: post-route die/core/macro area with SRAM/IO inclusion explicitly stated.
- Cost: yield-adjusted die cost, package, assembly, test, logistics, NRE amortization; board/memory/energy separately and system TCO. Report quote date, currency, volumes, uncertainty and sensitivity.
- Compare only matched scenarios. Preserve Pareto frontiers rather than inventing a universal score.
- Evidence ladder: estimated analytical / simulated RTL / formal / synthesized / routed / signed-off / FPGA / fabricated and characterized silicon. Do not conflate these levels.
