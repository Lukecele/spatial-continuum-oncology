#!/usr/bin/env python3
"""
Adversarial Stress-Testing & Falsification Suite for the Spatial Oncology Continuum.
Pure Python Standard Library (math, json, sys).

Stress Tests:
1. Physical Extremes & Singularities (Desmoplastic collapse, infinite clearance, zero resistance).
2. Convective Washout Regime at Tumor Periphery (Peclet Number Transition Pe > 1).
3. Pharmacokinetic Outliers (CYP3A4 hyper-induction, severe hypoalbuminemia).
4. False Negative / Blind Spot Audit (ctDNA non-shedders in lepidic/pure-GGO lesions).
5. De Novo Genetic Bypass (When genetics renders spatial biophysics irrelevant).
"""

import math
import json

def K0_integral(x, n_steps=2000):
    if x <= 0:
        return float('inf')
    u_max = math.sqrt(36.0 / x)
    h = u_max / n_steps
    s = 0.0
    for i in range(n_steps + 1):
        u = i * h
        f = 2.0 * math.exp(-x * (1.0 + u * u)) / math.sqrt(u * u + 2.0)
        weight = 4.0 if (i % 2 == 1) else 2.0
        if i == 0 or i == n_steps:
            weight = 1.0
        s += weight * f
    return (h / 3.0) * s

def find_rcrit(lambda_val, r0, theta, max_r=2000.0):
    K0_r0 = K0_integral(r0 / lambda_val)
    # Check if even at capillary wall ratio < theta
    if 1.0 < theta:
        return r0
    # Check if at max_r ratio > theta
    ratio_max = K0_integral(max_r / lambda_val) / K0_r0
    if ratio_max >= theta:
        return max_r
    
    low = r0
    high = max_r
    for _ in range(80):
        mid = 0.5 * (low + high)
        ratio = K0_integral(mid / lambda_val) / K0_r0
        if ratio > theta:
            low = mid
        else:
            high = mid
    return mid

def run_adversarial_suite():
    results = {}

    # -------------------------------------------------------------------------
    # STRESS TEST 1: EXTREME BIOPHYSICAL REGIMES & SINGULARITIES
    # -------------------------------------------------------------------------
    # Base parameters for Osimertinib
    D0 = 607.11 # um^2/s
    r0 = 10.0   # um
    theta_base = 0.35
    k_base = 1.5052e-4 # s^-1

    scenarios = [
        {"name": "Standard Solid Tumor (Baseline)", "eps": 0.25, "tau": 1.60, "k": k_base, "theta": 0.35},
        {"name": "Severe Desmoplasia / Dense Stroma (e.g. Sclerotic)", "eps": 0.05, "tau": 3.20, "k": k_base, "theta": 0.35},
        {"name": "Hyper-Permeable / Edematous Stroma", "eps": 0.55, "tau": 1.15, "k": k_base, "theta": 0.35},
        {"name": "Hyper-Metabolic / Rapid Cellular Uptake (k x 10)", "eps": 0.25, "tau": 1.60, "k": k_base * 10.0, "theta": 0.35},
        {"name": "Target-Depleted / Low Cellular Uptake (k / 10)", "eps": 0.25, "tau": 1.60, "k": k_base / 10.0, "theta": 0.35},
        {"name": "Pre-Existing Weak Sensitivity (IC50 shift, theta=0.80)", "eps": 0.25, "tau": 1.60, "k": k_base, "theta": 0.80},
        {"name": "High Affinity / Ultra-Potent (theta=0.10)", "eps": 0.25, "tau": 1.60, "k": k_base, "theta": 0.10}
    ]

    biophysical_stress = []
    r_ox = 200.0

    for sc in scenarios:
        Deff = D0 * (sc["eps"] / (sc["tau"] ** 2))
        lam = math.sqrt(Deff / sc["k"])
        rc = find_rcrit(lam, r0, sc["theta"], max_r=2500.0)
        delta_r = max(0.0, r_ox - rc)
        vol_pct = max(0.0, min(100.0, ((r_ox**2 - rc**2) / (r_ox**2 - r0**2)) * 100.0)) if rc < r_ox else 0.0
        
        # Qualitative failure mode check
        if rc <= r0 + 1.0:
            status = "COLLAPSE: Complete Sanctuary (Drug fails at vessel wall)"
        elif rc >= r_ox:
            status = "EXTINCTION: Zero Sanctuary (Drug covers entire vital cord)"
        else:
            status = "ACTIVE_SANCTUARY"

        biophysical_stress.append({
            "scenario": sc["name"],
            "Deff_um2_s": round(Deff, 2),
            "lambda_um": round(lam, 1),
            "rcrit_um": round(rc, 2),
            "sanctuary_delta_r_um": round(delta_r, 2),
            "volume_sanctuary_pct": round(vol_pct, 2),
            "regime_status": status
        })

    results["1_biophysical_stress_tests"] = biophysical_stress

    # -------------------------------------------------------------------------
    # STRESS TEST 2: PERIPHERAL CONVECTIVE WASHOUT & PECLET NUMBER CRISIS
    # -------------------------------------------------------------------------
    # In tumor core: IFP ~ 30 mmHg, microvascular pressure P_v ~ 30 mmHg -> grad(P) = 0 -> v_fluid = 0.
    # But at the tumor margin (0 to 500 um from periphery): IFP drops from 30 mmHg to 0 mmHg (lymphatics present).
    # Darcy's law: v_fluid = -K * grad(P).
    # Hydraulic conductivity K ~ 2e-7 cm^2 / (mmHg * s) = 2e-3 um^2 / (mmHg * s).
    # grad(P) = 30 mmHg / 500 um = 0.06 mmHg / um.
    # v_fluid = 2e-3 * 0.06 = 1.2e-4 um/s = 0.12 nm/s? Wait:
    # Standard literature values (Baxter & Jain 1989, Boucher et al.): v_fluid at margin = 0.1 to 0.5 um/s!
    # Let's evaluate Peclet number Pe = v * L / Deff across varying convective velocities.
    v_velocities = [0.0, 0.05, 0.10, 0.25, 0.50, 1.00] # um/s
    L_char = 100.0 # um (typical intercapillary distance / cord scale)
    Deff_base = 59.29 # um^2/s

    convective_audit = []
    for v in v_velocities:
        Pe = (v * L_char) / Deff_base
        if Pe < 0.1:
            regime = "Pure Diffusion Dominance (Spatial Continuum Model 100% Valid)"
        elif Pe < 1.0:
            regime = "Mixed Diffusion-Convection Transition"
        else:
            regime = "Convective Washout Dominance (Drug swept into normal parenchyma; Model boundary violated!)"
        convective_audit.append({
            "convective_velocity_um_s": v,
            "peclet_number": round(Pe, 3),
            "transport_regime": regime
        })

    results["2_convective_washout_peclet_audit"] = {
        "finding": "In tumor core (IFP plateau), Pe = 0.000 (Pure Diffusion valid). At outer 200 um rim, Pe reaches 0.42-0.84, causing asymmetric centrifugal drug wash-out.",
        "evaluations": convective_audit
    }

    # -------------------------------------------------------------------------
    # STRESS TEST 3: PHARMACOKINETIC RED-TEAMING (CYP3A4 & ALBUMIN OUTLIERS)
    # -------------------------------------------------------------------------
    # Normal: Ctrough = 540 nM (Dickinson et al. 2016), fu = 0.053 -> C_free = 28.62 nM. IC50 = 10 nM -> theta = IC50 / C_free = 0.349.
    pk_stress_scenarios = [
        {"desc": "Standard 80 mg daily steady-state", "Ctrough_nM": 540.0, "fu": 0.053, "IC50_nM": 10.0},
        {"desc": "CYP3A4 Strong Inducer (e.g. Rifampin/Phenytoin, AUC -80%)", "Ctrough_nM": 108.0, "fu": 0.053, "IC50_nM": 10.0},
        {"desc": "CYP3A4 Inhibitor (e.g. Itraconazole, AUC +40%)", "Ctrough_nM": 756.0, "fu": 0.053, "IC50_nM": 10.0},
        {"desc": "Severe Cachexia / Hypoalbuminemia (<2.0 g/dL, fu doubles to 0.106)", "Ctrough_nM": 450.0, "fu": 0.106, "IC50_nM": 10.0},
        {"desc": "Dose Reduction to 40 mg daily (Ctrough halved)", "Ctrough_nM": 270.0, "fu": 0.053, "IC50_nM": 10.0},
        {"desc": "Emergent Micro-Resistant Subclone (IC50 shifts 5x to 50 nM)", "Ctrough_nM": 540.0, "fu": 0.053, "IC50_nM": 50.0}
    ]

    pk_results = []
    lam_base = 627.6
    for pk in pk_stress_scenarios:
        C_free = pk["Ctrough_nM"] * pk["fu"]
        theta = pk["IC50_nM"] / C_free
        if theta >= 1.0:
            rc = r0 # Drug cannot inhibit even at vessel wall!
            status = "CRITICAL RESISTANCE / UNDERDOSING: Vessel-wall failure"
            delta_r = r_ox - r0
            vol_pct = 100.0
        else:
            rc = find_rcrit(lam_base, r0, theta)
            delta_r = max(0.0, r_ox - rc)
            vol_pct = ((r_ox**2 - rc**2) / (r_ox**2 - r0**2)) * 100.0 if rc < r_ox else 0.0
            status = "STABLE SANCTUARY" if vol_pct > 0 else "COMPLETE EXTINCTION"

        pk_results.append({
            "scenario": pk["desc"],
            "C_free_nM": round(C_free, 2),
            "effective_theta": round(theta, 3),
            "rcrit_um": round(rc, 2),
            "sanctuary_volume_pct": round(vol_pct, 2),
            "clinical_impact": status
        })

    results["3_pharmacokinetic_red_teaming"] = pk_results

    # -------------------------------------------------------------------------
    # STRESS TEST 4: BLIND SPOT AUDIT - LOW SHEDDERS & ctDNA FALSE NEGATIVES
    # -------------------------------------------------------------------------
    # In ADAURA (Herbst et al. 2025), ctDNA had 95.8% specificity, but what about sensitivity?
    # Low-shedding lesions (lepidic adenocarcinoma, mucinous, purely subcentimetric, low tumor fraction <0.01%):
    # If ctDNA is negative at month 36, does that GUARANTEE absence of sanctuary? NO!
    results["4_blind_spots_and_model_failure_modes"] = {
        "failure_mode_1_ctDNA_false_negatives": {
            "mechanism": "Pure lepidic or ground-glass adenocarcinomas have low cell turnover and minimal necrosis, shedding ctDNA below assay limit of detection (VAF < 0.005%).",
            "consequence_for_CRI": "CRI could falsely classify a patient into Tier 1 (Discontinue) if based solely on ctDNA negative status without histological/radiological integration.",
            "safeguard_in_CDSS": "CRI architecture explicitly decouples ctDNA (M) from Histological Cord Distance (S) and Co-genomics (G). If S (solid) or G (TP53) is high, patient remains Tier 2 or 3 even if ctDNA is negative!"
        },
        "failure_mode_2_de_novo_bypass_genetics": {
            "mechanism": "De novo MET amplification, HER2 amplification, or EGFR C797S bypasses Osimertinib inhibition regardless of spatial drug concentration.",
            "consequence_for_CRI": "Biophysical sanctuary radius rcrit is meaningless if the tumor is pharmacologically insensitive at C_trough.",
            "safeguard_in_CDSS": "CRI genomics score G assigns immediate maximum risk (1.00) if off-target bypass drivers are detected, triggering immediate combination escalation regardless of vascular density."
        },
        "failure_mode_3_cerebral_sanctuary_vs_lung_sanctuary": {
            "mechanism": "Blood-Brain Barrier (BBB) possesses tight junctions (ZO-1, claudin-5) and active efflux (P-gp/ABCB1, BCRP/ABCG2). Osimertinib penetrates BBB better than 1st-gen, but unbound CNS partition ratio Kp,uu,brain is ~0.2-0.3.",
            "consequence": "Brain micro-metastases have an expanded spatial sanctuary radius: theta_CNS = theta_lung / Kp,uu ~ 1.1-1.7! At theta > 1.0, brain metastases relapse even while lung parenchyma remains controlled.",
            "safeguard_in_CDSS": "Protocol SG-ADAURA mandates contrast-enhanced brain MRI every 6 months for Tier 2 and Tier 3 patients."
        }
    }

    # -------------------------------------------------------------------------
    # STRESS TEST 5: FORMAL FALSIFIABILITY HYPOTHESES (POPPERIAN REFUTATION)
    # -------------------------------------------------------------------------
    results["5_popperian_falsification_criteria"] = [
        {
            "hypothesis": "H0_1: Spatial Sanctuary Irrelevance",
            "falsification_test": "In vivo MALDI-MSI (Matrix-Assisted Laser Desorption/Ionization Mass Spectrometry Imaging) of resected human EGFR-mutant lung tumors on steady-state osimertinib.",
            "condition_that_falsifies_our_theory": "If intra-vital MALDI-MSI reveals that free osimertinib concentration is spatially uniform across hypoxic tumor cords (>150 um from CD31+ vessels) and equals plasma C_free, the diffusion-elimination decay hypothesis is FALSIFIED."
        },
        {
            "hypothesis": "H0_2: ctDNA Lead Time Independence from Vascular Density",
            "falsification_test": "Correlation of pre-recurrence ctDNA lead time with CD31/von Willebrand Factor microvascular area fraction in resected baseline tumors.",
            "condition_that_falsifies_our_theory": "If solid, hypo-vascular tumors show longer or identical ctDNA lead times compared to highly vascularized lepidic tumors, our mathematical lead-time coupling is FALSIFIED."
        },
        {
            "hypothesis": "H0_3: Vascular Normalization Inefficacy",
            "falsification_test": "Dual inhibition with anti-VEGFR2 (Ramucirumab) + Osimertinib in dense-cord patient-derived xenografts (PDX).",
            "condition_that_falsifies_our_theory": "If decompression of interstitial fluid pressure (reduction of IFP) fails to reduce the residual un-cleared viable tumor cord fraction, our Starling/Darcy coupling theorem is FALSIFIED."
        }
    ]

    return results

if __name__ == "__main__":
    out = run_adversarial_suite()
    print(json.dumps(out, indent=2))
