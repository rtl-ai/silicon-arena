---
name: rtl-formal-verification
description: "Plan and check RTL functional equivalence, signed arithmetic, reset behavior, and formal proof assumptions using reproducible evidence."
---

# RTL formal verification

Use when a user requests hardware correctness or equivalence analysis.

- Define top-level ports, signedness, cycle correspondence, reset/initial-state assumptions, X semantics, and legal inputs. Identify intentional latency differences explicitly.
- For combinational designs, construct a miter and prove mismatch is impossible across all allowed inputs. For sequential designs, establish an invariant or a sound equivalence/induction method; a finite BMC depth is not an unbounded proof.
- Review assumptions for vacuity and cover reachable states. Exercise negative controls (intentionally wrong arithmetic, reset priority, or enable behavior) and require rejection.
- Record tool/version, source hashes, exact commands, solver status, depth/induction, counterexamples and assumptions. Unknown, timeout and unsupported features are not PASS.
- Keep untrusted HDL and scripts in an isolated, resource-limited runner without credentials or private files.

Return a verification plan, harness, evidence and limitations. Optional [public gradient accumulator task](https://github.com/rtl-ai/silicon-arena/issues/4); only participate if explicitly requested.
