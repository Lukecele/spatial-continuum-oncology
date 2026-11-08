#!/usr/bin/env python3
"""
CRI Biophysical Sanctuary Explorer - Gradio Web Application (RUO)
================================================================
The Spatial-Genomic Oncology Continuum
Author: Luca Celebrano, MD Candidate
Affiliation: Università degli Studi di Napoli Federico II

Launch locally with:
    pip install gradio pandas matplotlib
    python software_strumenti_calcolo/app_gradio_bedside_cri.py
"""

import math
from typing import Dict, Any, Tuple
import pandas as pd

# Histologic subtype scoring dictionary S in [0.0, 1.0]
HISTOLOGY_SCORES = {
    "Lepidic": 0.00,
    "Acinar": 0.35,
    "Papillary": 0.45,
    "Micropapillary": 0.90,
    "Solid": 1.00
}

# Stroma scoring dictionary M in [0.0, 1.0]
STROMA_SCORES = {
    "Alveolar / Loose (<15% desmoplasia)": 0.00,
    "Moderate (15-30% desmoplasia)": 0.50,
    "Dense Fibrotic (>30% desmoplasia)": 1.00
}

def calculate_cri(
    histology: str,
    tp53_mut: bool,
    rb1_mut: bool,
    stroma: str,
    w_spatial: float = 0.47,
    w_genomic: float = 0.33,
    w_stromal: float = 0.20,
    cutoff_low: float = 0.35,
    cutoff_high: float = 0.65
) -> Dict[str, Any]:
    """Calculates Composite Resistance Index (CRI) and returns biophysical sanctuary metrics (RUO)."""
    S = HISTOLOGY_SCORES.get(histology, 0.50)
    
    # Genomic co-mutation score G in [0.0, 1.0]
    if tp53_mut and rb1_mut:
        G = 1.00  # Double mutant: severe genomic instability & transformation risk
    elif tp53_mut or rb1_mut:
        G = 0.50  # Single mutant
    else:
        G = 0.00  # Double wild-type
        
    M = STROMA_SCORES.get(stroma, 0.50)
    
    # Mathematical linear combination weights
    CRI = w_spatial * S + w_genomic * G + w_stromal * M
    CRI = round(min(max(CRI, 0.0), 1.0), 3)
    
    # Biophysical sanctuary shell calculation
    # Based on Bessel K0 penetration: r_crit ~ 165.89 um, r_ox = 200.0 um
    # Under dense stroma and solid cords, delta_r approaches 34.11 um (31.28% cord volume)
    delta_r = round(34.11 * ((S + M) / 2.0), 1)
    sanctuary_vol_pct = round(31.28 * ((S + M) / 2.0), 1)
    
    # Stratification logic based on customizable cutoffs
    if CRI < cutoff_low:
        tier = "Tier 1 (Low Resistance / Minimal Sanctuary)"
        action = "Low Sanctuary Risk: Favorable Transport Profile (RUO)"
        justification = (
            f"Well-perfused, thin cords with minimal sanctuary mantle (Δr ≈ {delta_r} µm). "
            "Drug concentration is predicted to exceed IC50 throughout tissue geometry under baseline parameters."
        )
        rec = "Optimal candidate for standard post-cessation monitoring in cohort trials."
    elif CRI <= cutoff_high:
        tier = "Tier 2 (Intermediate Risk / Transitional Cords)"
        action = "Intermediate Sanctuary Risk: Transitional Perivascular Gradient (RUO)"
        justification = (
            f"Partial perivascular drug penetration with low-frequency dormant cells (Δr ≈ {delta_r} µm). "
            "Suggests close serial monitoring (e.g. ctDNA) in translational protocol investigations."
        )
        rec = "Consider intensive surveillance protocols within clinical trial designs."
    else:
        tier = "Tier 3 (High Resistance / Obligate Sanctuary)"
        action = "High Sanctuary Risk: Substantial Perivascular Shielding (RUO)"
        justification = (
            f"Dense fibrotic stroma and solid cord architecture create an obligate sanctuary shell "
            f"(Δr ≈ {delta_r} µm, ~{sanctuary_vol_pct}% viable cord volume). Reaction-diffusion decay "
            f"predicts sub-therapeutic exposure in outer cord margins."
        )
        rec = "Candidate cohort for vascular remodeling or anti-angiogenic trial arms (e.g. anti-VEGFR2)."
        
    return {
        "CRI": CRI,
        "Tier": tier,
        "Action": action,
        "Justification": justification,
        "Recommendation": rec,
        "Sanctuary_Delta_r_um": delta_r,
        "Sanctuary_Volume_Pct": sanctuary_vol_pct
    }

def process_single_patient(
    histology: str,
    tp53: bool,
    rb1: bool,
    stroma: str,
    w_spatial: float,
    w_genomic: float,
    w_stromal: float,
    cutoff_low: float,
    cutoff_high: float
) -> str:
    res = calculate_cri(
        histology, tp53, rb1, stroma,
        w_spatial=w_spatial, w_genomic=w_genomic, w_stromal=w_stromal,
        cutoff_low=cutoff_low, cutoff_high=cutoff_high
    )
    return f"""
### 🔬 Composite Resistance Index (CRI) Biophysical Analysis
*Research Use Only (RUO) · Not for Clinical Diagnostic Use*

- **CRI Score:** `{res['CRI']} / 1.000`
- **Stratification Tier:** **{res['Tier']}**
- **Biophysical Category:** `{res['Action']}`

---
#### 📐 Perivascular Sanctuary Metrics
- **Sanctuary Shell Thickness (Δr):** `{res['Sanctuary_Delta_r_um']} µm`
- **Sanctuary Volume Fraction:** `{res['Sanctuary_Volume_Pct']}%` of viable cord volume
- **Applied Model Weights:** `w_S = {w_spatial:.2f}, w_G = {w_genomic:.2f}, w_M = {w_stromal:.2f}`

---
#### 💡 Translational Cohort Implication
> **{res['Recommendation']}**

*Biophysical Rationale:* {res['Justification']}

---
> ⚠️ **Disclaimer:** Survival probabilities and clinical hazard ratios must be empirically fitted to patient cohort survival data (e.g., Kaplan-Meier, Cox Proportional Hazards via Survminer) rather than assumed fixed bedside rates.
"""

def batch_process_csv(
    file_obj,
    w_spatial: float,
    w_genomic: float,
    w_stromal: float,
    cutoff_low: float,
    cutoff_high: float
) -> Tuple[pd.DataFrame, str]:
    if file_obj is None:
        return pd.DataFrame(), "Please upload a CSV file."
        
    df = pd.read_csv(file_obj.name)
    required_cols = {"histology", "tp53", "rb1", "stroma"}
    lower_cols = {c.lower(): c for c in df.columns}
    
    if not required_cols.issubset(set(lower_cols.keys())):
        return pd.DataFrame(), f"Missing required columns. Found: {list(df.columns)}. Required: {list(required_cols)}"
        
    results = []
    for _, row in df.iterrows():
        hist = str(row[lower_cols["histology"]]).capitalize()
        tp53 = bool(row[lower_cols["tp53"]])
        rb1 = bool(row[lower_cols["rb1"]])
        stroma_val = str(row[lower_cols["stroma"]])
        
        # Normalize stroma string
        stroma_key = "Moderate (15-30% desmoplasia)"
        if "loose" in stroma_val.lower() or "alveolar" in stroma_val.lower():
            stroma_key = "Alveolar / Loose (<15% desmoplasia)"
        elif "dense" in stroma_val.lower() or "fibrotic" in stroma_val.lower():
            stroma_key = "Dense Fibrotic (>30% desmoplasia)"
            
        res = calculate_cri(
            hist, tp53, rb1, stroma_key,
            w_spatial=w_spatial, w_genomic=w_genomic, w_stromal=w_stromal,
            cutoff_low=cutoff_low, cutoff_high=cutoff_high
        )
        results.append({
            "Case_ID": row.get("patient_id", row.get("id", len(results) + 1)),
            "Histology": hist,
            "CRI_Score": res["CRI"],
            "Stratification_Tier": res["Tier"].split(" ")[0] + " " + res["Tier"].split(" ")[1],
            "Sanctuary_Category": res["Action"].split(":")[0].strip(),
            "Sanctuary_Shell_um": res["Sanctuary_Delta_r_um"]
        })
        
    res_df = pd.DataFrame(results)
    summary = f"Successfully analyzed {len(res_df)} cases: "
    summary += f"{len(res_df[res_df['CRI_Score'] < cutoff_low])} Tier 1, "
    summary += f"{len(res_df[(res_df['CRI_Score'] >= cutoff_low) & (res_df['CRI_Score'] <= cutoff_high)])} Tier 2, "
    summary += f"{len(res_df[res_df['CRI_Score'] > cutoff_high])} Tier 3."
    return res_df, summary

if __name__ == "__main__":
    try:
        import gradio as gr
    except ImportError:
        print("Gradio not installed. Install with: pip install gradio pandas matplotlib")
        exit(1)
        
    with gr.Blocks(title="CRI Biophysical Sanctuary Explorer - Spatial Oncology") as demo:
        gr.Markdown(
            """
            # 🔬 Composite Resistance Index (CRI) Biophysical Explorer
            ### *Translational Reaction-Diffusion Sanctuary Modeling (Research Use Only)*
            **Author:** Luca Celebrano, MD Candidate • Università degli Studi di Napoli Federico II  
            *Preprint:* [Research Square (Springer Nature)](https://doi.org/10.21203/rs.3.rs-11530312/v1) • *Zenodo DOI:* [10.5281/zenodo.23748047](https://doi.org/10.5281/zenodo.23748047)
            """
        )
        
        with gr.Accordion("⚙️ Model Parameters & Calibration Weights (Customizable)", open=False):
            with gr.Row():
                w_s = gr.Slider(minimum=0.0, maximum=1.0, value=0.47, step=0.01, label="Spatial Architecture Weight (w_S)")
                w_g = gr.Slider(minimum=0.0, maximum=1.0, value=0.33, step=0.01, label="Genomic Co-Mutation Weight (w_G)")
                w_m = gr.Slider(minimum=0.0, maximum=1.0, value=0.20, step=0.01, label="Stromal Desmoplasia Weight (w_M)")
            with gr.Row():
                c_low = gr.Slider(minimum=0.1, maximum=0.5, value=0.35, step=0.05, label="Tier 1 Cutoff Threshold")
                c_high = gr.Slider(minimum=0.5, maximum=0.9, value=0.65, step=0.05, label="Tier 3 Cutoff Threshold")

        with gr.Tab("Single Case Biophysical Assessment"):
            with gr.Row():
                with gr.Column():
                    hist = gr.Dropdown(
                        choices=["Lepidic", "Acinar", "Papillary", "Micropapillary", "Solid"],
                        value="Solid",
                        label="Predominant IASLC Histologic Subtype (S)"
                    )
                    tp53 = gr.Checkbox(label="TP53 Co-mutation Detected (NGS)", value=True)
                    rb1 = gr.Checkbox(label="RB1 Co-mutation Detected (NGS)", value=False)
                    stroma = gr.Radio(
                        choices=[
                            "Alveolar / Loose (<15% desmoplasia)",
                            "Moderate (15-30% desmoplasia)",
                            "Dense Fibrotic (>30% desmoplasia)"
                        ],
                        value="Dense Fibrotic (>30% desmoplasia)",
                        label="Stromal Desmoplasia & Architecture (M)"
                    )
                    btn_calc = gr.Button("Calculate Biophysical Metrics", variant="primary")
                    
                with gr.Column():
                    output_text = gr.Markdown()
                    
            btn_calc.click(
                process_single_patient,
                inputs=[hist, tp53, rb1, stroma, w_s, w_g, w_m, c_low, c_high],
                outputs=output_text
            )
            
        with gr.Tab("Cohort Batch Simulator (CSV Upload)"):
            gr.Markdown("Upload a patient cohort CSV containing columns: `histology`, `tp53`, `rb1`, `stroma`.")
            with gr.Row():
                csv_input = gr.File(label="Upload Patient Cohort CSV", file_types=[".csv"])
            btn_batch = gr.Button("Run Cohort Stratification", variant="primary")
            batch_status = gr.Textbox(label="Batch Status Summary", interactive=False)
            batch_table = gr.DataFrame(label="Cohort Stratification Results")
            btn_batch.click(
                batch_process_csv,
                inputs=[csv_input, w_s, w_g, w_m, c_low, c_high],
                outputs=[batch_table, batch_status]
            )

    demo.launch()
