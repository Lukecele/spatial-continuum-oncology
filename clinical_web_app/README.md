---
title: In Silico Biophysical CRI Solver (RUO) - Post-ADAURA Stratification
emoji: 🧬
colorFrom: blue
colorTo: indigo
sdk: static
pinned: true
tags:
  - oncology
  - lung-cancer
  - egfr
  - biophysics
  - spatial-biology
  - precision-medicine
---

# In Silico Biophysical Composite Resistance Index (CRI) Solver (RUO)
### Post-ADAURA Adjuvant Stratification for Resected Stage IB–IIIA EGFR-Mutant NSCLC

**Lead Author & Principal Investigator:** Luca Celebrano, MD Candidate  
**Affiliation:** School of Medicine & Surgery, Università degli Studi di Napoli Federico II, Naples, Italy  
**Flagship Preprint:** *Nature Portfolio (Research Square)* DOI: [10.21203/rs.3.rs-11530312/v1](https://doi.org/10.21203/rs.3.rs-11530312/v1)  
**Journal Status:** Under Consideration at *Nature Communications* (Tracking: `NCOMMS-26-091227`)  
**CERN Zenodo Open Archive:** DOI [10.5281/zenodo.23754999](https://doi.org/10.5281/zenodo.23754999)  
**ELIXIR bio.tools:** [biotools:spatial-continuum-oncology](https://bio.tools/spatial-continuum-oncology)  
**Bioconda:** `conda install -c bioconda spatial-continuum`  
**BioContainers:** `quay.io/biocontainers/spatial-continuum:1.0.2--pyhdfd78af_0`  

---

## Overview

*Disclaimer: Research Use Only (RUO). This interactive application simulates reaction-diffusion transport physics to formulate translational hypotheses for prospective trial design; it does not constitute clinical prescribing advice or medical diagnostics.*

This interactive research application provides in silico biophysical transport simulations and cohort risk scoring for evaluating perivascular sanctuary burden in resected *EGFR*-mutated NSCLC.

### Core Capabilities:
1. **Single Patient In Silico CRI Solver (RUO):** Integrates IASLC architectural subtype, targeted NGS (*TP53* and *RB1* status), and stromal desmoplasia into the multi-parametric Composite Resistance Index (CRI).
2. **Cohort Batch Stratification & Kaplan-Meier Simulator:** Upload CSV patient cohorts or simulate the 604-patient MSKCC validation distribution to explore Disease-Free Survival (DFS) curves and hazard ratios.
3. **Reaction-Diffusion Biophysics Explorer:** Interactive simulation of radial osimertinib penetration gradients $C(r)$ across tumor cords to visualize perivascular persister sanctuaries.
4. **Direct Report Export:** Generates standardized research reports for documentation.

---

## Mathematical Formulation

$$\text{CRI} = w_S \cdot S + w_G \cdot G + w_M \cdot M$$

* $w_S = 0.47$ (Spatial Decoupling Score, derived from inter-capillary distance $\Delta r > 34\,\mu\text{m}$)
* $w_G = 0.33$ (Genomic Risk Tier, reflecting *TP53* and *RB1* co-mutational lineage plasticity)
* $w_M = 0.20$ (Microenvironmental Stroma Barrier, driven by interstitial fluid hypertension $P_{\text{ifp}} > 20\,\text{mmHg}$)

### Decision Stratification:
* **Tier 1 (CRI < 0.35):** Low Sanctuary Risk (5-Yr DFS > 85%). Protocolized safe discontinuation at Month 36.
* **Tier 2 (0.35 &le; CRI &le; 0.65):** Intermediate Risk (5-Yr DFS 50–65%). Intensified imaging & ctDNA surveillance or extended monotherapy.
* **Tier 3 (CRI > 0.65):** High Sanctuary Risk (5-Yr DFS < 25%). Mandatory maintenance extension or SG-ADAURA Arm B3 consolidation (Osimertinib + anti-VEGFR2 Ramucirumab).

---

## Citation

```bibtex
@article{celebrano2026spatialcontinuum,
  author    = {Celebrano, Luca},
  title     = {The Spatial-Genomic Oncology Continuum: Reaction-Diffusion Biophysics and Digital Twin Modeling Resolve the 36-Month Post-ADAURA Discontinuation Cliff in Non-Small Cell Lung Cancer},
  journal   = {Nature Communications (Under Consideration)},
  year      = {2026},
  doi       = {10.21203/rs.3.rs-11530312/v1},
  publisher = {Research Square (Nature Portfolio)},
  url       = {https://doi.org/10.21203/rs.3.rs-11530312/v1}
}
```
