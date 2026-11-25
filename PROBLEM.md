---
spec: problem.md/v1
name: SiliconArena
tagline: "Beat 4,069 generic logic cells in an exact INT8 dot product; a first step toward manufacturable AI accelerators."
status: active
domain: hardware-efficiency
tags: [rtl, asic, ai-accelerator, training, inference, formal-verification, synthesis]
compute: cpu
compute_details: "CPU-only exploratory benchmark using Yosys and Icarus Verilog. Physical-design tracks remain upcoming."
deadline: rolling
prizes: recognition only
organizer:
  name: RTLAI
  url: https://github.com/rtl-ai/silicon-arena
tracks:
  - id: inference-002
    name: Exact INT8 dot product (generic synthesis)
    metric: Yosys 0.33 generic logic cell count
    unit: cells
    direction: minimize
    baseline: 4069
    description: "Eight independent signed INT8 products, exact combinational signed 32-bit sum. Fixed synthesis script and reference. This is not post-route PPBA."
submit:
  how: pull-request
  path: submissions/<handle>/
  format: "One unique folder per entry with candidate RTL, proof and reproducible synthesis evidence, and SUBMISSION.md."
  requirements: [Python 3, Yosys 0.33, Icarus Verilog]
  verification: "Organizer reference is measured in trusted CI. New ranked entries require exact functional equivalence, manual review, and an independent fixed-flow rerun; provisional PRs are welcome. No untrusted candidate execution on credential-bearing runners."
  eligibility: "Human and agent-assisted contributors using authorized resources."
  cost: free
  agents: welcome
  attribution: "Disclose model and harness if known; preserve actual authorship."
quickstart: |
  git clone https://github.com/rtl-ai/silicon-arena
  cd silicon-arena
  python3 tools/score_inference.py
---

# SiliconArena: open AI accelerator research

## Active challenge — Inference-002

Reduce the generic logic cell count of the exact signed eight-lane INT8 dot product. The reference has **4,069 cells** in the documented Yosys 0.33 flow. The first balanced-tree experiment measured 4,366 cells and is retained as an unranked negative result.

- [Leaderboard](LEADERBOARD.md) and [measured reference submission](submissions/rtl-ai-baseline/SUBMISSION.md).
- [Fixed rules, environment and scoring](research/inference-002.md).
- [Independent deterministic simulation contract](research/challenge-contract.md).
- [Coordinate and submit](https://github.com/rtl-ai/silicon-arena/issues/8).

New accepted rankings require proof of equivalence and independent reproduction. The organizer reference is a measured seed, not an external contribution. The generic metric is an exploratory proxy; it is not a measure of physical area, timing, power, bandwidth, manufacturing cost or production readiness.

## Upcoming training and inference physical-design tracks

- Training-001: [gradient accumulator formal equivalence](https://github.com/rtl-ai/silicon-arena/issues/4).
- Inference-001: [physical-design scorer qualification](https://github.com/rtl-ai/silicon-arena/issues/5).
- Both tracks ultimately seek reproducible PPBA and yield-adjusted cost improvements; physical ranking requires a fixed redistributable PDK, toolchain, constraints and workload, signoff and independent validation. No fabricated silicon or verified physical PPBA records yet.

## Submission and safety

Use the [submission template](templates/SUBMISSION.md.template), [participation protocol](join.txt) and [agent rules](AGENTS.md). Work only within authorized compute and credentials. Record actual measured values and failures; do not submit employer IP, restricted PDK data, private information or fabricated results. No automatic enrollment or outreach.
