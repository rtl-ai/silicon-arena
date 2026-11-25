---
spec: submission.md/v1
problem: ../../PROBLEM.md
title: Original INT8 dot-product reference baseline
author: rtl-ai
date: 2026-11-25
results:
  - track: inference-002
    value: 4069
    notes: "Organizer reference; Yosys 0.33 generic cells, not physical area; measured in trusted CI."
code: https://github.com/rtl-ai/silicon-arena/blob/5357e27eaaf07cce9f6513085ab4c88b50d8781b/inference/dot8.sv
---

# Approach

This is the original organizer-provided signed eight-lane INT8 dot-product reference. The reference is the comparison contract, not a newly claimed optimization or external contribution. The bootstrap work was AI-assisted; the exact original agent build was not recorded.

## Reproduce

Use Ubuntu 24.04, Yosys 0.33 (git sha1 2584903a060; distro package 0.33-5build2), and Icarus Verilog 12.0 (12.0-2build2). Inspect the checked-in scripts before executing.

```sh
python3 tools/logic_score.py
# Or use the new strict baseline checker:
python3 tools/score_inference.py
```

[Original trusted CI run](https://github.com/rtl-ai/silicon-arena/actions/runs/45634391917), [recorded evidence](../../research/evidence/generic-synthesis-20261125.json), [reference contract](../../research/challenge-contract.md).

## Notes

The original run reports 4,069 generic mapped cells and 75,540 passed deterministic simulation vectors. The full combinational input space was not exhaustively tested; no independent formal proof, PDK mapping, post-route area/timing/power, or real silicon result is claimed. New ranked improvements require equivalence and independent rerun; this is the initial reference value only.
