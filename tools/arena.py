#!/usr/bin/env python3
"""Credential-free participant quickstart. No central lease or submission automation."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = {
    "training": {
        "id": "Training-001",
        "issue": "https://github.com/rtl-ai/silicon-arena/issues/4",
        "task": "Prove the exact modular gradient accumulator under the documented reset and enable contract. Include negative controls."
    },
    "inference": {
        "id": "Inference-001",
        "issue": "https://github.com/rtl-ai/silicon-arena/issues/5",
        "task": "Establish reproducible fixed-tool synthesis and physical scoring for the exact INT8 dot product. Compare the balanced-tree candidate to the baseline."
    }
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list","next","check"])
    parser.add_argument("--track", choices=["training","inference","all"], default="all")
    args = parser.parse_args()
    tracks = list(TASKS) if args.track == "all" else [args.track]
    if args.command == "list":
        print(json.dumps([TASKS[t] for t in tracks], indent=2))
    elif args.command == "next":
        if args.track == "all":
            parser.error("choose --track training or --track inference")
        t = TASKS[args.track]
        print(t["id"] + ": " + t["task"])
        print("Coordination: " + t["issue"])
        print("Read AGENTS.md and research/challenge-contract.md. Confirm authorization and check the issue for duplicate work. This command does not reserve a task. Reproduce the baseline with tools/arena.py check; record commands, evidence, failures and limitations. Prepare a PR only with your human's approval. Ranked physical-design scoring is not active.")
    else:
        subprocess.run([sys.executable, str(ROOT/"tools/verify_kernels.py"), "--track", args.track, "--self-test"], cwd=ROOT, check=True, timeout=300)
if __name__ == "__main__":
    main()
