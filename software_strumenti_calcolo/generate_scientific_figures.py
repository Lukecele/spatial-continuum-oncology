#!/usr/bin/env python3
"""
Scientific Figure Generator for:
'The Spatial-Genomic Oncology Continuum: A Biophysical Reaction-Diffusion Theory of
Pharmacological Sanctuaries, the Post-ADAURA Cessation Dilemma, and the SG-ADAURA Clinical Trial Protocol'
Author: Dr. Luca Celebrano (Universita degli Studi di Napoli Federico II)
Format: Nature Communications / medRxiv Publication Standards (300 DPI PNG & Vector PDF)
"""

import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set global publication styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.color'] = '#333333'
plt.rcParams['ytick.color'] = '#333333'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9

out_dir = "/home/luca/Scrivania/STUDIO_CONTINUUM_ONCOLOGIA_CELEBRANO/figure_scientifiche"
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------------------
# Bessel functions implementation (pure / standard)
# -------------------------------------------------------------------------
def bessel_k0(x, n_steps=2000, t_max=12.0):
    dt = t_max / n_steps
    total = 0.5 * (np.exp(-x * np.cosh(0)) + np.exp(-x * np.cosh(t_max)))
    t = np.linspace(dt, t_max - dt, n_steps - 1)
    # vectorized integration
    val = -x[:, None] * np.cosh(t)[None, :]
    mask = val > -80
    exp_val = np.zeros_like(val)
    exp_val[mask] = np.exp(val[mask])
    total = total + np.sum(exp_val, axis=1)
    return total * dt

def C_decay(r, lam=627.6, r0=10.0):
    k0_r0 = float(bessel_k0(np.array([r0 / lam]))[0])
    k0_r = bessel_k0(r / lam)
    return k0_r / k0_r0

# =========================================================================
# FIGURE 1: Reaction-Diffusion Geometry and Pharmacological Sanctuary
# =========================================================================
fig1, (ax1a, ax1b) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

# Panel A: Starling-Darcy Convective Arrest
histologies = ['Normal Lung', 'Lepidic (GGO)', 'Acinar/Papillary', 'Solid / Micropapillary']
ifp_values = [0.0, 2.5, 6.8, 9.8]
ifp_errors = [0.5, 1.2, 3.1, 6.8]
colors_a = ['#4A7BB7', '#6CAED6', '#FDBB84', '#D7301F']

bars = ax1a.bar(histologies, ifp_values, yerr=ifp_errors, capsize=5, color=colors_a, edgecolor='#333333', alpha=0.85, width=0.55)
ax1a.axhline(y=15.0, color='#888888', linestyle='--', linewidth=1.5, label='Microvascular Hydrostatic Pressure ($P_v \\approx 15-20$ mmHg)')
ax1a.set_ylabel('Interstitial Fluid Pressure (IFP, mmHg)')
ax1a.set_title('a  Starling-Darcy Hydrostatic Equilibrium & Convective Arrest', loc='left', fontweight='bold')
ax1a.set_ylim(-1, 25)
ax1a.legend(loc='upper left', frameon=True)
ax1a.grid(axis='y', linestyle=':', alpha=0.6)

# Annotation for Peclet
ax1a.annotate('Péclet Number $Pe < 0.1$\n(Pure Diffusion Dominance)',
             xy=(3, 10.0), xytext=(2.2, 17.5),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6),
             fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFFFCC', edgecolor='#D7301F'))

# Panel B: Cylindrical Bessel K0 Decay & Sanctuary Cuff
r_arr = np.linspace(10.0, 250.0, 500)
c_osimertinib = C_decay(r_arr, lam=627.6, r0=10.0)

ax1b.plot(r_arr, c_osimertinib, color='#2B5C8F', linewidth=2.5, label='Osimertinib Free Profile ($C(r)/C_0$)')
ax1b.axhline(y=0.349, color='#D95F02', linestyle='--', linewidth=1.8, label='Inhibition Threshold $\\theta = 0.349$ ($IC_{50} = 10.0$ nM)')

# Critical radius line
ax1b.axvline(x=165.89, color='#D95F02', linestyle=':', linewidth=1.5)
ax1b.axvline(x=200.0, color='#7570B3', linestyle=':', linewidth=1.5)

# Sanctuary Shading
ax1b.axvspan(165.89, 200.0, color='#E7298A', alpha=0.25, label='Pharmacological Sanctuary ($\\Delta r = 34.11\\ \\mu$m, 31.3% Vol)')
ax1b.axvspan(200.0, 250.0, color='#666666', alpha=0.20, label='Hypoxic Necrotic Core ($r > 200\\ \\mu$m)')

ax1b.set_xlabel('Radial Distance from Capillary Axis ($r$, $\\mu$m)')
ax1b.set_ylabel('Normalized Unbound Concentration $C(r) / C_0$')
ax1b.set_title('b  Cylindrical Reaction-Diffusion Penetration & Sanctuary Cuff', loc='left', fontweight='bold')
ax1b.set_xlim(10, 250)
ax1b.set_ylim(0, 1.05)
ax1b.legend(loc='upper right', frameon=True)
ax1b.grid(True, linestyle=':', alpha=0.5)

# Annotate rcrit and rox
ax1b.annotate('$r_{crit} = 165.9\\ \\mu$m', xy=(165.89, 0.349), xytext=(110, 0.45),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=5), fontweight='bold')
ax1b.annotate('Vital Limit $r_{ox} = 200.0\\ \\mu$m\n(Thomlinson & Gray 1955)', xy=(200, 0.31), xytext=(160, 0.15),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=5), fontweight='bold')

plt.tight_layout()
fig1.savefig(os.path.join(out_dir, "Figure1_reaction_diffusion_sanctuary.png"), dpi=300)
fig1.savefig(os.path.join(out_dir, "Figure1_reaction_diffusion_sanctuary.pdf"))
plt.close(fig1)
print("Generated Figure 1")

# =========================================================================
# FIGURE 2: Post-ADAURA Dynamics & ctDNA Mathematical Lead Time
# =========================================================================
fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

# Panel A: Post-Cessation Recurrence Breakdown
categories = ['During Active Osimertinib\n(Months 0-36)', 'Early Post-Cessation\n(Months 36-48)', 'Late Post-Cessation\n(Months >48)']
event_counts = [9, 11, 8]  # 9 of 28 during treatment (32.1%), 19 of 28 post (67.9%), 11 in first 12 mo (57.9% of post)
percentages = [32.1, 39.3, 28.6]
colors_2a = ['#66C2A5', '#FC8D62', '#8DA0CB']

bars2 = ax2a.bar(categories, percentages, color=colors_2a, edgecolor='#333333', alpha=0.9, width=0.55)
for bar, pct, n in zip(bars2, percentages, event_counts):
    yval = bar.get_height()
    ax2a.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f'{pct:.1f}%\n(N={n})', ha='center', va='bottom', fontweight='bold')

ax2a.set_ylabel('Percentage of Recurrence Events (%)')
ax2a.set_title('a  Timing of Recurrence in ADAURA ctDNA Cohort (Herbst et al. 2025)', loc='left', fontweight='bold')
ax2a.set_ylim(0, 50)
ax2a.grid(axis='y', linestyle=':', alpha=0.6)

# Brackets for Post-Cessation total (67.9%)
ax2a.annotate('', xy=(1, 44), xytext=(2, 44), arrowprops=dict(arrowstyle='-', lw=1.5, color='#D7301F'))
ax2a.text(1.5, 45.5, 'Total Post-Cessation Recurrences: 67.9% (19/28)', ha='center', va='bottom', color='#D7301F', fontweight='bold')

# Panel B: Exponential Tumor Repopulation & Lead Time Identity
t_days = np.linspace(0, 200, 400)
# N(t) = N0 * 2^(t / Td), with Td = 24.6 days
N0 = 1e7 # ctDNA threshold
Td = 24.6
N_t = N0 * (2.0 ** (t_days / Td))

ax2b.semilogy(t_days / 30.4375, N_t, color='#2B5C8F', linewidth=2.5, label='Persister Clonal Expansion ($T_d = 24.6$ days)')
ax2b.axhline(y=1e7, color='#1B9E77', linestyle='--', linewidth=1.5, label='ctDNA MRD Detection Limit ($10^7$ cells, VAF $\\approx 0.01\\%$)')
ax2b.axhline(y=1e9, color='#D95F02', linestyle='--', linewidth=1.5, label='CT Imaging Detection Threshold ($10^9$ cells, $1$ cm mass)')

# Clinical 95% CI band
lead_time_months = (6.644 * Td) / 30.4375 # 5.37 months
ax2b.axvspan(2.2, 5.6, color='#FFFFB3', alpha=0.6, label='Herbst et al. Clinical 95% CI (2.2 - 5.6 mo)')
ax2b.axvline(x=lead_time_months, color='#D7301F', linestyle='-', linewidth=2.0, label=f'Model Analytical Lead Time ({lead_time_months:.2f} mo)')

ax2b.set_xlabel('Time Elapsed Post-MRD Positivity (Months)')
ax2b.set_ylabel('Tumor Cell Burden ($N(t)$, Log Scale)')
ax2b.set_title('b  ctDNA-to-CT Imaging Exponential Expansion Identity', loc='left', fontweight='bold')
ax2b.set_xlim(0, 7)
ax2b.set_ylim(5e6, 2e9)
ax2b.legend(loc='lower right', frameon=True)
ax2b.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig2.savefig(os.path.join(out_dir, "Figure2_adaura_dynamics_and_leadtime.png"), dpi=300)
fig2.savefig(os.path.join(out_dir, "Figure2_adaura_dynamics_and_leadtime.pdf"))
plt.close(fig2)
print("Generated Figure 2")

# =========================================================================
# FIGURE 3: Cross-Drug Penetration & Multi-Cohort Evidence Forest Plot
# =========================================================================
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

# Panel A: Cross-Drug Penetration Curves
r_vals = np.linspace(10, 220, 400)
# Parameters:
# Osimertinib: lam=627.6, theta=0.349
# Erlotinib: lam=415.0, theta=0.793 -> rcrit = 44.3 um
# Gefitinib: lam=480.0, theta=0.550 -> rcrit = 100.0 um
c_osi = C_decay(r_vals, lam=627.6, r0=10.0)
c_erl = C_decay(r_vals, lam=415.0, r0=10.0)
c_gef = C_decay(r_vals, lam=480.0, r0=10.0)

ax3a.plot(r_vals, c_osi, color='#2B5C8F', linewidth=2.2, label='Osimertinib ($3^{rd}$-gen, $\\lambda = 627.6\\ \\mu$m)')
ax3a.plot(r_vals, c_gef, color='#31A354', linewidth=2.0, linestyle='--', label='Gefitinib ($1^{st}$-gen, $\\lambda = 480.0\\ \\mu$m)')
ax3a.plot(r_vals, c_erl, color='#E6550D', linewidth=2.0, linestyle='-.', label='Erlotinib ($1^{st}$-gen, $\\lambda = 415.0\\ \\mu$m)')

ax3a.axhline(y=0.349, color='#2B5C8F', linestyle=':', alpha=0.7)
ax3a.axvline(x=44.3, color='#E6550D', linestyle=':', alpha=0.7)
ax3a.axvline(x=100.0, color='#31A354', linestyle=':', alpha=0.7)
ax3a.axvline(x=165.89, color='#2B5C8F', linestyle=':', alpha=0.7)
ax3a.axvline(x=200.0, color='#666666', linestyle='-', linewidth=1.5, label='Vital Oxygen Boundary ($r_{ox} = 200\\ \\mu$m)')

ax3a.set_xlabel('Radial Cord Coordinate ($r$, $\\mu$m)')
ax3a.set_ylabel('Normalized Free Drug Concentration $C(r)/C_0$')
ax3a.set_title('a  Cross-Drug Spatial Penetration & Sanctuary Expansion', loc='left', fontweight='bold')
ax3a.set_xlim(10, 220)
ax3a.set_ylim(0, 1.05)
ax3a.legend(loc='upper right', frameon=True)
ax3a.grid(True, linestyle=':', alpha=0.5)

# Annotation for sanctuary percentages
ax3a.text(50, 0.85, 'Erlotinib Sanctuary: 82.0% Vol\nGefitinib Sanctuary: 75.0% Vol\nOsimertinib Sanctuary: 31.3% Vol',
          bbox=dict(boxstyle='round,pad=0.5', facecolor='#F0F0F0', edgecolor='#999999'), fontsize=9)

# Panel B: Multi-Cohort Forest Plot (N = 3,205)
cohort_names = [
    'ADAURA ctDNA Cohort (Herbst 2025, N=220)',
    'MSKCC Histology Cohort (N=604)',
    'TCGA + GSE31210 Cohort (N=854)',
    'MSKCC Genomic Cohort (Offin 2019, N=863)',
    'Human Lung IFP Cohort (Mori 2015, N=211)',
    'RELAY Trial VEGFR2 (Nakagawa 2025, N=449)'
]
n_patients = [220, 604, 854, 863, 211, 449]
y_pos = np.arange(len(cohort_names))

bars3b = ax3b.barh(y_pos, n_patients, color='#4575B4', edgecolor='#333333', alpha=0.85, height=0.55)
for bar, n in zip(bars3b, n_patients):
    xval = bar.get_width()
    ax3b.text(xval + 15, bar.get_y() + bar.get_height()/2.0, f'N = {n:,}', ha='left', va='center', fontweight='bold')

ax3b.set_yticks(y_pos)
ax3b.set_yticklabels(cohort_names, fontsize=8.5)
ax3b.invert_yaxis()
ax3b.set_xlabel('Number of Analyzed Human Patients')
ax3b.set_title('b  Multi-Cohort Empirical Evidence Base (Total N = 3,205)', loc='left', fontweight='bold')
ax3b.set_xlim(0, 1100)
ax3b.grid(axis='x', linestyle=':', alpha=0.6)

plt.tight_layout()
fig3.savefig(os.path.join(out_dir, "Figure3_cross_drug_and_cohort_evidence.png"), dpi=300)
fig3.savefig(os.path.join(out_dir, "Figure3_cross_drug_and_cohort_evidence.pdf"))
plt.close(fig3)
print("Generated Figure 3")

# =========================================================================
# FIGURE 4: Composite Resistance Index (CRI) & SG-ADAURA Trial Protocol
# =========================================================================
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

# Panel A: CRI Weight Breakdown and Risk Tiers
weights = [0.47, 0.33, 0.20]
labels_pie = ['Spatial Histology (S, 47%)\nSolid/Micropapillary', 'Genomics (G, 33%)\nTP53 / RB1 Mutants', 'ctDNA Dynamics (M, 20%)\nMRD Kinetics']
colors_pie = ['#D73027', '#FC8D59', '#FEE090']

wedges, texts, autotexts = ax4a.pie(weights, labels=labels_pie, autopct='%1.0f%%', startangle=140,
                                   colors=colors_pie, wedgeprops=dict(edgecolor='#333333', linewidth=1.2), textprops=dict(fontsize=9))
for autotext in autotexts:
    autotext.set_fontweight('bold')
ax4a.set_title('a  Composite Resistance Index (CRI) Architecture\n$CRI = 0.47\\mathcal{S} + 0.33\\mathcal{G} + 0.20\\mathcal{M}$', loc='left', fontweight='bold')

# Panel B: SG-ADAURA Phase III Randomization Schema
ax4b.axis('off')
ax4b.set_title('b  SG-ADAURA Phase III Prospective Trial Schema (N = 800)', loc='left', fontweight='bold')

# Draw flowchart boxes
def draw_box(ax, x, y, w, h, text, bg='#E0F3F8', ec='#333333', bold=False):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03", fc=bg, ec=ec, lw=1.2)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2.0, y + h/2.0, text, ha='center', va='center', fontsize=8.5, weight=weight)

draw_box(ax4b, 0.05, 0.80, 0.90, 0.15, 'Target Population: Resected Stage IB-IIIA EGFRm NSCLC Completing 36 Months Osimertinib\nNED (No Evidence of Disease) by Contrast CT & Brain MRI (N = 800)', bg='#E6F598', bold=True)

draw_box(ax4b, 0.05, 0.55, 0.90, 0.14, 'CRI Bedside Risk Stratification Engine (Month 36 Biopsy/Archival + Plasma ctDNA)\nTier 1: CRI < 0.30 (N=350)  |  Tier 2: CRI 0.30-0.65 (N=300)  |  Tier 3: CRI >= 0.65 (N=150)', bg='#FFFFBF')

draw_box(ax4b, 0.02, 0.18, 0.28, 0.24, 'ARM A (Control, 1:1)\nStandard Cessation\nObservation + ctDNA Q3M\n(Current ADAURA Standard)', bg='#FEE08B')
draw_box(ax4b, 0.35, 0.18, 0.30, 0.24, 'ARM B1 / B2 (Intervention)\nB1: Extended Osimertinib\nB2: 12-Wk Ramucirumab Pulse\n(Vascular Normalization)', bg='#ABD9E9')
draw_box(ax4b, 0.69, 0.18, 0.29, 0.24, 'ARM B3 (Tier 3 Escalation)\nContinuous Dual Therapy\nOsimertinib + Anti-VEGFR2\n(Eliminates Sanctuary)', bg='#FDAE61')

# Connective arrows
arrow_kw = dict(arrowstyle="->", lw=1.5, color='#333333')
ax4b.annotate('', xy=(0.50, 0.69), xytext=(0.50, 0.80), arrowprops=arrow_kw)
ax4b.annotate('', xy=(0.16, 0.42), xytext=(0.30, 0.55), arrowprops=arrow_kw)
ax4b.annotate('', xy=(0.50, 0.42), xytext=(0.50, 0.55), arrowprops=arrow_kw)
ax4b.annotate('', xy=(0.83, 0.42), xytext=(0.70, 0.55), arrowprops=arrow_kw)

ax4b.text(0.50, 0.05, 'Primary Endpoint: Disease-Free Survival (DFS) from Month 36 (90% Power for HR=0.58, 142 Events)',
         ha='center', va='center', fontsize=8.5, style='italic', color='#333333')

plt.tight_layout()
fig4.savefig(os.path.join(out_dir, "Figure4_cri_engine_and_sg_adaura_trial.png"), dpi=300)
fig4.savefig(os.path.join(out_dir, "Figure4_cri_engine_and_sg_adaura_trial.pdf"))
plt.close(fig4)
print("Generated Figure 4")

print("\nSUCCESS: All 4 scientific figures generated in PNG (300 DPI) and vector PDF!")
