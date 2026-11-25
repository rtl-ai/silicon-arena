from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ("gradient_tb", "training/gradient_accumulator.sv", "tests/gradient_tb.sv"),
    ("dot_tb", "inference/dot8.sv", "tests/dot_tb.sv"),
]
if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        for top, rtl, tb in CASES:
            output = str(Path(tmp) / top)
            subprocess.run(["iverilog", "-g2012", "-s", top, "-o", output, str(ROOT/rtl), str(ROOT/tb)], check=True, timeout=60)
            subprocess.run(["vvp", output], check=True, timeout=60)
