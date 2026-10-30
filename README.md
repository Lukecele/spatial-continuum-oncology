# The Spatial-Genomic Oncology Continuum

[![Read Full Manuscript PDF](https://img.shields.io/badge/%F0%9F%93%84%20Read%20Full%20Manuscript-PDF%20(Nature%20Communications)-dc2626.svg?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](01_MANOSCRITTO_FINALE_CON_FIGURE.pdf)
[![Live 60 FPS Digital Twin](https://img.shields.io/badge/%F0%9F%9A%80%20Live%20Digital%20Twin-60%20FPS%20Sanctuary%20Simulator-0284c7.svg?style=for-the-badge)](https://lukecele.github.io/spatial-continuum-oncology/simulator.html)
[![Live Web App: Bedside CRI](https://img.shields.io/badge/%F0%9F%8C%90%20Live%20Web%20App-Bedside%20CRI%20Engine-2ea44f.svg?style=for-the-badge)](https://lukecele.github.io/spatial-continuum-oncology/)
[![GitHub stars](https://img.shields.io/github/stars/Lukecele/spatial-continuum-oncology?style=for-the-badge&logo=github&color=gold)](https://github.com/Lukecele/spatial-continuum-oncology)
[![DOI](https://zenodo.org/badge/1437679243.svg)](https://doi.org/10.5281/zenodo.23754999)
[![Research Square DOI](https://img.shields.io/badge/Research%20Square-10.21203%2Frs.3.rs--11530312%2Fv1-blue.svg)](https://doi.org/10.21203/rs.3.rs-11530312/v1)
[![Software License: MIT](https://img.shields.io/badge/Software_License-MIT-blue.svg)](LICENSE-MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/Monograph_License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Target: Nature Communications](https://img.shields.io/badge/Target-Nature%20Communications-darkred.svg)](https://www.nature.com/ncomms/)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Simulator%20%26%20Bedside%20CRI-blue)](https://huggingface.co/spaces/Lucace/spatial-oncology-simulator)
[![Hugging Face Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset%20(N%3D604)-ffd21e)](https://huggingface.co/datasets/Lucace/mskcc-lung-adenocarcinoma-spatial-cohort)
[![Biophysical Base](https://img.shields.io/badge/Biophysical%20Base-spatial--oncology--master-007acc.svg)](https://github.com/Lukecele/spatial-oncology-master)
[![Bioconda](https://img.shields.io/badge/Bioconda-spatial--continuum%20v1.0.2-brightgreen.svg?style=for-the-badge&logo=anaconda)](https://anaconda.org/bioconda/spatial-continuum)
[![PyPI](https://img.shields.io/pypi/v/spatial-continuum.svg?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/spatial-continuum/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-pure%20standard%20lib-brightgreen.svg)]()

**A Biophysical Reaction-Diffusion Theory of Pharmacological Sanctuaries, the Post-ADAURA Cessation Dilemma, and the Bedside Composite Resistance Index (CRI)**

*Author:* **Luca Celebrano**, MD Candidate  
*Affiliation:* Department of Clinical Medicine and Surgery, School of Medicine, Università degli Studi di Napoli Federico II, Naples, Italy  
*Correspondence:* `l.celebrano@studenti.unina.it`  

---

> 🚀 **Interactive Clinical Web App Available**: Test the real-time Bedside CRI Decision Engine and Bessel $K_0$ reaction-diffusion sanctuary simulator directly in your browser:  
> 👉 **[https://lukecele.github.io/spatial-continuum-oncology/](https://lukecele.github.io/spatial-continuum-oncology/)**  
> 🎮 **60 FPS Live Digital Twin & 5-Year Trial Simulator**:  
> 👉 **[https://lukecele.github.io/spatial-continuum-oncology/simulator.html](https://lukecele.github.io/spatial-continuum-oncology/simulator.html)**

<p align="center">
  <a href="https://lukecele.github.io/spatial-continuum-oncology/simulator.html">
    <img src="assets/simulator-vessel-live.gif" alt="In Silico Tumor Sanctuary Digital Twin Simulator — 60 FPS Capillary Vessel Dynamics" width="100%" style="max-width: 960px; border-radius: 8px;">
  </a>
</p>

> ⭐️ **Support Open-Science Oncology**: If you find this framework, biophysical model, or web simulator useful, please consider giving the repository a star on GitHub — it directly aids community discovery and open-science adoption!

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

## 🏆 Head-to-Head Clinical Superiority Benchmark: SG-ADAURA vs. Standard of Care

To address whether our spatial-continuum framework provides superior clinical outcomes compared to current standard-of-care guidelines (36-month fixed adjuvant osimertinib discontinuation), we conducted a rigorous in silico trial ($N = 500$ virtual patients, 5 treatment arms, followed across 1,825 days / 5 years post-resection).

Full study: [📄 `11_STUDIO_SUPERIORITA_CLINICA_E_BENCHMARK_SOC_ADAURA.md`](11_STUDIO_SUPERIORITA_CLINICA_E_BENCHMARK_SOC_ADAURA.md)  
Live Portal Audit: [🌐 `10_REPORT_COLLAUDO_LIVE_PORTALE_E_AUDIT_E2E.md`](10_REPORT_COLLAUDO_LIVE_PORTALE_E_AUDIT_E2E.md)

### Key Head-to-Head Findings

| Treatment Arm | Therapeutic Strategy | 5-Year DFS (Overall) | Tier 1 (Lepidic) | Tier 3 (Solid) | Hazard Ratio (vs SOC) [95% CI] | p-value (Log-Rank) | Cumulative Drug Toxicity |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Arm 0: Historical / No Adjuvant** | Surgery alone ($R_0$) | **$0.0\%$** | $0.0\%$ | $0.0\%$ | $20.75$ [$17.95\text{--}23.99$] | $p < 10^{-15}$ | $0.0\%$ |
| **Arm 1: Standard ADAURA (SOC)** | 36 mo Osimertinib $\to$ Stop | **$42.4\%$** | **$100.0\%$** | **$0.0\%$** | **$1.00$ [Reference]** | Reference | $60.1\%$ |
| **Arm 2: Continuous Indefinite** | 60 mo un-interrupted Osimertinib | **$100.0\%$** | $100.0\%$ | $100.0\%$ | $< 0.05$ [$0.00\text{--}0.00$] | $p = 1.43 \times 10^{-30}$ | $100.4\%$ (+67% vs SOC) |
| **Arm 3: InSituGame Adaptive** | Dynamic MRD / Nash pulsing | **$100.0\%$** | $100.0\%$ | $100.0\%$ | $< 0.05$ [$0.00\text{--}0.00$] | $p = 1.43 \times 10^{-30}$ | **$70.9\%$** (-29.5% vs Arm 2) |
| **Arm 4: SG-ADAURA Stratified** | **Tier 1: Stop M36; Tier 3: Remodeling+Maint.** | **$100.0\%$** | **$100.0\%$** | **$100.0\%$** | **$< 0.05$ [$0.00\text{--}0.00$]** | **$p = 1.43 \times 10^{-30}$** | **$83.3\%$** (Optimal Balance) |

1. **Why Current Standard ADAURA Fails in High-Risk Patients:** In solid/micropapillary cords (Tier 3), cytostatic persisters reside in the unperfused pharmacological sanctuary shell ($\Delta r = 34.1\ \mu\text{m}$). Discontinuing drug at month 36 lifts the cytostatic block, causing 100% of Tier 3 patients to relapse within 5.4 months (5-year DFS drops to 0.0%).
2. **Personalized De-escalation (Tier 1):** Patients with thin, well-perfused lepidic cords have zero sanctuary ($\Delta r = 0$) and achieve 100% 5-year DFS with planned cessation at month 36. Sparing 2 years of continuous treatment saves ~$120,000 per patient and completely avoids unnecessary chronic toxicity (diarrhea, cardiotoxicity, paronychia).
3. **Biophysical Intensification (Tier 3):** Under SG-ADAURA Arm B3, transient vascular normalization (anti-VEGFR2 Ramucirumab) collapses interstitial fluid pressure, eradicating the sanctuary shell ($\Delta r \to 0$) and transforming a 0% survival into 100% 5-year DFS ($\text{HR} < 0.05$, $p = 1.43 \times 10^{-30}$).
4. **Adaptive Game-Theoretic Pulsing (InSituGame):** Exploits the stable Nash attractor ($x^* = 61.3\%$) to maintain identical 100% 5-year disease control while reducing cumulative drug exposure by **$29.5\%$**, protecting against the competitive release of resistant *EGFR* C797S mutants.

---

## 💻 Software Suite & Official Packages (PyPI & Bioconda)

The full framework is published on **PyPI** ([`spatial-continuum`](https://pypi.org/project/spatial-continuum/)), on **Bioconda** ([`bioconda/spatial-continuum`](https://anaconda.org/bioconda/spatial-continuum)), and operates with **zero third-party dependencies**:

```bash
# Install via PyPI (Official Python Package Index)
pip install spatial-continuum

# Or install via Bioconda
conda install -c bioconda spatial-continuum

# Or install from source in editable mode
git clone https://github.com/Lukecele/spatial-continuum-oncology.git
cd spatial-continuum-oncology
pip install -e .
```
Both provide the bedside CLI commands `cri-calc` and `spatial-continuum-audit`.

All calculation tools can also be run directly from `software_strumenti_calcolo/`:

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

### 5. Supplementary Spatial Benchmark Generator (Visium HD / GSE301973)
Generates Supplementary Figure S1 validating reaction-diffusion sanctuary predictions and `cri-calc` risk stratification against real spatial transcriptomics tissue data:
```bash
python3 software_strumenti_calcolo/generate_supplementary_spatial_benchmark.py
```

### 6. Clinical Superiority Monte Carlo Benchmark Suite
Executes the $N=500$ 5-arm comparative survival simulation over 1,825 days, computing Kaplan-Meier 5-year DFS curves, log-rank $p$-values, hazard ratios, and cumulative drug toxicity:
```bash
python3 software_strumenti_calcolo/run_fast_superiority_benchmark.py
```

### 7. End-to-End Live Web Portal Test Suite (Chrome DevTools Protocol)
Audits all 5 live portal modules with zero dependencies using headless Chrome:
```bash
node software_strumenti_calcolo/test_live_github_pages.js
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

## 📖 Citation & Scholarly Records

* **Research Square Preprint (Springer Nature):** [https://doi.org/10.21203/rs.3.rs-11530312/v1](https://doi.org/10.21203/rs.3.rs-11530312/v1)
* **Permanent Zenodo Software Archive:** [https://doi.org/10.5281/zenodo.23754999](https://doi.org/10.5281/zenodo.23754999)

If you use this biophysical model, the computational suite, or the CRI clinical decision engine, please cite:

```bibtex
@article{celebrano2026spatialcontinuum,
  title={Conditions for Pharmacological Sanctuaries in Perivascular Tumour Cords: A Reaction–Diffusion Analysis, a Regrowth-Kinetics Identity, and a Descriptive Survival Analysis of Histologic Subtype in Resected Lung Adenocarcinoma},
  author={Celebrano, Luca},
  journal={Research Square (Springer Nature)},
  year={2026},
  doi={10.21203/rs.3.rs-11530312/v1},
  url={https://doi.org/10.21203/rs.3.rs-11530312/v1},
  institution={Department of Clinical Medicine and Surgery, School of Medicine, Universit{\`a} degli Studi di Napoli Federico II},
  note={Independent Medical Student Research Program in Mathematical Oncology}
}
```

## ⚖️ License

This project is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** License — see the [LICENSE](LICENSE) file for details.
