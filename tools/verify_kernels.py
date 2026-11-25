#!/usr/bin/env python3
"""Independent deterministic simulation. NOT formal or physical signoff.
Run only trusted RTL, or in a separately sandboxed runner with no secrets.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261125
MASK32 = (1 << 32) - 1
RTL = {
    "training": ROOT / "training/gradient_accumulator.sv",
    "inference": ROOT / "inference/dot8.sv",
}
TRAIN_TB = """
module verifier_tb;
    reg clk=0, reset=0, clear=0, enable=0;
    reg signed [7:0] activation, gradient;
    wire signed [31:0] total;
    gradient_accumulator dut(clk,reset,clear,enable,activation,gradient,total);
    reg [31:0] expected;
    integer f, n, rc;
    initial begin
        f=$fopen("vectors.txt","r"); if (!f) $fatal(1,"vectors missing");
        n=0;
        while (!$feof(f)) begin
            rc=$fscanf(f,"%h %h %h %h %h %h", reset, clear, enable, activation, gradient, expected);
            if (rc != 6) begin if (!$feof(f)) $fatal(1,"bad vector"); end
            else begin
                #2; clk=1; #2;
                if (total !== expected) $fatal(1,"mismatch vector %0d got=%h want=%h",n,total,expected);
                clk=0; n=n+1;
            end
        end
        $display("PASS vectors=%0d",n); $finish;
    end
endmodule
"""
INFER_TB = """
module verifier_tb;
    reg [63:0] a, b;
    wire signed [31:0] result;
    dot8 dut(a,b,result);
    reg [31:0] expected;
    integer f, n, rc;
    initial begin
        f=$fopen("vectors.txt","r"); if (!f) $fatal(1,"vectors missing");
        n=0;
        while (!$feof(f)) begin
            rc=$fscanf(f,"%h %h %h",a,b,expected);
            if (rc != 3) begin if (!$feof(f)) $fatal(1,"bad vector"); end
            else begin
                #2;
                if (result !== expected) $fatal(1,"mismatch vector %0d got=%h want=%h",n,result,expected);
                n=n+1;
            end
        end
        $display("PASS vectors=%0d",n); $finish;
    end
endmodule
"""
def signed8(v):
    v &= 255
    return v - 256 if v >= 128 else v

def training_vectors():
    rng = random.Random(SEED)
    total = 0
    def row(r,c,e,a,b):
        nonlocal total
        if r or c:
            total = 0
        elif e:
            total = (total + a*b) & MASK32
        return f"{r:x} {c:x} {e:x} {a&255:02x} {b&255:02x} {total:08x}"
    yield row(1,0,0,0,0)
    # All 65,536 signed operand pairs, checking every accumulated output.
    for a in range(-128,128):
        for b in range(-128,128):
            yield row(0,0,1,a,b)
    # Explicit signed wraparound in both directions.
    yield row(0,1,1,127,127)
    for _ in range(131073):
        yield row(0,0,1,-128,-128)
    yield row(0,1,0,0,0)
    for _ in range(132105):
        yield row(0,0,1,-128,127)
    # All priority combinations, then reproducible arbitrary control sequences.
    for r in range(2):
        for c in range(2):
            for e in range(2):
                yield row(r,c,e,-128,127)
    for i in range(20000):
        yield row(int(i%101==0),int(i%29==0),rng.randrange(2),rng.randrange(-128,128),rng.randrange(-128,128))

def inference_vectors():
    rng = random.Random(SEED)
    def row(a,b):
        ap = sum((x&255)<<(8*i) for i,x in enumerate(a))
        bp = sum((x&255)<<(8*i) for i,x in enumerate(b))
        out = sum(x*y for x,y in zip(a,b)) & MASK32
        return f"{ap:016x} {bp:016x} {out:08x}"
    # Every lane sees every signed 8-bit operand pair.
    for ai in range(256):
        for bi in range(256):
            yield row([signed8(ai+37*i) for i in range(8)],
                      [signed8(bi+53*i) for i in range(8)])
    for a,b in [(-128,-128),(-128,127),(127,127),(0,127)]:
        yield row([a]*8,[b]*8)
    for _ in range(10000):
        yield row([rng.randrange(-128,128) for _ in range(8)],
                  [rng.randrange(-128,128) for _ in range(8)])

def verify(track, source):
    vectors = training_vectors() if track=="training" else inference_vectors()
    bench = TRAIN_TB if track=="training" else INFER_TB
    source = Path(source).resolve()
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory() as d:
        tmp=Path(d)
        count=0
        h=hashlib.sha256()
        with (tmp/"vectors.txt").open("wb") as f:
            for line in vectors:
                data=(line+"\n").encode("ascii")
                h.update(data); f.write(data); count+=1
        (tmp/"verifier_tb.sv").write_text(bench)
        compile_run=subprocess.run(["iverilog","-g2012","-s","verifier_tb","-o","sim",str(source),"verifier_tb.sv"],cwd=tmp,capture_output=True,text=True,timeout=60)
        if compile_run.returncode:
            raise RuntimeError("RTL compile failed: "+compile_run.stderr[-2000:])
        sim=subprocess.run(["vvp","sim"],cwd=tmp,capture_output=True,text=True,timeout=120)
        if sim.returncode or f"PASS vectors={count}" not in sim.stdout.splitlines():
            raise RuntimeError("simulation failed: "+(sim.stdout+sim.stderr)[-2000:])
    return {"track":track,"status":"pass","evidence":"deterministic RTL simulation only","vectors":count,
            "seed":SEED,"rtl_sha256":digest,"vectors_sha256":h.hexdigest(),
            "simulator":subprocess.run(["iverilog","-V"],capture_output=True,text=True,timeout=10,check=True).stdout.splitlines()[0]}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--track",choices=["training","inference","all"],default="all")
    p.add_argument("--trusted-candidate",type=Path,help="Only for an inspected RTL file with matching interface; never run arbitrary PR code on credential-bearing hosts.")
    p.add_argument("--self-test",action="store_true",help="Run intentionally incorrect candidates and require mismatches.")
    args=p.parse_args()
    if args.trusted_candidate and (args.track=="all" or args.self_test):
        p.error("candidate requires a single track and cannot be used with self-test")
    tracks=RTL if args.track=="all" else [args.track]
    results=[]
    for track in tracks:
        results.append(verify(track,args.trusted_candidate or RTL[track]))
        if args.self_test:
            with tempfile.TemporaryDirectory() as d:
                src=RTL[track].read_text()
                needle,replacement=("activation * gradient","activation + gradient") if track=="training" else ("lhs * rhs","lhs + rhs")
                if needle not in src:
                    raise RuntimeError("mutation target missing")
                mutant=Path(d)/"mutant.sv"; mutant.write_text(src.replace(needle,replacement,1))
                try:
                    verify(track,mutant)
                except RuntimeError as exc:
                    if "mismatch vector" not in str(exc):
                        raise
                    results.append({"track":track,"negative_control":"incorrect multiply replaced with add","status":"rejected"})
                else:
                    raise RuntimeError("negative control incorrectly passed")
    print(json.dumps(results,indent=2))

if __name__=="__main__":
    main()
