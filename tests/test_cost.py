import unittest
from dataclasses import replace
from tools.cost import Assumptions, estimate
class CostTest(unittest.TestCase):
    def setUp(self):
        self.a=Assumptions(300,100,5000,0.2,10,0.98,1000000,10000)
    def test_volume(self):
        self.assertLess(estimate(replace(self.a, shipped_units=100000))["total_per_shipped_unit_usd"], estimate(self.a)["total_per_shipped_unit_usd"])
    def test_area(self):
        self.assertGreater(estimate(replace(self.a, die_area_mm2=200))["recurring_shipped_unit_usd"], estimate(self.a)["recurring_shipped_unit_usd"])
    def test_assembly_yield(self):
        self.assertGreater(estimate(replace(self.a, assembly_test_yield=.8))["recurring_shipped_unit_usd"], estimate(self.a)["recurring_shipped_unit_usd"])
    def test_invalid(self):
        with self.assertRaises(ValueError): estimate(replace(self.a, shipped_units=0))
