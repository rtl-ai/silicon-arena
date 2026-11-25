import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("rtl-optimizer", "rtl-formal-verification", "asic-cost-estimator", "ai-accelerator-research")

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.scripts = 0
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.scripts += 1
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))

class DiscoveryTests(unittest.TestCase):
    def test_catalog(self):
        c=json.loads((ROOT/"docs/challenges.json").read_text())
        self.assertEqual(c["project"], "SiliconArena")
        self.assertFalse(c["physical_ppba_ranked"])
        self.assertIsNone(c["external_agents"])
        self.assertFalse(c["fabricated_silicon"])
        evidence=json.loads((ROOT/"research/evidence/generic-synthesis-20261125.json").read_text())
        counts={x["label"]:x["generic_cell_count"] for x in evidence["results"]}
        challenge=next(x for x in c["challenges"] if x["id"]=="inference-002")
        self.assertEqual(challenge["baseline"],counts["baseline"])
        self.assertEqual(challenge["prior_candidate"],counts["balanced_tree"])

    def test_static_page(self):
        page=(ROOT/"docs/index.html").read_text()
        parser=Parser()
        parser.feed(page)
        self.assertEqual(parser.scripts, 0)
        for url in parser.links:
            if url and not url.startswith(("https://", "#")):
                self.assertTrue((ROOT/"docs"/url).is_file(), url)
        self.assertIn("4,069",page)
        self.assertIn("4,366",page)
        tree=ElementTree.parse(ROOT/"docs/sitemap.xml")
        self.assertTrue(tree.getroot().tag.endswith("urlset"))
        self.assertEqual((ROOT/"llms.txt").read_bytes(), (ROOT/"docs/llms.txt").read_bytes())

    def test_skill_metadata(self):
        for name in SKILLS:
            content=(ROOT/"skills"/name/"SKILL.md").read_text()
            self.assertTrue(content.startswith("---\nname: "+name+"\n"))
            self.assertRegex(content, r'(?m)^description: ".+"$')
            self.assertLess(len(content.split("---",2)[1]),1500)

if __name__ == "__main__":
    unittest.main()
