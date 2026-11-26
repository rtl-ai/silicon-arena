"""Copy one regular new candidate blob from exact PR head. Never checkout fork code."""
import argparse
from pathlib import Path
import re
import shutil
import subprocess

def git(*args):
    return subprocess.check_output(["git",*args],timeout=30)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--head",required=True)
    p.add_argument("--base",required=True)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    assert re.fullmatch("[0-9a-f]{40}",a.head) and re.fullmatch("[0-9a-f]{40}",a.base)
    merge_base=git("merge-base",a.base,a.head).decode().strip()
    fields=git("diff","--name-status","--no-renames","-z",merge_base,a.head).split(b"\0")
    if fields[-1]!=b"": raise SystemExit("invalid diff")
    fields=fields[:-1]
    if len(fields)%2: raise SystemExit("invalid diff")
    paths={}
    for i in range(0,len(fields),2):
        if fields[i]!=b"A": raise SystemExit("submissions may only add new files")
        path=fields[i+1].decode("ascii")
        m=re.fullmatch(r"submissions/([A-Za-z0-9][A-Za-z0-9_-]{0,79})/(dot8\.sv|SUBMISSION\.md)",path)
        if not m: raise SystemExit("only one submission folder's dot8.sv and SUBMISSION.md allowed")
        paths[path]=m.group(1)
    if len(paths) not in (1,2) or len(set(paths.values()))!=1:
        raise SystemExit("exactly one submission folder required")
    candidates=[p for p in paths if p.endswith("/dot8.sv")]
    if len(candidates)!=1: raise SystemExit("missing candidate dot8.sv")
    path=candidates[0]
    entry=git("ls-tree","-z",a.head,"--",path).decode("ascii").strip("\0")
    if not re.fullmatch(r"100644 blob [0-9a-f]{40}\t"+re.escape(path),entry):
        raise SystemExit("candidate must be a regular 100644 blob")
    size=int(git("cat-file","-s",a.head+":"+path))
    if not 0<size<=65536: raise SystemExit("candidate size outside bounds")
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/"tools").mkdir()
    (a.out/"inference").mkdir()
    shutil.copyfile("tools/fast_judge.py",a.out/"tools/fast_judge.py")
    shutil.copyfile("inference/dot8.sv",a.out/"inference/dot8.sv")
    (a.out/"candidate.sv").write_bytes(git("show",a.head+":"+path))
    print("Prepared exactly one candidate blob; no fork checkout or execution.")

if __name__=="__main__": main()
