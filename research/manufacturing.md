# Manufacturing release gates (proposed)
A public predictive node (e.g. ASAP7) is not a fabrication offer. Public PDKs can be suitable for prototype flows without being qualified for production; confirm the exact foundry/PDK release.
- Specification: product/workload, target process, package, interfaces, quality, temperature, reliability and volume assumptions.
- RTL: formal equivalence, regression, lint, CDC/RDC, protocol verification, reset behavior, numerical edge cases, coverage closure.
- Physical: multi-corner setup/hold STA, extracted parasitics, congestion, signal integrity, power integrity/IR drop/EM, DRC/LVS/ERC/antenna and density checks, foundry acceptance.
- DFT and test: scan/ATPG, SRAM BIST/repair if applicable, test coverage, ATE plan and cost.
- FPGA and software: documented reproducible end-to-end workload; firmware, compiler/runtime, drivers, diagnostics.
- Prototype: MPW quotation, authorized budget, GDS release review, packaged silicon/board bring-up, characterization across operating conditions.
- Production: commercial production PDK and signoff methodology as applicable, package thermal/mechanical constraints, qualification/reliability plan, yield monitoring, test/binning, unit economics at stated volume and vendor acceptance.
- Cost assumptions must be labeled; no purchases or tapeout submissions without express owner approval.
