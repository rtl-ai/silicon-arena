# Local research coordinator

The first coordinator is a durable SQLite queue for four **reviewed, built-in** experiments. It can distribute distinct jobs among local workers, recover expired leases, and record pass/fail/blocked evidence. It does not autonomously invent new RTL, call external AI models, accept untrusted code, or operate a public work-assignment service.

## Run
```sh
python3 tools/coordinator.py init
python3 tools/coordinator.py run-once --track training
python3 tools/coordinator.py run-once --track inference
python3 tools/coordinator.py status
```

Repeat run-once to work through queued experiments. State is kept in local .arena/state.sqlite, not committed. Use retry-blocked after installing missing dependencies. A lease is not an external agent or proof; completed simulations do not establish formal equivalence or PPBA.

Workers execute only the checked-in registry, no arbitrary commands. A transactional claim prevents duplicate concurrent assignment; expired tokens cannot finalize a job. Hard timeouts bound each run. The registry and evidence format are local MVP choices, not an internet-facing service. For external submissions use reviewed PRs and a separate isolated verifier without credentials.

## Next
Qualify physical scoring with a redistributable PDK and pinned toolchain; obtain formal proofs before ranked submissions. Add reviewed candidate generation and task DAG dependencies only after baseline and evaluator are stable. Public statistics must come from actual durable records and distinguish local sessions from external contributors.
