# SiliconArena exact INT8 dot-product evolution benchmark

A CPU-only, exact combinational Verilog optimization example. The same Yosys 0.33 flow establishes a 4,069-cell reference. Every candidate needs a successful SAT miter proof before receiving a nonzero score. Fitness = 4069 / candidate generic cells (larger is better). This is not a physical PPA metric.

## Run the evaluator without any LLM

Use an isolated disposable workspace without personal files, credentials, or private repositories. Inspect the source. Do not evaluate third-party HDL directly on your personal machine. Python 3.11 and the pinned YoWASP dependency suffice for the portable benchmark. Native Yosys 0.33 also works if the reference reproduces exactly.

From the SiliconArena repo: `python3 tools/export_evolution_example.py /tmp/rtl_dot8_example`. In the exported directory:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python tools/fast_judge.py initial.sv --engine wasm
python evaluate.py --program_path initial.sv --results_dir ./result
python -c 'from evaluator import evaluate; print(evaluate("initial.sv"))'
```

## Framework adapters

- ShinkaEvolve: `initial.sv` and `evaluate.py` follow the upstream non-Python task interface (`--program_path`, `--results_dir`; metrics.json and correct.json). Configure language `verilog`, task_dir pointing here, and a model and budget you explicitly authorize. Start with one evaluation worker and one generation. No model is selected automatically.
- OpenEvolve: `initial.sv` uses // EVOLVE-BLOCK markers. `evaluator.py` exposes `evaluate(program_path)` returning numeric metrics. Use it as the evaluator for an OpenEvolve task with evaluator timeout >= 360 seconds. Configure your own provider and approved limits; no API keys are required for evaluator-only tests.
- Inspect the full candidate and rules before any public PR. A proven local score is not an official rank. The project repository and trusted CI are canonical.

Upstream references: https://github.com/SakanaAI/ShinkaEvolve/tree/main/examples/rtllm and https://github.com/algorithmicsuperintelligence/openevolve/blob/main/CONTRIBUTING.md.

This is an independently prepared adapter, not a claim that either upstream has accepted the example or endorsed SiliconArena. LLM-driven evolution was not run automatically. No telemetry, posting, installation of agent skills, or access to private systems is necessary.

Research and submission rules: https://github.com/rtl-ai/silicon-arena/blob/main/research/inference-002.md.
