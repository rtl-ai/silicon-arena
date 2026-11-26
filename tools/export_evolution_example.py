"""Export a standalone, reviewable evolution benchmark; no publishing or model calls."""
import argparse
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]
FILES={
 "integrations/rtl_dot8/initial.sv":"initial.sv",
 "integrations/rtl_dot8/evaluator.py":"evaluator.py",
 "integrations/rtl_dot8/evaluate.py":"evaluate.py",
 "integrations/rtl_dot8/README.md":"README.md",
 "tools/fast_judge.py":"tools/fast_judge.py",
 "inference/dot8.sv":"inference/dot8.sv",
 "judge/requirements.txt":"requirements.txt",
 "LICENSE":"LICENSE",
}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    for src,dst in FILES.items():
        path=a.output/dst
        path.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/src,path)
    print("Standalone example exported; review before proposing it upstream.")
if __name__=="__main__": main()
