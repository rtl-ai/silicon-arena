"""ShinkaEvolve non-Python evaluator interface."""
import argparse
import json
from pathlib import Path
from evaluator import score

def main(program_path,results_dir):
    metrics,error=score(program_path)
    out=Path(results_dir)
    out.mkdir(parents=True,exist_ok=True)
    correct=metrics["valid"]==1.0
    obj={"combined_score":metrics["combined_score"],"public":metrics,"private":{},"extra_data":{},
         "text_feedback":error or "RTL SAT equivalence proven. Minimize generic cells; this is not physical PPBA."}
    (out/"metrics.json").write_text(json.dumps(obj,indent=2)+"\n")
    (out/"correct.json").write_text(json.dumps({"correct":correct,"error":error or ""},indent=2)+"\n")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--program_path",required=True)
    p.add_argument("--results_dir",required=True)
    a=p.parse_args()
    main(a.program_path,a.results_dir)
