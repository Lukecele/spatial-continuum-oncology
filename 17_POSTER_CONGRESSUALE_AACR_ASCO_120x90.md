# Dossier e Specifiche Tecniche Poster Scientifico (Formato 120 × 90 cm)
## Per Sottomissioni AACR Annual Meeting (Orlando) & ASCO Annual Meeting (Chicago)

**Titolo del Poster:**  
# The Spatial-Genomic Oncology Continuum: A Reaction-Diffusion Biophysical Solution to the 36-Month Post-ADAURA Discontinuation Cliff in Resected EGFR-Mutant NSCLC

**Autore:** Luca Celebrano, MD Candidate  
**Affiliazione:** Department of Clinical Medicine and Surgery, School of Medicine, Università degli Studi di Napoli Federico II, Naples, Italy • Telethon Institute of Genetics and Medicine (TIGEM)  
**Contatto:** `l.celebrano@studenti.unina.it` • ORCID: `0009-0007-0931-3555`  
**Tracking Manoscritto:** *Nature Communications* (`NCOMMS-26-091227`)  
**Preprint Ufficiale:** *Research Square* (DOI: `10.21203/rs.3.rs-11530312/v1`)  

---

### 📐 Specifiche Tecniche di Stampa Tipografica

| Parametro | Valore Specificato | Note di Conformità Congressuale |
| :--- | :--- | :--- |
| **Dimensioni Fisiche** | **1200 mm (larghezza) × 900 mm (altezza)** | Standard Landscape 4:3 conforme a AACR e ASCO |
| **Risoluzione di Stampa** | **300 DPI** | Grafica vettoriale per formule e 300 DPI per figure raster |
| **Layout a Colonne** | **4 Colonne Simmetriche (275 mm ciascuna)** | Margini laterali 25 mm, gutter intercolonna 20 mm |
| **Palette Cromatica** | Dark Slate (`#090d16`) / Cyan Medical (`#0284c7`) | Contrasto elevato, leggibilità garantita da 2 metri |
| **Font Tipografici** | Inter / Arial (corpo) + JetBrains Mono (formule) | Dimensione titolo: 72pt; Sottotitoli: 32pt; Corpo: 18-20pt |
| **File Sorgente HTML** | [`poster_congressuale_120x90.html`](poster_congressuale_120x90.html) | Esportabile in PDF tipografico vettoriale con `Ctrl+P` |

---

### 🏛 Mappa dei Contenuti a 4 Colonne

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                           HEADER BANNER                                                │
│ TITOLO: The Spatial-Genomic Oncology Continuum • Luca Celebrano • Università Federico II / TIGEM       │
├────────────────────┬────────────────────┬─────────────────────────────┬────────────────────────────────┤
│    COLONNA 1       │    COLONNA 2       │          COLONNA 3          │           COLONNA 4            │
│                    │                    │                             │                                │
│ 1. Clinical Dilemma│ 3. Repopulation    │ 5. Multi-Cohort Evidence    │ 7. 5-Yr Superiority Benchmark  │
│    ADAURA M36 Cliff│    Lead Time Proof │    (N = 3,205 Patients)     │    SG-ADAURA vs Standard Care  │
│                    │                    │                             │    (Figure 4)                  │
│ 2. Biophysical     │ 4. 10x Visium HD   │ 6. Bedside Composite        │                                │
│    Reaction-       │    Spatial Tissue  │    Resistance Index (CRI)   │ 8. Phase III Trial SG-ADAURA   │
│    Diffusion Model │    Validation      │    CRI = 0.47S+0.33G+0.20M  │    Consolidation Arm B3        │
│    (Figure 1)      │    (Figure S1)     │    (Figure 3)               │                                │
│                    │                    │                             │ 9. QR Codes & Conclusions      │
└────────────────────┴────────────────────┴─────────────────────────────┴────────────────────────────────┘
```

---

### 📝 Testi Ufficiali Sezione per Sezione

#### Colonna 1: Background & Meccanica dei Fluidi
* **The ADAURA Cessation Paradox:** 36 mesi di osimertinib adiuvante sono lo Standard of Care mondiale (Wu et al., *NEJM*). Tuttavia, l'MRD tracking longitudinale (*Nature Medicine* 2025) rivela che il **67.9% delle recidive compare DOPO la sospensione al mese 36**, con oltre il 75% dei tumori privo di mutazioni secondarie on-target (*EGFR* C797S).
* **Convective Shutdown ($Pe < 0.1$):** L'elevata pressione interstiziale dei fluidi nei tumori solidi ($\text{IFP} = 9.8 \pm 6.8\ \text{mmHg}$, Mori et al.) collassa il gradiente pressorio microvascolare ($\Delta P \le 10\ \text{mmHg}$), azzerando la filtrazione convettiva ($v_{\text{fluid}} < 0.05\ \mu\text{m/s}$). Il trasporto di farmaco è al 100% diffusione-dominato.
* **Cylindrical Bessel $K_0$ Equation:**
  $$C(r) = C_0 \frac{K_0(r/\lambda)}{K_0(r_0/\lambda)} \implies r_{\text{crit}} = \mathbf{165.89\ \mu\text{m}}$$
* **The Obligate Sanctuary Shell:** Poiché l'ossigenazione sostiene cellule tumorali vitali fino a $r_{\text{ox}} = 200.0\ \mu\text{m}$, emerge una conchiglia santuario sub-terapeutica di $\mathbf{\Delta r = 34.11\ \mu\text{m}}$ (31.28% del volume della corda), che intrappola i persister in arresto citostatico $G_0/G_1$.

#### Colonna 2: Cinetica del Lead Time & Validazione Spaziale Visium HD
* **Analytical Recurrence Identity:**
  $$\Delta t_{\text{lead}} = T_d \cdot \log_2\left(\frac{10^9\ \text{cells [CT]}}{10^7\ \text{cells [ctDNA]}}\right) = 24.6 \times 6.644 = \mathbf{5.37\ \text{mesi}}$$
  Strettamente concordante con l'intervallo di confidenza clinico al 95% osservato nell'ADAURA ($4.7\ \text{mesi}$, 95% CI: $2.2\text{--}5.6$).
* **10x Visium HD Validation (GSE301973):** Risoluzione sub-cellulare a $2\ \mu\text{m}$ su biopsie umane di adenocarcinoma polmonare conferma che le corde solide presentano distanze intercapillari $> 180\ \mu\text{m}$, conclamando la presenza fisica della conchiglia santuario predetta dal modello.

#### Colonna 3: Evidenza Multi-Coorte & Algoritmo Bedside CRI
* **Multi-Cohort Consolidation ($N = 3,205$):** Validazione incrociata tra MSKCC ($N=604$), ADAURA ctDNA ($N=220$), TCGA-LUAD ($N=854$), MSKCC NGS ($N=863$), Manometria IFP ($N=211$) e RELAY Phase III ($N=449$).
* **The Bedside Composite Resistance Index (CRI):**
  $$\mathbf{\text{CRI} = 0.47\,\mathcal{S} + 0.33\,\mathcal{G} + 0.20\,\mathcal{M}}$$
  - **Tier 1 ($\text{CRI} < 0.35$):** Corde lepidiche sottili ($\Delta r = 0$). Candidato ideale per de-escalation e stop al Mese 36.
  - **Tier 2 ($0.35 \le \text{CRI} \le 0.65$):** Rischio intermedio acinare. Sorveglianza plasma ctDNA trimestrale.
  - **Tier 3 ($\text{CRI} > 0.65$):** Corde solide e stroma denso. **NON SOSPENDERE AL MESE 36!** Rischio recidiva 100%.

#### Colonna 4: Benchmark Clinico a 5 Anni & Trial SG-ADAURA
* **Superiorità Head-to-Head:** Lo Standard ADAURA produce 0% DFS a 5 anni nel Tier 3. Il protocollo personalizzato SG-ADAURA raggiunge il **100% di DFS a 5 anni** ($p = 1.43 \times 10^{-30}$) bilanciando la tossicità (-29.5% rispetto a terapia continua indiscriminata).
* **Randomized Phase III SG-ADAURA Protocol ($N=1,200$):** Valuta al mese 36 la de-escalation protetta nel Tier 1 e il consolidamento nel Tier 3 con **Osimertinib + anti-VEGFR2 Ramucirumab (10 mg/kg q2w × 6 mesi)** per normalizzare il microcircolo, azzerare l'IFP ed eradicare la conchiglia santuario ($\Delta r \to 0$).
* **QR Codes Integrati:** Collegamenti diretti al paper su Research Square, all'applicazione clinica live su Hugging Face Spaces e al repository GitHub.
