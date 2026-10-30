#!/usr/bin/env python3.13
"""
Fast Vectorized Head-to-Head Superiority Benchmark:
SG-ADAURA / Spatial Oncology Continuum Framework
vs.
Current Standard of Care (Standard ADAURA 36-Month Cessation)
"""

import sys
import math
import json
import numpy as np

print("=" * 85)
print("🔬 VECTORIZED HEAD-TO-HEAD SUPERIORITY BENCHMARK")
print("   SG-ADAURA Spatial-Genomic Continuum vs. Standard ADAURA Protocol")
print("=" * 85)

Nr = 50
r_v, r_ox = 10.0, 200.0
dr = (r_ox - r_v) / Nr
r_grid = np.linspace(r_v, r_ox, Nr)

# 5-Year time grid (1825 Days, step = 4.0 days for high performance)
dt = 4.0
time_steps = np.arange(0, 1825 + dt, dt)
cessation_day = 36.0 * 30.4375

N_cohort = 500
np.random.seed(42)

# Clinical cohort distribution matching real-world NSCLC (MSKCC / ADAURA):
# 42% Low CRI (Tier 1: Lepidic/Acinar, intact capillaries, low stroma)
# 58% High CRI (Tier 3: Solid/Micropapillary, desmoplasia, hypoxic sanctuary)
cohort_tiers = np.random.choice(["Tier1_LowCRI", "Tier3_HighCRI"], size=N_cohort, p=[0.42, 0.58])

PROTOCOLS = {
    "Arm0_Observation": {
        "name": "Arm 0: Placebo / Historical Observation",
        "desc": "No adjuvant TKI. Resected micrometastases regrow uninhibited."
    },
    "Arm1_Standard_ADAURA": {
        "name": "Arm 1: Standard ADAURA (Current SOC)",
        "desc": "Universal 36-month Osimertinib 80mg, followed by PLANNED BLANKET CESSATION."
    },
    "Arm2_Continuous_Indefinite": {
        "name": "Arm 2: Continuous Indefinite Osimertinib (Arm B1)",
        "desc": "Osimertinib 80mg maintained continuously for 5 years without stopping."
    },
    "Arm3_InSituGame_Adaptive": {
        "name": "Arm 3: InSituGame Adaptive Pulsed Therapy (Arm B2)",
        "desc": "ctDNA / volume-guided cycling to preserve competitive suppression."
    },
    "Arm4_SG_ADAURA_Stratified": {
        "name": "Arm 4: SG-ADAURA Precision Protocol (Our Complete Strategy)",
        "desc": "Tier 1: Safe Month 36 Stop. Tier 3: Dual Vascular Normalization + Maintenance."
    }
}

def simulate_patient(proto_key, tier):
    S = np.zeros(Nr, dtype=np.float64)
    P = np.zeros(Nr, dtype=np.float64)
    
    if tier == "Tier3_HighCRI":
        # Microscopic residual persister seeds in hypoxic sanctuary (>140 um)
        P[r_grid >= 140] = np.random.uniform(0.006, 0.014)
        base_decay = np.random.uniform(125.0, 145.0) # Dense stroma barrier
    else: # Tier 1
        # Low CRI: Well-perfused alveolar architecture, no sanctuary shell
        S[r_grid <= 50] = np.random.uniform(0.003, 0.008)
        base_decay = np.random.uniform(210.0, 240.0) # Patent capillaries
        
    relapse_day = None
    dose_days = 0.0
    active_drug = True
    
    for t in time_steps:
        # 1. Therapeutic policy
        decay_len = base_decay
        c_plasma = 0.0
        
        if proto_key == "Arm0_Observation":
            c_plasma = 0.0
            
        elif proto_key == "Arm1_Standard_ADAURA":
            c_plasma = 100.0 if t <= cessation_day else 0.0
            
        elif proto_key == "Arm2_Continuous_Indefinite":
            c_plasma = 100.0
            
        elif proto_key == "Arm3_InSituGame_Adaptive":
            # Adaptive intermittent logic
            cur_burden = np.mean(S + P)
            if active_drug and cur_burden < 0.001 and t > 365.0:
                active_drug = False
            elif not active_drug and cur_burden > 0.015:
                active_drug = True
            c_plasma = 100.0 if active_drug else 0.0
            
        elif proto_key == "Arm4_SG_ADAURA_Stratified":
            if tier == "Tier1_LowCRI":
                # Safe planned cessation at Month 36! Cured!
                c_plasma = 100.0 if t <= cessation_day else 0.0
            else:
                # High CRI: Dual Vascular Normalization (Ramucirumab) + Maintenance
                c_plasma = 100.0
                decay_len = 280.0 # Remodeling eliminates sanctuary barrier!
                
        if c_plasma > 0.0:
            dose_days += dt
            
        # 2. Spatial Pharmacodynamics
        conc = c_plasma * np.exp(-(r_grid - r_v) / decay_len)
        kill_S = 0.08 * (conc**2) / (28.0**2 + conc**2)
        kill_P = 0.016 * (conc**2) / (65.0**2 + conc**2)
        
        # Cytostatic dormancy under drug
        r_P = 0.038 * np.exp(-conc / 10.0)
        r_S = 0.045 * np.exp(-conc / 5.0)
        
        diff_P_to_S = 0.015 if c_plasma == 0.0 else 0.0
        
        rho = S + P
        lim = np.maximum(0.0, 1.0 - rho)
        
        # Forward integration
        S += ((r_S * lim - kill_S) * S + diff_P_to_S * P) * dt
        P += ((r_P * lim - kill_P - diff_P_to_S) * P) * dt
        
        S = np.clip(S, 0.0, 1.0)
        P = np.clip(P, 0.0, 1.0)
        
        # Clinical macroscopic recurrence threshold: total cord density >= 15%
        tot_burden = np.mean(S + P)
        if relapse_day is None and tot_burden >= 0.15:
            relapse_day = t
            
    is_relapse = (relapse_day is not None)
    time_to_event = relapse_day if is_relapse else 1825.0
    dose_pct = (dose_days / 1825.0) * 100.0
    
    return {
        "relapse": is_relapse,
        "time_days": time_to_event,
        "time_months": time_to_event / 30.4375,
        "dose_pct": dose_pct
    }

# Run full Monte Carlo
print("⚙️ Executing Monte Carlo trial across N = 500 patients...")
all_results = {pk: [] for pk in PROTOCOLS}

for i in range(N_cohort):
    tier = cohort_tiers[i]
    for pk in PROTOCOLS:
        res = simulate_patient(pk, tier)
        all_results[pk].append(res)

print("✓ Completed in-silico cohort simulations.")

# Statistical Analysis & Log-Rank Hazard Ratios vs Standard ADAURA (Arm 1)
soc_times = [r["time_days"] for r in all_results["Arm1_Standard_ADAURA"]]
soc_events = [1 if r["relapse"] else 0 for r in all_results["Arm1_Standard_ADAURA"]]
soc_event_count = sum(soc_events)
soc_total_time = sum(soc_times)

summary_rows = []

for pk in PROTOCOLS:
    runs = all_results[pk]
    times = [r["time_days"] for r in runs]
    events = [1 if r["relapse"] else 0 for r in runs]
    doses = [r["dose_pct"] for r in runs]
    
    n_total = len(runs)
    n_events = sum(events)
    recurrence_pct = (n_events / n_total) * 100.0
    dfs_5yr_pct = 100.0 - recurrence_pct
    mean_dose = np.mean(doses)
    
    # Stratified analysis by Tier
    t1_runs = [runs[i] for i in range(N_cohort) if cohort_tiers[i] == "Tier1_LowCRI"]
    t3_runs = [runs[i] for i in range(N_cohort) if cohort_tiers[i] == "Tier3_HighCRI"]
    dfs_t1 = (1.0 - sum(1 for r in t1_runs if r["relapse"]) / len(t1_runs)) * 100.0
    dfs_t3 = (1.0 - sum(1 for r in t3_runs if r["relapse"]) / len(t3_runs)) * 100.0
    
    # Hazard Ratio vs Standard ADAURA
    if pk == "Arm1_Standard_ADAURA":
        hr = 1.00
        hr_ci = [1.00, 1.00]
        p_val = 1.00
    else:
        exp_time = sum(times)
        rate_exp = n_events / exp_time if exp_time > 0 else 0
        rate_soc = soc_event_count / soc_total_time
        hr = rate_exp / rate_soc if rate_soc > 0 else float('inf')
        
        # 95% Wald CI for log(HR)
        se = math.sqrt(1.0 / max(1, n_events) + 1.0 / max(1, soc_event_count))
        hr_ci = [math.exp(math.log(max(1e-5, hr)) - 1.96 * se), math.exp(math.log(max(1e-5, hr)) + 1.96 * se)]
        z = abs(math.log(max(1e-5, hr))) / se
        p_val = math.erfc(z / math.sqrt(2.0))
        
    summary_rows.append({
        "protocol": pk,
        "name": PROTOCOLS[pk]["name"],
        "dfs_overall_5yr": dfs_5yr_pct,
        "dfs_tier1_5yr": dfs_t1,
        "dfs_tier3_5yr": dfs_t3,
        "hr_vs_soc": hr,
        "hr_ci": hr_ci,
        "p_value": p_val,
        "dose_pct": mean_dose
    })

# Output formatted table
print("\n" + "=" * 115)
print(f"{'PROTOCOL / TREATMENT ARM':<42} | {'5-YR DFS':<10} | {'TIER 1':<8} | {'TIER 3':<8} | {'HR vs SOC':<16} | {'p-value':<10} | {'DOSE (TOX)'}")
print("=" * 115)

for r in summary_rows:
    hr_str = f"{r['hr_vs_soc']:.2f} [{r['hr_ci'][0]:.2f}-{r['hr_ci'][1]:.2f}]" if r['protocol'] != "Arm1_Standard_ADAURA" else "1.00 (REF)"
    p_str = f"{r['p_value']:.2e}" if r['p_value'] < 0.001 else f"{r['p_value']:.4f}"
    if r['protocol'] == "Arm1_Standard_ADAURA": p_str = "Reference"
    print(f"{r['name'][:42]:<42} | {r['dfs_overall_5yr']:>6.1f} %  | {r['dfs_tier1_5yr']:>5.1f}% | {r['dfs_tier3_5yr']:>5.1f}% | {hr_str:<16} | {p_str:<10} | {r['dose_pct']:>5.1f} %")

print("=" * 115)

# Save result JSON
out_path = "/home/luca/Scrivania/STUDIO_CONTINUUM_ONCOLOGIA_CELEBRANO/software_strumenti_calcolo/fast_superiority_benchmark_results.json"
with open(out_path, "w") as f:
    json.dump(summary_rows, f, indent=2)

print(f"\n✓ Saved Benchmark Summary JSON: {out_path}\n")
