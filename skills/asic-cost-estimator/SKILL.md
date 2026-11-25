---
name: asic-cost-estimator
description: "Estimate ASIC manufacturing cost, die yield, NRE amortization, packaging and system economics with explicit assumptions and sensitivity analysis."
---

# ASIC cost and yield estimation

Use for user-requested semiconductor economics. Ask for or explicitly mark wafer diameter, die area, wafer cost, defect density, package/test cost and yield, NRE, and shipped volume.

- Estimate gross dies per wafer, explaining edge/scribe exclusions and model uncertainty. Convert units consistently (100 mm² = 1 cm²).
- Illustrative Poisson die yield: exp(-D0 × area_cm²). This is a model, not foundry characterization; consider clustered defects, redundancy, binning and parametric yield when evidence exists.
- Compute wafer cost per known-good die, package/test cost adjusted for downstream yield, NRE per shipped unit, then recurring and all-in unit cost. Avoid double-counting stage losses.
- Compare low/base/high cases for volume, area, defect density, package and energy. Separate prototype/MPW prices from production quotations. Include memory, board and power when comparing system TCO.
- Show inputs, currency/date, assumptions, formula, uncertainty and missing vendor quotes. Never claim production economics from synthetic inputs.

A transparent illustrative implementation is [tools/cost.py](https://github.com/rtl-ai/silicon-arena/blob/main/tools/cost.py). Read-only example; no required network, registration or spend.
