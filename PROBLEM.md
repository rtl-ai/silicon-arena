---
spec: problem.md/v1
name: SiliconArena
tagline: "Reproducible, manufacturable AI training and inference ASIC research"
status: upcoming
domain: hardware-efficiency
tags: [rtl, asic, ai-accelerator, training, inference, verification, ppba]
compute: cpu
compute_details: "Initial RTL smoke tests run on a CPU. Formal and physical-design ranking environments are not yet qualified."
deadline: rolling
prizes: recognition only
organizer:
  name: RTLAI
  url: https://github.com/rtl-ai/silicon-arena
tracks:
  - id: training-001
    name: Training compute primitive
    metric: post-route standard-cell area at fixed timing and correctness
    unit: um2
    direction: minimize
    description: "Planned exact signed gradient accumulation kernel; fixed PDK, constraints, tool versions and workload will be published before ranking."
  - id: inference-001
    name: Inference compute primitive
    metric: post-route standard-cell area at fixed timing and correctness
    unit: um2
    direction: minimize
    description: "Planned exact eight-lane INT8 dot product; fixed PDK, constraints, tool versions and workload will be published before ranking."
submit:
  how: pull-request
  path: submissions/<handle>/
  format: "Candidate RTL, reproduction commands, evidence and SUBMISSION.md; pre-ranking infrastructure contributions use normal PRs."
  requirements: [Python 3, Icarus Verilog]
  verification: "Maintainer independently checks equivalence and reruns a fixed scorer once qualified. No ranked scores accepted yet."
  eligibility: "Open to human and agent-assisted contributors using authorized resources."
  cost: free
  agents: welcome
  attribution: "Disclose model and harness when used; preserve authorship."
quickstart: |
  git clone https://github.com/rtl-ai/silicon-arena
  cd silicon-arena
  python3 tools/smoke.py
  python3 -m unittest discover -s tests -v
---

# SiliconArena research challenges

The project welcomes reproducible verification and benchmark-infrastructure contributions today. Ranked physical-design challenges are **upcoming**, not yet open for scored submissions. There are no verified PPBA records or fabricated chips. A small arithmetic kernel is not an end-to-end accelerator.

## Before ranking

- Establish formal equivalence, pinned open toolchain and redistributable PDK, fixed clock and PVT, and independent scoring.
- Measure power, performance, bandwidth and area separately; include precision, quality, workload and boundary. Preserve yield-adjusted cost and TCO assumptions.
- Publish a reproducible baseline and a trusted scoring procedure. Do not publish unverified numeric scores or fake baselines.
- No employer IP, credentials, restricted PDK data, unauthorized compute or paid resources.

## How to contribute now

Follow [join.txt](join.txt), [AGENTS.md](AGENTS.md), [measurement contract](research/measurement.md) and [issue #1](https://github.com/rtl-ai/silicon-arena/issues/1). Start with a bounded contribution and obtain maintainer review. See [submission template](templates/SUBMISSION.md.template) for the planned ranked format.
