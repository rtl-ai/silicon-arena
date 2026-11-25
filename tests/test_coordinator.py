import tempfile
import unittest
from pathlib import Path
from tools import coordinator as q

class CoordinatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/"test.sqlite"
        self.db=q.connect(self.path)
        q.seed(self.db,now=1000)

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_distinct_claims(self):
        other=q.connect(self.path)
        try:
            a=q.claim(self.db,"a",now=1001)
            b=q.claim(other,"b",now=1001)
            self.assertNotEqual(a["id"],b["id"])
        finally:
            other.close()

    def test_lease_and_token(self):
        a=q.claim(self.db,"a",track="training",now=1001)
        self.assertIsNone(q.claim(self.db,"b",track="training",now=1002))
        self.assertFalse(q.finish(self.db,a["id"],"wrong","passed",{},now=1002))
        self.assertFalse(q.finish(self.db,a["id"],a["token"],"passed",{},now=1001+q.LEASE))
        b=q.claim(self.db,"b",track="training",now=1001+q.LEASE)
        self.assertEqual(b["id"],a["id"])
        self.assertNotEqual(b["token"],a["token"])
        self.assertFalse(q.finish(self.db,a["id"],a["token"],"passed",{},now=1002+q.LEASE))
        self.assertTrue(q.finish(self.db,b["id"],b["token"],"passed",{},now=1002+q.LEASE))
        self.assertIsNone(q.claim(self.db,"a",track="training",now=1003+q.LEASE))

    def test_expiry_budget(self):
        for i in range(q.MAX_ATTEMPTS):
            a=q.claim(self.db,"a",track="training",now=1001+i*q.LEASE)
            self.assertIsNotNone(a)
        self.assertIsNone(q.claim(self.db,"a",track="training",now=1001+q.MAX_ATTEMPTS*q.LEASE))
        s=[x for x in q.status(self.db) if x["track"]=="training"][0]
        self.assertEqual(s["state"],"failed")

    def test_seed_preserves_state(self):
        a=q.claim(self.db,"a",track="training",now=1001)
        self.assertTrue(q.finish(self.db,a["id"],a["token"],"blocked",{"missing_dependencies":["example"]},now=1002))
        q.seed(self.db,now=1003)
        s=[x for x in q.status(self.db) if x["track"]=="training"][0]
        self.assertEqual(s["state"],"blocked")

if __name__=="__main__":
    unittest.main()
