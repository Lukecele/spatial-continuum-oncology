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


def _check_scipy():
    """Verify that scipy is available for spatial and Bessel computations."""
    try:
        from scipy.spatial import cKDTree
        from scipy.special import k0
        return cKDTree, k0
    except ImportError as e:
        raise ImportError(
            "Spatial sanctuary and distance computations require 'scipy'. "
            "Please install it via: pip install scipy"
        ) from e


def compute_spatial_bessel_sanctuary(
    adata: Any,
    spatial_key: str = "spatial",
    vessel_mask: Optional[Any] = None,
    vessel_gene: str = "PECAM1",
    tumor_mask: Optional[Any] = None,
    tumor_gene: str = "EPCAM",
    vessel_threshold: float = 1.0,
    tumor_threshold: float = 1.0,
    spot_pitch_um: float = 2.0,
    lambda_um: float = 25.5,
    r0_um: float = 8.0,
    rcrit_um: float = 165.9,
    copy: bool = False,
) -> Any:
    """
    Compute biophysical Bessel reaction-diffusion drug penetration and identify
    perivascular pharmacological sanctuary zones in spatial transcriptomics / Visium HD data.

    Maps physical distances from functional microvessels (CD31+/PECAM1+) using KD-Tree,
    solves the cylindrical Bessel K0 transport equation C(r)/C0, and annotates:
      - adata.obs['distance_to_nearest_capillary_um']: Euclidean distance in micrometers
      - adata.obs['bessel_drug_concentration_ratio']: C(r)/C0 normalized concentration (0.0 to 1.0)
      - adata.obs['sanctuary_class']: 'Capillary', 'Effective Penetration (<100 um)',
                                    'Attenuated Zone (100-166 um)', 'Pharmacological Sanctuary (>166 um)'
      - adata.obs['is_sanctuary_spot']: Boolean flag for spots in pharmacological sanctuary (> rcrit_um)
      - adata.uns['spatial_bessel_sanctuary']: Summary dictionary with tissue sanctuary burden statistics.

    Parameters:
      adata: anndata.AnnData instance with spatial coordinates.
      spatial_key: Key in adata.obsm storing (x, y) coordinates (default: 'spatial').
      vessel_mask: Optional boolean array identifying endothelial/capillary spots.
      vessel_gene: Gene name to identify vessels if vessel_mask is None (default: 'PECAM1').
      tumor_mask: Optional boolean array identifying tumor spots.
      tumor_gene: Gene name to identify tumor spots if tumor_mask is None (default: 'EPCAM').
      vessel_threshold: Expression cutoff for vessel detection (default: 1.0).
      tumor_threshold: Expression cutoff for tumor detection (default: 1.0).
      spot_pitch_um: Conversion factor from coordinate units to micrometers (default: 2.0 um).
      lambda_um: Biophysical mean penetration depth lambda in micrometers (default: 25.5 um).
      r0_um: Capillary radius in micrometers (default: 8.0 um).
      rcrit_um: Critical therapeutic penetration cutoff in micrometers (default: 165.9 um).
      copy: If True, returns a copy of adata; otherwise annotates in place.

    Returns:
      anndata.AnnData: Annotated spatial AnnData object.
    """
    anndata, pd, np = _check_dependencies()
    cKDTree, k0 = _check_scipy()

    if not isinstance(adata, anndata.AnnData):
        raise TypeError(f"Expected anndata.AnnData instance, got {type(adata)}")

    target = adata.copy() if copy else adata
    n_obs = target.n_obs

    # 1. Resolve 2D spatial coordinates
    if spatial_key in target.obsm and hasattr(target.obsm[spatial_key], "shape") and target.obsm[spatial_key].shape[1] >= 2:
        coords = np.asarray(target.obsm[spatial_key][:, :2], dtype=float)
    elif "spatial_x" in target.obs and "spatial_y" in target.obs:
        coords = target.obs[["spatial_x", "spatial_y"]].to_numpy(dtype=float)
    elif "x" in target.obs and "y" in target.obs:
        coords = target.obs[["x", "y"]].to_numpy(dtype=float)
    else:
        raise KeyError(
            f"Spatial coordinates not found. Checked target.obsm['{spatial_key}'] "
            "and target.obs['spatial_x'/'spatial_y']."
        )

    # Helper to extract gene expression array
    def _get_expr(gene: str) -> Optional[np.ndarray]:
        if gene in target.var_names:
            idx = target.var_names.get_loc(gene)
            col = target.X[:, idx]
            if hasattr(col, "toarray"):
                col = col.toarray()
            return np.asarray(col).flatten()
        if gene in target.obs:
            return target.obs[gene].to_numpy(dtype=float)
        # Case insensitive lookup in obs
        for c in target.obs.columns:
            if c.lower() == gene.lower():
                return target.obs[c].to_numpy(dtype=float)
        return None

    # 2. Resolve vessel mask
    if vessel_mask is not None:
        is_vessel = np.asarray(vessel_mask, dtype=bool)
    else:
        v_expr = _get_expr(vessel_gene)
        if v_expr is not None:
            is_vessel = v_expr > vessel_threshold
        elif "is_vessel" in target.obs:
            is_vessel = target.obs["is_vessel"].to_numpy(dtype=bool)
        elif "is_endo" in target.obs:
            is_vessel = target.obs["is_endo"].to_numpy(dtype=bool)
        else:
            raise ValueError(
                f"Cannot identify vessel spots: '{vessel_gene}' not found in var_names or obs."
            )

    if np.sum(is_vessel) == 0:
        raise ValueError("No vessel/capillary spots detected to compute diffusion distances.")

    # 3. Resolve tumor mask
    if tumor_mask is not None:
        is_tumor = np.asarray(tumor_mask, dtype=bool) & ~is_vessel
    else:
        t_expr = _get_expr(tumor_gene)
        if t_expr is not None:
            is_tumor = (t_expr > tumor_threshold) & ~is_vessel
        elif "is_tumor" in target.obs:
            is_tumor = target.obs["is_tumor"].to_numpy(dtype=bool) & ~is_vessel
        else:
            # Default: all non-vessel spots considered part of the parenchymal mass
            is_tumor = ~is_vessel

    # 4. KD-Tree distance calculation
    vessel_coords = coords[is_vessel]
    tree = cKDTree(vessel_coords)
    dists_raw, _ = tree.query(coords)
    dists_um = dists_raw * spot_pitch_um

    # 5. Modified Bessel K0 reaction-diffusion concentration ratio
    k0_r0 = k0(r0_um / lambda_um)
    bessel_ratio = np.ones(n_obs, dtype=float)
    beyond_r0 = dists_um > r0_um
    bessel_ratio[beyond_r0] = k0(dists_um[beyond_r0] / lambda_um) / k0_r0
    bessel_ratio = np.clip(bessel_ratio, 0.0, 1.0)

    # 6. Spot-by-spot sanctuary classification
    classes = []
    is_sanctuary = np.zeros(n_obs, dtype=bool)

    for i in range(n_obs):
        if is_vessel[i]:
            classes.append("Capillary (Endothelial)")
        elif is_tumor[i]:
            d = dists_um[i]
            if d <= 100.0:
                classes.append("Effective Penetration (<100 um)")
            elif d <= rcrit_um:
                classes.append("Attenuated Zone (100-166 um)")
            else:
                classes.append("Pharmacological Sanctuary (>166 um)")
                is_sanctuary[i] = True
        else:
            classes.append("Stroma / Normal Parenchyma")

    # 7. Write to obs
    target.obs["distance_to_nearest_capillary_um"] = dists_um
    target.obs["bessel_drug_concentration_ratio"] = bessel_ratio
    target.obs["sanctuary_class"] = classes
    target.obs["is_sanctuary_spot"] = is_sanctuary

    # 8. Compute tissue-level sanctuary burden
    n_tumor = int(np.sum(is_tumor))
    n_sanctuary = int(np.sum(is_sanctuary))
    sanctuary_fraction = round((n_sanctuary / max(n_tumor, 1)) * 100.0, 2)

    tumor_dists = dists_um[is_tumor] if n_tumor > 0 else np.array([0.0])

    if "spatial_continuum" not in target.uns:
        target.uns["spatial_continuum"] = {}

    target.uns["spatial_bessel_sanctuary"] = {
        "total_spots": n_obs,
        "vessel_spots": int(np.sum(is_vessel)),
        "tumor_spots": n_tumor,
        "sanctuary_spots": n_sanctuary,
        "sanctuary_fraction_pct": sanctuary_fraction,
        "mean_tumor_vessel_distance_um": round(float(np.mean(tumor_dists)), 2),
        "median_tumor_vessel_distance_um": round(float(np.median(tumor_dists)), 2),
        "lambda_penetration_depth_um": lambda_um,
        "r0_capillary_radius_um": r0_um,
        "rcrit_sanctuary_threshold_um": rcrit_um,
        "spot_pitch_um": spot_pitch_um,
    }

    return target

