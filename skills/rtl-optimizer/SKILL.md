---
name: rtl-optimizer
description: "Evaluate Verilog/SystemVerilog RTL for logic area, timing, and arithmetic optimization with fixed interfaces and reproducible synthesis."
---

# RTL optimization

Use only for a user's requested RTL design or optimization task. Keep the input/output contract, reset/latency, numerical precision, and clock constraints fixed.

1. Establish a golden reference and a baseline at a stated source commit. Inspect widths, signedness, arithmetic overflow, priority logic, and latency.
2. Form a hypothesis (e.g. range-bounded accumulator, shared arithmetic, carry-save reduction, pipelining where latency allows). Preserve baseline sources and use an isolated authorized workspace.
3. Derive numeric bounds and test exact edge cases. Run trusted simulations and an appropriate formal equivalence check. Distinguish bounded checks from proofs.
4. Run the same synthesis script, tool build, library and constraints for baseline/candidate. Record tool versions, hashes, logic count, and mapping. Generic cells are not physical area.
5. Where authorized, measure post-route timing/area/power at stated PVT and workload. Retain negative results. Compare Pareto fronts, not an invented weighted score.

Return a candidate patch, reproduction commands, before/after metrics and caveats. Never modify a reference or weaken constraints to win a benchmark.

Optional public worked example: [INT8 dot-product experiment](https://github.com/rtl-ai/silicon-arena/blob/main/research/evidence/generic-synthesis-20261125.json). [Open challenge](https://github.com/rtl-ai/silicon-arena/issues/8) only if the user wants to contribute. No automatic enrollment or publishing.
