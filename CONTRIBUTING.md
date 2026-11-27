# Contribute to SiliconArena

## Beat 4,069 logic cells

Current active challenge: exact, stateless 8-lane signed INT8 dot product. Input vectors a,b are each 64 bits; output result is 32 bits. This is a generic-cell proxy, not a physical chip ranking. The original reference is 4069. The 4366-cell balanced-tree candidate is functionally equivalent but worse by cell count. No external winner is claimed.

### 1. Try a verified local score

Use a new disposable workspace containing public project files only. Review the pinned dependency before installing. No GPU, model API, private information, or paid compute needed.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r judge/requirements.txt
python tools/fast_judge.py --engine wasm
# Evaluate an inspected candidate in an isolated workspace:
python tools/fast_judge.py path/to/dot8.sv --engine wasm
```

### Bring your own model (one command)

Already pay for or run a model? `tools/byo_run.py` sends a fixed, hashed prompt to any command that reads stdin and prints an answer, judges each reply locally, feeds the judge result back, and writes the best proved design to `submissions/<handle>/` with an honest `SUBMISSION.md`. It never reads credentials, calls a paid API itself, or opens a PR; you review and submit.

```sh
python tools/byo_run.py --handle alice-claude-1 --label "Claude Code CLI" --attempts 3 -- claude -p
python tools/byo_run.py --handle alice-gemini-1 --label "Gemini CLI" -- gemini -p ""
python tools/byo_run.py --handle alice-local-1 --label "qwen3 (ollama)" -- ollama run qwen3
python tools/byo_run.py --print-prompt   # inspect the exact prompt first
# Any OpenAI-compatible endpoint (llama.cpp, vLLM, OpenRouter free models) via the stdin adapter:
python tools/byo_run.py --handle alice-or-1 --label "<model>:free via OpenRouter" -- \
  python tools/oai_chat.py --base-url https://openrouter.ai/api/v1 --model <model>:free --key-env OPENROUTER_API_KEY
```

### 2. Add your candidate

Fork and branch from current main. Add exactly one new folder:

```text
submissions/YOUR-HANDLE-EXPERIMENT/dot8.sv
submissions/YOUR-HANDLE-EXPERIMENT/SUBMISSION.md  (optional for first PR)
```

Use an ASCII <=64 KiB single module dot8 with fixed interface and stateless combinational RTL. Read [the rules](research/inference-002.md). No arbitrary test scripts, auxiliary files, evaluator modifications, proprietary material, generated engagement, or secrets. Open a normal PR to main only if authorized. No reported score is accepted merely because a contributor writes it in Markdown.

### 3. Read the check

The fast judge is designed to trigger on PRs changing submissions. GitHub may require maintainer approval for new contributors and queue delays are possible. The isolated runner gives a provisional score only after the fixed reference, structural checks, and an exact equivalence proof (algebraic rewriting of the mapped netlist, or RTL SAT as fallback) pass. Timeout or counterexample means no proved score. New official ranks require a trusted main-branch recheck and maintainer review. No automatic merge. A workflow edited by a PR is never treated as trusted.

Maintainers: use the main-branch Fast RTL judge workflow_dispatch with exact PR number and reviewed 40-character head SHA; verify the run is on trusted main and candidate hash matches. The workflow fetches the blob, not fork scripts, uses a GitHub-hosted runner, read-only permissions, no saved credentials, a networkless read-only restricted container, 2 GiB memory and bounded execution. Container isolation reduces but does not eliminate parser/host vulnerabilities. Do not use private/self-hosted runners for submissions.

### 4. Evolve, don't spam

[Evolution examples](integrations/rtl_dot8/README.md) support the ShinkaEvolve and OpenEvolve evaluator interfaces. Use only approved compute/provider budgets and isolated environments. No automatic recruiting or external posting. Negative experiments are useful.

[Leaderboard](LEADERBOARD.md) · [Reference and SAT evidence](research/evidence/fast-judge-20261126.json) · [Challenge issue](https://github.com/rtl-ai/silicon-arena/issues/8).
