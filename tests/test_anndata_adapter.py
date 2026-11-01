"""
Unit tests for scverse AnnData interoperability adapter.
Verifies bidirectional conversion, feature matrix X, observation metadata obs,
spatial coordinates obsm['spatial'], and biophysical transport metadata uns.
"""

import os
import unittest
import tempfile
import csv

from spatial_continuum import (
    to_anndata,
    annotate_anndata,
    from_anndata,
    calculate_cri,
    BESSEL_TRANSPORT_METRICS,
    SCIENTIFIC_ANCHORS,
)


class TestAnnDataAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import anndata
            import pandas
            import numpy
            cls.has_deps = True
        except ImportError:
            cls.has_deps = False

    def setUp(self):
        if not self.has_deps:
            self.skipTest("anndata/pandas/numpy not available in current environment")

    def test_to_anndata_from_dict_list(self):
        records = [
            {
                "patient_id": "P001",
                "histology_pattern": "Lepidic",
                "tp53_status": "wt",
                "rb1_status": "wt",
                "stromal_grade": "loose",
                "spatial_x": 120.5,
                "spatial_y": 340.2,
            },
            {
                "patient_id": "P002",
                "histology_pattern": "Solid",
                "tp53_status": "mut",
                "rb1_status": "mut",
                "stromal_grade": "dense",
                "spatial_x": 450.0,
                "spatial_y": 780.0,
            },
            {
                "patient_id": "P003",
                "histology_pattern": "Acinar",
                "tp53_status": "mut",
                "rb1_status": "wt",
                "stromal_grade": "moderate",
                "spatial_x": 210.0,
                "spatial_y": 550.0,
            },
        ]

        adata = to_anndata(records)

        # 1. Dimensions check
        self.assertEqual(adata.n_obs, 3)
        self.assertEqual(adata.n_vars, 4)
        self.assertEqual(list(adata.obs_names), ["P001", "P002", "P003"])

        # 2. X feature matrix check [S, G, M, CRI]
        # P001: Lepidic(0.0), WT(0.0), Loose(0.0) -> CRI = 0.0
        self.assertAlmostEqual(float(adata.X[0, 0]), 0.00, places=2)
        self.assertAlmostEqual(float(adata.X[0, 1]), 0.00, places=2)
        self.assertAlmostEqual(float(adata.X[0, 2]), 0.00, places=2)
        self.assertAlmostEqual(float(adata.X[0, 3]), 0.00, places=2)

        # P002: Solid(1.0), Triple(1.0), Dense(1.0) -> CRI = 1.0
        self.assertAlmostEqual(float(adata.X[1, 0]), 1.00, places=2)
        self.assertAlmostEqual(float(adata.X[1, 1]), 1.00, places=2)
        self.assertAlmostEqual(float(adata.X[1, 2]), 1.00, places=2)
        self.assertAlmostEqual(float(adata.X[1, 3]), 1.00, places=2)

        # 3. Obs columns check
        self.assertIn("S_score", adata.obs.columns)
        self.assertIn("G_score", adata.obs.columns)
        self.assertIn("M_score", adata.obs.columns)
        self.assertIn("CRI_Score", adata.obs.columns)
        self.assertIn("Risk_Tier", adata.obs.columns)
        self.assertIn("Expected_5yr_DFS", adata.obs.columns)
        self.assertIn("Clinical_Action", adata.obs.columns)

        self.assertIn("TIER 1", adata.obs.loc["P001", "Risk_Tier"])
        self.assertIn("TIER 3", adata.obs.loc["P002", "Risk_Tier"])

        # 4. Spatial coordinates obsm['spatial']
        self.assertIn("spatial", adata.obsm)
        self.assertEqual(adata.obsm["spatial"].shape, (3, 2))
        self.assertAlmostEqual(adata.obsm["spatial"][0, 0], 120.5)
        self.assertAlmostEqual(adata.obsm["spatial"][0, 1], 340.2)

        # 5. Uns biophysical transport metadata
        self.assertIn("spatial_continuum", adata.uns)
        sc_meta = adata.uns["spatial_continuum"]
        self.assertEqual(sc_meta["primary_doi"], "10.21203/rs.3.rs-11530312/v1")
        self.assertEqual(sc_meta["bessel_transport_metrics"]["delta_r_sanctuary_thickness_um"], 34.1)
        self.assertEqual(sc_meta["bessel_transport_metrics"]["r0_vessel_radius_um"], 8.0)
        self.assertEqual(sc_meta["bessel_transport_metrics"]["rcrit_effective_penetration_um"], 42.1)

    def test_to_anndata_from_tsv_file(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".tsv", delete=False) as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(["sample_id", "pattern", "tp53", "rb1", "stroma", "x", "y"])
            writer.writerow(["SMP_01", "solid", "mutant", "mutant", "severe", 10.0, 20.0])
            writer.writerow(["SMP_02", "lepidic", "wildtype", "wildtype", "loose", 30.0, 40.0])
            f_path = f.name

        try:
            adata = to_anndata(f_path)
            self.assertEqual(adata.n_obs, 2)
            self.assertEqual(adata.n_vars, 4)
            self.assertIn("SMP_01", adata.obs_names)
            self.assertIn("SMP_02", adata.obs_names)
            self.assertAlmostEqual(adata.obs.loc["SMP_01", "CRI_Score"], 1.0)
            self.assertAlmostEqual(adata.obs.loc["SMP_02", "CRI_Score"], 0.0)
            self.assertEqual(adata.obsm["spatial"].shape, (2, 2))
        finally:
            if os.path.exists(f_path):
                os.remove(f_path)

    def test_annotate_anndata_inplace_and_copy(self):
        import anndata
        import pandas as pd
        import numpy as np

        obs_df = pd.DataFrame(
            {
                "pattern": ["solid", "lepidic"],
                "tp53": ["mut", "wt"],
                "rb1": ["wt", "wt"],
                "stroma": ["dense", "loose"],
            },
            index=["Cell_A", "Cell_B"],
        )
        base_adata = anndata.AnnData(
            X=np.zeros((2, 10)),
            obs=obs_df,
        )

        # Test copy=True
        adata_copy = annotate_anndata(base_adata, copy=True)
        self.assertNotIn("CRI_Score", base_adata.obs.columns)
        self.assertIn("CRI_Score", adata_copy.obs.columns)
        self.assertEqual(adata_copy.obs.loc["Cell_A", "S_score"], 1.0)
        self.assertEqual(adata_copy.obs.loc["Cell_A", "G_score"], 0.5)

        # Test in-place
        annotate_anndata(base_adata, copy=False)
        self.assertIn("CRI_Score", base_adata.obs.columns)
        self.assertIn("spatial_continuum", base_adata.uns)

    def test_from_anndata_roundtrip(self):
        records = [
            {"patient_id": "P_RT1", "histology_pattern": "Micropapillary", "tp53_status": "mut", "rb1_status": "wt", "stromal_grade": "dense", "spatial_x": 1.0, "spatial_y": 2.0}
        ]
        adata = to_anndata(records)
        df_out = from_anndata(adata, to_dataframe=True)
        self.assertEqual(len(df_out), 1)
        self.assertEqual(df_out.index[0], "P_RT1")
        self.assertAlmostEqual(df_out.loc["P_RT1", "S_score"], 1.0)
        self.assertAlmostEqual(df_out.loc["P_RT1", "spatial_x"], 1.0)

        records_out = from_anndata(adata, to_dataframe=False)
        self.assertEqual(len(records_out), 1)
        self.assertEqual(records_out[0]["Risk_Tier"], adata.obs.loc["P_RT1", "Risk_Tier"])


if __name__ == "__main__":
    unittest.main()
