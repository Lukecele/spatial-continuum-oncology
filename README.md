# The Spatial-Genomic Oncology Continuum

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Target: Nature Communications](https://img.shields.io/badge/Target-Nature%20Communications-darkred.svg)](https://www.nature.com/ncomms/)
[![Preprint: medRxiv](https://img.shields.io/badge/Preprint-medRxiv-orange.svg)](https://www.medrxiv.org/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-pure%20standard%20lib-brightgreen.svg)]()

**A Biophysical Reaction-Diffusion Theory of Pharmacological Sanctuaries, the Post-ADAURA Cessation Dilemma, and the Bedside Composite Resistance Index (CRI)**

*Author:* **Dr. Luca Celebrano**, MD Candidate  
*Affiliation:* Department of Clinical Medicine and Surgery, School of Medicine, Università degli Studi di Napoli Federico II, Naples, Italy  
*Correspondence:* `l.celebrano@studenti.unina.it`  

---

## 📌 Executive Summary

In early-stage *EGFR*-mutated non-small cell lung cancer (NSCLC), 36 months of adjuvant osimertinib significantly extends disease-free survival (ADAURA trial). However, longitudinal molecular residual disease (MRD) monitoring (*Herbst et al., Nature Medicine 2025*) reveals an alarming paradox:
* **$67.9\%$ of all recurrence events occur after the planned 36-month discontinuation.**
* **$57.9\%$ of post-cessation relapses cluster within the first 12 months** post-discontinuation.
* **$75\text{--}80\%$ of relapsing patients do NOT harbor secondary pocket mutations** (such as *EGFR* C797S), and 4th-generation allosteric inhibitors fail to prevent relapse.

This repository provides the complete, mathematically closed, and empirical literature-validated computational framework resolving this dilemma from **first physical principles**.

```
    Microvascular Reaction-Diffusion Cord & Pharmacological Sanctuary:
    Capillary (r0 = 10 um)        Sterilized Cuff                Cytostatic Sanctuary Cuff             Necrotic Core
    [ C0 = 28.6 nM ] ======> [ C(r) > IC50 (10 nM) ] ======> [ 2 nM < C(r) < 10 nM (G0/G1) ] ======> [ Hypoxia / Necrosis ]
    |------------------------ 0 to 165.9 um ----------------|--- 165.9 um to 200.0 um (31.3% Vol) ---|---- r > 200 um ----|
```

---

## 🔬 Core Biophysical Equations

### 1. Starling-Darcy Convective Shutdown ($Pe < 0.1$)
In solid lung adenocarcinoma, elevated Interstitial Fluid Pressure ($\text{IFP} = 9.8 \pm 6.8\ \text{mmHg}$, *Mori et al. 2015*) equilibrates with microvascular pressure ($P_v \approx 15\text{--}20\ \text{mmHg}$), collapsing the transvascular hydrostatic pressure gradient:
$$\Delta P = P_v - \text{IFP} \le 10\ \text{mmHg} \implies \mathbf{v}_{\text{fluid}} < 0.05\ \mu\text{m/s}$$
$$Pe = \frac{v_{\text{fluid}} \cdot L}{D_{\text{eff}}} < 0.1$$
Convective filtration ceases, establishing **100% diffusion-dominated transport**.

### 2. Cylindrical Bessel $K_0$ Reaction-Diffusion Concentration Profile
Steady-state radial concentration from a cylindrical microvessel is governed by the modified Bessel function of the second kind of order zero:
$$C(r) = C_0 \cdot \frac{K_0(r/\lambda)}{K_0(r_0/\lambda)}$$
where:
* $r_0 = 10.0\ \mu\text{m}$ (capillary radius)
* $D_{\text{eff}} = 59.29\ \mu\text{m}^2/\text{s}$ (interstitial diffusivity)
* $k = 1.5052 \times 10^{-4}\ \text{s}^{-1}$ (tissue clearance rate constant)
* $\lambda = \sqrt{D_{\text{eff}} / k} = 627.6\ \mu\text{m}$ (characteristic penetration length)
* $\theta = \frac{\text{IC}_{50}}{C_{0,\text{free}}} = \frac{10.0\ \text{nM}}{28.62\ \text{nM}} = 0.349$

The critical radius at which $C(r_{\text{crit}}) = \text{IC}_{50}$ is:
$$r_{\text{crit}} = \mathbf{165.89\ \mu\text{m}}$$

Because the empirical oxygen viability boundary in human lung carcinoma extends to $r_{\text{ox}} = 200.0\ \mu\text{m}$ (*Thomlinson & Gray, Br J Cancer 1955*), a **mandatory sub-therapeutic pharmacological sanctuary** exists:
$$\Delta r = r_{\text{ox}} - r_{\text{crit}} = 200.0 - 165.89 = \mathbf{34.11\ \mu\text{m}}$$
$$f_{\text{vol}} = \frac{r_{\text{ox}}^2 - r_{\text{crit}}^2}{r_{\text{ox}}^2 - r_0^2} = \frac{200^2 - 165.89^2}{200^2 - 10^2} = \mathbf{31.28\%}$$

---

## 📊 Longitudinal ctDNA Mathematical Lead Time Identity

During active therapy, sanctuary cells ($2\text{--}8\ \text{nM}$) remain trapped in cytostatic $G_0/G_1$ dormancy. Upon drug withdrawal at Month 36 ($C \to 0$), persister cells awaken into exponential clonal expansion ($T_d = 24.6\ \text{days}$):
$$\Delta t_{\text{lead}} = T_d \cdot \log_2(100) = 6.644 \cdot 24.6\ \text{days} = 163.4\ \text{days} = \mathbf{5.37\ \text{months}}$$
* **Clinical Trial Observation (Herbst et al., *Nat Med* 2025):** Median $4.7\ \text{months}$ ($95\%\,\text{CI}: 2.2\text{--}5.6\ \text{months}$).  
* **Concordance:** Our derived analytical lead time falls strictly inside the human clinical $95\%\,\text{CI}$.

---

## 💻 Software Suite (Zero External Dependencies)

All calculation tools are located in `software_strumenti_calcolo/` and run using the Python standard library with **zero external pip dependencies**:

### 1. Bedside Composite Resistance Index (CRI) Calculator
Computes risk tier and clinical action at ADAURA Month 36:
$$\text{CRI} = 0.47 \mathcal{S} + 0.33 \mathcal{G} + 0.20 \mathcal{M}$$

```bash
python3 software_strumenti_calcolo/cri_calc.py --pattern solid --tp53 mutated --rb1 mutated --stroma dense
```
**Output:**
```
========================================================================
  COMPOSITE RESISTANCE INDEX (CRI): 1.000 / 1.000
  CLINICAL RISK STRATIFICATION:    TIER 3 (HIGH RESISTANCE & SANCTUARY RISK)
  RECOMMENDATION: DO NOT DISCONTINUE OSIMERTINIB AT MONTH 36!
  Mandatory ongoing treatment: Extended Osimertinib or SG-ADAURA Arm B3
========================================================================
```

### 2. Analytical & Statistical Audit Suite
Verifies dimensional consistency, Bessel $K_0$ root, and 6-cohort compatibility ($N = 3,205$):
```bash
python3 software_strumenti_calcolo/audit_matematica_e_statistica.py
```

### 3. Adversarial Stress-Testing & Falsification Suite
Evaluates non-universality boundaries (Péclet breakdown, BBB, bypass genetics):
```bash
python3 software_strumenti_calcolo/test_stress_avversi.py
```

### 4. Scientific Figure Generator (300 DPI & Vector PDF)
```bash
python3 software_strumenti_calcolo/generate_scientific_figures.py
```

---

## 📚 Multi-Cohort Clinical Validation Summary ($N = 3,205$)

| Cohort | N | Primary Endpoint Verified | Reference |
| :--- | :---: | :--- | :--- |
| **ADAURA ctDNA MRD** | 220 | 67.9% post-stop relapses; ctDNA lead time 4.7 mo | Herbst et al., *Nat Med* 2025 (PMID: [40097663](https://pubmed.ncbi.nlm.nih.gov/40097663/)) |
| **MSKCC Thoracic Histology** | 604 | Solid/Micropapillary recurrence HR raw 6.75 (Firth 2.60–3.42) | MSKCC Thoracic Database 2020 |
| **TCGA-LUAD + GSE31210** | 854 | Spatial gene expression prognostic signature validation | TCGA / Okayama et al. |
| **MSKCC Targeted Genomics** | 863 | *EGFR*/*TP53*/*RB1* triple mutant TTD 9.5 mo, SCLC 18–25% | Offin et al., *J Thorac Oncol* 2019 (PMID: [31228622](https://pubmed.ncbi.nlm.nih.gov/31228622/)) |
| **Human Lung Cancer IFP** | 211 | Mean IFP 8.5 mmHg, Solid 9.8 mmHg (independent RFS predictor) | Mori et al., *Ann Thorac Cardiovasc Surg* 2015 (PMID: [25641031](https://pubmed.ncbi.nlm.nih.gov/25641031/)) |
| **RELAY Phase III Trial** | 449 | Ramucirumab (anti-VEGFR2) + TKI PFS HR = 0.59 ($p < 0.0001$) | Nakagawa et al., *J Thorac Oncol* 2025 (PMID: [39622410](https://pubmed.ncbi.nlm.nih.gov/39622410/)) |

---

## 📖 Citation

If you use this model, software tools, or the CRI score in your research, please cite:

```bibtex
@article{celebrano2026spatialcontinuum,
  title={The Spatial-Genomic Oncology Continuum: A Biophysical Reaction-Diffusion Theory of Pharmacological Sanctuaries, the Post-ADAURA Cessation Dilemma, and the SG-ADAURA Clinical Trial Protocol},
  author={Celebrano, Luca},
  journal={medRxiv / Nature Communications (Submitted)},
  year={2026},
  institution={Department of Clinical Medicine and Surgery, School of Medicine, Universit{\`a} degli Studi di Napoli Federico II},
  note={Independent Medical Student Research Program in Mathematical Oncology}
}
```

## ⚖️ License

This project is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** License — see the [LICENSE](LICENSE) file for details.
