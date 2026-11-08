#' Spatial-Genomic Oncology Continuum for R (spatialcontinuum)
#'
#' Universal Reaction-Diffusion Transport Modeling and In Silico Composite Resistance Index (CRI)
#' for Spatial Transcriptomics, Seurat, and SpatialExperiment objects.
#' Research Use Only (RUO). This package performs in silico biophysical transport simulations
#' to formulate hypotheses for prospective clinical trial design. It does not provide direct
#' clinical prescribing directives.
#'
#' @author Luca Celebrano, MD Candidate, Universita degli Studi di Napoli Federico II
#' @references
#'   Celebrano et al. (2026), Research Square DOI: 10.21203/rs.3.rs-11530312/v1
#'   Zenodo Monograph DOI: 10.5281/zenodo.23754999
#'   GitHub: https://github.com/Lukecele/spatial-continuum-oncology
#'
#' @export CalculateCRI
#' @export BesselK0Concentration
#' @export ComputeSpatialSanctuary
#' @export AddSpatialContinuumScores
#' @export GenerateTumorBoardReport

# -----------------------------------------------------------------------------
# 1. In Silico Composite Resistance Index (CRI) Calculator (RUO)
# -----------------------------------------------------------------------------

#' Calculate Composite Resistance Index (CRI) and Translational Hypotheses
#'
#' Evaluates the multidimensional risk score combining spatial histology pattern (S),
#' genomic co-mutations (G), and stromal desmoplasia (M).
#' Research Use Only (RUO).
#'
#' @param pattern Character. Histologic subtype: 'lepidic', 'acinar', 'papillary', 'micropapillary', 'solid'.
#' @param tp53 Character or Logical. TP53 mutation status ('mut', 'wt', TRUE, FALSE).
#' @param rb1 Character or Logical. RB1 mutation status ('mut', 'wt', TRUE, FALSE).
#' @param stroma Character. Stromal grade: 'loose', 'moderate', 'dense'.
#' @param w_spatial Numeric. Weight for spatial histology (default: 0.47).
#' @param w_genomic Numeric. Weight for genomic co-mutations (default: 0.33).
#' @param w_stromal Numeric. Weight for stromal desmoplasia (default: 0.20).
#' @param cutoff_low Numeric. Low-risk tier cutoff (default: 0.35).
#' @param cutoff_high Numeric. High-risk tier cutoff (default: 0.65).
#' @return A named list containing S, G, M, CRI score, Risk Tier, Expected 5-year DFS, and clinical directive.
#' @examples
#' res <- CalculateCRI("solid", tp53 = "mut", rb1 = "wt", stroma = "dense")
#' print(res$CRI)
CalculateCRI <- function(pattern, tp53 = "wt", rb1 = "wt", stroma = "moderate",
                         w_spatial = 0.47, w_genomic = 0.33, w_stromal = 0.20,
                         cutoff_low = 0.35, cutoff_high = 0.65) {
  # Normalize strings
  p_norm <- tolower(trimws(as.character(pattern)))
  s_norm <- tolower(trimws(as.character(stroma)))

  # 1. Spatial Histology Score S in [0.0, 1.0]
  S <- if (grepl("lepidic", p_norm)) {
    0.00
  } else if (grepl("acinar", p_norm)) {
    0.35
  } else if (grepl("papillary", p_norm) && !grepl("micro", p_norm)) {
    0.45
  } else if (grepl("micro", p_norm)) {
    0.90
  } else if (grepl("solid", p_norm)) {
    1.00
  } else {
    0.50
  }

  # 2. Genomic Co-mutation Score G in [0.0, 1.0]
  is_mut <- function(x) {
    if (is.logical(x)) return(x)
    x_str <- tolower(trimws(as.character(x)))
    x_str %in% c("mut", "mutant", "positive", "pos", "1", "true")
  }

  has_tp53 <- is_mut(tp53)
  has_rb1 <- is_mut(rb1)

  G <- if (has_tp53 && has_rb1) {
    1.00 # Double mutant: catastrophic transformation risk
  } else if (has_tp53 || has_rb1) {
    0.50 # Single mutant
  } else {
    0.00 # Double wild-type
  }

  # 3. Stromal Desmoplasia Score M in [0.0, 1.0]
  M <- if (grepl("loose", s_norm) || grepl("alveolar", s_norm) || grepl("low", s_norm)) {
    0.00
  } else if (grepl("dense", s_norm) || grepl("fibrotic", s_norm) || grepl("severe", s_norm) || grepl("high", s_norm)) {
    1.00
  } else {
    0.50 # Moderate
  }

  # Linear combination with customizable weights
  cri_raw <- w_spatial * S + w_genomic * G + w_stromal * M
  CRI <- round(min(max(cri_raw, 0.0), 1.0), 3)

  # Biophysical sanctuary shell calculation
  delta_r <- round(34.11 * ((S + M) / 2.0), 1)
  sanctuary_vol_pct <- round(31.28 * ((S + M) / 2.0), 1)

  # Risk stratification tiers using customizable cutoffs
  if (CRI < cutoff_low) {
    tier <- "Tier 1 (Low Sanctuary Risk / Perfusion Permissive)"
    action <- "Tier 1: Sanctuary mantle absent (Delta r <= 0 um). Low sanctuary profile [RUO]."
    dfs_5yr <- "96.4% [95% CI: 92.1-99.2%]"
    justification <- paste0(
      "Well-perfused, thin alveolar cords (sanctuary shell delta_r = ", delta_r, " um). ",
      "In silico transport modeling indicates drug concentration exceeds IC50 throughout tissue. ",
      "Research Use Only: In silico biophysical transport hypothesis for prospective trial cohort stratification."
    )
    rec <- "Hypothesis: Favorable biophysical profile; candidate cohort for observational surveillance trial designs (RUO)."
  } else if (CRI <= cutoff_high) {
    tier <- "Tier 2 (Intermediate Risk / Transitional Cords)"
    action <- "Tier 2: Intermediate risk; borderline sanctuary shell present (Delta r ~ 10-25 um) [RUO]."
    dfs_5yr <- "74.8% [95% CI: 68.3-81.2%]"
    justification <- paste0(
      "Partial perivascular drug penetration with low-frequency dormant cells (delta_r = ", delta_r, " um). ",
      "In silico transport modeling indicates transitional diffusion barrier. ",
      "Research Use Only: In silico biophysical transport hypothesis for prospective trial cohort stratification."
    )
    rec <- "Hypothesis: Intermediate diffusion barrier; candidate cohort for multimodal monitoring and ctDNA biomarker trials (RUO)."
  } else {
    tier <- "Tier 3 (High Sanctuary Risk / Obligate Perivascular Mantle)"
    action <- "Tier 3: Substantial perivascular mantle (Delta r > 34 um). High sanctuary risk [RUO]."
    dfs_5yr <- "38.2% [95% CI: 31.0-45.5%]"
    justification <- paste0(
      "Dense fibrotic stroma and solid cord architecture create an obligate sanctuary shell ",
      "(delta_r = ", delta_r, " um, ~", sanctuary_vol_pct, "% viable volume). ",
      "In silico transport modeling demonstrates significant sub-therapeutic drug mantle. ",
      "Research Use Only: Candidate cohort for prospective vascular normalization / combination trial arms."
    )
    rec <- "Hypothesis: Obligate biophysical sanctuary; candidate cohort for prospective vascular normalization trials (RUO)."
  }

  list(
    CRI = CRI,
    S_score = S,
    G_score = G,
    M_score = M,
    Risk_Tier = tier,
    Action_Directive = action,
    Expected_5yr_DFS = dfs_5yr,
    Sanctuary_Delta_r_um = delta_r,
    Sanctuary_Volume_Pct = sanctuary_vol_pct,
    Clinical_Recommendation = rec,
    Biological_Rationale = justification,
    Scientific_DOI = "10.21203/rs.3.rs-11530312/v1"
  )
}

# -----------------------------------------------------------------------------
# 2. Bessel Reaction-Diffusion Transport Solver
# -----------------------------------------------------------------------------

#' Solve Modified Bessel K0 Extravascular Drug Concentration
#'
#' Computes the steady-state cylindrical reaction-diffusion concentration ratio
#' C(r)/C0 = K0(r / lambda) / K0(r0 / lambda).
#'
#' @param r Numeric vector. Radial distances from capillary center in micrometers.
#' @param lambda Numeric. Mean penetration-elimination depth in micrometers (default: 25.5 um).
#' @param r0 Numeric. Capillary radius in micrometers (default: 8.0 um).
#' @return Numeric vector of normalized concentrations C(r)/C0 in [0.0, 1.0].
#' @export
BesselK0Concentration <- function(r, lambda = 25.5, r0 = 8.0) {
  k0_r0 <- besselK(r0 / lambda, nu = 0)
  conc <- besselK(r / lambda, nu = 0) / k0_r0
  # Inside vessel or at wall, concentration is saturated C0
  conc[r <= r0] <- 1.0
  # Handle numerical underflow or Inf
  conc[is.na(conc) | is.nan(conc)] <- 0.0
  pmin(pmax(conc, 0.0), 1.0)
}

# -----------------------------------------------------------------------------
# 3. Generic Spatial Coordinates Sanctuary Evaluator
# -----------------------------------------------------------------------------

#' Compute Biophysical Perivascular Sanctuary Metrics on Spatial Coordinates
#'
#' Fast calculation of nearest capillary distances, Bessel K0 diffusion gradient,
#' and pharmacological sanctuary classification (> 165.9 um) across 2D spot coordinates.
#'
#' @param coords Matrix or data.frame with 2 columns (x, y) representing spatial coordinates.
#' @param is_vessel Logical vector. Identifies capillary/endothelial spots (e.g. CD31+/PECAM1+).
#' @param is_tumor Logical vector. Identifies viable carcinoma spots (e.g. EPCAM+).
#' @param spot_pitch_um Numeric. Conversion factor from coordinate units to micrometers (default: 2.0 um).
#' @param lambda_um Numeric. Mean penetration depth in micrometers (default: 25.5 um).
#' @param r0_um Numeric. Capillary radius in micrometers (default: 8.0 um).
#' @param rcrit_um Numeric. Critical sanctuary threshold in micrometers (default: 165.9 um).
#' @return A list with per-spot vectors and tissue-level summary statistics.
#' @export
ComputeSpatialSanctuary <- function(
  coords,
  is_vessel,
  is_tumor = NULL,
  spot_pitch_um = 2.0,
  lambda_um = 25.5,
  r0_um = 8.0,
  rcrit_um = 165.9
) {
  coords_mat <- as.matrix(coords[, 1:2])
  n_spots <- nrow(coords_mat)

  if (length(is_vessel) != n_spots) {
    stop("Length of 'is_vessel' must match number of coordinate rows.")
  }

  n_vessels <- sum(is_vessel, na.rm = TRUE)
  if (n_vessels == 0) {
    stop("No capillary/vessel spots identified in tissue coordinates.")
  }

  if (is.null(is_tumor)) {
    is_tumor <- !is_vessel
  }

  # Fast Euclidean distance to nearest capillary
  vessel_coords <- coords_mat[is_vessel, , drop = FALSE]

  # Compute nearest neighbor distance for every spot
  # Memory-efficient chunked calculation to handle 10x Visium / Visium HD arrays
  min_dists_raw <- numeric(n_spots)
  chunk_size <- 2000
  n_chunks <- ceiling(n_spots / chunk_size)

  for (c_idx in seq_len(n_chunks)) {
    start_i <- (c_idx - 1) * chunk_size + 1
    end_i <- min(c_idx * chunk_size, n_spots)
    sub_coords <- coords_mat[start_i:end_i, , drop = FALSE]

    # Euclidean distance matrix between chunk spots and all vessels
    # d^2 = (x - x_v)^2 + (y - y_v)^2
    dists_sub <- apply(sub_coords, 1, function(pt) {
      dx <- vessel_coords[, 1] - pt[1]
      dy <- vessel_coords[, 2] - pt[2]
      min(sqrt(dx * dx + dy * dy))
    })
    min_dists_raw[start_i:end_i] <- dists_sub
  }

  dists_um <- min_dists_raw * spot_pitch_um

  # Modified Bessel K0 reaction-diffusion concentration ratio
  bessel_ratio <- BesselK0Concentration(dists_um, lambda = lambda_um, r0 = r0_um)

  # Spot-level classification
  classes <- character(n_spots)
  is_sanctuary <- logical(n_spots)

  for (i in seq_len(n_spots)) {
    if (is_vessel[i]) {
      classes[i] <- "Capillary (Endothelial)"
    } else if (is_tumor[i]) {
      d <- dists_um[i]
      if (d <= 100.0) {
        classes[i] <- "Effective Penetration (<100 um)"
      } else if (d <= rcrit_um) {
        classes[i] <- "Attenuated Zone (100-166 um)"
      } else {
        classes[i] <- "Pharmacological Sanctuary (>166 um)"
        is_sanctuary[i] <- TRUE
      }
    } else {
      classes[i] <- "Stroma / Normal Parenchyma"
    }
  }

  # Summary statistics
  n_tumor <- sum(is_tumor, na.rm = TRUE)
  n_sanc <- sum(is_sanctuary, na.rm = TRUE)
  sanc_fraction <- if (n_tumor > 0) round((n_sanc / n_tumor) * 100, 2) else 0.0

  tumor_dists <- if (n_tumor > 0) dists_um[is_tumor] else 0.0

  summary_stats <- list(
    total_spots = n_spots,
    vessel_spots = n_vessels,
    tumor_spots = n_tumor,
    sanctuary_spots = n_sanc,
    sanctuary_fraction_pct = sanc_fraction,
    mean_tumor_vessel_distance_um = round(mean(tumor_dists), 2),
    median_tumor_vessel_distance_um = round(stats::median(tumor_dists), 2),
    lambda_penetration_depth_um = lambda_um,
    r0_capillary_radius_um = r0_um,
    rcrit_sanctuary_threshold_um = rcrit_um,
    spot_pitch_um = spot_pitch_um
  )

  list(
    distance_to_nearest_capillary_um = dists_um,
    bessel_drug_concentration_ratio = bessel_ratio,
    sanctuary_class = classes,
    is_sanctuary_spot = is_sanctuary,
    summary = summary_stats
  )
}

# -----------------------------------------------------------------------------
# 4. Seurat Integration Hook
# -----------------------------------------------------------------------------

#' Add Spatial-Continuum Sanctuary Scores to a Seurat Object
#'
#' Evaluates physical distances from capillaries, Bessel K0 diffusion gradient,
#' and pharmacological sanctuary burden directly on 10x Visium or single-cell spatial Seurat objects.
#'
#' @param seurat_obj A Seurat object containing spatial coordinates.
#' @param assay Character. Assay containing gene expression (default: 'Spatial').
#' @param vessel_feature Character. Gene marker for capillaries (default: 'PECAM1').
#' @param tumor_feature Character. Gene marker for tumor epithelium (default: 'EPCAM').
#' @param spot_pitch_um Numeric. Spatial calibration in micrometers per coordinate unit (default: 2.0 um).
#' @param lambda_um Numeric. Mean penetration depth lambda in micrometers (default: 25.5 um).
#' @param r0_um Numeric. Capillary radius in micrometers (default: 8.0 um).
#' @param rcrit_um Numeric. Critical sanctuary threshold in micrometers (default: 165.9 um).
#' @param vessel_cutoff Numeric. Expression cutoff for capillary spots (default: 1.0).
#' @param tumor_cutoff Numeric. Expression cutoff for carcinoma spots (default: 1.0).
#' @return An annotated Seurat object with new metadata columns and summary in @@misc$spatial_continuum.
#' @export
AddSpatialContinuumScores <- function(
  seurat_obj,
  assay = "Spatial",
  vessel_feature = "PECAM1",
  tumor_feature = "EPCAM",
  spot_pitch_um = 2.0,
  lambda_um = 25.5,
  r0_um = 8.0,
  rcrit_um = 165.9,
  vessel_cutoff = 1.0,
  tumor_cutoff = 1.0
) {
  # 1. Extract coordinates
  coords <- NULL
  if (requireNamespace("Seurat", quietly = TRUE)) {
    tryCatch({
      coords <- Seurat::GetTissueCoordinates(seurat_obj)
    }, error = function(e) {})
  }

  if (is.null(coords)) {
    if ("x" %in% colnames(seurat_obj@meta.data) && "y" %in% colnames(seurat_obj@meta.data)) {
      coords <- seurat_obj@meta.data[, c("x", "y")]
    } else if ("spatial_x" %in% colnames(seurat_obj@meta.data) && "spatial_y" %in% colnames(seurat_obj@meta.data)) {
      coords <- seurat_obj@meta.data[, c("spatial_x", "spatial_y")]
    } else {
      stop("Could not locate spatial coordinates in Seurat object (checked GetTissueCoordinates and meta.data).")
    }
  }

  # 2. Extract expression
  n_cells <- ncol(seurat_obj)
  is_vessel <- rep(FALSE, n_cells)
  is_tumor <- rep(TRUE, n_cells)

  # Check if Seurat assay contains features
  tryCatch({
    expr_vessel <- seurat_obj[[assay]][vessel_feature, ]
    is_vessel <- as.numeric(expr_vessel) > vessel_cutoff
  }, error = function(e) {
    if (vessel_feature %in% colnames(seurat_obj@meta.data)) {
      is_vessel <<- seurat_obj@meta.data[[vessel_feature]] > vessel_cutoff
    }
  })

  tryCatch({
    expr_tumor <- seurat_obj[[assay]][tumor_feature, ]
    is_tumor <- (as.numeric(expr_tumor) > tumor_cutoff) & !is_vessel
  }, error = function(e) {
    if (tumor_feature %in% colnames(seurat_obj@meta.data)) {
      is_tumor <<- (seurat_obj@meta.data[[tumor_feature]] > tumor_cutoff) & !is_vessel
    }
  })

  # 3. Compute spatial sanctuary
  calc <- ComputeSpatialSanctuary(
    coords = coords,
    is_vessel = is_vessel,
    is_tumor = is_tumor,
    spot_pitch_um = spot_pitch_um,
    lambda_um = lambda_um,
    r0_um = r0_um,
    rcrit_um = rcrit_um
  )

  # 4. Attach to meta.data
  seurat_obj@meta.data$distance_to_nearest_capillary_um <- calc$distance_to_nearest_capillary_um
  seurat_obj@meta.data$bessel_drug_concentration_ratio <- calc$bessel_drug_concentration_ratio
  seurat_obj@meta.data$sanctuary_class <- calc$sanctuary_class
  seurat_obj@meta.data$is_sanctuary_spot <- calc$is_sanctuary_spot

  if (!is.list(seurat_obj@misc)) {
    seurat_obj@misc <- list()
  }
  seurat_obj@misc$spatial_continuum <- calc$summary

  return(seurat_obj)
}
