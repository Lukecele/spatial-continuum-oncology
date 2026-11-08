#!/usr/bin/env Rscript
# ==============================================================================
# Comprehensive Unit Test Suite for spatialcontinuum R Bridge
# ==============================================================================

# Dynamically locate spatial_continuum.R relative to this script or repo root
script_dir <- tryCatch({
  dirname(normalizePath(sys.frame(1)$ofile))
}, error = function(e) {
  getwd()
})
r_file <- file.path(script_dir, "../R/spatial_continuum.R")
if (!file.exists(r_file)) {
  r_file <- file.path(getwd(), "R/spatial_continuum.R")
}
if (!file.exists(r_file)) {
  r_file <- "/home/luca/Scrivania/STUDIO_CONTINUUM_ONCOLOGIA_CELEBRANO/R/spatial_continuum.R"
}
if (file.exists(r_file)) {
  source(r_file)
}

cat("================================================================\n")
cat("🧪 RUNNING UNIT TESTS FOR SPATIAL CONTINUUM R MODULE\n")
cat("================================================================\n")

test_count <- 0
fail_count <- 0

assert <- function(condition, message) {
  test_count <<- test_count + 1
  if (!condition) {
    fail_count <<- fail_count + 1
    cat(sprintf("❌ FAIL: %s\n", message))
  } else {
    cat(sprintf("✓ PASS: %s\n", message))
  }
}

# -----------------------------------------------------------------------------
# Test 1: CalculateCRI extreme tiers and exact weights
# -----------------------------------------------------------------------------
cat("\n--- Test Suite 1: In Silico CalculateCRI (RUO) ---\n")

# Tier 1 patient: Lepidic (0.0), Double WT (0.0), Loose (0.0)
p1 <- CalculateCRI("Lepidic", tp53 = "wt", rb1 = "wt", stroma = "loose")
assert(p1$CRI == 0.000, "Tier 1 CRI must be 0.000")
assert(grepl("Tier 1", p1$Risk_Tier), "Risk Tier must be Tier 1")
assert(grepl("Tier 1", p1$Action_Directive), "Directive must identify Tier 1 profile")
assert(p1$Sanctuary_Delta_r_um == 0.0, "Delta r for Lepidic/Loose must be 0 um")

# Tier 3 patient: Solid (1.0), Double Mut (1.0), Dense (1.0)
p3 <- CalculateCRI("Solid", tp53 = "mut", rb1 = "mut", stroma = "dense")
assert(p3$CRI == 1.000, "Tier 3 CRI must be 1.000")
assert(grepl("Tier 3", p3$Risk_Tier), "Risk Tier must be Tier 3")
assert(grepl("Tier 3", p3$Action_Directive), "Directive must identify Tier 3 profile")
assert(p3$Sanctuary_Delta_r_um == 34.1, "Delta r for Solid/Dense must approach 34.1 um")

# Intermediate patient: Acinar (0.35), TP53 mut only (0.50), Moderate (0.50)
# CRI = 0.47 * 0.35 + 0.33 * 0.50 + 0.20 * 0.50 = 0.1645 + 0.165 + 0.100 = 0.4295 -> 0.430
p2 <- CalculateCRI("Acinar", tp53 = "mut", rb1 = "wt", stroma = "moderate")
assert(abs(p2$CRI - 0.430) < 0.002, sprintf("Tier 2 CRI calculation matches formula (got %f)", p2$CRI))
assert(grepl("Tier 2", p2$Risk_Tier), "Risk Tier must be Tier 2")

# -----------------------------------------------------------------------------
# Test 2: BesselK0Concentration physical decay
# -----------------------------------------------------------------------------
cat("\n--- Test Suite 2: Bessel K0 Transport Physics ---\n")

# Within vessel (r <= 8.0)
c_vessel <- BesselK0Concentration(c(0, 4, 8))
assert(all(c_vessel == 1.0), "Concentration inside capillary wall must be clamped to 1.0")

# Monotonic decay
dists <- c(10, 25.5, 50, 100, 165.9, 200)
c_profile <- BesselK0Concentration(dists, lambda = 25.5, r0 = 8.0)
assert(all(diff(c_profile) < 0), "Concentration must strictly monotonically decrease with radial distance")

# Effective penetration vs sanctuary threshold
c_rcrit <- BesselK0Concentration(165.9, lambda = 25.5, r0 = 8.0)
assert(c_rcrit < 0.05, sprintf("Concentration at rcrit (165.9 um) must be sub-therapeutic (< 0.05, got %f)", c_rcrit))

# -----------------------------------------------------------------------------
# Test 3: ComputeSpatialSanctuary KD-Tree coordinates and classification
# -----------------------------------------------------------------------------
cat("\n--- Test Suite 3: ComputeSpatialSanctuary Matrix & KD-Tree ---\n")

# Synthetic tissue coordinates:
# Spot 1: Capillary at (0, 0)
# Spot 2: Tumor spot at (50, 0) -> distance = 50 um (< 100 um, Effective)
# Spot 3: Tumor spot at (120, 0) -> distance = 120 um (Attenuated)
# Spot 4: Tumor spot at (250, 0) -> distance = 250 um (> 165.9 um, Sanctuary)
# Spot 5: Stroma spot at (300, 0)
coords <- matrix(c(
  0.0, 0.0,
  50.0, 0.0,
  120.0, 0.0,
  250.0, 0.0,
  300.0, 0.0
), ncol = 2, byrow = TRUE)

is_vessel <- c(TRUE, FALSE, FALSE, FALSE, FALSE)
is_tumor <- c(FALSE, TRUE, TRUE, TRUE, FALSE)

res_spatial <- ComputeSpatialSanctuary(
  coords = coords,
  is_vessel = is_vessel,
  is_tumor = is_tumor,
  spot_pitch_um = 1.0,
  lambda_um = 25.5,
  r0_um = 8.0,
  rcrit_um = 165.9
)

assert(res_spatial$distance_to_nearest_capillary_um[1] == 0.0, "Capillary spot distance must be 0 um")
assert(res_spatial$distance_to_nearest_capillary_um[2] == 50.0, "Spot 2 distance must be 50 um")
assert(res_spatial$distance_to_nearest_capillary_um[3] == 120.0, "Spot 3 distance must be 120 um")
assert(res_spatial$distance_to_nearest_capillary_um[4] == 250.0, "Spot 4 distance must be 250 um")

assert(res_spatial$sanctuary_class[1] == "Capillary (Endothelial)", "Class 1 matches capillary")
assert(res_spatial$sanctuary_class[2] == "Effective Penetration (<100 um)", "Class 2 matches effective")
assert(res_spatial$sanctuary_class[3] == "Attenuated Zone (100-166 um)", "Class 3 matches attenuated")
assert(res_spatial$sanctuary_class[4] == "Pharmacological Sanctuary (>166 um)", "Class 4 matches sanctuary")
assert(res_spatial$sanctuary_class[5] == "Stroma / Normal Parenchyma", "Class 5 matches stroma")

assert(res_spatial$is_sanctuary_spot[4] == TRUE, "Spot 4 must be flagged as sanctuary")
assert(res_spatial$is_sanctuary_spot[2] == FALSE, "Spot 2 must NOT be flagged as sanctuary")

assert(res_spatial$summary$total_spots == 5, "Total spots count must be 5")
assert(res_spatial$summary$tumor_spots == 3, "Tumor spots count must be 3")
assert(res_spatial$summary$sanctuary_spots == 1, "Sanctuary spots count must be 1")
assert(abs(res_spatial$summary$sanctuary_fraction_pct - 33.33) < 0.1, "Sanctuary percentage must be 33.33%")

# Error handling: missing capillaries
err_caught <- FALSE
tryCatch({
  ComputeSpatialSanctuary(coords, is_vessel = c(FALSE, FALSE, FALSE, FALSE, FALSE))
}, error = function(e) {
  err_caught <<- TRUE
})
assert(err_caught, "ComputeSpatialSanctuary must throw error when no capillaries are present")

cat("\n================================================================\n")
cat(sprintf("RESULTS: %d / %d TESTS PASSED (Failures: %d)\n", test_count - fail_count, test_count, fail_count))
cat("================================================================\n")

if (fail_count > 0) {
  quit(status = 1)
} else {
  cat("🚀 ALL R BRIDGE UNIT TESTS PASSED WITH 100% SUCCESS!\n")
}
