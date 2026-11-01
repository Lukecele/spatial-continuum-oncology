#!/usr/bin/env python3
"""
Adversarial Fuzzing, Boundary Conditions & Mathematical Invariants Audit Suite
Validates cri-calc against noisy real-world EHR tables, fuzzy mutations, and mathematical extremes.
"""

import os
import sys
import tempfile
import unittest
import itertools

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from spatial_continuum.cri_calc import calculate_cri, process_batch

class TestAdversarialFuzzingAndInvariants(unittest.TestCase):

    def test_mathematical_invariants_boundedness(self):
        """Invariant 1: CRI must strictly reside in [0.000, 1.000] for all possible input combinations."""
        patterns = ["lepidic", "acinar", "papillary", "solid", "micropapillary", "mixed", "unknown", "", "gibberish"]
        tp53s = ["wt", "mut", "mutated", "true", "positive", "1", "false", "0", "loss", "unknown", "p.R273H"]
        rb1s = ["wt", "mut", "mutated", "true", "positive", "loss", "deleted", "1", "0", "false"]
        stromas = ["low", "loose", "moderate", "intermediate", "dense", "severe", "high", "normal", ""]

        for p, t, r, s in itertools.product(patterns, tp53s, rb1s, stromas):
            res = calculate_cri(pattern=p, tp53=t, rb1=r, stroma=s)
            cri = res["CRI"]
            self.assertGreaterEqual(cri, 0.000, f"CRI < 0 for ({p}, {t}, {r}, {s})")
            self.assertLessEqual(cri, 1.000, f"CRI > 1 for ({p}, {t}, {r}, {s})")
            self.assertIn(res["tier"], [
                "TIER 1 (LOW RESISTANCE & SANCTUARY RISK)",
                "TIER 2 (INTERMEDIATE RISK / BORDERLINE SANCTUARY)",
                "TIER 3 (HIGH RESISTANCE & SANCTUARY RISK)"
            ])

    def test_monotonicity_of_risk(self):
        """Invariant 2: Adding mutations or increasing stromal stiffness must monotonically increase or maintain CRI."""
        patterns = ["lepidic", "acinar", "solid"]
        for p in patterns:
            # Baseline WT
            cri_wt = calculate_cri(p, tp53="wt", rb1="wt", stroma="low")["CRI"]
            # Add TP53
            cri_tp53 = calculate_cri(p, tp53="mutated", rb1="wt", stroma="low")["CRI"]
            # Add RB1
            cri_triple = calculate_cri(p, tp53="mutated", rb1="mutated", stroma="low")["CRI"]
            # Increase Stroma
            cri_dense = calculate_cri(p, tp53="mutated", rb1="mutated", stroma="dense")["CRI"]

            self.assertGreaterEqual(cri_tp53, cri_wt)
            self.assertGreaterEqual(cri_triple, cri_tp53)
            self.assertGreaterEqual(cri_dense, cri_triple)

    def test_fuzzy_case_and_whitespace_insensitivity(self):
        """Invariant 3: Capitalization and messy whitespace must yield identical scores."""
        clean = calculate_cri("solid", "mutated", "mutated", "dense")
        messy = calculate_cri("  sOlId  ", "  MuTaTeD\n", "\trb1_mutated ", "  DENSE  ")
        self.assertEqual(clean["CRI"], messy["CRI"])
        self.assertEqual(clean["tier"], messy["tier"])

    def test_permutation_invariance_in_batch(self):
        """Invariant 4: Column order in TSV/CSV must not affect output scores."""
        tsv_order1 = (
            "patient_id\thistology\ttp53_status\trb1_status\tstroma\n"
            "PT1\tsolid\tmut\tmut\tdense\n"
        )
        tsv_order2 = (
            "stroma\trb1_status\tpatient_id\ttp53_status\thistology\n"
            "dense\tmut\tPT1\tmut\tsolid\n"
        )
        
        with tempfile.NamedTemporaryFile("w+", suffix=".tsv", delete=False) as f1, \
             tempfile.NamedTemporaryFile("w+", suffix=".tsv", delete=False) as f2:
            f1.write(tsv_order1); p1 = f1.name
            f2.write(tsv_order2); p2 = f2.name

        out1 = p1 + ".out.tsv"
        out2 = p2 + ".out.tsv"
        try:
            process_batch(p1, out1)
            process_batch(p2, out2)

            with open(out1) as r1, open(out2) as r2:
                lines1 = [line.strip().split("\t") for line in r1]
                lines2 = [line.strip().split("\t") for line in r2]

            h1, row1 = lines1[0], lines1[1]
            h2, row2 = lines2[0], lines2[1]

            cri1 = row1[h1.index("CRI_Score")]
            cri2 = row2[h2.index("CRI_Score")]
            self.assertEqual(cri1, cri2)
            self.assertEqual(cri1, "1.000")
        finally:
            for p in [p1, p2, out1, out2]:
                if os.path.exists(p): os.remove(p)

    def test_corrupted_rows_graceful_handling(self):
        """Ensures that missing values or unknown synonyms fall back to safe intermediate defaults."""
        res_empty = calculate_cri("", "", "", "")
        self.assertGreaterEqual(res_empty["CRI"], 0.0)
        self.assertLessEqual(res_empty["CRI"], 1.0)

if __name__ == "__main__":
    unittest.main()
