import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from fast_judge import validate_source,Rejected,algebraic_proof,design_json

GOOD=b"module dot8(input wire [63:0] a,b,output wire signed [31:0] result); assign result=0; endmodule"
class SourcePolicy(unittest.TestCase):
    def test_plain(self):
        validate_source(GOOD)
    def test_bad(self):
        for data in (bytes([96])+b'include "secret"\n'+GOOD,GOOD+b"\nmodule x; endmodule",GOOD.replace(b"assign result=0;",b'initial $system("bad");'),GOOD.replace(b"assign result=0;",b"always @(posedge a[0]) result=0;"),GOOD.replace(b"assign result=0;",b"(* blackbox *) wire x; assign result=0;"),b"x"*65537):
            with self.subTest(data=data[:50]), self.assertRaises(Rejected):
                validate_source(data)
    def test_comment_not_code(self):
        validate_source(b"// $system and initial are forbidden\n"+GOOD)

def mapped(source):
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp)
        shutil.copyfile(source,d/"design.sv")
        subprocess.run([shutil.which("yowasp-yosys"),"-q","-p","read_verilog -sv design.sv; synth -top dot8; check -assert; write_json mapped.json"],cwd=d,check=True,timeout=300)
        return design_json(d/"mapped.json",True)

def ports(result):
    return {"a":{"direction":"input","bits":list(range(2,66))},"b":{"direction":"input","bits":list(range(66,130))},
            "result":{"direction":"output","bits":result}}

class AlgebraicProof(unittest.TestCase):
    def test_constant_zero_is_disproved(self):
        self.assertIs(algebraic_proof({"ports":ports(["0"]*32),"cells":{}}),False)
    def test_single_product_is_disproved(self):
        cell={"type":"$_AND_","connections":{"A":[2],"B":[66],"Y":[200]}}
        self.assertIs(algebraic_proof({"ports":ports([200]+["0"]*31),"cells":{"g":cell}}),False)
    def test_missing_sign_extension_is_inconclusive(self):
        self.assertIsNone(algebraic_proof({"ports":ports(["0"]*19+["1"]+["0"]*12),"cells":{}}))
    def test_unknown_cell_type_is_inconclusive(self):
        cell={"type":"$_DFF_P_","connections":{"C":[2],"D":[66],"Q":[200]}}
        self.assertIsNone(algebraic_proof({"ports":ports([200]+["0"]*31),"cells":{"ff":cell}}))

@unittest.skipUnless(shutil.which("yowasp-yosys"),"pinned yowasp-yosys from judge/requirements.txt is required")
class AlgebraicProofNetlists(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=mapped(ROOT/"candidates/inference/balanced_tree.sv")
    def test_correct_netlist_is_proved(self):
        self.assertIs(algebraic_proof(self.m),True)
    def test_mutated_netlists_are_disproved(self):
        cells=[k for k,c in self.m["cells"].items() if c["type"] in ("$_XOR_","$_AND_")][:20:4]
        verdicts=[]
        for name in cells:
            m=copy.deepcopy(self.m)
            m["cells"][name]["type"]={"$_XOR_":"$_XNOR_","$_AND_":"$_OR_"}[m["cells"][name]["type"]]
            verdicts.append(algebraic_proof(m))
            with self.subTest(cell=name):
                self.assertIsNot(verdicts[-1],True)  # None defers to the SAT engine
        self.assertIn(False,verdicts)
