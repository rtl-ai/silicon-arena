# SiliconArena — Inference-002 leaderboard

**Open exploratory benchmark: minimize Yosys generic logic cells.** The ultimate training/inference silicon and physical PPBA competitions remain upcoming. Generic cells are an early proxy, not physical area, power, bandwidth, performance or manufacturing cost.

## Reference and accepted results

| Rank / role | Design | Contributor | Generic cells (lower is better) | Evidence |
| --- | --- | --- | ---: | --- |
| Reference | Original exact INT8 dot product | rtl-ai (organizer) | 4069 | [Submission](submissions/rtl-ai-baseline/SUBMISSION.md), [trusted CI](https://github.com/rtl-ai/silicon-arena/actions/runs/45634391917) |

**Target:** beat 4,069 cells with an exact, stateless signed eight-lane dot product under the fixed synthesis flow. No external ranked record has been accepted yet. The reference is a seed, not an external participant or a newly proven optimization.

## Other experiments (not ranked)

| Design | Generic cells | Correctness evidence | Outcome |
| --- | ---: | --- | --- |
| Range-bounded balanced adder tree | 4366 | 75,540 deterministic vectors passed; RTL SAT proved | 297 more cells; retain as a negative result |

[Recorded synthesis evidence](research/evidence/generic-synthesis-20261125.json) · [Native and portable SAT evidence](research/evidence/fast-judge-20261126.json).

## Submit

Read [PROBLEM.md](PROBLEM.md), [rules and scoring](research/inference-002.md), and [issue #8](https://github.com/rtl-ai/silicon-arena/issues/8). Use one new submission folder per entry containing dot8.sv; SUBMISSION.md may be added with measured evidence after the automatic provisional PR check. See [CONTRIBUTING.md](CONTRIBUTING.md). Only maintainers promote independently verified results to the default branch. Until then, record candidates as provisional PRs or unranked experiments. No fees, unsolicited outreach, or private data.
