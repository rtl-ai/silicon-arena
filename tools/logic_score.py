#!/usr/bin/env python3
"""Trusted-source generic synthesis comparison; not physical PPBA or a ranked score."""
import collections
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "baseline": ROOT / "inference/dot8.sv",
    "balanced_tree": ROOT / "candidates/inference/balanced_tree.sv",
}

def score(yosys, label, source, workdir):
    # Copy only the reviewed fixed source. No arbitrary HDL from untrusted PRs.
    d = workdir / label
    d.mkdir()
    shutil.copyfile(source, d/"design.sv")
    command = "read_verilog -sv design.sv; synth -top dot8; check -assert; write_json design.json"
    run = subprocess.run([yosys, "-Q", "-T", "-p", command], cwd=d, capture_output=True, text=True, timeout=180)
    if run.returncode:
        raise RuntimeError(run.stderr[-3000:] + run.stdout[-3000:])
    cells = json.loads((d/"design.json").read_text())["modules"]["dot8"]["cells"]
    counts = collections.Counter(c["type"] for c in cells.values())
    return {"label": label, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "generic_cell_count": len(cells), "cell_types": dict(sorted(counts.items()))}

def main():
    yosys = shutil.which("yosys")
    if not yosys:
        raise SystemExit("Yosys unavailable; no score produced.")
    version = subprocess.run([yosys,"-V"],check=True,capture_output=True,text=True,timeout=15).stdout.strip()
    # Correctness simulation is required, but is not a formal proof.
    subprocess.run(["python3",str(ROOT/"tools/verify_kernels.py"),"--track","inference","--self-test"],check=True,timeout=180)
    subprocess.run(["python3",str(ROOT/"tools/verify_kernels.py"),"--track","inference","--trusted-candidate",str(SOURCES["balanced_tree"])],check=True,timeout=180)
    with tempfile.TemporaryDirectory() as tmp:
        results = [score(yosys,label,source,Path(tmp)) for label,source in SOURCES.items()]
    report={"evidence_level":"generic synthesis only; not PPBA, no ranking",
            "yosys_version":version,"results":results,"formal":None,"post_route":None}
    Path("logic-score.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
if __name__ == "__main__":
    main()
