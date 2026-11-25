#!/usr/bin/env python3
"""Reproduce the organizer baseline and measure a reviewed candidate.

This is an exploratory generic-cell score, not a proof, physical PPBA,
or an accepted rank. Do not run untrusted HDL on a credential-bearing host.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from logic_score import score, ROOT, SOURCES
from verify_kernels import verify

VERSION = "Yosys 0.33 (git sha1 2584903a060)"
BASELINE_SHA256 = "a41f047a8bebbce72cf331b7fcad1d61d4f9e6e6ff6b854a1cbfbd1a274b3ab5"
BASELINE_CELLS = 4069

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--trusted-candidate", type=Path,
                   help="Reviewed SystemVerilog dot8 source, in a separate isolated runner")
    args = p.parse_args()
    yosys = shutil.which("yosys")
    if not yosys:
        raise SystemExit("Yosys unavailable; no score.")
    version = subprocess.run([yosys, "-V"], capture_output=True, text=True,
                             check=True, timeout=15).stdout.strip()
    if version != VERSION:
        raise SystemExit("Unmatched Yosys version: " + version)
    ref = SOURCES["baseline"]
    if hashlib.sha256(ref.read_bytes()).hexdigest() != BASELINE_SHA256:
        raise SystemExit("Reference source changed; no comparable score.")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        base = score(yosys, "baseline", ref, root)
        if base["generic_cell_count"] != BASELINE_CELLS:
            raise SystemExit("Reference cell count does not match 4069; no comparable score.")
        data = {"metric": "generic_cell_count", "yosys_version": version,
                "baseline": base, "evidence": "generic synthesis + deterministic simulation",
                "formal_proof": None, "physical_ppba": None,
                "ranking_acceptance": "reference only"}
        data["baseline_simulation"] = verify("inference", ref)
        if args.trusted_candidate:
            path = args.trusted_candidate.resolve()
            data["candidate_simulation"] = verify("inference", path)
            data["candidate"] = score(yosys, "candidate", path, root)
            data["ranking_acceptance"] = "provisional; independent rerun and proof required"
            data["delta_cells"] = data["candidate"]["generic_cell_count"] - BASELINE_CELLS
        print(json.dumps(data, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
