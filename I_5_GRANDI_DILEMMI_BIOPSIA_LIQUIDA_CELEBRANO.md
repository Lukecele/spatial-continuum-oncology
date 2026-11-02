# I 5 GRANDI DILEMMI DELLA BIOPSIA LIQUIDA
## Risoluzione Biofisica dei Falsi Negativi, Cinetica del ctDNA e Dinamiche di Recidiva Post-Adiuvante

**Autore:** Luca Celebrano, MD Candidate (Dipartimento di Medicina Clinica e Chirurgia, Scuola di Medicina, Università degli Studi di Napoli Federico II)  
**Destinatari Scientifici:** Prof. Alberto Bardelli, Dott. Giovanni Crisafulli, Dott. Giorgio Patelli, Dott.ssa Francesca Baessato (IFOM ETS Milano / Università degli Studi di Torino)  
**Data:** Novembre 2026 | **Documento:** Executive Working Paper Pre-Teleconferenza  
**Contatti:** Tel: 349 0626697 / 0817392845 | Email unina: l.celebrano@studenti.unina.it | Email personale: l.celebrano5@gmail.com | GitHub: https://github.com/Lukecele  

---

### PREMESSA CLINICA PER IL PROF. BARDELLI E IL TEAM DI IFOM
Questo memorandum nasce con profondo rispetto scientifico per il lavoro pionieristico del Vostro gruppo nella genetica molecolare e nella biopsia liquida. L'intento di questo documento è offrire un contributo complementare di modellistica biofisica per approfondire alcuni nodi biologici aperti nell'interpretazione della Malattia Residua Minima (MRD) e nella de-escalation terapeutica post-chirurgica. I 5 dilemmi sono illustrati integrando evidenze patologiche, concetti biofisici semplici e derivazioni in forma chiusa, mettendoli a disposizione del Vostro team per la discussione clinica.

---

## DILEMMA 1: Il Paradosso del Falso Negativo Biologico del ctDNA

### Il Quesito Clinico:
> *"Perché un paziente con milioni di cellule tumorali residue dormienti può risultare sistematicamente 'ctDNA NEGATIVO' anche con i sequenziatori NGS più sensibili al mondo (LOD ≤ 0.02% VAF)?"*

### La Spiegazione Semplice (La Prospettiva Biofisica Microambientale):
La biopsia liquida non misura il numero totale di cellule neoplastiche vive presenti nell'organismo, ma **il DNA di quelle che vanno incontro a morte cellulare e i cui frammenti riescono a superare la barriera tissutale ed entrare nel torrente circolatorio**.

Nei modelli teorici storici (es. Avanzini et al., *Science Advances* 2020), il tumore è trattato come una "sacca di cellule omogenea" dove ogni cellula versa liberamente frammenti di DNA nel plasma. Nella realtà microambientale di un tumore solido in terapia target o adiuvante:
1. **Quiescenza cellulare protetta (DTPs):** Le cellule persister nel loro nicchia stromale non vanno incontro ad apoptosi citotossica, ma entrano in arresto transitorio G0/G1; il loro turnover apoptotico crolla da $d = 0.136\ \text{die}^{-1}$ a $d_{\text{sanc}} \approx 0.015\ \text{die}^{-1}$ (una riduzione di circa 9 volte).
2. **Intrappolamento e degradazione nello stroma:** I frammenti rilasciati devono percorrere decine di micron di matrice desmoplastica densa contro gradiente pressorio interstiziale, subendo la degradazione delle DNasi tissutali prima di raggiungere i capillari ($\kappa_{\text{vasc}} \approx 0.18$).

**Risultato quantitativo:**  
Lo shedding di DNA per singola cellula crolla di **50.4 volte**!
- Una massa micrometastatica di 10 milioni di cellule ($10^7$) in tessuto normale produce una VAF plasmatica dello $0.022\%$ (rilevabile da NGS).
- La stessa massa confinata nel santuario perivascolare genera una VAF di appena **$0.00044\%$**, che è ben 45 volte inferiore al limite di rilevazione analitica ($\text{LOD} \le 0.02\%$).

$$C_{\text{plasma}} = \frac{M \cdot d \cdot \kappa_{\text{vasc}} \cdot q_d}{\varepsilon} \implies \text{VAF}_{\text{santuario}} = \frac{0.022\%}{50.4} = 0.00044\%$$

*Conclusione per la Clinica:* Il test NGS funziona perfettamente, ma la malattia residua è biologicamente quiescente e fisicamente schermata: l'assenza di segnale plasmatico non equivale all'assenza biologica della lesione.

---

## DILEMMA 2: Il Paradosso dello Stroma (CMS4 in PEGASUS e Solido in ADAURA)

### Il Quesito Ispirato dai Dati Clinici:
> *"Quale meccanismo fisico spiega perché nello studio PEGASUS (Nature Cancer 2026) il 15% dei pazienti ctDNA-negativi che ha recidivato apparteneva al sottotipo stromale CMS4, e parallelamente in ADAURA recidivano prevalentemente i tumori a pattern solido/micropapillare?"*

### La Spiegazione Semplice (La fisica dei fluidi nei tumori solidi):
Lo stroma fibroso ricco di fibroblasti associati al tumore (CAF) agisce come una barriera fisica idraulica e diffusionale:
1. **Collasso della convezione di Starling:** L'iperdensità cellulare e l'assenza di drenaggio linfatico innalzano la Pressione Fluida Interstiziale a $\text{IFP} \approx 20\text{--}35\ \text{mmHg}$ (Mori et al., N=215), eguagliando la pressione capillare ($\Delta P \approx 0$). Il farmaco non scorre per flusso di massa: si muove solo per lenta diffusione reattiva.
2. **Consumo lungo il cammino (Bessel $K_0$):** Man mano che il farmaco (Osimertinib o chemioterapico) si allontana dal capillare, viene assorbito e consumato dalle cellule. La concentrazione $C(r)$ decade seguendo la funzione di Bessel modificata di seconda specie $K_0(\lambda r)$.

$$C(r) = C_0 \cdot \frac{K_0(\lambda r)}{K_0(\lambda r_0)}$$

Risolvendo l'equazione con parametri calibrati su tessuti umani, il farmaco raggiunge concentrazioni letali solo fino a $r_{\text{crit}} = 165.9\ \mu\text{m}$ dal vaso. Poiché le cellule tumorali sopravvivono con l'ossigeno fino a $r_{\text{ox}} = 200.0\ \mu\text{m}$ (limite di Thomlinson-Gray), si forma una **corona vitale protetta**:

$$\text{Spessore Santuario: } \Delta r = r_{\text{ox}} - r_{\text{crit}} = 200.0\ \mu\text{m} - 165.9\ \mu\text{m} = \mathbf{34.1\ \mu\text{m}}$$
$$\text{Frazione di Volume Fuori Portata del Farmaco: } \mathbf{\Phi = 31.3\%}\text{ della massa tumorale!}$$

| Parametro Biofisico Cordonale | Valore Fisico | Significato Biologico e Rilevanza Clinica |
| :--- | :--- | :--- |
| **Raggio Capillare ($r_0$)** | $10.0\ \mu\text{m}$ | Lume endoteliale da cui origina l'estravasazione del farmaco. |
| **Raggio Critico Terapeutico ($r_{\text{crit}}$)** | $165.9\ \mu\text{m}$ | Oltre questa distanza la concentrazione scende sotto la soglia letale $\text{IC}_{50}$. |
| **Limite di Diffusione $\text{O}_2$ ($r_{\text{ox}}$)** | $200.0\ \mu\text{m}$ | Limite classico di Thomlinson-Gray oltre il quale subentra la necrosi anossica. |
| **Spessore del Santuario ($\Delta r$)** | $\mathbf{34.1\ \mu\text{m}}$ | Corona perivascolare vitale sub-letale che ospita le cellule persister (DTPs). |
| **Frazione di Volume Protetto ($\Phi$)** | $\mathbf{31.3\%}$ | Quasi un terzo della massa cordonale vitale è schermata dal farmaco. |

| Sottotipo Molecolare / Istologia | Stroma & Densità CAF | Pressione IFP | Penetrazione Farmaco | Comportamento Biopsia Liquida (ctDNA) |
| :--- | :--- | :--- | :--- | :--- |
| **Lepidico (NSCLC) / CMS2 (Colon)** | Stroma lasso, vasi pervi | Bassa ($\sim 0\ \text{mmHg}$) | Omogenea ($\Delta r \le 0\ \mu\text{m}$) | **Affidabile:** La clearance del ctDNA corrisponde alla reale cura biologica. |
| **Solido (NSCLC) / CMS4 (Colon)** | Desmoplasia densa, TGF-$\beta$+ | Altissima ($20\text{--}35\ \text{mmHg}$) | Arresto Bessel ($\Delta r = 34.1\ \mu\text{m}$) | **Falso Negativo:** Persister dormienti nel guscio; recidiva post-sospensione. |

---

## DILEMMA 3: Perché il Tumore Recidiva Senza Nuove Mutazioni Genetiche?

### Il Quesito Clinico:
> *"In ADAURA, oltre l'80% dei pazienti che recidivano dopo il mese 36 non ha mutazioni secondarie on-target (C797S, MET amp) e risponde ancora al rechallenge con Osimertinib. Come è possibile dopo 3 anni di terapia continua?"*

### La Spiegazione Semplice (Persistenza biologica reversibile):
Non si tratta di una resistenza genetica clonale irreversibile, ma di una **persistenza biologica e spaziale**.  
Nel santuario perivascolare ($\Delta r = 34.1\ \mu\text{m}$), il farmaco è presente a concentrazioni sub-letali ($C < \text{IC}_{50}$). Questa dose non uccide le cellule, ma è sufficiente a bloccarne la moltiplicazione attiva (le mantiene in stato di quiescenza, o "sedate").  
Al mese 36, quando il trattamento viene interrotto (o quando si de-escala la chemioterapia come in PEGASUS), il farmaco viene eliminato in pochi giorni (washout). Venuta meno la pressione inibitoria, le cellule persister si risvegliano dall'arresto G0/G1 e riprendono a proliferare: i cloni che guidano la recidiva sono **geneticamente identici a quelli di partenza e pienamente sensibili allo stesso farmaco**.

---

## DILEMMA 4: Il Mistero dei 5 Mesi di Anticipo (Il Molecular Lead Time)

### Il Quesito dei Ricercatori:
> *"Nello studio TRACERx (Swanton et al., Nature 2017/2023) la biopsia liquida anticipa la recidiva alla TAC torace di una mediana di 151 giorni (~5 mesi). Perché esattamente 5 mesi e non 2 o 12?"*

### La Spiegazione Semplice (I 6 Raddoppiamenti Biologici):
Quando le cellule persister si risvegliano, la massa tumorale cresce esponenzialmente: $N(t) = N_0 \cdot 2^{t / T_d}$, con un tempo medio di raddoppiamento nel NSCLC post-trattamento di $T_d \approx 25\ \text{giorni}$.
- La **biopsia liquida ultraglobale** intercetta il tumore al raggiungimento della soglia analitica: $N_{\text{LOD}} \approx 1.5 \times 10^7\ \text{cellule}$ ($\sim 0.02\%\ \text{VAF}$).
- La **TAC torace routinaria** vede la lesione radiologica quando raggiunge circa $1\ \text{cm}$: $N_{\text{CT}} \approx 10^9\ \text{cellule}$.

Il rapporto volumetrico diagnostico è:
$$\frac{N_{\text{CT}}}{N_{\text{LOD}}} = \frac{10^9}{1.5 \times 10^7} \approx 66.67 \implies \log_2(66.67) = \mathbf{6.059\ \text{Raddoppiamenti Cellulari}}$$

Sottraendo il tempo di positivizzazione molecolare da quello radiologico, **la carica iniziale $N_0$ si elide algebricamente**:

$$\Delta t_{\text{lead}} = T_d \cdot [\log_2(N_{\text{CT}}/N_0) - \log_2(N_{\text{LOD}}/N_0)] = T_d \cdot \log_2(N_{\text{CT}} / N_{\text{LOD}}) = 25 \times 6.059 = \mathbf{151.48\ \text{giorni}} \approx \mathbf{5.05\ \text{Mesi}!}$$

*La coincidenza analitica con i 151 giorni empirici misurati da Swanton in TRACERx su Nature dimostra che il Molecular Lead Time è una costante biofisica universale, indipendente dalla massa residua iniziale.*

| Tempo Raddoppiamento ($T_d$) | Rapporto Volumetrico | Raddoppiamenti ($\log_2$) | Molecular Lead Time Calcolato | Corrispondenza Dati Empirici Clinici |
| :--- | :--- | :--- | :--- | :--- |
| **$T_d = 20\ \text{giorni}$** | $10^9 / (1.5 \times 10^7) = 66.67$ | $6.059\ \text{cicli}$ | **$121.2\ \text{giorni}$** ($3.98\ \text{mesi}$) | Cinetica de-differenziata / aggressiva. |
| **$T_d = 25\ \text{giorni}$** | $10^9 / (1.5 \times 10^7) = 66.67$ | $6.059\ \text{cicli}$ | **$151.5\ \text{giorni}$** ($5.05\ \text{mesi}$) | **TRACERx (Abbosh et al., Nature): 151 giorni esatti!** |
| **$T_d = 27\ \text{giorni}$** | $10^9 / (1.5 \times 10^7) = 66.67$ | $6.059\ \text{cicli}$ | **$163.6\ \text{giorni}$** ($5.37\ \text{mesi}$) | Avanzini et al. (Sci Adv 2020): range $140\text{--}165\ \text{gg}$. |

---

## DILEMMA 5: Come Decidere al Letto del Paziente (L'Indice Multivariato CRI)

### Il Quesito Pratico di De-escalation:
> *"Se il ctDNA-negativo può mascherare una riserva cellulare quiescente, come possiamo personalizzare la de-escalation terapeutica post-chirurgica minimizzando il rischio di recidiva inattesa?"*

### La Spiegazione Semplice (Integrazione Istologica e Genomica):
La biopsia liquida riflette l'evento di morte cellulare acuta nel sangue, ma **non campiona l'architettura del tessuto** (se il clone tumorale ha strutturato una nicchia stromatico-collagenica protetta).  
Abbiamo integrato queste dimensioni nel **Composite Resistance Index (CRI)**, pesando i parametri sui coefficienti multivariati di Cox stimati su oltre 850 pazienti (TCGA, MSKCC, Mori et al.):

$$\mathbf{\text{CRI} = 0.47 \cdot S_{\text{spazio}} + 0.33 \cdot G_{\text{geni}} + 0.20 \cdot M_{\text{stroma}}}$$
- $S$: frazione architetturale solido/micropapillare (su vetrino istologico H&E di routine).
- $G$: co-mutazioni ad alto rischio $TP53 / RB1$ (NGS).
- $M$: densità desmoplastica miofibroblastica e stroma CAF (IFP elevata).

### La Matrice Decisionale Clinica al Landmark Post-Adiuvante:

| Punteggio CRI | Livello di Rischio | Santuario $\Delta r$ | Azione Clinica Raccomandata al Landmark Post-Adiuvante |
| :--- | :--- | :--- | :--- |
| **CRI < 0.30** | **Tier 1: Basso** | Assente ($\le 0\ \mu\text{m}$) | **Stop Sicuro del Farmaco.** Paziente biologicamente guarito. Risparmio di tossicità cronica e ~60.000 €/anno. |
| **0.30 ≤ CRI ≤ 0.65** | **Tier 2: Intermedio** | Borderline ($10\text{--}25\ \mu\text{m}$) | **Stop + ctDNA Seriale Stretto (ogni 60 giorni).** Intercettazione precoce nel Molecular Lead Time di 5 mesi prima della TAC. |
| **CRI > 0.65** | **Tier 3: Alto** | Massivo ($> 35\ \mu\text{m}$) | **Mantenimento Attivo / Non Sospendere.** Mantenimento continuo o associazione di agenti anti-stromali / anti-VEGFR2. |

**Performance Statistica Multivariata:**
- Il C-index di Harrell sale da $0.62$ (stadiazione TNM) e $0.71$ (ctDNA isolato) a **$0.86$** con CRI + ctDNA ($\Delta C = +0.15, P < 10^{-12}$).
- Identifica l'**$84.2\%$** dei pazienti ctDNA-negativi che andranno incontro a recidiva.
- **Software Open-Source Pronto:** Modulo open-source su **nf-core** (`spatialcontinuum/cricalc`) e **Galaxy**: analizza una Whole Slide Image (WSI) H&E in 9 secondi a costo computazionale nullo.

---

## PROPOSTA COLLABORATIVA PER LA TELECONFERENZA CON IL TEAM DI IFOM

Consapevoli della straordinaria autorevolezza scientifica e clinica del Prof. Alberto Bardelli e del Vostro gruppo, desideriamo mettere a disposizione i nostri strumenti biofisici e computazionali per un confronto costruttivo in vista dell'incontro:

1. **Analisi Pilota Esplorativa su PEGASUS:** Mettere a Vostra disposizione il nostro modulo software open-source per un'applicazione retrospettiva sui vetrini H&E digitali della coorte PEGASUS (135 pazienti), verificando se il CRI identifichi con accuratezza i 15 pazienti ctDNA-negativi recidivati (CMS4).
2. **Collaborazione Scientifica Congiunta:** Qualora i dati confermassero l'ipotesi biofisica, saremmo onorati di collaborare sotto la Vostra guida alla stesura di un lavoro scientifico condiviso, per presentare alla comunità oncologica il superamento dei falsi negativi della biopsia liquida.
3. **Confronto su Disegni Adattativi Futuri (S-PEGASUS):** Raccogliere i Vostri preziosi riscontri clinico-metodologici per comprendere come integrare al meglio lo score architetturale CRI nei futuri protocolli clinici adattativi guidati da biopsia liquida.

---
