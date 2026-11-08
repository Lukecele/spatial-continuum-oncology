#!/usr/bin/env python3
"""
Unit tests for cri-calc: Single-Patient and High-Throughput Batch Processing.
"""

import os
import tempfile
import unittest

from spatial_continuum.cri_calc import calculate_cri, process_batch


class TestCRICalculator(unittest.TestCase):

    def test_single_patient_lepidic_wt(self):
        res = calculate_cri(pattern="lepidic", tp53="wt", rb1="wt", stroma="low")
        self.assertEqual(res["S"], 0.0)
        self.assertEqual(res["G"], 0.0)
        self.assertEqual(res["M"], 0.0)
        self.assertEqual(res["CRI"], 0.0)
        self.assertIn("TIER 1", res["tier"])
        self.assertIn("mantle absent", res["action"])

    def test_single_patient_solid_triple_dense(self):
        res = calculate_cri(pattern="solid", tp53="mut", rb1="mut", stroma="dense")
        self.assertEqual(res["S"], 1.0)
        self.assertEqual(res["G"], 1.0)
        self.assertEqual(res["M"], 1.0)
        self.assertEqual(res["CRI"], 1.0)
        self.assertIn("TIER 3", res["tier"])
        self.assertIn("Substantial perivascular mantle", res["action"])

    def test_single_patient_acinar_intermediate(self):
        res = calculate_cri(pattern="acinar", tp53="mut", rb1="wt", stroma="moderate")
        # S=0.40, G=0.50, M=0.50 -> CRI = 0.47*0.4 + 0.33*0.5 + 0.20*0.5 = 0.188 + 0.165 + 0.100 = 0.453
        self.assertAlmostEqual(res["CRI"], 0.453, places=2)
        self.assertIn("TIER 2", res["tier"])

    def test_batch_processing_tsv(self):
        input_data = (
            "patient_id\thistology\ttp53_status\trb1_status\tstroma\n"
            "PT_001\tlepidic\twt\twt\tlow\n"
            "PT_002\tsolid\tmutated\tmutated\tdense\n"
            "PT_003\tacinar\tmutated\twt\tmoderate\n"
        )
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".tsv") as tf_in:
            tf_in.write(input_data)
            tf_in_path = tf_in.name

        tf_out_path = tf_in_path + ".out.tsv"

        try:
            process_batch(tf_in_path, tf_out_path, delimiter="\t")
            with open(tf_out_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.assertEqual(len(lines), 4)  # Header + 3 patients
            header = lines[0].strip().split("\t")
            self.assertIn("CRI_Score", header)
            self.assertIn("Risk_Tier", header)
            self.assertIn("Actionable_Recommendation", header)

            pt1 = lines[1].strip().split("\t")
            cri_idx = header.index("CRI_Score")
            tier_idx = header.index("Risk_Tier")
            self.assertEqual(pt1[cri_idx], "0.000")
            self.assertIn("TIER 1", pt1[tier_idx])

            pt2 = lines[2].strip().split("\t")
            self.assertEqual(pt2[cri_idx], "1.000")
            self.assertIn("TIER 3", pt2[tier_idx])

        finally:
            if os.path.exists(tf_in_path):
                os.remove(tf_in_path)
            if os.path.exists(tf_out_path):
                os.remove(tf_out_path)

    def test_batch_processing_csv(self):
        input_data = (
            "case_id,pattern,tp53,rb1,stroma\n"
            "CASE_A,micropapillary,mut,loss,high\n"
            "CASE_B,papillary,wt,wt,loose\n"
        )
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tf_in:
            tf_in.write(input_data)
            tf_in_path = tf_in.name

        tf_out_path = tf_in_path + ".out.csv"

        try:
            process_batch(tf_in_path, tf_out_path)
            with open(tf_out_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.assertEqual(len(lines), 3)  # Header + 2 cases
            self.assertIn("CRI_Score", lines[0])
            self.assertIn("TIER 3", lines[1])
            self.assertIn("TIER 1", lines[2])
        finally:
            if os.path.exists(tf_in_path):
                os.remove(tf_in_path)
            if os.path.exists(tf_out_path):
                os.remove(tf_out_path)

    def test_custom_weights_and_cutoffs(self):
        # S=1.0, G=0.0, M=0.0
        # Default weights: 0.47*1.0 = 0.47 -> TIER 2 (0.30 <= CRI <= 0.65)
        # Custom weights: w_spatial=0.80, w_genomic=0.10, w_stromal=0.10 -> CRI = 0.80 -> TIER 3
        res = calculate_cri(
            pattern="solid", tp53="wt", rb1="wt", stroma="low",
            w_spatial=0.80, w_genomic=0.10, w_stromal=0.10,
            cutoff_low=0.25, cutoff_high=0.75
        )
        self.assertAlmostEqual(res["CRI"], 0.80, places=2)
        self.assertIn("TIER 3", res["tier"])
        self.assertGreater(res["sanctuary_depth_um"], 0.0)
        self.assertLess(res["concentration_ratio"], 1.0)

    def test_biophysical_sanctuary_metrics(self):
        res = calculate_cri(
            pattern="solid", tp53="mut", rb1="mut", stroma="dense",
            lambda_pen=34.1, r_vessel=8.0
        )
        self.assertIn("sanctuary_depth_um", res)
        self.assertIn("concentration_ratio", res)
        self.assertIn("bio_summary", res)
        self.assertAlmostEqual(res["sanctuary_depth_um"], 57.9, delta=0.5)
        self.assertAlmostEqual(res["concentration_ratio"], 0.022, places=3)


if __name__ == "__main__":
    unittest.main()
