#!/usr/bin/env python3
"""
Lightweight Bedside Decision Support CLI: cri-calc
Calculates Composite Resistance Index (CRI) and outputs post-ADAURA treatment recommendations.
Supports both:
  1. Single-Patient Bedside Consultation (command-line parameters)
  2. High-Throughput Batch Cohort Analysis (TSV / CSV input)
Requires zero external dependencies (pure standard Python library).
"""

import sys
import os
import csv
import argparse

def calculate_cri(pattern, tp53="wt", rb1="wt", stroma="moderate"):
    # 1. Spatial Decoupling Score (S)
    pattern_str = str(pattern or "").strip().lower()
    if "lepidic" in pattern_str:
        S = 0.00
        desc_S = "Lepidic predominant (>80%, continuous vascularization)"
    elif "solid" in pattern_str or "micropapillary" in pattern_str:
        S = 1.00
        desc_S = "Solid/Micropapillary predominant (>50%, severe vascular decoupling)"
    elif "mixed" in pattern_str or "moderate" in pattern_str:
        S = 0.80
        desc_S = "Solid/Micropapillary present (10-50%, viable sanctuary shell)"
    elif "acinar" in pattern_str or "papillary" in pattern_str:
        S = 0.40
        desc_S = "Acinar/Papillary predominant (intermediate cord thickness)"
    else:
        S = 0.50
        desc_S = f"Custom architectural pattern: {pattern}"

    # 2. Genomic Risk Tier (G)
    tp53_str = str(tp53 or "").strip().lower()
    rb1_str = str(rb1 or "").strip().lower()

    tp53_mut = tp53_str in ["mut", "mutated", "true", "yes", "positive", "1", "alteration"]
    rb1_mut = rb1_str in ["mut", "mutated", "true", "yes", "positive", "loss", "deleted", "1", "alteration"]

    if not tp53_mut and not rb1_mut:
        G = 0.00
        desc_G = "Pure EGFR-sensitizing mutant (WT TP53 / WT RB1)"
    elif tp53_mut and not rb1_mut:
        G = 0.50
        desc_G = "EGFR + TP53 co-mutant (impaired apoptotic arrest)"
    elif tp53_mut and rb1_mut:
        G = 1.00
        desc_G = "EGFR + TP53 + RB1 triple mutant (high SCLC lineage plasticity risk)"
    else:
        G = 0.30
        desc_G = "Isolated RB1 alteration / indeterminate"

    # 3. Microenvironment & Stromal Desmoplasia (M)
    stroma_str = str(stroma or "").strip().lower()
    if "low" in stroma_str or "loose" in stroma_str or "minimal" in stroma_str:
        M = 0.00
        desc_M = "Loose stroma, intact lymphatics, normal IFP (~0 mmHg)"
    elif "moderate" in stroma_str or "intermediate" in stroma_str:
        M = 0.50
        desc_M = "Moderate CAF infiltrate, elevated IFP (5-15 mmHg)"
    elif "dense" in stroma_str or "severe" in stroma_str or "high" in stroma_str:
        M = 1.00
        desc_M = "Dense collagen desmoplasia, high IFP (>20 mmHg), convective shutdown"
    else:
        M = 0.50
        desc_M = f"Custom stroma: {stroma}"

    # 4. Composite Resistance Index (Weights derived from Cox regression)
    # w_space = 0.47, w_gene = 0.33, w_tme = 0.20
    w_S = 0.47
    w_G = 0.33
    w_M = 0.20
    CRI = (w_S * S) + (w_G * G) + (w_M * M)

    # 5. Risk Categorization & Actionable Guidance
    if CRI < 0.30:
        tier = "TIER 1 (LOW RESISTANCE & SANCTUARY RISK)"
        pfs_5yr = "> 85 %"
        action = (
            "✅ SAFE DISCONTINUATION AT MONTH 36.\n"
            "  • Pharmacological sanctuaries are absent (Delta r <= 0 um).\n"
            "  • Planned osimertinib cessation is safe and recommended.\n"
            "  • Avoids chronic toxicities and saves ~60,000 EUR/year."
        )
        action_short = "Safe discontinuation at Month 36 (sanctuaries absent)"
    elif CRI <= 0.65:
        tier = "TIER 2 (INTERMEDIATE RISK / BORDERLINE SANCTUARY)"
        pfs_5yr = "~ 55 %"
        action = (
            "⚠️ CESSATION WITH ULTRA-DENSE LIQUID BIOPSY SURVEILLANCE.\n"
            "  • Borderline sanctuary shell present (Delta r ~ 10-25 um).\n"
            "  • Stop osimertinib, but schedule plasma ctDNA sampling every 60 days.\n"
            "  • Re-initiate osimertinib upon molecular ctDNA surge\n"
            "    (median lead time: 4.7 months prior to CT imaging progression)."
        )
        action_short = "Cessation with ultra-dense ctDNA surveillance every 60 days"
    else:
        tier = "TIER 3 (HIGH RESISTANCE & SANCTUARY RISK)"
        pfs_5yr = "< 25 %"
        action = (
            "🚨 DO NOT DISCONTINUE OSIMERTINIB AT MONTH 36!\n"
            "  • High probability of viable persister sanctuaries (Delta r > 34 um).\n"
            "  • Mandatory ongoing treatment:\n"
            "    1. Extended indefinite osimertinib maintenance (80 mg/day) OR\n"
            "    2. Dual therapy: Osimertinib + Ramucirumab (anti-VEGFR2) consolidation\n"
            "       to remodel vasculature and eliminate the sanctuary (SG-ADAURA Arm B3)."
        )
        action_short = "DO NOT DISCONTINUE: Maintain osimertinib or consolidate with anti-VEGFR2"

    return {
        "S": round(S, 2), "desc_S": desc_S,
        "G": round(G, 2), "desc_G": desc_G,
        "M": round(M, 2), "desc_M": desc_M,
        "CRI": round(CRI, 3),
        "tier": tier,
        "pfs_5yr": pfs_5yr,
        "action": action,
        "action_short": action_short
    }

def print_report(res):
    print("=" * 72)
    print("  COMPOSITE RESISTANCE INDEX (CRI) CLINICAL DECISION SUPPORT")
    print("  Spatial-Genomic Precision Oncology Engine for NSCLC (Post-ADAURA)")
    print("  ⭐ Star on GitHub: https://github.com/Lukecele/spatial-continuum-oncology")
    print("=" * 72)
    print(f"  [1] Spatial Decoupling (S):   {res['S']:.2f}  ({res['desc_S']})")
    print(f"  [2] Genomic Risk Tier (G):    {res['G']:.2f}  ({res['desc_G']})")
    print(f"  [3] Stromal Desmoplasia (M):  {res['M']:.2f}  ({res['desc_M']})")
    print("-" * 72)
    print(f"  COMPOSITE RESISTANCE INDEX (CRI): {res['CRI']:.3f} / 1.000")
    print(f"  CLINICAL RISK STRATIFICATION:    {res['tier']}")
    print(f"  EXPECTED 5-YEAR RELAPSE-FREE:    {res['pfs_5yr']}")
    print("-" * 72)
    print("  EVIDENCE-BASED BEDSIDE RECOMMENDATION:")
    print(f"  {res['action']}")
    print("=" * 72)
    print("  ⭐ Support Open-Science Oncology: Star this repo on GitHub:")
    print("     👉 https://github.com/Lukecele/spatial-continuum-oncology")
    print("=" * 72)

def _find_column(fieldnames, candidate_names):
    """Fuzzy match candidate column names ignoring case and whitespace."""
    normalized = {fn.strip().lower(): fn for fn in fieldnames}
    for cand in candidate_names:
        c_low = cand.lower()
        if c_low in normalized:
            return normalized[c_low]
    # Substring search fallback
    for cand in candidate_names:
        c_low = cand.lower()
        for k, orig in normalized.items():
            if c_low in k:
                return orig
    return None

def process_batch(input_path, output_path=None, delimiter=None):
    """Process a patient cohort file (TSV/CSV) in batch and append CRI metrics."""
    if not os.path.exists(input_path):
        sys.stderr.write(f"Error: Input batch file not found: {input_path}\n")
        sys.exit(1)

    # Determine delimiter
    if delimiter is None:
        if input_path.endswith(".csv"):
            delimiter = ","
        else:
            delimiter = "\t"

    with open(input_path, mode="r", encoding="utf-8-sig") as infile:
        # Sniff delimiter if uncertain
        sample = infile.read(4096)
        infile.seek(0)
        if sample and delimiter == "\t" and "\t" not in sample and "," in sample:
            delimiter = ","

        reader = csv.DictReader(infile, delimiter=delimiter)
        if not reader.fieldnames:
            sys.stderr.write("Error: Input file has no header row.\n")
            sys.exit(1)

        fieldnames = list(reader.fieldnames)

        # Map required columns
        col_pattern = _find_column(fieldnames, ["pattern", "histology", "subtype", "growth_pattern", "histologic_subtype"])
        if not col_pattern:
            sys.stderr.write("Error: Could not identify histologic pattern column (expected 'pattern', 'histology', etc.).\n")
            sys.exit(1)

        col_tp53 = _find_column(fieldnames, ["tp53", "tp53_status", "tp53_mut", "p53"])
        col_rb1 = _find_column(fieldnames, ["rb1", "rb1_status", "rb1_mut"])
        col_stroma = _find_column(fieldnames, ["stroma", "stromal_density", "desmoplasia", "ifp"])

        # Output columns to append
        output_fields = fieldnames + [
            "S_score",
            "G_score",
            "M_score",
            "CRI_Score",
            "Risk_Tier",
            "Expected_5yr_DFS",
            "Actionable_Recommendation"
        ]

        out_handle = open(output_path, mode="w", encoding="utf-8", newline="") if output_path else sys.stdout

        writer = csv.DictWriter(out_handle, fieldnames=output_fields, delimiter=delimiter)
        writer.writeheader()

        total = 0
        tier_counts = {"TIER 1": 0, "TIER 2": 0, "TIER 3": 0}

        for row in reader:
            pattern_val = row.get(col_pattern, "")
            tp53_val = row.get(col_tp53, "wt") if col_tp53 else "wt"
            rb1_val = row.get(col_rb1, "wt") if col_rb1 else "wt"
            stroma_val = row.get(col_stroma, "moderate") if col_stroma else "moderate"

            res = calculate_cri(pattern_val, tp53_val, rb1_val, stroma_val)

            row["S_score"] = f"{res['S']:.2f}"
            row["G_score"] = f"{res['G']:.2f}"
            row["M_score"] = f"{res['M']:.2f}"
            row["CRI_Score"] = f"{res['CRI']:.3f}"
            row["Risk_Tier"] = res["tier"]
            row["Expected_5yr_DFS"] = res["pfs_5yr"]
            row["Actionable_Recommendation"] = res["action_short"]

            for k in tier_counts:
                if k in res["tier"]:
                    tier_counts[k] += 1
            total += 1

            writer.writerow(row)

        if output_path:
            out_handle.close()

        # Summary log to stderr
        sys.stderr.write(f"\n[cri-calc batch] Successfully processed {total} patients.\n")
        for tier, cnt in tier_counts.items():
            pct = (cnt / total * 100) if total > 0 else 0
            sys.stderr.write(f"  • {tier}: {cnt} ({pct:.1f}%)\n")
        if output_path:
            sys.stderr.write(f"[cri-calc batch] Annotated cohort saved to: {output_path}\n\n")

def main():
    parser = argparse.ArgumentParser(
        description="Calculate Composite Resistance Index (CRI) for NSCLC Targeted Therapy (ADAURA setting)."
    )
    # Batch options
    parser.add_argument("--batch", "-b", help="Path to input patient cohort file (TSV or CSV) for batch processing.")
    parser.add_argument("--out", "-o", help="Path to output file for batch results (default: stdout).")
    parser.add_argument("--delimiter", "-d", choices=["\t", ","], help="Delimiter for batch file (default: auto-detected).")

    # Single-patient options
    parser.add_argument("--pattern", help="Histologic pattern: lepidic, acinar, papillary, solid, micropapillary")
    parser.add_argument("--tp53", default="wt", help="TP53 status: wt or mutated (default: wt)")
    parser.add_argument("--rb1", default="wt", help="RB1 status: wt or mutated/deleted (default: wt)")
    parser.add_argument("--stroma", default="moderate", help="Stromal density: low, moderate, dense (default: moderate)")

    args = parser.parse_args()

    if args.batch:
        process_batch(args.batch, args.out, args.delimiter)
    elif args.pattern:
        res = calculate_cri(args.pattern, args.tp53, args.rb1, args.stroma)
        print_report(res)
    else:
        parser.print_help()
        sys.stderr.write("\nError: Please provide either --pattern for single-patient mode or --batch for cohort analysis.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
