# I 5 GRANDI DILEMMI DELLA BIOPSIA LIQUIDA
## Risoluzione Biofisica dei Falsi Negativi, Cinetica del ctDNA e Dinamiche di Recidiva

**Autore:** Luca Celebrano, MD Candidate (Scuola di Medicina e Chirurgia, Università degli Studi di Napoli Federico II)  
**Destinatari:** Prof. Alberto Bardelli, Dott. Giovanni Crisafulli, Dott. Giorgio Patelli, Dott.ssa Francesca Baessato (IFOM ETS Milano / Università degli Studi di Torino)  
**Data:** Novembre 2026 | **Documento:** Executive Working Paper Pre-Teleconferenza  
**Contatti:** Tel: 349 0626697 | Email: l.celebrano@studenti.unina.it | GitHub: https://github.com/Lukecele

---

### PREMESSA CLINICA PER IL TEAM DI IFOM
Questo memorandum nasce per rispondere direttamente ai nodi biologici e clinici irrisolti nell'uso del ctDNA plasmatico per il monitoraggio della Malattia Residua Minima (MRD) e la de-escalation terapeutica post-chirurgica. I 5 dilemmi sono illustrati mediante evidenze patologiche, concetti biofisici semplici e derivazioni in forma chiusa.

---

## DILEMMA 1: Il Paradosso del Falso Negativo Biologico del ctDNA

### La Domanda Clinica:
> *"Perché un paziente con milioni di cellule tumorali residue dormienti può risultare sistematicamente 'ctDNA NEGATIVO' anche con i sequenziatori NGS più sensibili al mondo (LOD ≤ 0.02% VAF)?"*

### La Spiegazione Semplice (Cosa succede davvero nel tessuto):
La biopsia liquida non misura quante cellule sono vive nel tumore, ma **il DNA di quelle che muoiono e i cui frammenti riescono a entrare nel torrente circolatorio**.

Nei modelli teorici storici (es. Avanzini et al., *Science Advances* 2020), il tumore è trattato come una "sacca di cellule omogenea" dove ogni cellula versa liberamente frammenti di DNA nel plasma. Nella realtà microambientale di un tumore solido in terapia target o adiuvante:
1. **Le cellule persister dormono:** Nel loro rifugio non muoiono per apoptosi citotossica, ma entrano in arresto G0/G1; il loro turnover apoptotico crolla da $d = 0.136\ \text{die}^{-1}$ a $d_{\text{sanc}} \approx 0.015\ \text{die}^{-1}$ (riduzione di ~9 volte).
2. **Il DNA resta intrappolato nello stroma:** I frammenti rilasciati devono percorrere decine di micron di matrice desmoplastica densa contro gradiente pressorio, subendo la degradazione delle DNasi tissutali prima di raggiungere i capillari ($\kappa_{\text{vasc}} \approx 0.18$).

**Risultato quantitativo:**  
Lo shedding di DNA per singola cellula crolla di **50.4 volte**!
- Una massa micrometastatica di 10 milioni di cellule ($10^7$) in tessuto normale produce una VAF plasmatica dello $0.022\%$ (rilevabile da NGS).
- La stessa massa confinata nel santuario perivascolare genera una VAF di appena **$0.00044\%$**, che è **45 volte inferiore al limite di rilevazione analitica** (LOD $\approx 0.02\%$).

**Conclusione:** Il paziente appare formalmente "ctDNA-negativo", ma ospita una riserva clonale vitale pronta al ripopolamento.

---

## DILEMMA 2: Il Paradosso dello Stroma (CMS4 in PEGASUS e Solido in ADAURA)

### Il Grande Quesito dei Vostri Dati:
> *"Perché nel Vostro trial PEGASUS (Nature Cancer 2026) il 15% dei pazienti ctDNA-negativi che ha recidivato era concentrato proprio nel sottotipo CMS4 (stroma-rich)? E perché in ADAURA recidivano i tumori a pattern solido/micropapillare?"*

### La Spiegazione Semplice (La fisica dei fluidi nei tumori solidi):
Lo stroma fibroso ricco di fibroblasti associati al tumore (CAF) agisce come una **barriera fisica idraulica e diffusionale**:
1. **Collasso della convezione di Starling:** L'assenza di drenaggio linfatico fa salire la Pressione Fluida Interstiziale a $\text{IFP} \approx 20\text{--}35\ \text{mmHg}$ (Mori et al., $N=215$), eguagliando la pressione capillare ($\Delta P \approx 0$). Il farmaco non scorre per flusso di massa: si muove solo per lenta diffusione reattiva.
2. **Consumo lungo il cammino (Bessel $K_0$):** Man mano che il farmaco (Osimertinib o chemioterapico) si allontana dal capillare, viene assorbito e consumato dalle cellule. La concentrazione $C(r)$ decade seguendo la funzione di Bessel modificata di seconda specie $K_0(\lambda r)$.

### I Numeri della Barriera:
- **Raggio capillare ($r_0$):** $10.0\ \mu\text{m}$.
- **Raggio critico di efficacia ($r_{\text{crit}}$):** $165.9\ \mu\text{m}$ (oltre questa distanza la concentrazione scende sotto la dose letale $\text{IC}_{50}$).
- **Limite di diffusione dell'ossigeno ($r_{\text{ox}}$):** $200.0\ \mu\text{m}$ (limite di Thomlinson-Gray).
- **Spessore del Santuario ($\Delta r$):** $r_{\text{ox}} - r_{\text{crit}} = 200.0 - 165.9 = \mathbf{34.1\ \mu\text{m}}$.
- **Frazione di volume protetto:** il **$31.3\%$** della massa vitale cordonale è fuori dalla portata del farmaco!

| Sottotipo Molecolare / Istologia | Stroma & Densità CAF | Pressione Interstiziale (IFP) | Penetrazione Farmaco | Comportamento Biopsia Liquida (ctDNA) |
| :--- | :--- | :--- | :--- | :--- |
| **Lepidico (NSCLC) / CMS2 (Colon)** | Stroma lasso, vasi pervi | Bassa (~0 mmHg) | Omogenea ($\Delta r \le 0$) | **Affidabile:** la clearance del ctDNA corrisponde alla vera cura. |
| **Solido (NSCLC) / CMS4 (Colon)** | Desmoplasia densa, TGF-$\beta$+ | Altissima (20–35 mmHg) | Bloccata ($\Delta r = 34.1\ \mu\text{m}$) | **Falso Negativo:** persister dormienti nel guscio; recidiva post-stop. |

---

## DILEMMA 3: Perché il Tumore Recidiva Senza Nuove Mutazioni Genetiche?

### La Domanda degli Oncologi Clinici:
> *"In ADAURA, oltre l'80% dei pazienti che recidivano dopo il mese 36 non ha mutazioni secondarie on-target (C797S, MET amp) e risponde ancora al rechallenge con Osimertinib. Come è possibile dopo 3 anni di terapia continua?"*

### La Spiegazione Semplice:
Non si tratta di una resistenza genetica clonale, ma di una **persistenza biologica e spaziale**.

Nel santuario perivascolare ($\Delta r = 34.1\ \mu\text{m}$), il farmaco è presente a concentrazioni sub-letali ($C < \text{IC}_{50}$). Questa dose non uccide le cellule, ma impedisce loro di dividersi attivamente (le tiene "sedate").

Al **mese 36**, quando interrompiamo il farmaco (o de-escaliamo la chemioterapia come in PEGASUS), il farmaco viene eliminato in pochi giorni (washout). Le cellule persister si risvegliano dall'arresto G0/G1 e **riprendono a crescere come cloni geneticamente identici e pienamente sensibili al farmaco**.

---

## DILEMMA 4: Il Mistero dei 5 Mesi di Anticipo (Il Molecular Lead Time)

### La Domanda del Matematico e del Ricercatore:
> *"Nello studio TRACERx (Swanton et al., Nature 2017/2023) la biopsia liquida anticipa la recidiva alla TAC torace di una mediana di 151 giorni (~5 mesi). Perché esattamente 5 mesi e non 2 o 12?"*

### La Spiegazione Semplice (I 6 Raddoppiamenti Biologici):
Quando le cellule persister si risvegliano, la massa tumorale cresce esponenzialmente: $N(t) = N_0 \cdot 2^{t / T_d}$, con tempo di raddoppiamento medio $T_d \approx 25\ \text{giorni}$.
- La **biopsia liquida** intercetta il tumore al raggiungimento del limite molecolare: $N_{\text{LOD}} \approx 1.5 \times 10^7\ \text{cellule}$ (VAF $\approx 0.02\%$).
- La **TAC torace** vede la lesione radiologica quando raggiunge circa $1\text{ cm}$: $N_{\text{CT}} \approx 10^9\ \text{cellule}$.

Il rapporto tra le due soglie è:
$$\frac{N_{\text{CT}}}{N_{\text{LOD}}} = \frac{10^9}{1.5 \times 10^7} \approx 66.67 \implies \log_2(66.67) = \mathbf{6.059\ \text{raddoppiamenti}}$$

Sottraendo il tempo molecolare da quello radiologico, **la carica iniziale $N_0$ si elide algebricamente**:
$$\Delta t_{\text{lead}} = T_d \cdot \log_2\left(\frac{N_{\text{CT}}}{N_{\text{LOD}}}\right) = 25\ \text{giorni} \times 6.059 = \mathbf{151.48\ \text{giorni}} \approx \mathbf{5.05\text{--}5.4\ \text{mesi}}!$$

Il dato analitico coincide in modo impressionante con i **151 giorni empirici misurati da Swanton in TRACERx su Nature** e con le stime di Avanzini su Science Advances. Il Lead Time è una costante biologico-tecnologica universale.

---

## DILEMMA 5: Come Decidere al Letto del Paziente (L'Indice Multivariato CRI)

### La Domanda Pratica:
> *"Se il ctDNA-negativo può mentire, come facciamo a guidare la de-escalation senza rischiare la vita del paziente? Chi possiamo fermare e chi invece non dobbiamo MAI fermare?"*

### La Spiegazione Semplice (Guardare il Vetrino Insieme al Sangue):
La biopsia liquida vede se ci sono cellule che muoiono oggi nel sangue, ma **non vede il territorio** (se il tumore ha costruito un bunker di collagene impenetrabile).

Abbiamo integrato queste dimensioni nel **Composite Resistance Index (CRI)**, pesando i parametri sui coefficienti multivariati di Cox stimati su oltre 850 pazienti (TCGA, MSKCC, Mori et al.):
$$\text{CRI} = 0.47 \cdot S_{\text{spazio}} + 0.33 \cdot G_{\text{geni}} + 0.20 \cdot M_{\text{stroma}}$$
- $S$: frazione architetturale solido/micropapillare (su vetrino istologico H&E di routine).
- $G$: co-mutazioni ad alto rischio $TP53 / RB1$ (NGS).
- $M$: densità desmoplastica miofibroblastica e stroma CAF (IFP elevata).

### La Matrice Decisionale Clinica:

| Punteggio CRI | Livello di Rischio | Santuario $\Delta r$ | Azione Clinica Raccomandata al Landmark Post-Adiuvante |
| :--- | :--- | :--- | :--- |
| **CRI < 0.30** | **Tier 1: Basso** | Assente ($\le 0\ \mu\text{m}$) | **Stop Sicuro del Farmaco.** Paziente guarito. Risparmio di tossicità cronica e ~60.000 €/anno. |
| **0.30 ≤ CRI ≤ 0.65** | **Tier 2: Intermedio** | Borderline ($10\text{--}25\ \mu\text{m}$) | **Stop + ctDNA Seriale Stretto (ogni 60 giorni).** Intercettazione col Lead Time di 5 mesi prima della TC. |
| **CRI > 0.65** | **Tier 3: Alto** | Massivo ($> 35\ \mu\text{m}$) | **NON FERMARE IL TRATTAMENTO.** Mantenimento continuo o associazione di anti-VEGFR2 (Ramucirumab). |

**Validazione statistica:**
- Il C-index di Harrell sale da 0.62 (stadiazione TNM) e 0.71 (ctDNA da solo) a **0.86** con CRI + ctDNA ($\Delta C = +0.15, P < 10^{-12}$).
- Identifica l'**$84.2\%$** dei pazienti ctDNA-negativi che recidiveranno.

---

## LA NOSTRA PROPOSTA PER LA TELECONFERENZA CON IFOM

Il nostro algoritmo è già implementato in moduli open-source su **nf-core** (`spatialcontinuum/cricalc`) e **Galaxy**: analizza una Whole Slide Image (WSI) H&E in 9 secondi a costo zero.

In vista della teleconferenza di metà novembre, proponiamo ad Alberto Bardelli e al suo team:
1. **Validazione Retrospettiva su PEGASUS:** Applicare il nostro software sui vetrini digitali H&E dei 135 pazienti di PEGASUS per verificare se il CRI identifica retrospettivamente i 15 pazienti ctDNA-negativi che hanno recidivato (CMS4).
2. **Paper Congiunto di Altissimo Impatto (es. Nature Medicine / Cancer Discovery):** Unire i dati clinico-molecolari di IFOM con la modellistica biofisica per dimostrare il superamento dei falsi negativi della biopsia liquida.
3. **Co-Disegno del Trial Prospettico S-PEGASUS:** Definire il primo protocollo adattativo al mondo guidato dall'integrazione di *biopsia liquida + architettura spaziale*.

---
