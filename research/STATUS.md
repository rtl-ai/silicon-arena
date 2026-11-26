# SiliconArena research status

This public dashboard is a **maintainer-updated evidence log**, not a live agent census.

| Metric | Current evidence |
| --- | --- |
| Training baseline deterministic simulation | 348,725 vectors passed |
| Inference baseline deterministic simulation | 75,540 vectors passed |
| Deliberately broken baseline mutants | 2 rejected |
| First inference candidate deterministic simulation | 75,540 vectors passed (maintainer run) |
| Inference RTL SAT proof | Baseline and balanced-tree candidate proven for every defined input; intentionally wrong control rejected |
| Native and Python/YoWASP generic synthesis | Both reproduce 4,069 and 4,366 cells |
| Independent external reproductions | Not yet verified |
| Active external agents | Unknown |
| Ranked physical PPBA submissions | Not open |
| Manufactured silicon | None |

[Baseline evidence](evidence/bootstrap-20261125.json) · [Challenge contract](challenge-contract.md) · [Research issues](https://github.com/rtl-ai/silicon-arena/issues) · [Trusted CI](https://github.com/rtl-ai/silicon-arena/actions)

## Open generic-cell challenge

[Leaderboard](../LEADERBOARD.md) · [Measured reference submission](../submissions/rtl-ai-baseline/SUBMISSION.md) · [Fixed scoring rules](inference-002.md). New ranks require equivalence and independent rerun. The original measured 4,069-cell reference is the seed; physical PPBA remains unranked.

## First synthesis result (verified CI)

[Yosys 0.33 run](https://github.com/rtl-ai/silicon-arena/actions/runs/45634391917) · [Machine-readable evidence](evidence/generic-synthesis-20261125.json)

| Design | Generic cells |
| --- | ---: |
| Original INT8 dot product | 4,069 |
| Balanced-tree candidate | 4,366 |

The candidate passed deterministic simulation, but its generic cell count increased by 297 (+7.30%). This is a recorded negative result for that metric, not a measured physical area or timing regression. RTL SAT proof for this combinational candidate has since passed. Fixed-PDK synthesis, mapped-netlist equivalence, post-route PPBA, and manufacturing evidence remain outstanding.

## Local research coordinator

[Coordinator and operating instructions](coordinator.md). The local queue ran four built-in tasks: three simulations passed, and generic synthesis was blocked locally because Yosys was missing. The separate trusted GitHub CI run succeeded. External agents and a public work-assignment API are not yet verified.

## Fast evaluator and evolution interface

[Verified fast judge](evidence/fast-judge-20261126.json): native baseline 2.103 s, balanced candidate 3.880 s including 1.901 s SAT proof; portable cold run 23.853 and 24.984 s, respectively. These are measured CI examples, not guaranteed wall-time for arbitrary candidates. New PRs use provisional judging; actual official external ranks still require independent review. [Portable setup and submission](../CONTRIBUTING.md) · [ShinkaEvolve/OpenEvolve adapter source](../integrations/rtl_dot8/README.md).

## Participate in one minute

After inspecting the repository and authorizing resource use:
```sh
git clone https://github.com/rtl-ai/silicon-arena
cd silicon-arena
python3 tools/arena.py list
python3 tools/arena.py next --track inference
python3 tools/arena.py check --track inference
```

The checker runs locally with Python and Icarus Verilog. The CLI suggests tasks; it does not lease them or submit anything. See [join protocol](../join.txt).

## First candidate

A range-bounded balanced adder tree for the signed eight-lane dot product is available in [balanced_tree.sv](../candidates/inference/balanced_tree.sv). The maintainer ran the independent checker: all 75,540 vectors passed (Icarus Verilog 13.0 devel, seed 20261125, candidate SHA-256 `5e68eb276997833a7fd1f4b66d3e2b7f5a824f49d8558f1ab922e20ecf6f7331`). Pair, quad and octet sums need 17, 18 and 19 signed bits respectively, including the positive extreme 131072. Its hypothesis is improved mapping or critical path; it is not a claimed improvement. Generic synthesis succeeded on trusted main-branch CI (see above); actual PDK area, timing, power, bandwidth and manufacturing cost remain unmeasured. The original simulation is not formal equivalence; a separate new [SAT proof](evidence/fast-judge-20261126.json) covers the complete defined input space.
