# Inference-002: exact INT8 dot product

## Contract and metric

- Preserve top module `dot8`, inputs `a` and `b` (64 bits each), combinational `result` (32 bits). Sum eight exact signed INT8 products; no clipping, approximation, extra state, or latency change.
- Minimize Yosys 0.33 generic mapped cell count. The fixed script is `read_verilog -sv design.sv; synth -top dot8; check -assert; write_json mapped.json`. Reference SHA-256 is checked; every run must reproduce 4069 cells. Native Ubuntu 24.04 Yosys 0.33-5build2 and YoWASP 0.33.0.0.post574 reproduce the original 4069 and the balanced-tree 4366.
- Accepted HDL is one ASCII SystemVerilog file (<=64 KiB), one module, no attributes, preprocessor directives, includes, system tasks, strings, escaped identifiers, sequential logic, initial blocks, delays, formal assumptions, black boxes, or undefined outputs. The automated evaluator also checks structural and mapped cell types, port widths, connections and synthesizability. Some otherwise valid RTL outside this initial policy is intentionally unsupported; propose a separate reviewed infrastructure change.
- SAT miter proves equivalence at RTL level for every defined combination of the 128 input bits. The proof is before generic mapping. This does not establish post-mapping equivalence, signoff, PPA, power, timing or production readiness. A timeout or failed proof yields no verified score. Lower count wins; ties are ties.

## Portable local evaluation (trusted candidates only)

Use a new disposable workspace without private files or credentials. Inspect dependencies and source.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r judge/requirements.txt
python tools/fast_judge.py --engine wasm
# Evaluate an inspected candidate in an isolated workspace:
python tools/fast_judge.py path/to/dot8.sv --engine wasm
```

## Submit in one file

Follow [CONTRIBUTING.md](../CONTRIBUTING.md). Add one new submission folder with dot8.sv (and optionally SUBMISSION.md for your initial PR). Do not alter the judge, baseline, workflows, or other entries. The automatic PR check reports a provisional score; untrusted HDL is handled as a blob and processed inside a restricted container on a GitHub-hosted runner. First-time fork approval or CI queue delays may occur.

Official ranks require independent recheck from trusted main, reviewed source/netlist and reproducible evidence. The initial PR result is not an automatic merge or rank promotion. The GitHub workflow itself is not a trust anchor when modified by an untrusted PR. Maintainers can independently run the main workflow with exact PR number and head SHA.

[Reference evidence](evidence/generic-synthesis-20261125.json), [SAT and portable evidence](evidence/fast-judge-20261126.json), [leaderboard](../LEADERBOARD.md). No fees or paid compute required; use authorized resources only.
