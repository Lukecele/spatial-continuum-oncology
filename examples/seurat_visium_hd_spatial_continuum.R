#!/usr/bin/env Rscript
# ==============================================================================
# Visium HD 10x Subcellular Spatial Benchmark in R (Seurat & Spatial Interop)
# ==============================================================================
# Author: Luca Celebrano, MD Candidate, Università degli Studi di Napoli Federico II
# Framework: Spatial-Genomic Oncology Continuum
# Scientific Anchors: Research Square DOI: 10.21203/rs.3.rs-11530312/v1
#                    Zenodo DOI: 10.5281/zenodo.23754999
# ==============================================================================

source("/home/luca/Scrivania/STUDIO_CONTINUUM_ONCOLOGIA_CELEBRANO/R/spatial_continuum.R")

cat("================================================================\n")
cat("🧬 R / BIOCONDUCTOR VISIUM HD SUBCELLULAR SANCTUARY BENCHMARK\n")
cat("================================================================\n")

root_dir <- "/home/luca/Scrivania/STUDIO_CONTINUUM_ONCOLOGIA_CELEBRANO"
json_path <- file.path(root_dir, "visium_data.json")
out_png <- file.path(root_dir, "figure_scientifiche", "R_VisiumHD_Bessel_Sanctuary_Benchmark.png")

# 1. Load real 10x Visium HD tissue spots
cat("[*] Loading real 10x Visium HD lung adenocarcinoma biopsy from visium_data.json...\n")
if (!requireNamespace("jsonlite", quietly = TRUE)) {
  # Fast base R JSON parser for array of 4-element vectors
  raw_text <- readChar(json_path, file.info(json_path)$size)
  # Replace brackets to parse numeric matrix
  clean_text <- gsub("\\[|\\]", "", raw_text)
  nums <- as.numeric(strsplit(clean_text, ",")[[1]])
  mat <- matrix(nums, ncol = 4, byrow = TRUE)
} else {
  mat <- as.matrix(jsonlite::fromJSON(json_path))
}

coords <- mat[, 1:2]
types <- mat[, 3]

# Classification mapping: 1=endo, 2=sanctuary, 3=attenuated, 4=effective, 0=stroma, 5=parenchyma
is_vessel <- types == 1
is_tumor <- (types >= 2) & (types <= 4)

cat(sprintf("[✓] Loaded %d spots (Vessels: %d, Viable Tumor: %d)\n", nrow(coords), sum(is_vessel), sum(is_tumor)))

# 2. Compute Bessel reaction-diffusion sanctuary metrics
cat("[*] Executing ComputeSpatialSanctuary() in R...\n")
res <- ComputeSpatialSanctuary(
  coords = coords,
  is_vessel = is_vessel,
  is_tumor = is_tumor,
  spot_pitch_um = 1.0, # 1 coordinate unit
  lambda_um = 25.5,
  r0_um = 8.0,
  rcrit_um = 165.9
)

stats <- res$summary
cat("\n[✓] Tissue Sanctuary Burden Computed in R:\n")
cat(sprintf("    • Total Analyzed Spots:       %d\n", stats$total_spots))
cat(sprintf("    • Capillaries (CD31+):        %d\n", stats$vessel_spots))
cat(sprintf("    • Viable Carcinoma Spots:     %d\n", stats$tumor_spots))
cat(sprintf("    • Pharmacological Sanctuary:  %d spots (%.1f%%)\n", stats$sanctuary_spots, stats$sanctuary_fraction_pct))
cat(sprintf("    • Median Tumor-Vessel Dist:   %.1f um\n", stats$median_tumor_vessel_distance_um))
cat(sprintf("    • Mean Tumor-Vessel Dist:     %.1f um\n", stats$mean_tumor_vessel_distance_um))

# 3. Generate high-resolution 300 DPI multi-panel publication plot in R
cat("[*] Rendering 300 DPI multi-panel plot to:", out_png, "\n")
png(out_png, width = 3600, height = 1200, res = 300, bg = "#0b0f19")
par(mfrow = c(1, 3), mar = c(4.5, 4.5, 3.5, 2.0), col.axis = "#64748b", col.lab = "#94a3b8", col.main = "#f8fafc", fg = "#334155")

# Panel A: Spatial Spots Map
color_map <- rep("#1e293b", nrow(coords)) # stroma/normal
color_map[res$sanctuary_class == "Effective Penetration (<100 um)"] <- "#06b6d4"
color_map[res$sanctuary_class == "Attenuated Zone (100-166 um)"] <- "#eab308"
color_map[res$sanctuary_class == "Pharmacological Sanctuary (>166 um)"] <- "#f97316"
color_map[is_vessel] <- "#f43f5e"

plot(coords[, 1], coords[, 2], col = color_map, pch = 16, cex = ifelse(is_vessel, 0.8, 0.5),
     xlab = "Tissue Coordinate X", ylab = "Tissue Coordinate Y",
     main = "A. Visium HD Spatial Sanctuary Map (R)",
     bty = "n")
grid(col = "#1e293b")
points(coords[is_vessel, 1], coords[is_vessel, 2], col = "#f43f5e", pch = 16, cex = 0.9)
legend("topright", legend = c("Capillary (CD31+)", "Effective (<100 um)", "Attenuated (100-166 um)", "Sanctuary (>166 um)"),
       col = c("#f43f5e", "#06b6d4", "#eab308", "#f97316"), pch = 16, bty = "n", cex = 0.8, text.col = "#e2e8f0")

# Panel B: Continuous Bessel Field
conc <- res$bessel_drug_concentration_ratio
# Custom dark inferno palette
inferno_cols <- colorRampPalette(c("#070a13", "#3b0f70", "#8c2981", "#de4968", "#fe9f6d", "#fcfdbf"))(100)
conc_idx <- pmax(1, pmin(100, round(conc * 99) + 1))

plot(coords[, 1], coords[, 2], col = inferno_cols[conc_idx], pch = 16, cex = 0.55,
     xlab = "Tissue Coordinate X", ylab = "Tissue Coordinate Y",
     main = "B. Bessel Reaction-Diffusion Gradient C(r)/C0",
     bty = "n")
grid(col = "#1e293b")
points(coords[is_vessel, 1], coords[is_vessel, 2], col = "#38bdf8", pch = 16, cex = 0.8)

# Panel C: Sanctuary Distance Distribution
tumor_dists <- res$distance_to_nearest_capillary_um[is_tumor]
h <- hist(tumor_dists, breaks = 35, plot = FALSE)

# Color histogram bars based on sanctuary cutoffs
bar_cols <- ifelse(h$mids < 100, "#06b6d4", ifelse(h$mids < 165.9, "#eab308", "#f97316"))
plot(h, col = bar_cols, border = "#0b0f19",
     xlab = "Perivascular Distance (um)", ylab = "Viable Carcinoma Spots",
     main = "C. Microvascular Distance Distribution",
     bty = "n")
grid(col = "#1e293b")
abline(v = 165.9, col = "#f43f5e", lty = 2, lwd = 2)
abline(v = stats$median_tumor_vessel_distance_um, col = "#38bdf8", lty = 3, lwd = 2)
legend("topright", legend = c(sprintf("rcrit = 165.9 um (Sanctuary: %.1f%%)", stats$sanctuary_fraction_pct),
                              sprintf("Median = %.1f um", stats$median_tumor_vessel_distance_um)),
       col = c("#f43f5e", "#38bdf8"), lty = c(2, 3), lwd = 2, bty = "n", cex = 0.85, text.col = "#e2e8f0")

dev.off()
cat("[✓] Figure saved successfully:", out_png, "\n")
cat("================================================================\n")
cat("🚀 SENTIERO 3 R / SEURAT BENCHMARK COMPLETED WITH 100% SUCCESS!\n")
cat("================================================================\n")
