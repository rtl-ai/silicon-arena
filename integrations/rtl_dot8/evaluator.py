"""OpenEvolve-compatible evaluation; call only in a disposable, authorized workspace."""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
JUDGE = HERE / "tools/fast_judge.py" if (HERE/"tools/fast_judge.py").is_file() else ROOT/"tools/fast_judge.py"

def score(program_path):
    # The candidate is HDL data, never a Python import or executable.
    # No model calls or external submissions are made here.
    env = {k:os.environ[k] for k in ("PATH","SYSTEMROOT","LANG","LC_ALL","LD_LIBRARY_PATH") if k in os.environ}
    try:
        p = subprocess.run([sys.executable,str(JUDGE),str(Path(program_path).resolve()),"--proof-timeout","90"],
                           capture_output=True,text=True,timeout=360,env=env)
        data = json.loads(p.stdout)
        if p.returncode != 0 or data.get("status") != "proved":
            return {"combined_score":0.0,"valid":0.0},data.get("reason","candidate rejected or proof incomplete")
        cells = data["generic_cells"]
        if not isinstance(cells,int) or cells<=0 or data["baseline"]!=4069:
            return {"combined_score":0.0,"valid":0.0},"invalid score"
        return {"combined_score":4069.0/cells,"valid":1.0,"generic_cells":float(cells),"proof_seconds":float(data["proof_seconds"])},None
    except (OSError,ValueError,KeyError,subprocess.SubprocessError):
        return {"combined_score":0.0,"valid":0.0},"evaluation unavailable or timed out"

def evaluate(program_path):
    metrics,_=score(program_path)
    return metrics
