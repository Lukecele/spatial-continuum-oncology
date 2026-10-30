# Progetto di Ricerca: The Spatial-Genomic Oncology Continuum
## Guida Ragionata ai Documenti e ai Software
**Autore:** Luca Celebrano  
**Affiliazione:** Dipartimento di Medicina Clinica e Chirurgia, Scuola di Medicina e Chirurgia, Università degli Studi di Napoli Federico II  
**Contatto:** `l.celebrano@studenti.unina.it`  

---

### Mappa dei Documenti nella Cartella

| Nome File | Descrizione e Scopo | A Chi Inviarlo / Come Usarlo |
| :--- | :--- | :--- |
| **`01_MANOSCRITTO_NATURE_COMMUNICATIONS_CELEBRANO.pdf`** | **Il Manoscritto Tipografico Ufficiale in PDF (16 pagine)** pronto per la sottomissione a Nature Communications e medRxiv. | **Da depositare su medRxiv e inviare all'Editor di Nature Communications**. |
| **`01_MANOSCRITTO_PAPER_COMPLETO_UNIFICATO.md`** | **Il Paper Scientifico Completo in Markdown** (formule, biologia, trial e discussione). | Sorgente del paper accademico unificato. |
| **`figure_scientifiche/`** | **Le Figure Ufficiali del Paper** in formato PNG (300 DPI) e PDF vettoriale: Figure 1-4 per il main text e **Supplementary Figure 1** (validazione spaziale 10x Visium HD / GSE301973). | Da allegare alla sottomissione (Figure 1, 2, 3, 4 + Supplementary Figure 1). |
| **`COVER_LETTER_NATURE_COMMUNICATIONS.md`** | **La Lettera Ufficiale all'Editor** di Nature Communications con razionale e revisori suggeriti (Jain, Gatenby, Herbst, Tannock). | Da incollare nel portale di sottomissione Nature. |
| **`METADATI_SOTTOMISSIONE_MEDRXIV.md`** | **Il Dossier Completo di Metadati, Dichiarazioni Etiche e Abstract Strutturato** per medRxiv. | Guida copia-incolla per il deposito preprint immediato. |
| **`02_TRATTATO_MONOGRAFICO_MASTER_8_CAPITOLI.md`** | Trattato accademico esteso in 8 capitoli con trattazione analitica approfondita. | Base per tesi o monografia scientifica completa. |
| **`03_PROTOCOLLO_TRIAL_FASE_3_SG_ADAURA_E_CRI.md`** | Il protocollo formale del trial clinico randomizzato di Fase III **SG-ADAURA** ($N=800$) e l'algoritmo CRI. | Da presentare a oncologi clinici e comitati etici. |
| **`04_TEST_AVVERSI_LIMITI_E_FALSIFICAZIONE_POPPER.md`** | Dossier di red-teaming: dove il modello NON è universale (Péclet, barriera emato-encefalica, low-shedders) e cancelli di Popper. | Fondamentale per rispondere a revisori severi. |
| **`05_FORMALIZZAZIONE_BIOFISICA_DARCY_BESSEL.md`** | Dimostrazione matematica da primo principio (Starling-Darcy, Stokes-Einstein, Bessel $K_0$). | Per biofisici e biologi matematici. |
| **`06_DOSSIER_PARAMETRI_CLINICI_UMANI_E_PMID.md`** | Raccolta e audit di tutti i parametri farmacocinetici e pressori con PMID PubMed. | Prova di assenza di parametri arbitrari o toy model. |
| **`07_REPORT_BENCHMARK_SOBOL_E_CROSS_FARMACO.md`** | Analisi di sensibilità globale Sobol (56.000 iterazioni) e confronto cross-farmaco (TKI vs ADC). | Documentazione del comportamento computazionale. |
| **`08_ARCHITETTURA_SISTEMA_7_PILASTRI.md`** | Schema concettuale dei 7 pilastri unificati del framework. | Sintesi visiva e concettuale d'insieme. |
| **`09_PIANO_PROGRAMMATICO_RICERCA_FEDERICO_II.md`** | Piano programmatico in 5 fasi dello studio indipendente. | Roadmap accademica. |
| **`10_REPORT_COLLAUDO_LIVE_PORTALE_E_AUDIT_E2E.md`** | Report di collaudo live E2E del portale GitHub Pages (5 moduli verificati, zero NaN, audit headless CDP). | Verifica di conformità software, rendering live e sanità numerica. |
| **`11_STUDIO_SUPERIORITA_CLINICA_E_BENCHMARK_SOC_ADAURA.md`** | Studio quantitativo di superiorità clinica head-to-head vs Standard of Care (ADAURA 36m stop): 5-Yr DFS 100% vs 42.4% ($p = 1.43 \times 10^{-30}$). | Dimostrazione di superiorità terapeutica, evolutiva ed economica per oncologi e revisori. |

---

### Software e Strumenti di Calcolo (`software_strumenti_calcolo/`)

Tutti gli script sono scritti in **puro Python 3 standard** (zero librerie esterne da installare, zero dipendenze):

1. **`cri_calc.py`**: Calcolatore bedside del Composite Resistance Index.
   ```bash
   python3 cri_calc.py --histology solid --size 3.8 --tp53 --ctdna negative
   ```
2. **`audit_matematica_e_statistica.py`**: Motore di audit analitico (verifica Bessel $K_0$, unità dimensionali e correzione di Firth).
   ```bash
   python3 audit_matematica_e_statistica.py
   ```
3. **`test_stress_avversi.py`**: Motore di simulazione delle condizioni di confine estreme e singolarità fisiche.
   ```bash
   python3 test_stress_avversi.py
   ```
4. **`generate_supplementary_spatial_benchmark.py`**: Generatore della **Supplementary Figure S1** per Nature Communications (benchmark su 10x Visium HD reale e stratificazione clinica GSE301973 con `cri-calc`).
   ```bash
   python3 generate_supplementary_spatial_benchmark.py
   ```
5. **`run_fast_superiority_benchmark.py`**: Benchmark Monte Carlo vettorizzato ($N=500$ pazienti virtuali, 5 bracci di trattamento su 1.825 giorni) che confronta la DFS a 5 anni e la tossicità di SG-ADAURA e InSituGame contro lo Standard ADAURA.
   ```bash
   python3 run_fast_superiority_benchmark.py
   ```
6. **`test_live_github_pages.js`**: Suite di collaudo live automatizzata via Chrome DevTools Protocol (CDP) che audita tutti i 5 moduli del portale GitHub Pages.
   ```bash
   node test_live_github_pages.js
   ```
7. **`test_digital_twin_engine.js`**: Suite di collaudo automatizzato via CDP del simulatore interattivo 60 FPS (`simulator.html`).
   ```bash
   node test_digital_twin_engine.js
   ```
8. **`test_portal_e2e.js`**: Suite di collaudo end-to-end locale via CDP dei 5 moduli di `index.html`.
   ```bash
   node test_portal_e2e.js
   ```

---

### Libreria Python Installabile (`src/`)

Il repository include il pacchetto Python standard installabile via `pip`:
```bash
pip install -e .
```
Comandi CLI forniti:
- `cri-calc`: Calcolatore a riga di comando del Composite Resistance Index.
- `spatial-continuum-audit`: Motore di audit analitico e verifica dimensionale.
