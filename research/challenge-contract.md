# Bootstrap challenge contract

The production PPBA leaderboard is not active. This stage establishes **independent deterministic RTL functional simulation**, not formal equivalence or a post-route score.

## Training-001
- Exact signed 8-bit activation × signed 8-bit gradient; accumulate into signed 32-bit modular two's complement state.
- One rising edge per update. Synchronous reset or clear overrides enable; enable=0 holds state.
- Maintain interface and observable behavior. Proposed future objective: physical area under fixed timing, then power, throughput, bandwidth and cost.

## Inference-001
- Exact eight signed 8×8 products summed into a signed 32-bit combinational result; lane i is bits [8i+7:8i] of each 64-bit input.
- Maintain bit exactness, no state or latency changes.
- Proposed future objective: physical area under fixed timing, then energy/operation and bandwidth.

## Reproduce
Run from the repository root:
```sh
python3 tools/verify_kernels.py --self-test
```
The reference is computed in Python independently from RTL. Exhaustive operand pairs per lane, explicit wraparound/control cases and deterministic randomized vectors are tested. Mutation checks must reject deliberately incorrect arithmetic. These checks do not exhaust all multi-lane combinations or all sequences; do not call them formal proofs.

For a trusted candidate, run e.g. `python3 tools/verify_kernels.py --track inference --trusted-candidate /path/to/dot8.sv`. Keep this verifier and reference immutable in scored evaluation. Untrusted candidate HDL may execute system tasks; evaluate only in resource-bounded isolated workers with no credentials or network, not on the maintainer's host.

## Next gates
1. Formal proof with explicit reset/induction contract and negative controls.
2. Pinned Yosys/ABC, versioned PDK/library, fixed constraints, baseline synthesis and post-route reproducibility.
3. Independent candidate reruns before rankings. No arbitrary weighted score or production claim.
4. Cost/yield model calibration, SRAM/interconnect/IO and full system workload characterization.

Submit reproducible reports through a pull request; include failures and all missing evidence.
