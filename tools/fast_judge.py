#!/usr/bin/env python3
"""Fixed exact INT8 judge. Run untrusted HDL only in the supplied isolated CI sandbox."""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "inference/dot8.sv"
REF_HASH = "a41f047a8bebbce72cf331b7fcad1d61d4f9e6e6ff6b854a1cbfbd1a274b3ab5"
BASELINE = 4069
COMB = set("add sub mul div mod divfloor modfloor pow neg pos not and or xor xnor reduce_and reduce_or reduce_xor reduce_xnor reduce_bool logic_not logic_and logic_or lt le eq ne ge gt eqx nex mux pmux shift shiftx shl shr sshl sshr concat slice alu macc fa lut".split())
GATES = set("ANDNOT AND NAND NOR NOT ORNOT OR XNOR XOR MUX BUF NMUX".split())

class Rejected(Exception):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def validate_source(data):
    if len(data) > 65536 or not data:
        raise Rejected("candidate must be one nonempty RTL file <=64 KiB")
    try:
        s = data.decode("ascii")
    except UnicodeError:
        raise Rejected("candidate must use ASCII RTL")
    if any(ord(c) < 32 and c not in "\n\r\t" for c in s):
        raise Rejected("control characters")
    clean = re.sub(r"/\*[\s\S]*?\*/|//[^\n]*", "", s)
    if re.search(r'[\x60"\\#]|\(\*|\*/', clean):
        raise Rejected("directives, strings, escaped identifiers, delay/parameter syntax, and attributes are disallowed")
    if re.search(r"\b(initial|final|always_ff|posedge|negedge|assert|assume|cover|restrict|force|release|wait|bind|specify|primitive|config|interface|program|checker|package|import|export)\b", clean):
        raise Rejected("only stateless combinational RTL is accepted")
    if re.findall(r"\bmodule\s+([A-Za-z_]\w*)",clean) != ["dot8"]:
        raise Rejected("exactly one module named dot8 is required")
    if any(x not in ("$signed","$unsigned","$clog2","$bits") for x in re.findall(r"\$[A-Za-z_][A-Za-z_0-9]*",clean)):
        raise Rejected("system tasks/functions are disallowed")

def run(yosys, script, directory, timeout):
    env={k:os.environ[k] for k in ("PATH","SYSTEMROOT","LANG","LC_ALL","LD_LIBRARY_PATH") if k in os.environ}
    env["HOME"]=str(directory)
    env["XDG_CACHE_HOME"]=str(directory/".cache")
    env["TMPDIR"]=str(directory)
    try:
        r=subprocess.run([yosys,"-Q","-T","-p",script],cwd=directory,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    except subprocess.TimeoutExpired:
        raise Rejected("tool timeout; no proven score")
    if r.returncode:
        if b"proof did fail" in r.stdout or b"model found: FAIL" in r.stdout:
            raise Rejected("SAT counterexample: not equivalent")
        if b"timeout" in r.stdout.lower():
            raise Rejected("proof timeout; no proven score")
        raise Rejected("Yosys rejected design or proof (exit %d)" % r.returncode)
    return r.stdout

def design_json(path, mapped=False):
    obj=json.loads(path.read_text())
    modules=obj["modules"]
    if set(modules)!={"dot8"}:
        raise Rejected("extra modules or unresolved hierarchy")
    m=modules["dot8"]
    ports={k:(v["direction"],len(v["bits"])) for k,v in m["ports"].items()}
    if ports!={"a":("input",64),"b":("input",64),"result":("output",32)}:
        raise Rejected("wrong interface")
    if any(str(m.get("attributes",{}).get(k,"0")).strip("0") for k in ("blackbox","whitebox")):
        raise Rejected("blackbox or whitebox")
    for c in m["cells"].values():
        typ=c["type"]
        if mapped:
            if not (typ.startswith("$_") and typ.endswith("_") and typ[2:-1] in GATES):
                raise Rejected("non-combinational or unsupported mapped primitive")
        elif not (typ.startswith("$") and typ[1:] in COMB):
            raise Rejected("stateful or unsupported RTL primitive")
        if any(isinstance(b,str) and b not in ("0","1") for bits in c["connections"].values() for b in bits):
            raise Rejected("undefined cell connection")
    if any(isinstance(b,str) and b not in ("0","1") for p in m["ports"].values() for b in p["bits"]):
        raise Rejected("undefined port")
    return m

SPEC_BITS = 19  # every exact dot8 result lies in [-130048, 131072], so it fits signed 19 bits
ALG_CAP = 200000

def _poly(cell, M):
    """Multilinear polynomial (frozenset of nets -> coefficient mod M) of one mapped gate output."""
    t,c=cell
    def v(p):
        x=c[p][0]
        return {} if x=="0" else {frozenset():1} if x=="1" else {frozenset([x]):1}
    def lin(*terms):
        r=collections.defaultdict(int)
        for k,q in terms:
            for m,x in q.items(): r[m]=(r[m]+k*x)%M
        return {m:x for m,x in r.items() if x}
    def mul(p,q):
        return lin(*[(x*y,{m|n:1}) for m,x in p.items() for n,y in q.items()])
    one={frozenset():1}
    A=v("A")
    if t=="BUF": return A
    if t=="NOT": return lin((1,one),(-1,A))
    B=v("B")
    if t in ("MUX","NMUX"):
        S=v("S"); mux=lin((1,A),(1,mul(S,B)),(-1,mul(S,A)))
        return mux if t=="MUX" else lin((1,one),(-1,mux))
    AB=mul(A,B)
    return {"AND":lambda:AB,"NAND":lambda:lin((1,one),(-1,AB)),"OR":lambda:lin((1,A),(1,B),(-1,AB)),
            "NOR":lambda:lin((1,one),(-1,A),(-1,B),(1,AB)),"XOR":lambda:lin((1,A),(1,B),(-2,AB)),
            "XNOR":lambda:lin((1,one),(-1,A),(-1,B),(2,AB)),"ANDNOT":lambda:lin((1,A),(-1,AB)),
            "ORNOT":lambda:lin((1,one),(-1,B),(1,AB))}[t]()

def algebraic_proof(m, cap=ALG_CAP):
    """Backward-rewrite sum(2^k result[k]) over the mapped gates and compare with the exact
    signed dot-product polynomial modulo 2^19. Multilinear forms are unique over Z/2^19, so
    equality is a proof and a mismatch over input nets only is a disproof. Returns True,
    False, or None (inconclusive: let the SAT engine decide)."""
    a,b,r=(m["ports"][k]["bits"] for k in ("a","b","result"))
    if any(r[k]!=r[SPEC_BITS-1] for k in range(SPEC_BITS,32)):
        return None
    M=1<<SPEC_BITS
    drv={c["connections"]["Y"][0]:(c["type"][2:-1],c["connections"]) for c in m["cells"].values()}
    fanin=lambda n:[drv[n][1][p][0] for p in ("A","B","S") if p in drv[n][1]]
    order,seen=[],set()
    for root in r[:SPEC_BITS]:
        stack=[(root,False)]
        while stack:
            n,done=stack.pop()
            if done: order.append(n); continue
            if n in seen or n not in drv: continue
            seen.add(n); stack.append((n,True))
            stack.extend((x,False) for x in fanin(n) if x not in seen)
    users=collections.defaultdict(list)
    for n in order:
        for x in fanin(n): users[x].append(n)
    depth={}
    for n in reversed(order): depth[n]=1+max([depth[u] for u in users[n]] or [0])
    P=collections.defaultdict(int)
    for k in range(SPEC_BITS):
        if r[k]=="1": P[frozenset()]+=1<<k
        elif r[k]!="0": P[frozenset([r[k]])]+=1<<k
    P={x:y%M for x,y in P.items() if y%M}
    occ=collections.defaultdict(set)
    for x in P:
        for n in x: occ[n].add(x)
    for y in sorted(reversed(order),key=lambda n:depth[n]):
        F=_poly(drv[y],M)
        for x in list(occ.pop(y,())):
            c=P.pop(x)
            for n in x:
                if n!=y: occ[n].discard(x)
            base=x-{y}
            for f,fc in F.items():
                nx=base|f; old=P.get(nx,0); new=(old+c*fc)%M
                if new:
                    if not old:
                        for n in nx: occ[n].add(nx)
                    P[nx]=new
                elif old:
                    del P[nx]
                    for n in nx: occ[n].discard(nx)
        if len(P)>cap: return None
    w=[1<<i for i in range(7)]+[-128]
    spec=collections.defaultdict(int)
    for lane in range(8):
        for i in range(8):
            for j in range(8): spec[frozenset([a[8*lane+i],b[8*lane+j]])]+=w[i]*w[j]
    spec={x:y%M for x,y in spec.items() if y%M}
    if P==spec: return True
    inputs=set(a)|set(b)
    return False if all(n in inputs for x in P for n in x) else None

def synth(yosys, directory, source):
    d=directory/source
    d.mkdir()
    shutil.copyfile(directory/(source+".sv"),d/"design.sv")
    run(yosys,"read_verilog -sv design.sv; synth -top dot8; check -assert; write_json mapped.json",d,90)
    m=design_json(d/"mapped.json",True)
    counts=collections.Counter(c["type"] for c in m["cells"].values())
    return len(m["cells"]),dict(sorted(counts.items())),m

def evaluate(candidate, engine="auto", proof_timeout=120):
    exe=shutil.which("yosys") if engine=="native" else shutil.which("yowasp-yosys") if engine=="wasm" else (shutil.which("yowasp-yosys") or shutil.which("yosys"))
    if not exe: raise Rejected("Yosys 0.33 missing; install pinned YoWASP in a new venv or use native flow")
    version=subprocess.run([exe,"-V"],capture_output=True,text=True,timeout=30,check=True).stdout.strip()
    if not re.match(r"Yosys 0\.33(?:\s|\()",version):
        raise Rejected("unmatched Yosys version")
    reference=REF.read_bytes()
    if digest(reference)!=REF_HASH: raise Rejected("reference hash changed")
    raw=Path(candidate).read_bytes()
    validate_source(raw)
    start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix="arena-") as tmp:
        d=Path(tmp)
        (d/"ref.sv").write_bytes(reference)
        (d/"candidate.sv").write_bytes(raw)
        baseline,_,_=synth(exe,d,"ref")
        if baseline!=BASELINE: raise Rejected("baseline mismatch: %d != 4069" % baseline)
        run(exe,"read_verilog -sv -noautowire candidate.sv; hierarchy -check -top dot8; proc; opt; check -assert; write_json structural.json",d,60)
        design_json(d/"structural.json")
        count,cell_types,mapped=synth(exe,d,"candidate")
        pstart=time.monotonic()
        verdict=algebraic_proof(mapped)
        if verdict is False:
            raise Rejected("algebraic counterexample: scored netlist differs from exact dot product")
        if verdict:
            proof="algebraic rewriting of the scored gate netlist against the exact signed dot-product polynomial (mod 2^19, sign-extended)"
            log=b"algebraic proof: equal"
        else:
            proof="combinational RTL SAT equivalence for all 128 defined input bits"
            script=("read_verilog -sv -noautowire ref.sv; hierarchy -check -top dot8; proc; flatten; opt; check -assert; rename dot8 gold; design -stash reference; "
                    "read_verilog -sv -noautowire candidate.sv; hierarchy -check -top dot8; proc; flatten; opt; check -assert; rename dot8 gate; "
                    "design -copy-from reference gold; miter -equiv -make_assert -make_outputs gold gate miter; hierarchy -top miter; flatten; opt; "
                    "sat -verify -prove-asserts -set-def-inputs -enable_undef -timeout %d miter" % proof_timeout)
            log=run(exe,script,d,proof_timeout+15)
            if b"SAT proof finished - no model found: SUCCESS!" not in log:
                raise Rejected("missing affirmative SAT proof marker")
        proof_seconds=round(time.monotonic()-pstart,3)
    return {"status":"proved","proof":proof,
            "proof_seconds":proof_seconds,"seconds":round(time.monotonic()-start,3),
            "yosys_version":version,"engine":Path(exe).name,"baseline":baseline,"generic_cells":count,
            "delta_cells":count-baseline,"cell_types":cell_types,"candidate_sha256":digest(raw),
            "reference_sha256":REF_HASH,"proof_log_sha256":digest(log),
            "physical_ppba":None,"ranking":"provisional; independent trusted review required"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("candidate",type=Path,nargs="?",default=REF)
    p.add_argument("--engine",choices=("auto","native","wasm"),default="auto")
    p.add_argument("--proof-timeout",type=int,default=120,choices=range(1,121),metavar="1..120")
    args=p.parse_args()
    try:
        print(json.dumps(evaluate(args.candidate,args.engine,args.proof_timeout),sort_keys=True))
    except (Rejected,OSError,ValueError,KeyError,subprocess.SubprocessError) as e:
        reason=str(e) if isinstance(e,Rejected) else type(e).__name__
        print(json.dumps({"status":"rejected_or_unproved","reason":reason,"generic_cells":None,"physical_ppba":None}))
        raise SystemExit(2)

if __name__=="__main__": main()
