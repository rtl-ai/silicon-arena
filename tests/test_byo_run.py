import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import byo_run  # noqa: E402

GOOD = "module dot8(input [63:0] a, input [63:0] b, output [31:0] result); assign result = 0; endmodule"
PROVED = {"status": "proved", "proof": "algebraic rewriting ...", "generic_cells": 4000,
          "yosys_version": "Yosys 0.33", "candidate_sha256": "ab" * 32}


def args(**kw):
    base = dict(handle="t-fake-1", label="fake model", author=None, attempts=3, model_timeout=5,
                engine="wasm", proof_timeout=10, model_cmd=["fake"])
    base.update(kw)
    return mock.Mock(**base)


class Extract(unittest.TestCase):
    def test_last_dot8_block_wins(self):
        answer = "```sv\nmodule helper; endmodule\n```\ntext\n```systemverilog\n%s\n```\n```systemverilog\n%s // v2\n```" % (GOOD, GOOD)
        self.assertTrue(byo_run.extract_rtl(answer).rstrip().endswith("// v2"))

    def test_bare_module(self):
        self.assertEqual(byo_run.extract_rtl("Here:\n" + GOOD + "\nDone"), GOOD + "\n")

    def test_none(self):
        self.assertIsNone(byo_run.extract_rtl("I cannot do that."))


class Prompt(unittest.TestCase):
    def test_fixed_prompt_contains_reference_and_baseline(self):
        p = byo_run.base_prompt()
        self.assertIn(byo_run.fast_judge.REF.read_text().strip(), p)
        self.assertIn(str(byo_run.fast_judge.BASELINE), p)
        self.assertEqual(byo_run.sha256(p), byo_run.sha256(byo_run.base_prompt()))


class Loop(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        patcher = mock.patch.object(byo_run, "ROOT", self.tmp)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_keeps_best_and_feeds_back(self):
        prompts = []
        answers = iter(["no code", "```systemverilog\n%s // a\n```" % GOOD, "```systemverilog\n%s // b\n```" % GOOD])
        scores = iter([dict(PROVED, generic_cells=3900), dict(PROVED, generic_cells=3950)])

        def model(cmd, prompt, timeout):
            prompts.append(prompt)
            return next(answers)

        with mock.patch.object(byo_run, "judge", lambda *a: next(scores)):
            self.assertEqual(byo_run.run(args(), model), 0)
        out = self.tmp / "submissions/t-fake-1"
        self.assertTrue((out / "dot8.sv").read_text().rstrip().endswith("// a"))
        md = (out / "SUBMISSION.md").read_text()
        self.assertIn("value: 3900", md)
        self.assertIn("no module dot8 code block", md)
        self.assertIn("REJECTED - no module dot8", prompts[1])
        self.assertIn("Best proved so far: 3900", prompts[2])
        self.assertEqual(sorted(p.name for p in out.iterdir()), ["SUBMISSION.md", "dot8.sv"])

    def test_nothing_written_without_proof(self):
        with mock.patch.object(byo_run, "judge", lambda *a: {"status": "rejected", "reason": "x"}):
            self.assertEqual(byo_run.run(args(attempts=2), lambda *a: GOOD), 1)
        self.assertFalse((self.tmp / "submissions/t-fake-1").exists())

    def test_model_error_stops(self):
        def model(*a):
            raise RuntimeError("quota")
        self.assertEqual(byo_run.run(args(), model), 1)

    def test_existing_handle_refused(self):
        (self.tmp / "submissions/t-fake-1").mkdir(parents=True)
        with self.assertRaises(SystemExit):
            byo_run.run(args(), lambda *a: GOOD)


class Cli(unittest.TestCase):
    def test_bad_handle_and_missing_cmd(self):
        for argv in (["--handle", "../x", "--label", "l", "--", "m"], ["--handle", "ok", "--label", "l"], ["--label", "l", "--", "m"]):
            with self.subTest(argv=argv), self.assertRaises(SystemExit), mock.patch("sys.stderr"):
                byo_run.main(argv)

    def test_print_prompt_needs_no_handle(self):
        with mock.patch("builtins.print") as out:
            self.assertEqual(byo_run.main(["--print-prompt"]), 0)
        self.assertIn("module dot8", out.call_args[0][0])


class OaiChat(unittest.TestCase):
    def test_posts_prompt_and_prints_reply(self):
        import io
        import json
        import oai_chat
        seen = {}

        def fake_urlopen(req, timeout):
            seen["url"], seen["body"], seen["auth"] = req.full_url, json.loads(req.data), req.get_header("Authorization")
            return io.BytesIO(json.dumps({"choices": [{"message": {"content": "ANSWER"}}]}).encode())

        with mock.patch.object(oai_chat.urllib.request, "urlopen", fake_urlopen), \
                mock.patch("sys.stdin", io.StringIO("PROMPT")), mock.patch("sys.stdout", new_callable=io.StringIO) as out, \
                mock.patch.dict("os.environ", {"K": "secret"}):
            oai_chat.main(["--base-url", "http://x/v1/", "--model", "m", "--key-env", "K"])
        self.assertEqual(out.getvalue(), "ANSWER")
        self.assertEqual(seen["url"], "http://x/v1/chat/completions")
        self.assertEqual(seen["body"]["messages"][0]["content"], "PROMPT")
        self.assertEqual(seen["auth"], "Bearer secret")


@unittest.skipUnless(shutil.which("yowasp-yosys"), "pinned yowasp-yosys from judge/requirements.txt is required")
class RealJudge(unittest.TestCase):
    def test_reference_answer_is_proved(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = byo_run.judge(byo_run.fast_judge.REF.read_text(), Path(tmp), "wasm", 60)
        self.assertEqual(result["status"], "proved")
        self.assertEqual(result["generic_cells"], byo_run.fast_judge.BASELINE)


if __name__ == "__main__":
    unittest.main()
