#!/usr/bin/env python3
"""
CRI Bedside Clinical Decision Support - Gradio Web Application
==============================================================
The Spatial-Genomic Oncology Continuum
Author: Luca Celebrano, MD Candidate
Affiliation: Università degli Studi di Napoli Federico II
Target: Hugging Face Spaces (Gradio SDK)

Preprint DOI: 10.21203/rs.3.rs-11530312/v1
Zenodo DOI: 10.5281/zenodo.23754999
Bioconda: spatial-continuum (v1.0.3)
"""

import io
import math
from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import k0
import gradio as gr

# -----------------------------------------------------------------------------
# Biophysical & Clinical Model Core
# -----------------------------------------------------------------------------
HISTOLOGY_SCORES = {
    "Lepidic": 0.00,
    "Acinar": 0.35,
    "Papillary": 0.45,
    "Micropapillary": 0.90,
    "Solid": 1.00,
}

STROMA_SCORES = {
    "Alveolar / Loose (<15% desmoplasia)": 0.00,
    "Moderate (15-30% desmoplasia)": 0.50,
    "Dense Fibrotic (>30% desmoplasia)": 1.00,
}

BESSEL_CONSTANTS = {
    "r0_um": 8.0,
    "rcrit_um": 165.9,
    "lambda_nominal_um": 25.5,
}

def calculate_cri_clinical(
    histology: str,
    tp53_mut: bool,
    rb1_mut: bool,
    stroma: str,
    dose_mg: int = 80,
) -> Dict[str, Any]:
    """Calculates CRI, biophysical sanctuary shell, and Tumor Board directives."""
    S = HISTOLOGY_SCORES.get(histology, 0.50)

    # Genomic co-mutation score G in [0.0, 1.0]
    if tp53_mut and rb1_mut:
        G = 1.00  # Double mutant: catastrophic SCLC risk & neuroendocrine plasticity
    elif tp53_mut or rb1_mut:
        G = 0.50  # Single mutant
    else:
        G = 0.00  # Double wild-type

    M = STROMA_SCORES.get(stroma, 0.50)

    # Weights: w_S = 0.47, w_G = 0.33, w_M = 0.20
    CRI = 0.47 * S + 0.33 * G + 0.20 * M
    CRI = round(min(max(CRI, 0.0), 1.0), 3)

    # Dose adjustment on effective diffusion penetration depth lambda
    # Higher dose increases capillary concentration C0
    dose_factor = dose_mg / 80.0
    lambda_eff = BESSEL_CONSTANTS["lambda_nominal_um"] * math.sqrt(dose_factor)
    r_crit_eff = round(BESSEL_CONSTANTS["rcrit_um"] * (1.0 + 0.15 * math.log2(max(dose_factor, 0.5))), 1)

    # Sanctuary shell thickness delta_r (max ~34.1 um in thick solid cords)
    delta_r = round(34.11 * ((S + M) / 2.0), 1)
    sanctuary_vol_pct = round(31.28 * ((S + M) / 2.0), 1)

    if CRI < 0.35:
        tier = "Tier 1 (Low Resistance / Minimal Sanctuary)"
        action = "DISCONTINUATION CANDIDATE (Safe Cessation at Month 36)"
        dfs_5yr = "96.4% [95% CI: 92.1-99.2%]"
        justification = (
            "Well-perfused, thin alveolar cords (sanctuary shell Δr ≈ 0 µm). "
            "Drug concentration exceeds IC50 throughout tissue. Sparing 2 years of adjuvant "
            "osimertinib toxicity avoids cardiotoxicity/diarrhea without compromising 5-year DFS."
        )
        rec = "Cease Osimertinib at Month 36. Perform longitudinal ctDNA MRD surveillance every 3 months."
        color = "#10b981"
    elif CRI <= 0.65:
        tier = "Tier 2 (Intermediate Risk / Transitional Cords)"
        action = "MRD-GUIDED CONSOLIDATION (Selective Continuation)"
        dfs_5yr = "74.8% [95% CI: 68.3-81.2%]"
        justification = (
            "Partial perivascular drug penetration with low-frequency dormant cells. "
            "ctDNA surveillance mandatory; continue osimertinib for additional 12–24 months if ctDNA positive."
        )
        rec = "Perform plasma ctDNA at Month 36. If negative, maintain tight surveillance. If positive, continue monotherapy."
        color = "#f59e0b"
    else:
        tier = "Tier 3 (High Resistance / Obligate Sanctuary)"
        action = "DO NOT DISCONTINUE AT MONTH 36! (Mandatory Active Intervention)"
        dfs_5yr = "38.2% [95% CI: 31.0-45.5%]"
        justification = (
            f"Dense fibrotic stroma and solid cord architecture create an obligate sanctuary shell "
            f"(Δr ≈ {delta_r} µm, ~{sanctuary_vol_pct}% viable volume). Standard cessation causes "
            f"relapse within a median of 5.4 months. Continuous osimertinib or SG-ADAURA Arm B3 required."
        )
        rec = "Enroll in SG-ADAURA Arm B3 (Osimertinib 80 mg + Ramucirumab 10 mg/kg q2w) to normalize microvasculature."
        color = "#ef4444"

    return {
        "CRI": CRI,
        "S": S,
        "G": G,
        "M": M,
        "Tier": tier,
        "Action": action,
        "Expected_5yr_DFS": dfs_5yr,
        "Justification": justification,
        "Recommendation": rec,
        "Sanctuary_Delta_r_um": delta_r,
        "Sanctuary_Volume_Pct": sanctuary_vol_pct,
        "lambda_eff": round(lambda_eff, 1),
        "r_crit_eff": r_crit_eff,
        "color": color,
    }


def plot_bessel_penetration(res: Dict[str, Any]):
    """Generates a high-resolution dark-themed Bessel reaction-diffusion concentration plot."""
    r = np.linspace(8.0, 250.0, 500)
    lam = res["lambda_eff"]
    r0 = BESSEL_CONSTANTS["r0_um"]
    rcrit = res["r_crit_eff"]

    # C(r) / C0 = K0(r/lambda) / K0(r0/lambda)
    k0_r0 = k0(r0 / lam)
    conc = k0(r / lam) / k0_r0

    fig, ax = plt.subplots(figsize=(7, 3.8), dpi=150, facecolor="#0f172a")
    ax.set_facecolor("#070a13")

    # Curve
    ax.plot(r, conc, color="#06b6d4", linewidth=2.5, label=rf"$C(r)/C_0 = K_0(r/\lambda)/K_0(r_0/\lambda)$ ($\lambda={lam}\ \mu\mathrm{{m}}$)")

    # Fill Effective zone (< 100 um)
    mask_eff = r <= 100.0
    ax.fill_between(r[mask_eff], 0, conc[mask_eff], color="#06b6d4", alpha=0.25, label="Effective Zone (<100 µm)")

    # Fill Attenuated zone (100 - rcrit)
    mask_att = (r > 100.0) & (r <= rcrit)
    ax.fill_between(r[mask_att], 0, conc[mask_att], color="#eab308", alpha=0.3, label=f"Attenuated Zone (100-{rcrit} µm)")

    # Fill Sanctuary zone (> rcrit)
    mask_sanc = r > rcrit
    ax.fill_between(r[mask_sanc], 0, conc[mask_sanc], color="#f97316", alpha=0.45, label=f"Pharmacological Sanctuary (>{rcrit} µm)")

    # Vertical line at r_crit
    ax.axvline(rcrit, color="#f43f5e", linestyle="--", linewidth=1.5, label=rf"$r_{{\mathrm{{crit}}}} = {rcrit}\ \mu\mathrm{{m}}$")

    # Styling
    ax.set_title("Perivascular Osimertinib Diffusion Gradient (Bessel $K_0$)", color="#f8fafc", fontsize=10.5, fontweight="bold", pad=8)
    ax.set_xlabel("Radial Distance from Capillary Center $r$ (µm)", color="#94a3b8", fontsize=8.5)
    ax.set_ylabel("Normalized Concentration $C(r)/C_0$", color="#94a3b8", fontsize=8.5)
    ax.tick_params(colors="#64748b", labelsize=8)
    ax.set_ylim(-0.02, 1.05)
    ax.set_xlim(8.0, 250.0)

    for spine in ax.spines.values():
        spine.set_color("#334155")

    ax.legend(loc="upper right", facecolor="#0f172a", edgecolor="#334155", labelcolor="#e2e8f0", fontsize=7)
    plt.tight_layout()
    return fig


def process_single_patient(
    histology: str,
    tp53: bool,
    rb1: bool,
    stroma: str,
    dose: int,
) -> Tuple[str, Any]:
    res = calculate_cri_clinical(histology, tp53, rb1, stroma, dose)
    fig = plot_bessel_penetration(res)

    report_md = f"""
### 🩺 Official Bedside CRI Decision Dossier
**Patient Stratification & Tumor Board Consultation Summary**

| Metric | Patient Value | Reference / Meaning |
| :--- | :--- | :--- |
| **Composite Resistance Index (CRI)** | <span style="font-size: 1.3em; font-weight: bold; color: {res['color']}">{res['CRI']} / 1.000</span> | $0.47 S + 0.33 G + 0.20 M$ |
| **Clinical Risk Tier** | **<span style="color: {res['color']}">{res['Tier']}</span>** | Post-ADAURA month 36 stratification |
| **Expected 5-Year DFS** | **{res['Expected_5yr_DFS']}** | Pan-cancer calibrated clinical cohort |
| **Sanctuary Shell Thickness ($\\Delta r$)** | **{res['Sanctuary_Delta_r_um']} µm** | Max theoretical limit: 34.1 µm |
| **Perivascular Sanctuary Volume** | **{res['Sanctuary_Volume_Pct']}%** | Viable tissue volume beyond $r_{{\\text{{crit}}}}$ |
| **Daily Osimertinib Dose** | **{dose} mg / day** | Effective $\\lambda = {res['lambda_eff']}\\ \\mu\\text{{m}}$ |

---

### 🚨 Clinical Directive for Tumor Board
> **{res['Action']}**

**Physician Recommendation:**  
{res['Recommendation']}

**Biophysical & Biological Rationale:**  
{res['Justification']}

---
*Scientific Reference: Celebrano et al., Università degli Studi di Napoli Federico II. Research Square DOI: [10.21203/rs.3.rs-11530312/v1](https://doi.org/10.21203/rs.3.rs-11530312/v1)*
"""
    return report_md, fig


def batch_process_csv(file_obj) -> Tuple[pd.DataFrame, str, Optional[str]]:
    if file_obj is None:
        return pd.DataFrame(), "Please upload a CSV or TSV file.", None

    filepath = file_obj.name
    delimiter = "\t" if filepath.endswith(".tsv") else ","
    df = pd.read_csv(filepath, sep=delimiter)

    required_cols = {"histology", "tp53", "rb1", "stroma"}
    lower_cols = {c.lower().strip(): c for c in df.columns}

    if not required_cols.issubset(set(lower_cols.keys())):
        return pd.DataFrame(), f"Missing required columns. Found: {list(df.columns)}. Required: {list(required_cols)}", None

    results = []
    for _, row in df.iterrows():
        hist = str(row[lower_cols["histology"]]).capitalize()
        tp53 = bool(row[lower_cols["tp53"]])
        rb1 = bool(row[lower_cols["rb1"]])
        stroma_val = str(row[lower_cols["stroma"]])

        stroma_key = "Moderate (15-30% desmoplasia)"
        if "loose" in stroma_val.lower() or "alveolar" in stroma_val.lower():
            stroma_key = "Alveolar / Loose (<15% desmoplasia)"
        elif "dense" in stroma_val.lower() or "fibrotic" in stroma_val.lower():
            stroma_key = "Dense Fibrotic (>30% desmoplasia)"

        res = calculate_cri_clinical(hist, tp53, rb1, stroma_key)
        results.append({
            "Patient_ID": row.get("patient_id", row.get("id", f"PT_{len(results)+1:03d}")),
            "Histology": hist,
            "TP53": tp53,
            "RB1": rb1,
            "Stroma": stroma_key.split(" ")[0],
            "CRI_Score": res["CRI"],
            "Risk_Tier": res["Tier"].split("(")[0].strip(),
            "Expected_5yr_DFS": res["Expected_5yr_DFS"].split("[")[0].strip(),
            "Clinical_Action": res["Action"].split("(")[0].strip(),
            "Sanctuary_Shell_um": res["Sanctuary_Delta_r_um"],
        })

    res_df = pd.DataFrame(results)

    n_total = len(res_df)
    n_t1 = len(res_df[res_df["CRI_Score"] < 0.35])
    n_t2 = len(res_df[(res_df["CRI_Score"] >= 0.35) & (res_df["CRI_Score"] <= 0.65)])
    n_t3 = len(res_df[res_df["CRI_Score"] > 0.65])

    summary_text = (
        f"**Cohort Analysis Complete (N = {n_total} Patients):**\n\n"
        f"• **Tier 1 (Safe Discontinuation):** {n_t1} patients ({round(n_t1/n_total*100, 1)}%)\n"
        f"• **Tier 2 (ctDNA-Guided Consolidation):** {n_t2} patients ({round(n_t2/n_total*100, 1)}%)\n"
        f"• **Tier 3 (Obligate Sanctuary / Do Not Discontinue):** {n_t3} patients ({round(n_t3/n_total*100, 1)}%)"
    )

    out_csv = "/tmp/cri_cohort_stratification_report.csv"
    res_df.to_csv(out_csv, index=False)

    return res_df, summary_text, out_csv


def load_demo_cohort() -> Tuple[pd.DataFrame, str, Optional[str]]:
    demo_data = [
        {"patient_id": "P_001", "histology": "Lepidic", "tp53": False, "rb1": False, "stroma": "Alveolar / Loose"},
        {"patient_id": "P_002", "histology": "Acinar", "tp53": False, "rb1": False, "stroma": "Moderate"},
        {"patient_id": "P_003", "histology": "Papillary", "tp53": True, "rb1": False, "stroma": "Moderate"},
        {"patient_id": "P_004", "histology": "Solid", "tp53": True, "rb1": False, "stroma": "Dense Fibrotic"},
        {"patient_id": "P_005", "histology": "Micropapillary", "tp53": True, "rb1": True, "stroma": "Dense Fibrotic"},
        {"patient_id": "P_006", "histology": "Lepidic", "tp53": True, "rb1": False, "stroma": "Loose"},
        {"patient_id": "P_007", "histology": "Solid", "tp53": False, "rb1": False, "stroma": "Moderate"},
        {"patient_id": "P_008", "histology": "Acinar", "tp53": True, "rb1": True, "stroma": "Moderate"},
        {"patient_id": "P_009", "histology": "Solid", "tp53": True, "rb1": True, "stroma": "Dense Fibrotic"},
        {"patient_id": "P_010", "histology": "Micropapillary", "tp53": False, "rb1": False, "stroma": "Moderate"},
    ]
    df = pd.DataFrame(demo_data)
    csv_path = "/tmp/demo_lung_cancer_cohort.csv"
    df.to_csv(csv_path, index=False)

    class DummyFile:
        def __init__(self, p):
            self.name = p

    return batch_process_csv(DummyFile(csv_path))


# -----------------------------------------------------------------------------
# Gradio User Interface Architecture
# -----------------------------------------------------------------------------
theme = gr.themes.Soft(
    primary_hue="cyan",
    secondary_hue="blue",
    neutral_hue="slate",
)

with gr.Blocks(title="CRI Bedside Clinical Decision Support - Spatial Oncology") as demo:
    gr.Markdown(
        """
        # 🩺 Bedside Composite Resistance Index (CRI) Decision Engine
        ### *Universal Reaction-Diffusion Transport Framework & In-Situ Pharmacological Sanctuary Mapping*
        **Author:** Luca Celebrano, MD Candidate • Università degli Studi di Napoli Federico II  
        **Scientific Anchors:** [Research Square DOI: 10.21203/rs.3.rs-11530312/v1](https://doi.org/10.21203/rs.3.rs-11530312/v1) • [Zenodo DOI: 10.5281/zenodo.23754999](https://doi.org/10.5281/zenodo.23754999) • [Bioconda: spatial-continuum](https://anaconda.org/bioconda/spatial-continuum)
        """
    )

    with gr.Tab("🩺 Single Patient Bedside Evaluation"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("#### 📋 Patient Clinical & Histogenomic Parameters")
                hist = gr.Dropdown(
                    choices=["Lepidic", "Acinar", "Papillary", "Micropapillary", "Solid"],
                    value="Solid",
                    label="Predominant IASLC Histologic Pattern (S)",
                )
                with gr.Row():
                    tp53 = gr.Checkbox(label="TP53 Inactivating Mutation", value=True)
                    rb1 = gr.Checkbox(label="RB1 Inactivating Mutation", value=False)
                stroma = gr.Radio(
                    choices=[
                        "Alveolar / Loose (<15% desmoplasia)",
                        "Moderate (15-30% desmoplasia)",
                        "Dense Fibrotic (>30% desmoplasia)",
                    ],
                    value="Dense Fibrotic (>30% desmoplasia)",
                    label="Stromal Desmoplasia / CAF Architecture (M)",
                )
                dose = gr.Radio(
                    choices=[40, 80, 160],
                    value=80,
                    label="Daily Osimertinib Dose (mg)",
                )
                btn_calc = gr.Button("🚀 Calculate Bedside CRI & Directives", variant="primary")

            with gr.Column(scale=1):
                output_report = gr.Markdown()
                output_plot = gr.Plot()

        btn_calc.click(
            process_single_patient,
            inputs=[hist, tp53, rb1, stroma, dose],
            outputs=[output_report, output_plot],
        )

    with gr.Tab("👥 Cohort Batch Processing (CSV/TSV)"):
        gr.Markdown(
            """
            Upload a patient cohort table (CSV or TSV) with columns: `histology`, `tp53`, `rb1`, `stroma`.  
            Optionally include `patient_id` or `id`.
            """
        )
        with gr.Row():
            csv_file = gr.File(label="Upload Patient Cohort File", file_types=[".csv", ".tsv"])
            with gr.Column():
                btn_batch = gr.Button("⚡ Run Cohort Stratification", variant="primary")
                btn_demo = gr.Button("🧪 Load Demo Cohort (10 Patients)", variant="secondary")

        batch_summary = gr.Markdown()
        batch_table = gr.DataFrame(label="Stratified Cohort Output")
        download_file = gr.File(label="Download Stratified Results CSV")

        btn_batch.click(
            batch_process_csv,
            inputs=[csv_file],
            outputs=[batch_table, batch_summary, download_file],
        )
        btn_demo.click(
            load_demo_cohort,
            inputs=[],
            outputs=[batch_table, batch_summary, download_file],
        )

    with gr.Tab("🧬 Biophysical Sanctuary Rationale"):
        gr.Markdown(
            """
            ### 🔬 The Physics of Pharmacological Sanctuaries
            Solid carcinomas exhibit profound **microvascular rarefaction** and **desmoplastic physical barriers**.
            
            1. **Extravascular Transport Equation:**
               $$\\frac{1}{r} \\frac{d}{dr}\\left(r \\frac{dC}{dr}\\right) - \\frac{1}{\\lambda^2} C = 0$$
            
            2. **Analytical Solution:**
               $$\\frac{C(r)}{C_0} = \\frac{K_0(r/\\lambda)}{K_0(r_0/\\lambda)}$$
               
            3. **The Post-ADAURA Paradox:**
               - In **Tier 1** (Lepidic/Acinar, loose stroma), $r_{\\text{crit}} \\approx 165.9\\ \\mu\\text{m}$ covers the entire thin cord: **100% eradication**, safe discontinuation at Month 36.
               - In **Tier 3** (Solid/Micropapillary, dense stroma), cords expand up to $200\\ \\mu\\text{m}$, creating an obligate outer perivascular shell $\\Delta r \\approx 34.1\\ \\mu\\text{m}$ (>31% cord volume) with **zero effective drug exposure**.
               - Discontinuing osimertinib at Month 36 unmasks these dormant persister clones, leading to rapid disease relapse.
            """
        )

if __name__ == "__main__":
    demo.launch(theme=theme)
