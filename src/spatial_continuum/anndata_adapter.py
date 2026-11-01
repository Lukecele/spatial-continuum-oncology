"""
scverse AnnData Interoperability Adapter for spatial-continuum.
Provides bidirectional conversion and direct annotation of scverse AnnData objects
with reaction-diffusion biophysical parameters, spatial sanctuary metrics,
and Composite Resistance Index (CRI) clinical stratification tiers.

Design Philosophy:
- Zero-impact on base package: pure standard library remains default.
- If 'anndata', 'pandas', or 'numpy' are absent, informative ImportError is raised on use.
- Conforms fully to scverse ecosystem guidelines:
  * Cell/sample clinical annotations and risk tiers stored in adata.obs
  * Quantitative CRI component scores mapped to adata.X (or var)
  * Spatial 2D coordinates automatically recognized and mapped to adata.obsm['spatial']
  * Exact Bessel transport parameters and scientific DOI anchors stored in adata.uns['spatial_continuum']
"""

import os
import csv
from typing import Any, Dict, List, Optional, Tuple, Union

from .cri_calc import calculate_cri

# Biophysical constants derived from Bessel reaction-diffusion transport modeling
# (Celebrano et al., Research Square DOI: 10.21203/rs.3.rs-11530312/v1)
BESSEL_TRANSPORT_METRICS = {
    "r0_vessel_radius_um": 8.0,
    "rcrit_effective_penetration_um": 42.1,
    "delta_r_sanctuary_thickness_um": 34.1,
    "mean_penetration_depth_lambda_um": 25.5,
    "free_diffusion_coefficient_cm2_s": 1.2e-6,
    "effective_diffusivity_cm2_s": 1.5e-7,
    "interstitial_elimination_rate_s_inv": 2.3e-4,
    "model_equation": "C(r) = C0 * [K0(r/lambda) * I0(R/lambda) - I0(r/lambda) * K0(R/lambda)] / [K0(r0/lambda) * I0(R/lambda) - I0(r0/lambda) * K0(R/lambda)]",
}

SCIENTIFIC_ANCHORS = {
    "framework": "Spatial-Genomic Oncology Continuum",
    "primary_doi": "10.21203/rs.3.rs-11530312/v1",
    "primary_doi_url": "https://doi.org/10.21203/rs.3.rs-11530312/v1",
    "zenodo_monograph_doi": "10.5281/zenodo.23754999",
    "repository": "https://github.com/Lukecele/spatial-continuum-oncology",
    "documentation": "https://lukecele.github.io/spatial-continuum-oncology/",
    "weights": {"w_spatial": 0.47, "w_genomic": 0.33, "w_stroma": 0.20},
    "clinical_protocol": "Post-ADAURA Osimertinib Cessation vs Consolidation Protocol",
}


def _check_dependencies():
    """Verify that anndata, pandas, and numpy are available."""
    try:
        import anndata
        import pandas
        import numpy
        return anndata, pandas, numpy
    except ImportError as e:
        raise ImportError(
            "scverse AnnData interoperability requires 'anndata' and 'pandas'. "
            "Please install them via: pip install anndata pandas"
        ) from e


def to_anndata(
    data: Union[str, os.PathLike, List[Dict[str, Any]], Any],
    pattern_col: str = "histology_pattern",
    tp53_col: str = "tp53_status",
    rb1_col: str = "rb1_status",
    stroma_col: str = "stromal_grade",
    patient_id_col: Optional[str] = None,
    spatial_cols: Tuple[str, str] = ("spatial_x", "spatial_y"),
) -> Any:
    """
    Convert a clinical cohort (file path, DataFrame, or list of dicts) into an scverse AnnData object.

    Calculates CRI metrics for every record and populates:
      - adata.obs: all input annotations + S_score, G_score, M_score, CRI_Score, Risk_Tier, Expected_5yr_DFS, Clinical_Action
      - adata.X: 2D matrix of shape (n_obs, 4) with [S, G, M, CRI]
      - adata.var_names: ['spatial_decoupling_score', 'genomic_risk_score', 'stromal_barrier_score', 'composite_resistance_index']
      - adata.obsm['spatial']: 2D coordinates if spatial_cols or standard aliases (x/y) exist
      - adata.uns['spatial_continuum']: biophysical transport constants and publication metadata

    Parameters:
      data: File path (TSV/CSV), pandas DataFrame, or list of record dicts.
      pattern_col: Name or alias of the histology pattern column.
      tp53_col: Name or alias of the TP53 mutation status column.
      rb1_col: Name or alias of the RB1 mutation status column.
      stroma_col: Name or alias of the stromal desmoplasia / CAF grade column.
      patient_id_col: Column to use for observation index (default: auto-detected or numeric).
      spatial_cols: Tuple of column names for 2D spatial coordinates (e.g. ('spatial_x', 'spatial_y')).

    Returns:
      anndata.AnnData: Annotated data object conforming to scverse ecosystem standards.
    """
    anndata, pd, np = _check_dependencies()

    # 1. Parse input to pandas DataFrame
    if isinstance(data, (str, os.PathLike)):
        filepath = str(data)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Cohort data file not found: {filepath}")
        delimiter = "\t" if filepath.endswith(".tsv") else ","
        df = pd.read_csv(filepath, sep=delimiter)
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        df = pd.DataFrame(data)
    else:
        raise TypeError(
            f"Unsupported data type for to_anndata: {type(data)}. Expected path string, pandas DataFrame, or list of dicts."
        )

    # 2. Identify column mappings with case-insensitive and alias fallbacks
    col_map = {col.lower().strip(): col for col in df.columns}

    def _resolve_col(preferred: str, aliases: List[str]) -> Optional[str]:
        p = preferred.lower().strip()
        if p in col_map:
            return col_map[p]
        for a in aliases:
            al = a.lower().strip()
            if al in col_map:
                return col_map[al]
            # Partial substring match
            for col_lower, orig in col_map.items():
                if al in col_lower:
                    return orig
        return None

    resolved_pattern = _resolve_col(pattern_col, ["pattern", "histology", "architecture", "morphology"])
    resolved_tp53 = _resolve_col(tp53_col, ["tp53", "p53", "tp53_mut", "tp53_status"])
    resolved_rb1 = _resolve_col(rb1_col, ["rb1", "rb", "rb1_mut", "rb1_status"])
    resolved_stroma = _resolve_col(stroma_col, ["stroma", "desmoplasia", "caf", "fibrosis", "stromal_grade"])

    # 3. Compute CRI for every row
    s_scores = []
    desc_s_list = []
    g_scores = []
    desc_g_list = []
    m_scores = []
    desc_m_list = []
    cri_scores = []
    tiers = []
    pfs_list = []
    actions = []
    action_shorts = []

    for _, row in df.iterrows():
        p_val = row[resolved_pattern] if resolved_pattern else ""
        t_val = row[resolved_tp53] if resolved_tp53 else "wt"
        r_val = row[resolved_rb1] if resolved_rb1 else "wt"
        m_val = row[resolved_stroma] if resolved_stroma else "moderate"

        res = calculate_cri(p_val, tp53=t_val, rb1=r_val, stroma=m_val)
        s_scores.append(res["S"])
        desc_s_list.append(res["desc_S"])
        g_scores.append(res["G"])
        desc_g_list.append(res["desc_G"])
        m_scores.append(res["M"])
        desc_m_list.append(res["desc_M"])
        cri_scores.append(res["CRI"])
        tiers.append(res["tier"])
        pfs_list.append(res["pfs_5yr"])
        actions.append(res["action"])
        action_shorts.append(res["action_short"])

    # Populate calculated columns in DataFrame
    df["S_score"] = s_scores
    df["desc_S"] = desc_s_list
    df["G_score"] = g_scores
    df["desc_G"] = desc_g_list
    df["M_score"] = m_scores
    df["desc_M"] = desc_m_list
    df["CRI_Score"] = cri_scores
    df["Risk_Tier"] = tiers
    df["Expected_5yr_DFS"] = pfs_list
    df["Clinical_Action"] = actions
    df["Action_Summary"] = action_shorts

    # 4. Resolve observation index
    resolved_id = None
    if patient_id_col and patient_id_col.lower().strip() in col_map:
        resolved_id = col_map[patient_id_col.lower().strip()]
    else:
        for candidate in ["patient_id", "sample_id", "id", "cell_id", "barcode", "patient"]:
            if candidate in col_map:
                resolved_id = col_map[candidate]
                break

    if resolved_id:
        df.index = df[resolved_id].astype(str)
    else:
        df.index = [f"sample_{i+1:04d}" for i in range(len(df))]

    # 5. Extract Feature Matrix X
    feature_matrix = np.column_stack([s_scores, g_scores, m_scores, cri_scores]).astype(np.float32)
    var_names = [
        "spatial_decoupling_score",
        "genomic_risk_score",
        "stromal_barrier_score",
        "composite_resistance_index",
    ]
    var_df = pd.DataFrame(
        {
            "feature_name": var_names,
            "weight": [0.47, 0.33, 0.20, 1.00],
            "description": [
                "Bessel-derived spatial vascular decoupling distance score (S)",
                "Co-mutational clonal plasticity score (G)",
                "Stromal desmoplasia and interstitial fluid pressure score (M)",
                "Composite Resistance Index weighted sum (CRI)",
            ],
        },
        index=var_names,
    )

    # 6. Check for spatial 2D coordinates
    obsm_dict = {}
    x_col = _resolve_col(spatial_cols[0], ["spatial_x", "coord_x", "x", "pos_x", "image_x"])
    y_col = _resolve_col(spatial_cols[1], ["spatial_y", "coord_y", "y", "pos_y", "image_y"])

    if x_col and y_col and x_col != y_col:
        try:
            x_vals = pd.to_numeric(df[x_col], errors="coerce").fillna(0.0).values
            y_vals = pd.to_numeric(df[y_col], errors="coerce").fillna(0.0).values
            obsm_dict["spatial"] = np.column_stack([x_vals, y_vals]).astype(np.float64)
        except Exception:
            pass

    # 7. Construct AnnData
    adata = anndata.AnnData(
        X=feature_matrix,
        obs=df,
        var=var_df,
        obsm=obsm_dict if obsm_dict else None,
    )

    # 8. Set unstructured metadata uns
    adata.uns["spatial_continuum"] = {
        **SCIENTIFIC_ANCHORS,
        "bessel_transport_metrics": BESSEL_TRANSPORT_METRICS,
        "anndata_adapter_version": "1.0.3",
    }

    return adata


def annotate_anndata(
    adata: Any,
    pattern_key: str = "histology_pattern",
    tp53_key: str = "tp53_status",
    rb1_key: str = "rb1_status",
    stroma_key: str = "stromal_grade",
    copy: bool = False,
) -> Any:
    """
    Annotate an existing scverse AnnData object in-place (or on a copy) with CRI scores.

    Takes cell/spot/patient observations in adata.obs, computes CRI resistance tiers,
    adds CRI columns to adata.obs, and records biophysical transport constants in adata.uns.

    Parameters:
      adata: An existing anndata.AnnData instance.
      pattern_key: Column key in adata.obs for histology pattern.
      tp53_key: Column key in adata.obs for TP53 status.
      rb1_key: Column key in adata.obs for RB1 status.
      stroma_key: Column key in adata.obs for stromal desmoplasia.
      copy: If True, operates on and returns a copy; otherwise modifies in-place.

    Returns:
      anndata.AnnData: Annotated AnnData instance.
    """
    anndata, pd, np = _check_dependencies()

    if not isinstance(adata, anndata.AnnData):
        raise TypeError(f"Expected anndata.AnnData instance, got {type(adata)}")

    target = adata.copy() if copy else adata

    obs_cols = {col.lower().strip(): col for col in target.obs.columns}

    def _resolve(key: str, aliases: List[str]) -> Optional[str]:
        k = key.lower().strip()
        if k in obs_cols:
            return obs_cols[k]
        for a in aliases:
            al = a.lower().strip()
            if al in obs_cols:
                return obs_cols[al]
            for c_lower, orig in obs_cols.items():
                if al in c_lower:
                    return orig
        return None

    resolved_pattern = _resolve(pattern_key, ["pattern", "histology", "architecture"])
    resolved_tp53 = _resolve(tp53_key, ["tp53", "p53", "tp53_mut"])
    resolved_rb1 = _resolve(rb1_key, ["rb1", "rb", "rb1_mut"])
    resolved_stroma = _resolve(stroma_key, ["stroma", "desmoplasia", "caf", "fibrosis"])

    s_scores = []
    desc_s_list = []
    g_scores = []
    desc_g_list = []
    m_scores = []
    desc_m_list = []
    cri_scores = []
    tiers = []
    pfs_list = []
    actions = []
    action_shorts = []

    for _, row in target.obs.iterrows():
        p_val = row[resolved_pattern] if resolved_pattern else ""
        t_val = row[resolved_tp53] if resolved_tp53 else "wt"
        r_val = row[resolved_rb1] if resolved_rb1 else "wt"
        m_val = row[resolved_stroma] if resolved_stroma else "moderate"

        res = calculate_cri(p_val, tp53=t_val, rb1=r_val, stroma=m_val)
        s_scores.append(res["S"])
        desc_s_list.append(res["desc_S"])
        g_scores.append(res["G"])
        desc_g_list.append(res["desc_G"])
        m_scores.append(res["M"])
        desc_m_list.append(res["desc_M"])
        cri_scores.append(res["CRI"])
        tiers.append(res["tier"])
        pfs_list.append(res["pfs_5yr"])
        actions.append(res["action"])
        action_shorts.append(res["action_short"])

    target.obs["S_score"] = s_scores
    target.obs["desc_S"] = desc_s_list
    target.obs["G_score"] = g_scores
    target.obs["desc_G"] = desc_g_list
    target.obs["M_score"] = m_scores
    target.obs["desc_M"] = desc_m_list
    target.obs["CRI_Score"] = cri_scores
    target.obs["Risk_Tier"] = tiers
    target.obs["Expected_5yr_DFS"] = pfs_list
    target.obs["Clinical_Action"] = actions
    target.obs["Action_Summary"] = action_shorts

    if "spatial_continuum" not in target.uns:
        target.uns["spatial_continuum"] = {}

    target.uns["spatial_continuum"].update({
        **SCIENTIFIC_ANCHORS,
        "bessel_transport_metrics": BESSEL_TRANSPORT_METRICS,
        "anndata_adapter_version": "1.0.3",
    })

    return target


def from_anndata(
    adata: Any,
    to_dataframe: bool = True,
) -> Union[Any, List[Dict[str, Any]]]:
    """
    Extract annotated clinical observations and CRI resistance metrics from an scverse AnnData object.

    Parameters:
      adata: An anndata.AnnData instance containing spatial_continuum annotations.
      to_dataframe: If True, returns a pandas DataFrame; otherwise returns a list of dictionaries.

    Returns:
      pandas.DataFrame or List[Dict[str, Any]]: The extracted table of observations.
    """
    anndata, pd, np = _check_dependencies()

    if not isinstance(adata, anndata.AnnData):
        raise TypeError(f"Expected anndata.AnnData instance, got {type(adata)}")

    df = adata.obs.copy()

    # Append spatial coordinates if present in obsm
    if "spatial" in adata.obsm and hasattr(adata.obsm["spatial"], "shape") and adata.obsm["spatial"].shape[1] >= 2:
        coords = adata.obsm["spatial"]
        df["spatial_x"] = coords[:, 0]
        df["spatial_y"] = coords[:, 1]

    if to_dataframe:
        return df
    return df.to_dict(orient="records")
