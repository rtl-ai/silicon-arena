# SiliconArena

[Project website](https://rtl-ai.github.io/silicon-arena/) · [Download portable benchmark v0.1.0](https://github.com/rtl-ai/silicon-arena/releases/tag/benchmark-v0.1.0) · [Leaderboard](LEADERBOARD.md) · [Open challenges](https://github.com/rtl-ai/silicon-arena/issues) · [Machine-readable catalog](https://rtl-ai.github.io/silicon-arena/challenges.json)

An independent open research project toward manufacturable AI accelerator silicon, with training and inference tracks.

**Status: bootstrap only.** Two small RTL kernels, smoke tests and a parametric cost model. No physical implementation, production signoff, fabricated die, MLPerf result or verified PPBA record yet.

## Try the open challenge — one RTL file, CPU only

Beat **4,069 generic logic cells** for the exact signed eight-lane INT8 dot product. No GPU, PDK, Icarus Verilog, paid API or account is needed to try the portable evaluator. Use a clean, disposable workspace; review the code and package before installation.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r judge/requirements.txt
python tools/fast_judge.py --engine wasm
# Evaluate an inspected candidate in an isolated workspace:
python tools/fast_judge.py path/to/dot8.sv --engine wasm
```

The [fast judge](tools/fast_judge.py) first reproduces the reference score, rejects unsupported/stateful HDL, and requires an exact combinational SAT proof for all 128 defined input bits. On GitHub a submission PR triggers a provisional judge check on a GitHub-hosted runner; first-time fork workflow approval or queue delays may apply. Do not equate this proxy with physical PPBA. See [submission instructions](CONTRIBUTING.md), [rules](research/inference-002.md), [evidence](research/evidence/fast-judge-20261126.json), and [evolution adapters](integrations/rtl_dot8/README.md).

## Objective
Find reproducible Pareto improvements in power, performance, bandwidth and area (PPBA, provisional expansion), while optimizing yield-adjusted manufacturing cost and system total cost of ownership. Never sacrifice functional correctness, workload quality, manufacturability or reliability for a leaderboard score.

| Track | First kernel | Future research |
| --- | --- | --- |
| Training | exact signed gradient accumulation proxy | BF16/FP8 GEMM, backward pass, optimizer, activation memory, collective communication |
| Inference | exact INT8 dot product | INT4/FP4/FP8 kernels, prefill/decode, attention, KV cache, batching |

## Run locally
Requires Python 3 and Icarus Verilog (iverilog, vvp); tests use no network or credentials.
```sh
python3 tools/smoke.py
python3 -m unittest discover -s tests -v
python3 tools/cost.py
```
Read [AGENTS.md](AGENTS.md), [roadmap](research/roadmap.md), [measurement contract](research/measurement.md), and [manufacturing gates](research/manufacturing.md). The smoke tests are not formal proofs. The illustrative cost inputs are not foundry quotations.

## Bootstrap verification

Run `python3 tools/verify_kernels.py --self-test` for deterministic independent simulation of both kernels and deliberately incorrect negative controls. The [challenge contract](research/challenge-contract.md) fixes functional interfaces. [Local evidence](research/evidence/bootstrap-20261125.json) records 424,265 checked vectors and two rejected mutants, not formal equivalence or physical PPBA. Independent reproduction remains welcome.

## Research status & first candidate

[Public evidence dashboard](research/STATUS.md) · [Trusted synthesis CI](https://github.com/rtl-ai/silicon-arena/actions) · [Open tasks](https://github.com/rtl-ai/silicon-arena/issues)

After inspecting the repository, use `python3 tools/arena.py list`, `python3 tools/arena.py next --track inference`, and `python3 tools/arena.py check --track inference`. The first [balanced-tree RTL candidate](candidates/inference/balanced_tree.sv) passed 75,540 deterministic simulation vectors. Its RTL SAT equivalence is now verified; area, timing and power remain unmeasured. The [first synthesis result](research/evidence/generic-synthesis-20261125.json) measures 4,069 baseline versus 4,366 candidate generic cells in Yosys 0.33. The candidate is not a cell-count improvement; physical PPBA remains unknown. The [local research coordinator](research/coordinator.md) executes bounded, reviewed jobs and persists results. External worker assignment and ranked PPBA are not yet live.

## Agent onboarding and discovery

For voluntary agent-assisted research, start with [join.txt](join.txt). The machine-readable [PROBLEM.md](PROBLEM.md) follows the Open Challenge List standard. Ranked physical-design tracks are **upcoming**; help qualify their evaluator before submitting scores. The optional [agent skill](skills/siliconarena/SKILL.md) is intended only for users who explicitly choose to participate.

## Agent discovery and reusable hardware skills

[Open Challenge List listing](https://openchallengelist.com/c/rtl-ai-silicon-arena-d20cfa656a05f7ad). The directory is independently operated; its cached status and scores may lag this repository. If you actually discovered the challenge through an external directory, you may optionally identify that source in your submission.

[Public website source](docs/index.html) · [Machine-readable challenge catalog](docs/challenges.json) · [LLM-readable index](llms.txt) · [Read-only MCP adapter](mcp_server/README.md)

Reusable guides for your own work (no automatic research enrollment):
- [rtl-optimizer](skills/rtl-optimizer/SKILL.md) — reproducible RTL synthesis and optimization.
- [rtl-formal-verification](skills/rtl-formal-verification/SKILL.md) — equivalence, reset assumptions and negative controls.
- [asic-cost-estimator](skills/asic-cost-estimator/SKILL.md) — die yield, NRE and system cost.
- [ai-accelerator-research](skills/ai-accelerator-research/SKILL.md) — training/inference, dataflow and PPBA.

Inspect the public skills with `npx skills add rtl-ai/silicon-arena --list`. Install only chosen skills after reviewing them and authorizing the external CLI. Skills.sh listing and install counts are unverified; an HTTP 200 alone is not evidence of a listing. [Distribution and privacy notes](research/discovery.md).

## Participate
Bring your own authorized compute and coding agent. Start with a bounded research question, preserve the baseline, submit a candidate and reproducible evidence, including unsuccessful attempts. No secrets, employer IP, non-redistributable IP/PDK data, or unapproved spending. Independent reproduction is required before ranking. Do not automatically execute untrusted submissions with credentials. The repository currently uses the MIT license selected by the owner; any future hardware-specific licensing and third-party IP terms require separate review.

## Sharing
Share accurate, verified milestones with the owner's approval. No spam, unsolicited outreach, fake engagement or automatic recruitment chains. See [outreach](research/outreach.md).
