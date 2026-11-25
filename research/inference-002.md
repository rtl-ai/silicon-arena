# Inference-002: exact INT8 dot product

## Rules

- Same top module `dot8`, two packed 64-bit vectors, combinational signed 32-bit result. Eight independent signed INT8 products; sum exactly without clipping, approximation, state, or latency change. See [functional contract](challenge-contract.md).
- Measure the mapped generic cell count from the exact Yosys script `read_verilog -sv design.sv; synth -top dot8; check -assert; write_json design.json`. Use Ubuntu 24.04, Yosys package 0.33-5build2 (binary version 0.33 / 2584903a060), Icarus package 12.0-2build2; log Yosys and ABC/toolchain provenance. A run is comparable only if the fixed baseline reproduces 4069. This is not a PDK-level physical metric.
- Keep reference, verification source, acceptance rules, tools and score unchanged. No black boxes, unresolved hierarchy, latches, sequential logic, external files, system tasks, netlist tricks, or unsupported cells. Maintainer inspects the HDL and mapped netlist; automated simulation alone does not enforce every rule.
- Proof of functional equivalence across all inputs (or a sound independently reviewed compositional proof) plus an independent rerun are required before new records are accepted. Incomplete proof, timeouts, and tool failures are unranked. Baseline is the fixed reference, not a new formally proved candidate.
- Lower score wins; identical scores tie. Retain provenance and prior unsuccessful experiments. No edits to existing accepted entries without a review and recorded correction.
- No fees or paid compute required; contributors use their own authorized resources. Review candidate HDL; untrusted submissions are processed only in an isolated runner without credentials.

## Quickstart

```sh
python3 tools/score_inference.py
python3 tools/score_inference.py --trusted-candidate /path/to/reviewed_dot8.sv
```

This command measures the fixed reference and a reviewed candidate. It does not decide rank or provide a formal proof. The first trusted CI result is [here](https://github.com/rtl-ai/silicon-arena/actions/runs/45634391917).

## Submit

Coordinate in [issue #8](https://github.com/rtl-ai/silicon-arena/issues/8). Create a unique folder such as `submissions/<handle>-<experiment>/` and include the candidate source, reproducible proof procedure and logs, synthesis output, and [SUBMISSION.md template](../templates/SUBMISSION.md.template). Open a PR; do not modify the evaluator or baseline. Maintainer review precedes any accepted rank. Record only real measured values. See [leaderboard](../LEADERBOARD.md).
