"""Illustrative economic model; not a vendor quote or a calibrated yield model."""
from dataclasses import dataclass, asdict
from math import pi, sqrt, exp, isfinite
import json

@dataclass(frozen=True)
class Assumptions:
    wafer_diameter_mm: float
    die_area_mm2: float
    wafer_cost_usd: float
    defect_density_cm2: float
    package_test_per_attempt_usd: float
    assembly_test_yield: float
    nre_usd: float
    shipped_units: int

def estimate(a: Assumptions):
    if any(not isfinite(x) for x in asdict(a).values()):
        raise ValueError("non-finite assumptions")
    if min(a.wafer_diameter_mm, a.die_area_mm2, a.wafer_cost_usd, a.shipped_units) <= 0:
        raise ValueError("positive wafer diameter, area, cost, volume required")
    if min(a.defect_density_cm2, a.package_test_per_attempt_usd, a.nre_usd) < 0 or not 0 < a.assembly_test_yield <= 1:
        raise ValueError("invalid cost or yield")
    # Common continuous gross-die approximation; excludes scribe/edge exclusion.
    gross = pi*(a.wafer_diameter_mm/2)**2/a.die_area_mm2 - pi*a.wafer_diameter_mm/sqrt(2*a.die_area_mm2)
    if gross < 1:
        raise ValueError("die too large for approximation")
    wafer_yield = exp(-a.defect_density_cm2*a.die_area_mm2/100)
    if wafer_yield == 0:
        raise ValueError("yield too small")
    die_cost = a.wafer_cost_usd/(gross*wafer_yield)
    recurring = (die_cost+a.package_test_per_attempt_usd)/a.assembly_test_yield
    return {"gross_dies_approx":gross,"wafer_yield_poisson":wafer_yield,
            "known_good_die_usd":die_cost,"recurring_shipped_unit_usd":recurring,
            "nre_per_unit_usd":a.nre_usd/a.shipped_units,
            "total_per_shipped_unit_usd":recurring+a.nre_usd/a.shipped_units}

if __name__ == "__main__":
    a=Assumptions(300,100,5000,0.2,10,0.98,1000000,10000)
    print(json.dumps({"status":"illustrative assumptions only","inputs":asdict(a),"estimates":estimate(a)},indent=2))
