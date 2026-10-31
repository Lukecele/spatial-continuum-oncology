<div align="center">

# 🔬 The Spatial-Genomic Oncology Continuum
### Resolving the Post-ADAURA Cessation Paradox with First-Principles Biophysics

**An open-source reaction-diffusion transport solver, 60 FPS tumor digital twin, and bedside clinical decision engine (`cri-calc`) for targeted lung oncology.**

<p align="center">
  <a href="https://colab.research.google.com/github/Lukecele/spatial-continuum-oncology/blob/main/demo_spatial_continuum.ipynb">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" height="28" alt="Open in Colab">
  </a>
  <a href="https://lukecele.github.io/spatial-continuum-oncology/simulator.html">
    <img src="https://img.shields.io/badge/%F0%9F%9A%80%20Live%20Simulator-60%20FPS%20Digital%20Twin-0284c7.svg?style=for-the-badge" height="28" alt="Live Simulator">
  </a>
  <a href="https://lukecele.github.io/spatial-continuum-oncology/">
    <img src="https://img.shields.io/badge/%F0%9F%8C%90%20Live%20Web%20App-Bedside%20CRI%20Engine-2ea44f.svg?style=for-the-badge" height="28" alt="Live Web App">
  </a>
  <a href="https://anaconda.org/bioconda/spatial-continuum">
    <img src="https://img.shields.io/badge/Bioconda-spatial--continuum%20v1.0.2-brightgreen.svg?style=for-the-badge&logo=anaconda" height="28" alt="Bioconda">
  </a>
  <a href="https://github.com/Lukecele/spatial-continuum-oncology">
    <img src="https://img.shields.io/github/stars/Lukecele/spatial-continuum-oncology?style=for-the-badge&logo=github&color=gold" height="28" alt="GitHub stars">
  </a>
</p>

<p align="center">
  <a href="01_MANOSCRITTO_FINALE_CON_FIGURE.pdf"><img src="https://img.shields.io/badge/%F0%9F%93%84%20Read%20Full%20Manuscript-PDF%20(Nature%20Communications)-dc2626.svg" alt="Manuscript PDF"></a>
  <a href="https://doi.org/10.21203/rs.3.rs-11530312/v1"><img src="https://img.shields.io/badge/Research%20Square-10.21203%2Frs.3.rs--11530312%2Fv1-blue.svg" alt="Research Square"></a>
  <a href="https://doi.org/10.5281/zenodo.23754999"><img src="https://zenodo.org/badge/1437679243.svg" alt="Zenodo"></a>
  <a href="https://www.nature.com/ncomms/"><img src="https://img.shields.io/badge/Target-Nature%20Communications-darkred.svg" alt="Target Nature Communications"></a>
  <a href="https://pypi.org/project/spatial-continuum/"><img src="https://img.shields.io/pypi/v/spatial-continuum.svg?logo=pypi&logoColor=white" alt="PyPI"></a>
  <a href="https://quay.io/repository/biocontainers/spatial-continuum"><img src="https://img.shields.io/badge/BioContainers-Docker%20%26%20Singularity-brightgreen.svg?logo=docker&logoColor=white" alt="BioContainers"></a>
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/dependencies-pure%20standard%20lib-brightgreen.svg" alt="Zero Dependencies">
</p>

*Author:* **Luca Celebrano**, MD Candidate · Department of Clinical Medicine and Surgery, School of Medicine, Università degli Studi di Napoli Federico II · `l.celebrano@studenti.unina.it`

---

### ⚡ 10-Second Interactive Quickstart (Zero Install Required)

| 🚀 **1-Click Google Colab** | 🎮 **60 FPS Live Digital Twin** | 🏥 **Bedside CRI Clinical Decision** |
| :---: | :---: | :---: |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Lukecele/spatial-continuum-oncology/blob/main/demo_spatial_continuum.ipynb) | [**▶ Launch 60 FPS Simulator**](https://lukecele.github.io/spatial-continuum-oncology/simulator.html) | [**▶ Open Bedside Web App**](https://lukecele.github.io/spatial-continuum-oncology/) |
| Run Bessel $K_0$ diffusion & in silico trials in 10s | Watch dormant persisters awaken in real-time | Compute patient risk tier & clinical guidance |

```bash
# Or run locally from your terminal in 3 seconds:
pip install spatial-continuum
cri-calc --pattern solid --tp53 mutated --rb1 loss --stroma dense
```

---

<a href="https://lukecele.github.io/spatial-continuum-oncology/simulator.html">
  <img src="assets/simulator-vessel-live.gif" alt="In Silico Tumor Sanctuary Digital Twin Simulator — 60 FPS Capillary Vessel Dynamics" width="100%" style="max-width: 900px; border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.15);">
</a>

<p align="center">
  <i><b>Live 60 FPS Digital Twin:</b> Capillary microvessel ($r_0=10\,\mu\text{m}$) diffusing osimertinib. Drug concentration drops below cytocidal $\text{IC}_{50}$ ($10\,\text{nM}$) at $r_{\text{crit}}=165.9\,\mu\text{m}$, creating a <b>34.1 $\mu$m cytostatic sanctuary sleeve (31.3% of viable tumor cord volume)</b> where dormant persister cells survive until drug discontinuation at Month 36.</i>
</p>

</div>

---

## ⚡ The Project in 30 Seconds: Why This Matters

<div align="center">

| 🎯 The Clinical Paradox (ADAURA) | 🔬 The Biophysical Discovery | 💡 The Precision Solution (SG-ADAURA) |
| :--- | :--- | :--- |
| **67.9% of relapses occur AFTER planned 36-month stop** (*Herbst et al., Nature Medicine 2025*), and **75–80% harbor NO resistant mutations** (e.g. *EGFR* C797S). Why do drug-sensitive cells recur? | Elevated Interstitial Fluid Pressure shuts down convection ($Pe < 0.1$). Cylindrical Bessel $K_0$ diffusion leaves an **unperfused 34.1 $\mu$m sanctuary sleeve** where cells arrest cytostatically in $G_0/G_1$. | Bedside **Composite Resistance Index (`cri-calc`)**: safe cessation for Lepidic cords (saves €60k/yr & toxicity) vs **anti-VEGFR2 vascular normalization** for Solid cords ($\text{HR} < 0.05, p < 10^{-15}$). |

</div>

> ⭐️ **Support Open-Science Oncology**: If you find this mathematical framework, biophysical model, or web simulator useful, please consider giving the repository a star on GitHub — it directly aids community discovery and open-science adoption!

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

## 💻 Software Suite & Official Packages (PyPI, Bioconda, BioContainers, Galaxy & Snakemake)

The full framework is published on **PyPI** ([`spatial-continuum`](https://pypi.org/project/spatial-continuum/)), on **Bioconda** ([`bioconda/spatial-continuum`](https://anaconda.org/bioconda/spatial-continuum)), and supported across all major scientific workflow environments:

```bash
# 1. Install via PyPI (Official Python Package Index)
pip install spatial-continuum

# 2. Or install via Bioconda
conda install -c bioconda spatial-continuum

# 3. Or run directly with Docker (BioContainers)
docker pull quay.io/biocontainers/spatial-continuum:1.0.2--pyhdfd78af_0
docker run --rm quay.io/biocontainers/spatial-continuum:1.0.2--pyhdfd78af_0 cri-calc --help

# 4. Or run on HPC / Clusters with Singularity / Apptainer (Zero root required)
singularity exec https://depot.galaxyproject.org/singularity/spatial-continuum:1.0.2--pyhdfd78af_0 cri-calc --help

# 5. Or execute in Galaxy (Point-and-click GUI for clinicians)
# Tool ID: cri_calc (galaxyproject/tools-iuc PR #8838)

# 6. Or run inside Snakemake pipelines
# Wrapper: master/bio/spatialcontinuum (snakemake-wrappers PR #6233)

# 7. Or install from source in editable mode
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

## 🏛 Strategic Clinical, Congress & Editorial Dossiers

| Document | Description | Target & Purpose |
| :--- | :--- | :--- |
| [📄 `14_EXECUTIVE_CLINICAL_BRIEF_ADAURA_HERBST_ASTRAZENECA.md`](14_EXECUTIVE_CLINICAL_BRIEF_ADAURA_HERBST_ASTRAZENECA.md) | **Clinical Executive One-Pager & Strategic Trial Brief** | Addressed to Prof. Roy S. Herbst (Yale Cancer Center), AstraZeneca Oncology R&D, and Clinical Oncology Centers (IRCCS Pascale, AIOM). Details the in silico Phase III trial SG-ADAURA and Arm B3 consolidation. |
| [📄 `15_DOSSIER_ANTICIPAZIONE_REVIEWERS_NATURE_COMMS.md`](15_DOSSIER_ANTICIPAZIONE_REVIEWERS_NATURE_COMMS.md) | **Pre-Emptive Reviewer Response Matrix** | Prepared for *Nature Communications* (tracking `NCOMMS-26-091227`). Formulates pre-computed mathematical proofs and empirical answers to 12 referee objections across biophysics, clinical oncology, and spatial pathology. |
| [📄 `12_ABSTRACT_SOTTOMISSIONE_AACR_2027.md`](12_ABSTRACT_SOTTOMISSIONE_AACR_2027.md) | **Official AACR 2027 Abstract** | Calibrated to 2,423 characters (strictly under the 2,600 character ceiling) for the AACR Annual Meeting in Orlando, FL. |
| [📄 `13_DOSSIER_CONGRESSI_MONDIALI_AACR_ASCO_ESMO.md`](13_DOSSIER_CONGRESSI_MONDIALI_AACR_ASCO_ESMO.md) | **Tri-Congress Strategy Dossier (AACR, ASCO, ESMO)** | Tailored abstracts and submission calendar across biological, clinical, and translational tracks for the 3 major worldwide oncology congresses. |
| [📊 `16_MASTER_SLIDE_DECK_CONGRESSI_E_PRIMARI.md`](16_MASTER_SLIDE_DECK_CONGRESSI_E_PRIMARI.md) | **Master Slide Deck (12 Slides)** | Oral presentation deck for oncology congresses and department grand rounds. Includes companion interactive deck: [`slide_deck_interattivo.html`](slide_deck_interattivo.html). |
| [🖼 `17_POSTER_CONGRESSUALE_AACR_ASCO_120x90.md`](17_POSTER_CONGRESSUALE_AACR_ASCO_120x90.md) | **Official Congress Poster (120 × 90 cm)** | Print-ready scientific poster layout with 300 DPI figures and offline QR codes: [`poster_congressuale_120x90.html`](poster_congressuale_120x90.html). |
| [🌐 `Hugging Face Clinical Decision App`](https://huggingface.co/spaces/spatial-continuum-lab/spatial-continuum-clinical-app) | **Live Clinical Decision Web Application** | Interactive clinical tool on Hugging Face Spaces for real-time Bedside CRI calculation, patient cohort CSV batch analysis, and dynamic Kaplan-Meier survival curve plotting. |

---

## 📖 Citation & Scholarly Records

* **Research Square Preprint (Springer Nature):** [https://doi.org/10.21203/rs.3.rs-11530312/v1](https://doi.org/10.21203/rs.3.rs-11530312/v1)
* **Gist.Science Plain-Language Explanation (Author-Reviewed):** [https://gist.science/paper/rs/rs-11530312](https://gist.science/paper/rs/rs-11530312)
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
