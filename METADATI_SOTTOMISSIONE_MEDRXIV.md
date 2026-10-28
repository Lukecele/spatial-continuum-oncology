# medRxiv Submission Metadata & Checklist Dossier

**Target Server:** medRxiv (Cold Spring Harbor Laboratory, BMJ, Yale)  
**Subject Area:** Oncology / Translational Medicine  
**Manuscript Type:** Research Article  

---

## 1. Title & Abstract Metadata

### Full Title:
> The Spatial-Genomic Oncology Continuum: A Biophysical Reaction-Diffusion Theory of Pharmacological Sanctuaries, the Post-ADAURA Cessation Dilemma, and the SG-ADAURA Clinical Trial Protocol

### Running Title / Short Title (max 50 chars):
> Spatial Biophysics of Post-ADAURA Relapse

### Corresponding & Solo Author:
* **Full Name:** Luca Celebrano
* **Academic Degree / Status:** MD Candidate
* **Institutional Affiliation:** Department of Clinical Medicine and Surgery, School of Medicine and Surgery, Università degli Studi di Napoli Federico II
* **Address:** Via Sergio Pansini 5, 80131 Naples, Italy
* **Official Institutional Email:** `l.celebrano@studenti.unina.it`

---

## 2. Structured Abstract (medRxiv Format)

* **Background:** In early-stage EGFR-mutated non-small cell lung cancer (NSCLC), 36 months of adjuvant osimertinib significantly prolongs disease-free survival (ADAURA trial). However, longitudinal molecular residual disease (MRD) tracking reveals that 67.9% of all recurrence events occur after the planned 36-month discontinuation, with 57.9% clustering within the first 12 months post-cessation. 75–80% of relapsing patients exhibit no secondary on-target enzymatic resistance mutations (such as EGFR C797S).
* **Methods:** We formulated a multi-scale biophysical reaction-diffusion framework coupling Starling-Darcy fluid mechanics, Stokes-Einstein tissue transport, and modified cylindrical Bessel functions of the second kind ($K_0$) to calculate spatial drug penetration across tumor cords. The model was calibrated with human clinical pharmacokinetics ($f_u = 0.053$, $C_{0,\text{free}} = 28.62\ \text{nM}$, cellular $\text{IC}_{50} = 10.0\ \text{nM}$) and human lung cancer interstitial fluid pressure (IFP) manometry ($N = 211$ analyzed, Mori et al. 2015). We validated the framework across 6 independent cohorts totaling 3,205 human patients (ADAURA ctDNA $N=220$, MSKCC histology $N=604$, transcriptomic $N=854$, MSKCC targeted genomics $N=863$, Mori IFP $N=211$, and RELAY trial $N=449$).
* **Results:** High tumor IFP ($9.8 \pm 6.8\ \text{mmHg}$) annihilates the transvascular hydrostatic pressure gradient ($\Delta P \le 10\ \text{mmHg}$, $v_{\text{fluid}} < 0.05\ \mu\text{m/s}$), causing convective shutdown ($Pe < 0.1$) and establishing pure diffusion dominance. Osimertinib decays below therapeutic efficacy at a nominal radius $r_{\text{crit}} \approx 166\ \mu\text{m}$. Because the histological oxygen viability boundary extends to $r_{\text{ox}} = 200.0\ \mu\text{m}$ (Thomlinson & Gray 1955), a mandatory sub-therapeutic sleeve of width $\Delta r = 34.11\ \mu\text{m}$ (engulfing 31.28% of cord volume) emerges, maintaining persister cells in cytostatic $G_0/G_1$ dormancy during treatment. Tumor repopulation kinetics ($T_d = 24.6$ days) predict an MRD-to-imaging lead time of $5.37\ \text{months}$, matching the clinical $95\%\,\text{CI}$ ($2.2\text{--}5.6\ \text{months}$) observed in ADAURA. We translate these findings into the Composite Resistance Index (CRI = $0.47\mathcal{S} + 0.33\mathcal{G} + 0.20\mathcal{M}$) and design the prospective Phase III SG-ADAURA trial ($N = 800$).
* **Conclusions:** Post-adjuvant osimertinib relapse is primarily driven by physical tissue-level sanctuaries rather than immediate catalytic site mutations. The CRI engine transitions oncology from empirical trial-and-error to biophysically grounded precision decision-making.

---

## 3. Mandatory Regulatory & Ethical Declarations

* **Funding Statement:**  
  "This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. It was conducted independently by the author as part of an independent medical student research program at the Department of Clinical Medicine and Surgery, Università degli Studi di Napoli Federico II, Naples, Italy."
* **Competing Interest Statement:**  
  "The author declares no competing financial or non-financial interests."
* **Ethics Approval Statement:**  
  "This study involves theoretical biophysical modeling and secondary analysis of fully anonymized, publicly available data from previously published clinical trials and genomic databases (TCGA, GSE31210, ADAURA post-hoc analysis, and MSKCC NGS). No new human subjects were prospectively recruited or subjected to experimental interventions for this theoretical study; thus, formal institutional review board (IRB) ethical approval was exempt. The prospective clinical trial protocol SG-ADAURA included in the manuscript is a proposed theoretical protocol designed in strict compliance with the Declaration of Helsinki and SPIRIT 2013 guidelines."
* **Data and Code Availability Statement:**  
  "All computational calculation tools (`cri_calc.py`, `audit_matematica_e_statistica.py`, `test_stress_avversi.py`, and `generate_scientific_figures.py`) were developed using the pure standard library of Python (version 3.9+) with zero external dependencies to ensure permanent reproducibility. All code, analytical formulas, and clinical calibration dossiers are fully available on GitHub under an open-source license."
* **Clinical Trial Registration:**  
  "The proposed SG-ADAURA trial protocol is pre-registered conceptually in the manuscript and will be formally registered on ClinicalTrials.gov upon institutional committee activation."
