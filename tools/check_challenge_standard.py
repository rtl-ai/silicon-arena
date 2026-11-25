"""Check local challenge and submission metadata against the documented v1 contract.
This is a project-side check, not a certification by the external directory.
Requires PyYAML.
"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
def meta(path):
    raw = path.read_text(encoding="utf-8")
    assert raw.startswith("---\n"), str(path)
    return yaml.safe_load(raw.split("---", 2)[1])

def main():
    p = meta(ROOT / "PROBLEM.md")
    assert p["spec"] == "problem.md/v1"
    assert p["name"] and p["submit"]["path"] == "submissions/<handle>/"
    tracks = {x["id"]: x for x in p["tracks"]}
    assert tracks["inference-002"]["baseline"] == 4069
    assert tracks["inference-002"]["direction"] == "minimize"
    assert all(x["metric"] and x["direction"] in ("minimize", "maximize") for x in tracks.values())
    entries = list((ROOT/"submissions").glob("*/SUBMISSION.md"))
    assert entries, "No actual submissions"
    for entry in entries:
        s = meta(entry)
        assert s["spec"] == "submission.md/v1"
        assert s.get("author") or s.get("authors")
        assert (entry.parent/s["problem"]).resolve() == ROOT/"PROBLEM.md"
        assert s["results"]
        for r in s["results"]:
            assert r["track"] in tracks
            assert isinstance(r["value"], (int,float)) and not isinstance(r["value"], bool)
    baseline=meta(ROOT/"submissions/rtl-ai-baseline/SUBMISSION.md")
    assert baseline["results"][0]["value"] == 4069
    print("Local PROBLEM.md / SUBMISSION.md v1 structure: PASS")

if __name__ == "__main__":
    main()
