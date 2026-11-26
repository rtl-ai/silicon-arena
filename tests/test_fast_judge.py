import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from fast_judge import validate_source,Rejected

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
