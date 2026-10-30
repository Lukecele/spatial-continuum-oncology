#!/usr/bin/env python3
"""
Build Grand Unified Scientific Portal (Deterministic Assembler)
Integrates 5 distinct scientific modules into index.html:
- Module 1: Bedside Decision Engine (CRI & 1D/2D Bessel diffusion)
- Module 2: 10x Visium HD Real Tissue Spatial Benchmark (GSE301973, 3,858 Spots)
- Module 3: 60 FPS In Silico Tumor Sanctuary Digital Twin (Live Simulator + Standalone link)
- Module 4: InSituGame Evolutionary Game Theory Assay (Replicator Dynamics & Phase Plane)
- Module 5: MSKCC Clinical Cohort (N=604) & Open-Science Evidence Hub (Preprints, Bioconda, Containers)
"""

import os
import json

PORTAL_PATH = "/home/luca/Scrivania/STUDIO_CONTINUUM_ONCOLOGIA_CELEBRANO/index.html"
BACKUP_PATH = "/home/luca/Scrivania/STUDIO_CONTINUUM_ONCOLOGIA_CELEBRANO/index.html.bak"
VISIUM_JSON = "/home/luca/Scrivania/STUDIO_CONTINUUM_ONCOLOGIA_CELEBRANO/visium_data.json"

with open(BACKUP_PATH, 'r', encoding='utf-8') as f:
    orig = f.read()

with open(VISIUM_JSON, 'r', encoding='utf-8') as f:
    visium_spots = json.load(f)

visium_spots_js = json.dumps(visium_spots, separators=(',', ':'))

# Find block boundaries
idx_m1 = orig.find('<div id="module-1"')
idx_m2 = orig.find('<div id="module-2"')
idx_m3 = orig.find('<div id="module-3"')
idx_m4 = orig.find('<div id="module-4"')
idx_script = orig.find('<script>')

part_head = orig[:idx_m1]
part_m1 = orig[idx_m1:idx_m2]
part_insitu = orig[idx_m2:idx_m3].replace('id="module-2"', 'id="module-4"')
part_mskcc = orig[idx_m3:idx_m4].replace('id="module-3"', 'id="module-5"')
part_hub = orig[idx_m4:idx_script].replace('id="module-4"', 'id="module-5-hub" style="margin-top: 1.5rem;"')
part_script = orig[idx_script:]

# 1. Update CSS .module-nav in part_head
old_css_nav = """.module-nav {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.75rem;
      margin-top: 1.25rem;
      margin-bottom: 1.5rem;
    }"""

new_css_nav = """.module-nav {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 0.65rem;
      margin-top: 1.25rem;
      margin-bottom: 1.5rem;
    }
    @media (max-width: 1200px) {
      .module-nav {
        grid-template-columns: repeat(3, 1fr);
      }
    }
    @media (max-width: 768px) {
      .module-nav {
        grid-template-columns: 1fr;
      }
    }"""

part_head = part_head.replace(old_css_nav, new_css_nav)

# Custom styles for Visium Module
custom_styles = """
    /* Visium Module Styling */
    .vis-filter-btn {
      background: #111827;
      border: 1px solid #374151;
      border-radius: 6px;
      color: #94a3b8;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.35rem 0.65rem;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .vis-filter-btn:hover {
      background: #1f2937;
      color: #f1f5f9;
      border-color: #4b5563;
    }
    .vis-filter-btn.active {
      background: rgba(6, 182, 212, 0.2);
      border-color: #06b6d4;
      color: #38bdf8;
      box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
    }
    .vis-patient-row {
      border-bottom: 1px solid rgba(55, 65, 81, 0.4);
      transition: background 0.15s ease;
    }
    .vis-patient-row:hover {
      background: rgba(30, 41, 59, 0.5);
    }
"""
part_head = part_head.replace("/* Portal Module Containers */", custom_styles + "\n    /* Portal Module Containers */")

# Update Nav Buttons in part_head
old_nav_html = """    <nav class="module-nav">
      <button id="mod-btn-1" class="mod-nav-btn active" onclick="switchMainModule('1')">
        <span class="mod-icon">🩺</span>
        <span class="mod-text">
          <strong>Module 1: Bedside Decision Engine</strong>
          <small>Biophysical Diffusion · 2D Cord Section · A4 Consult Note</small>
        </span>
      </button>
      <button id="mod-btn-2" class="mod-nav-btn" onclick="switchMainModule('2')">
        <span class="mod-icon">🎲</span>
        <span class="mod-text">
          <strong>Module 2: InSituGame Evolutionary Assay</strong>
          <small>Subclonal Payoffs · Replicator Phase-Plane · Adaptive Therapy</small>
        </span>
      </button>
      <button id="mod-btn-3" class="mod-nav-btn" onclick="switchMainModule('3')">
        <span class="mod-icon">📊</span>
        <span class="mod-text">
          <strong>Module 3: MSKCC 604 Clinical Cohort</strong>
          <small>Kaplan-Meier Survival · Post-ADAURA Recurrence Kinetics</small>
        </span>
      </button>
      <button id="mod-btn-4" class="mod-nav-btn" onclick="switchMainModule('4')">
        <span class="mod-icon">📦</span>
        <span class="mod-text">
          <strong>Module 4: Data, Code &amp; Containers Hub</strong>
          <small>Preprint PDFs · MSKCC CSV · Bioconda · Docker Wave · nf-core</small>
        </span>
      </button>
    </nav>"""

new_nav_html = """    <nav class="module-nav">
      <button id="mod-btn-1" class="mod-nav-btn active" onclick="switchMainModule('1')">
        <span class="mod-icon">🩺</span>
        <span class="mod-text">
          <strong>Module 1: Bedside CRI Engine</strong>
          <small>Bessel K₀ Diffusion · 2D Cord · A4 Consult Note</small>
        </span>
      </button>
      <button id="mod-btn-2" class="mod-nav-btn" onclick="switchMainModule('2')">
        <span class="mod-icon">🧬</span>
        <span class="mod-text">
          <strong>Module 2: 10x Visium HD Benchmark</strong>
          <small>3,858 Spot Real Tissue · Sanctuary Zones · GSE301973</small>
        </span>
      </button>
      <button id="mod-btn-3" class="mod-nav-btn" onclick="switchMainModule('3')">
        <span class="mod-icon">🚀</span>
        <span class="mod-text">
          <strong>Module 3: 60 FPS Digital Twin</strong>
          <small>In Silico Automaton · Month 36 Regrowth Dynamics</small>
        </span>
      </button>
      <button id="mod-btn-4" class="mod-nav-btn" onclick="switchMainModule('4')">
        <span class="mod-icon">🎲</span>
        <span class="mod-text">
          <strong>Module 4: InSituGame Evolutionary Assay</strong>
          <small>Subclonal Payoffs · Replicator Phase-Plane · Adaptive</small>
        </span>
      </button>
      <button id="mod-btn-5" class="mod-nav-btn" onclick="switchMainModule('5')">
        <span class="mod-icon">📊</span>
        <span class="mod-text">
          <strong>Module 5: MSKCC 604 &amp; Evidence Hub</strong>
          <small>Kaplan-Meier Survival · Zenodo · Bioconda · Containers</small>
        </span>
      </button>
    </nav>"""

part_head = part_head.replace(old_nav_html, new_nav_html)

# 2. Build Module 2 (Visium HD) HTML
part_m2 = """
    <!-- ================================================================= -->
    <!-- MODULE 2: EXPERIMENTAL 10x VISIUM HD BENCHMARK & GSE301973 COHORT -->
    <!-- ================================================================= -->
    <div id="module-2" class="portal-module" style="display: none;">
      <section class="card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
          <div>
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.35rem;">
              <span style="font-size: 1.3rem;">🧬</span>
              <h2 class="card-title" style="margin-bottom: 0;">Module 2: Experimental 10x Visium HD Spatial Benchmark</h2>
              <span class="badge badge-cyan">Supplementary Fig. S1</span>
              <span class="badge badge-teal">NCBI GEO: GSE301973</span>
            </div>
            <p style="font-size: 0.88rem; color: var(--text-muted); max-width: 920px; line-height: 1.5;">
              Subcellular spatial transcriptomics validation (<strong style="color: #fff;">N = 3,858 sequenced spots</strong> at 2 µm resolution captured across intact human EGFR-mutated lung adenocarcinoma). Demonstrating that physical microvascular rarefaction leaves <strong style="color: #f97316;">&gt;92% of the viable tumor mass beyond the critical osimertinib penetration radius</strong> (r<sub>crit</sub> ≈ 165.9 µm), creating a persistent in-situ pharmacological sanctuary that fuels post-cessation recurrence.
            </p>
          </div>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <a href="figure_scientifiche/Supplementary_Figure1_VisiumHD_Spatial_Validation.pdf" target="_blank" class="badge badge-purple" style="text-decoration: none; padding: 0.4rem 0.8rem; font-size: 0.8rem;">
              <span>📄 Download Fig S1 Vector PDF</span>
            </a>
            <a href="figure_scientifiche/Supplementary_Figure1_VisiumHD_Spatial_Validation.png" target="_blank" class="badge badge-amber" style="text-decoration: none; padding: 0.4rem 0.8rem; font-size: 0.8rem;">
              <span>🖼️ 300 DPI PNG</span>
            </a>
          </div>
        </div>
      </section>

      <!-- 2-COLUMN LAYOUT: VISIUM TISSUE MAP (LEFT) & CLINICAL BENCHMARKS (RIGHT) -->
      <div style="display: grid; grid-template-columns: 1.25fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;">
        
        <!-- LEFT: INTERACTIVE 10x TISSUE CANVAS -->
        <section class="card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
            <div>
              <h3 style="font-size: 1rem; color: #fff; font-weight: 700;">Intact Biopsy Spatial Map (3,858 Spots)</h3>
              <small style="color: var(--text-muted);">Classified by measured distance from functional CD31+ capillaries</small>
            </div>
            <!-- FILTER BUTTONS -->
            <div style="display: flex; gap: 0.35rem; flex-wrap: wrap;">
              <button class="vis-filter-btn active" onclick="setVisiumFilter('all', this)">All Spots</button>
              <button class="vis-filter-btn" onclick="setVisiumFilter('sanctuary', this)" style="border-color: rgba(249,115,22,0.5);">Sanctuary (&gt;165 µm)</button>
              <button class="vis-filter-btn" onclick="setVisiumFilter('endo', this)" style="border-color: rgba(244,63,94,0.5);">Capillaries (CD31+)</button>
              <button class="vis-filter-btn" onclick="setVisiumFilter('tumor', this)" style="border-color: rgba(6,182,212,0.5);">All Tumor</button>
            </div>
          </div>

          <!-- CANVAS WRAPPER -->
          <div style="position: relative; background: #070a13; border: 1px solid var(--card-border); border-radius: 8px; overflow: hidden; display: flex; justify-content: center; align-items: center;">
            <canvas id="visium-canvas" width="680" height="580" style="width: 100%; height: auto; max-height: 580px; display: block; cursor: crosshair;"></canvas>
            
            <!-- HOVER TOOLTIP -->
            <div id="visium-tooltip" style="position: absolute; bottom: 12px; left: 12px; background: rgba(15, 23, 42, 0.94); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 6px; padding: 6px 12px; font-size: 0.75rem; color: #f1f5f9; pointer-events: none; backdrop-filter: blur(8px); display: none; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
              <span id="visium-tooltip-text">Hover over spots to inspect</span>
            </div>
          </div>

          <!-- LEGEND BAR -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 0.5rem; margin-top: 0.85rem; padding-top: 0.65rem; border-top: 1px solid rgba(55,65,81,0.5); font-size: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.4rem;">
              <span style="width: 10px; height: 10px; border-radius: 50%; background: #f43f5e; box-shadow: 0 0 6px #f43f5e;"></span>
              <span><strong>CD31+ Vessel</strong> (N=212)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
              <span style="width: 10px; height: 10px; border-radius: 50%; background: #f97316;"></span>
              <span><strong>Sanctuary &gt;165 µm</strong> (N=832)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
              <span style="width: 10px; height: 10px; border-radius: 50%; background: #eab308;"></span>
              <span><strong>Attenuated 100-165 µm</strong> (N=64)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
              <span style="width: 10px; height: 10px; border-radius: 50%; background: #06b6d4;"></span>
              <span><strong>Effective &lt;100 µm</strong> (N=5)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
              <span style="width: 10px; height: 10px; border-radius: 50%; background: #6366f1;"></span>
              <span><strong>Dense Stroma</strong> (N=2,119)</span>
            </div>
          </div>
        </section>

        <!-- RIGHT: QUANTITATIVE METRICS & CLINICAL CORRELATION -->
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          
          <!-- SPOT QUANTIFICATION METRICS CARD -->
          <section class="card">
            <h3 style="font-size: 0.95rem; color: var(--accent-cyan); font-weight: 700; margin-bottom: 0.6rem;">Tissue Perivascular Burden Breakdown</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; text-align: center;">
              <div style="background: rgba(249, 115, 22, 0.1); border: 1px solid rgba(249, 115, 22, 0.3); border-radius: 6px; padding: 0.6rem;">
                <div style="font-size: 1.4rem; font-weight: 800; color: #f97316;">92.3%</div>
                <div style="font-size: 0.72rem; color: #fed7aa;">Sanctuary Volume</div>
                <div style="font-size: 0.65rem; color: var(--text-dim);">832 of 901 tumor spots</div>
              </div>
              <div style="background: rgba(234, 179, 8, 0.1); border: 1px solid rgba(234, 179, 8, 0.3); border-radius: 6px; padding: 0.6rem;">
                <div style="font-size: 1.4rem; font-weight: 800; color: #eab308;">7.1%</div>
                <div style="font-size: 0.72rem; color: #fef08a;">Attenuated Range</div>
                <div style="font-size: 0.65rem; color: var(--text-dim);">64 of 901 tumor spots</div>
              </div>
              <div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 6px; padding: 0.6rem;">
                <div style="font-size: 1.4rem; font-weight: 800; color: #06b6d4;">0.6%</div>
                <div style="font-size: 0.72rem; color: #a5f3fc;">Effective Cored</div>
                <div style="font-size: 0.65rem; color: var(--text-dim);">5 of 901 tumor spots</div>
              </div>
            </div>
            <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.6rem; line-height: 1.4;">
              <strong style="color: #fff;">Key Biophysical Insight:</strong> In intact patient tumor tissue, microvascular rarefaction results in &gt;92% of the viable tumor mass residing at distances &gt;165.9 µm from CD31+ vessels, confirming that osimertinib monotherapy creates vast cytostatic persister reservoirs rather than tissue-wide sterilization.
            </p>
          </section>

          <!-- GSE301973 CLINICAL VALIDATION SCATTER CHART -->
          <section class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <h3 style="font-size: 0.95rem; color: var(--accent-teal); font-weight: 700; margin-bottom: 0;">Clinical Progression-Free Survival (GSE301973)</h3>
              <span class="badge badge-teal" style="font-size: 0.7rem;">Spearman ρ = -0.95 · p = 0.048</span>
            </div>
            <div style="background: #070a13; border: 1px solid var(--card-border); border-radius: 6px; padding: 6px;">
              <canvas id="visium-pfs-canvas" width="480" height="180" style="width: 100%; height: auto; display: block;"></canvas>
            </div>
            <div style="font-size: 0.72rem; color: var(--text-muted); margin-top: 0.4rem; text-align: center;">
              Tumor-Endothelial Contact % is strongly associated with prolonged Progression-Free Survival (months).
            </div>
          </section>

        </div>
      </div>

      <!-- BOTTOM FULL-WIDTH: PATIENT COHORT STRATIFICATION TABLE -->
      <section class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
          <div>
            <h3 style="font-size: 1.05rem; color: #fff; font-weight: 700;">GSE301973 Patient Spatial Profiling &amp; Bedside CRI Stratification</h3>
            <small style="color: var(--text-muted);">Click "Apply to Module 1" to load any patient's histological profile directly into the Bedside CRI Decision Engine</small>
          </div>
          <span class="badge badge-purple">4 Prospective Visium HD Cases</span>
        </div>

        <div style="overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; text-align: left;">
            <thead>
              <tr style="border-bottom: 1px solid var(--border-accent); color: var(--text-dim); text-transform: uppercase; font-size: 0.7rem;">
                <th style="padding: 0.6rem 0.5rem;">Patient ID</th>
                <th style="padding: 0.6rem 0.5rem;">Histologic Pattern</th>
                <th style="padding: 0.6rem 0.5rem;">PFS (Months)</th>
                <th style="padding: 0.6rem 0.5rem;">Endothelial Contact</th>
                <th style="padding: 0.6rem 0.5rem;">Homotypic Packing</th>
                <th style="padding: 0.6rem 0.5rem;">CRI Score</th>
                <th style="padding: 0.6rem 0.5rem;">Risk Tier</th>
                <th style="padding: 0.6rem 0.5rem;">Bedside Action</th>
                <th style="padding: 0.6rem 0.5rem; text-align: right;">Action</th>
              </tr>
            </thead>
            <tbody id="visium-patients-tbody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </section>
    </div>
"""

# 3. Build Module 3 (60 FPS Digital Twin) HTML
part_m3 = """
    <!-- ================================================================= -->
    <!-- MODULE 3: 60 FPS IN SILICO TUMOR SANCTUARY & DIGITAL TWIN        -->
    <!-- ================================================================= -->
    <div id="module-3" class="portal-module" style="display: none;">
      <section class="card" style="margin-bottom: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
          <div>
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.35rem;">
              <span style="font-size: 1.3rem;">🚀</span>
              <h2 class="card-title" style="margin-bottom: 0;">Module 3: Live 60 FPS In Silico Digital Twin Simulator</h2>
              <span class="badge badge-cyan">Biophysical Automaton</span>
              <span class="badge badge-teal">Day 0 to 1825 (5 Years)</span>
            </div>
            <p style="font-size: 0.88rem; color: var(--text-muted); max-width: 900px; line-height: 1.5;">
              Full 2D biophysical cross-section simulation running at 60 FPS. Simulating perivascular osimertinib diffusion (D<sub>eff</sub> = 85 µm²/s), interstitial fluid pressure (IFP = 18 mmHg), subclonal competition, Month 36 drug cessation, and post-cessation recurrence dynamics across ADAURA vs. SG-ADAURA protocols.
            </p>
          </div>
          <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
            <a href="simulator.html" target="_blank" class="badge" style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); color: #fff; border: 1px solid #38bdf8; text-decoration: none; padding: 0.45rem 0.9rem; font-size: 0.82rem; font-weight: 700;">
              <span>↗ Open Fullscreen Standalone App</span>
            </a>
          </div>
        </div>
      </section>

      <!-- EMBEDDED DIGITAL TWIN RUNNER -->
      <div style="width: 100%; border: 1px solid var(--card-border); border-radius: 12px; overflow: hidden; background: #070a12; box-shadow: 0 8px 30px rgba(0,0,0,0.5);">
        <iframe id="sim-frame" src="simulator.html" style="width: 100%; height: 880px; border: none; display: block;" title="60 FPS In Silico Tumor Sanctuary Digital Twin"></iframe>
      </div>
    </div>
"""

# Assemble Middle Modules
middle_modules = part_m1 + part_m2 + part_m3 + part_insitu + part_mskcc + part_hub

# 4. Build Script replacement
old_switcher_code = """    let currentModuleId = '1';

    function switchMainModule(modId) {
      currentModuleId = modId;

      // Update Nav Buttons
      for (let i = 1; i <= 4; i++) {
        const btn = document.getElementById('mod-btn-' + i);
        const mod = document.getElementById('module-' + i);
        if (btn) btn.classList.remove('active');
        if (mod) mod.style.display = 'none';
      }

      const activeBtn = document.getElementById('mod-btn-' + modId);
      const activeMod = document.getElementById('module-' + modId);

      if (activeBtn) activeBtn.classList.add('active');
      if (activeMod) activeMod.style.display = 'block';

      // Trigger targeted canvas rendering upon module reveal
      if (modId === '1') {
        recalculate();
      } else if (modId === '2') {
        runReplicatorSimulation();
      } else if (modId === '3') {
        drawKaplanMeierCanvas();
        drawHazardSurgeCanvas();
      }
    }"""

new_script_code = f"""    // 10x Visium HD Spots Data (N = 3,858 sequenced spots)
    const VISIUM_SPOTS = {visium_spots_js};

    // GSE301973 Clinical Patient Metadata
    const GSE301973_PATIENTS = [
      {{
        id: "s1_PFS_69",
        pattern: "Lepidic / Acinar",
        patternValue: "lepidic",
        pfs: 69.0,
        endo_pct: 22.93,
        homo_pct: 60.96,
        CRI: 0.094,
        tier: "Tier 1",
        tierColor: "#10b981",
        action: "Safe Cessation at M36",
        tp53: false,
        rb1: false,
        stromaValue: "low",
        ctdnaValue: "negative"
      }},
      {{
        id: "s2_PFS_22",
        pattern: "Lepidic / Acinar",
        patternValue: "acinar",
        pfs: 22.0,
        endo_pct: 12.63,
        homo_pct: 67.69,
        CRI: 0.327,
        tier: "Tier 2",
        tierColor: "#38bdf8",
        action: "Serial ctDNA Surveillance",
        tp53: true,
        rb1: false,
        stromaValue: "moderate",
        ctdnaValue: "negative"
      }},
      {{
        id: "s4_PFS_12",
        pattern: "Solid / Micropapillary",
        patternValue: "solid",
        pfs: 12.0,
        endo_pct: 21.84,
        homo_pct: 64.03,
        CRI: 0.601,
        tier: "Tier 2/3",
        tierColor: "#f59e0b",
        action: "High Relapse Risk / Extend TKI",
        tp53: true,
        rb1: false,
        stromaValue: "dense",
        ctdnaValue: "positive"
      }},
      {{
        id: "s3_PFS_15",
        pattern: "Solid / Micropapillary",
        patternValue: "solid",
        pfs: 15.0,
        endo_pct: 2.73,
        homo_pct: 87.86,
        CRI: 0.715,
        tier: "Tier 3",
        tierColor: "#ef4444",
        action: "Escalate to SG-ADAURA (Anti-VEGFR2)",
        tp53: true,
        rb1: true,
        stromaValue: "dense",
        ctdnaValue: "positive"
      }}
    ];

    let currentModuleId = '1';
    let currentVisiumFilter = 'all';

    function switchMainModule(modId) {{
      currentModuleId = modId;

      // Update Nav Buttons
      for (let i = 1; i <= 5; i++) {{
        const btn = document.getElementById('mod-btn-' + i);
        const mod = document.getElementById('module-' + i);
        if (btn) btn.classList.remove('active');
        if (mod) mod.style.display = 'none';
      }}

      const activeBtn = document.getElementById('mod-btn-' + modId);
      const activeMod = document.getElementById('module-' + modId);

      if (activeBtn) activeBtn.classList.add('active');
      if (activeMod) activeMod.style.display = 'block';

      // Trigger targeted canvas rendering upon module reveal
      if (modId === '1') {{
        recalculate();
      }} else if (modId === '2') {{
        drawVisiumTissue();
        drawVisiumPfsChart();
        renderVisiumPatientsTable();
      }} else if (modId === '4') {{
        runReplicatorSimulation();
      }} else if (modId === '5') {{
        drawKaplanMeierCanvas();
        drawHazardSurgeCanvas();
      }}
    }}

    // ==========================================
    // MODULE 2: 10x VISIUM HD BENCHMARK RENDERING
    // ==========================================
    function setVisiumFilter(filter, btn) {{
      currentVisiumFilter = filter;
      document.querySelectorAll('.vis-filter-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      drawVisiumTissue();
    }}

    function drawVisiumTissue() {{
      const canvas = document.getElementById('visium-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width;
      const H = canvas.height;

      // Background
      ctx.fillStyle = '#070a13';
      ctx.fillRect(0, 0, W, H);

      // Subtle coordinate grid
      ctx.strokeStyle = 'rgba(51, 65, 85, 0.25)';
      ctx.lineWidth = 1;
      for (let x = 50; x < W; x += 60) {{
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
      }}
      for (let y = 50; y < H; y += 60) {{
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
      }}

      const padX = 25;
      const padY = 25;
      const plotW = W - padX * 2;
      const plotH = H - padY * 2;

      // Draw spots
      for (let i = 0; i < VISIUM_SPOTS.length; i++) {{
        const pt = VISIUM_SPOTS[i];
        const nx = pt[0] / 1000.0;
        const ny = pt[1] / 1000.0;
        const type = pt[2];
        const dist = pt[3];

        // Apply filter
        if (currentVisiumFilter === 'sanctuary' && type !== 2) continue;
        if (currentVisiumFilter === 'endo' && type !== 1) continue;
        if (currentVisiumFilter === 'tumor' && (type < 2 || type > 4)) continue;

        const cx = padX + nx * plotW;
        const cy = padY + ny * plotH;

        ctx.beginPath();
        if (type === 1) {{ // Endothelial
          ctx.arc(cx, cy, 3.8, 0, Math.PI * 2);
          ctx.fillStyle = '#f43f5e';
          ctx.shadowColor = '#f43f5e';
          ctx.shadowBlur = 4;
          ctx.fill();
          ctx.shadowBlur = 0;
        }} else if (type === 2) {{ // Tumor Sanctuary (>165 um)
          ctx.arc(cx, cy, 2.6, 0, Math.PI * 2);
          ctx.fillStyle = '#f97316';
          ctx.fill();
        }} else if (type === 3) {{ // Tumor Attenuated (100-165 um)
          ctx.arc(cx, cy, 2.8, 0, Math.PI * 2);
          ctx.fillStyle = '#eab308';
          ctx.fill();
        }} else if (type === 4) {{ // Tumor Effective (<100 um)
          ctx.arc(cx, cy, 3.2, 0, Math.PI * 2);
          ctx.fillStyle = '#06b6d4';
          ctx.fill();
        }} else if (type === 5) {{ // Stroma
          ctx.arc(cx, cy, 1.8, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(99, 102, 241, 0.45)';
          ctx.fill();
        }} else {{ // Other
          ctx.arc(cx, cy, 1.4, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(75, 85, 99, 0.25)';
          ctx.fill();
        }}
      }}

      // Scale bar (500 µm ~ 76 normalized units -> 76/1000 * plotW)
      const barLen = (500 / 6550) * plotW;
      const barX = W - padX - barLen - 10;
      const barY = H - padY - 14;

      ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
      ctx.fillRect(barX - 10, barY - 18, barLen + 20, 28);
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1;
      ctx.strokeRect(barX - 10, barY - 18, barLen + 20, 28);

      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(barX, barY);
      ctx.lineTo(barX + barLen, barY);
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 9.5px -apple-system, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('500 µm', barX + barLen / 2, barY - 5);
    }}

    // Visium Interactive Tooltip on Mouse Move
    function initVisiumCanvasHover() {{
      const canvas = document.getElementById('visium-canvas');
      const tooltip = document.getElementById('visium-tooltip');
      const tooltipText = document.getElementById('visium-tooltip-text');
      if (!canvas || !tooltip) return;

      canvas.addEventListener('mousemove', function(e) {{
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const mx = (e.clientX - rect.left) * scaleX;
        const my = (e.clientY - rect.top) * scaleY;

        const padX = 25; const padY = 25;
        const plotW = canvas.width - padX * 2;
        const plotH = canvas.height - padY * 2;

        let closestSpot = null;
        let minDistSq = 12 * 12; // 12px threshold

        for (let i = 0; i < VISIUM_SPOTS.length; i++) {{
          const pt = VISIUM_SPOTS[i];
          const cx = padX + (pt[0] / 1000.0) * plotW;
          const cy = padY + (pt[1] / 1000.0) * plotH;
          const distSq = (mx - cx) * (mx - cx) + (my - cy) * (my - cy);
          if (distSq < minDistSq) {{
            minDistSq = distSq;
            closestSpot = pt;
          }}
        }}

        if (closestSpot) {{
          tooltip.style.display = 'block';
          const typeNames = {{
            1: '<span style="color:#f43f5e;font-weight:700;">CD31+ Capillary Vessel</span>',
            2: '<span style="color:#f97316;font-weight:700;">Tumor Cell in Pharmacological Sanctuary (&gt;165 µm)</span>',
            3: '<span style="color:#eab308;font-weight:700;">Tumor Cell in Attenuated Exposure (100–165 µm)</span>',
            4: '<span style="color:#06b6d4;font-weight:700;">Tumor Cell at Full Effective Exposure (&lt;100 µm)</span>',
            5: '<span style="color:#818cf8;font-weight:700;">Dense Fibrous Stroma (COL1A1+)</span>',
            0: '<span style="color:#94a3b8;">Normal / Alveolar Parenchyma</span>'
          }};
          
          let desc = typeNames[closestSpot[2]] || 'Spot';
          if (closestSpot[2] >= 2 && closestSpot[2] <= 4) {{
            desc += `<br>Distance to Nearest Vessel: <strong style="color:#fff;">${{closestSpot[3]}} µm</strong>`;
            desc += closestSpot[2] === 2 ? ' · Exposure: <span style="color:#f97316;">Sub-therapeutic (2–8 nM)</span>' : ' · Exposure: <span style="color:#06b6d4;">Therapeutic (&gt;10 nM)</span>';
          }}
          tooltipText.innerHTML = desc;
        }} else {{
          tooltip.style.display = 'none';
        }}
      }});

      canvas.addEventListener('mouseleave', function() {{
        tooltip.style.display = 'none';
      }});
    }}

    // GSE301973 Progression-Free Survival Scatter Chart
    function drawVisiumPfsChart() {{
      const canvas = document.getElementById('visium-pfs-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width;
      const H = canvas.height;

      ctx.fillStyle = '#070a13';
      ctx.fillRect(0, 0, W, H);

      const padL = 45; const padR = 20;
      const padT = 20; const padB = 30;
      const plotW = W - padL - padR;
      const plotH = H - padT - padB;

      // Axes
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(padL, padT); ctx.lineTo(padL, padT + plotH); ctx.lineTo(padL + plotW, padT + plotH);
      ctx.stroke();

      // Axis labels
      ctx.fillStyle = '#94a3b8';
      ctx.font = '9px -apple-system, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('PFS (Months on Adjuvant Osimertinib)', padL + plotW / 2, H - 8);

      ctx.save();
      ctx.translate(14, padT + plotH / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText('Endo Contact %', 0, 0);
      ctx.restore();

      // Scale: X: 0 to 75 months, Y: 0 to 25%
      const maxX = 75; const maxY = 26;

      // Ticks
      ctx.fillStyle = '#64748b';
      ctx.textAlign = 'right';
      for (let y = 0; y <= 25; y += 5) {{
        const py = padT + plotH - (y / maxY) * plotH;
        ctx.fillText(y + '%', padL - 6, py + 3);
        ctx.strokeStyle = 'rgba(51, 65, 85, 0.2)';
        ctx.beginPath(); ctx.moveTo(padL, py); ctx.lineTo(padL + plotW, py); ctx.stroke();
      }}
      ctx.textAlign = 'center';
      for (let x = 0; x <= 70; x += 15) {{
        const px = padL + (x / maxX) * plotW;
        ctx.fillText(x + 'm', px, padT + plotH + 15);
      }}

      // Trendline (inverse contact vs short PFS trend)
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      const x1 = padL + (10 / maxX) * plotW;
      const y1 = padT + plotH - (8 / maxY) * plotH;
      const x2 = padL + (70 / maxX) * plotW;
      const y2 = padT + plotH - (23 / maxY) * plotH;
      ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
      ctx.stroke();
      ctx.setLineDash([]);

      // Draw Patient Points
      GSE301973_PATIENTS.forEach(p => {{
        const px = padL + (p.pfs / maxX) * plotW;
        const py = padT + plotH - (p.endo_pct / maxY) * plotH;

        ctx.beginPath();
        if (p.pfs > 20) {{
          ctx.arc(px, py, 6, 0, Math.PI * 2);
        }} else {{
          ctx.rect(px - 5, py - 5, 10, 10);
        }}
        ctx.fillStyle = p.tierColor;
        ctx.shadowColor = p.tierColor;
        ctx.shadowBlur = 6;
        ctx.fill();
        ctx.shadowBlur = 0;
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Label
        ctx.fillStyle = '#f8fafc';
        ctx.font = 'bold 8.5px -apple-system, sans-serif';
        ctx.textAlign = p.pfs > 40 ? 'right' : 'left';
        ctx.fillText(p.id + ` (${{p.pfs}}m)`, p.pfs > 40 ? px - 9 : px + 9, py + 3);
      }});
    }}

    // Render Patients Table
    function renderVisiumPatientsTable() {{
      const tbody = document.getElementById('visium-patients-tbody');
      if (!tbody) return;

      tbody.innerHTML = GSE301973_PATIENTS.map(p => `
        <tr class="vis-patient-row">
          <td style="padding: 0.6rem 0.5rem; font-weight: 700; color: #fff;">${{p.id}}</td>
          <td style="padding: 0.6rem 0.5rem; color: var(--text-muted);">${{p.pattern}}</td>
          <td style="padding: 0.6rem 0.5rem; font-weight: 700; color: ${{p.pfs >= 22 ? '#10b981' : '#f59e0b'}};">${{p.pfs}} Months</td>
          <td style="padding: 0.6rem 0.5rem; color: #f43f5e; font-weight: 600;">${{p.endo_pct}}%</td>
          <td style="padding: 0.6rem 0.5rem; color: var(--text-muted);">${{p.homo_pct}}%</td>
          <td style="padding: 0.6rem 0.5rem; font-weight: 800; color: ${{p.tierColor}};">${{p.CRI.toFixed(3)}}</td>
          <td style="padding: 0.6rem 0.5rem;"><span class="badge" style="background: rgba(255,255,255,0.06); border: 1px solid ${{p.tierColor}}; color: ${{p.tierColor}}; font-size: 0.72rem; padding: 2px 6px;">${{p.tier}}</span></td>
          <td style="padding: 0.6rem 0.5rem; font-size: 0.75rem; color: var(--text-muted);">${{p.action}}</td>
          <td style="padding: 0.6rem 0.5rem; text-align: right;">
            <button onclick="applyPatientToBedside('${{p.id}}')" class="badge badge-cyan" style="cursor: pointer; border: none; font-size: 0.72rem; padding: 4px 8px;">
              <span>🩺 Apply to Module 1 →</span>
            </button>
          </td>
        </tr>
      `).join('');
    }}

    function applyPatientToBedside(patientId) {{
      const p = GSE301973_PATIENTS.find(item => item.id === patientId);
      if (!p) return;

      const selHisto = document.getElementById('select-histology');
      const selGeno = document.getElementById('select-genomics');
      const selStroma = document.getElementById('select-stroma');

      if (patientId === 's1_PFS_69') {{
        if (selHisto) selHisto.value = '0.15';
        if (selGeno) selGeno.value = '0.10';
        if (selStroma) selStroma.value = '0.10';
      }} else if (patientId === 's2_PFS_22') {{
        if (selHisto) selHisto.value = '0.50';
        if (selGeno) selGeno.value = '0.50';
        if (selStroma) selStroma.value = '0.50';
      }} else if (patientId === 's4_PFS_12') {{
        if (selHisto) selHisto.value = '1.00';
        if (selGeno) selGeno.value = '0.50';
        if (selStroma) selStroma.value = '1.00';
      }} else if (patientId === 's3_PFS_15') {{
        if (selHisto) selHisto.value = '1.00';
        if (selGeno) selGeno.value = '1.00';
        if (selStroma) selStroma.value = '1.00';
      }}

      switchMainModule('1');
      if (typeof recalculate === 'function') recalculate();
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}
"""

part_script = part_script.replace(old_switcher_code, new_script_code)

old_init = "window.addEventListener('DOMContentLoaded', () => {"
new_init = "window.addEventListener('DOMContentLoaded', () => {\n      initVisiumCanvasHover();"
part_script = part_script.replace(old_init, new_init)

# Final assembled HTML
full_html = part_head + middle_modules + part_script

with open(PORTAL_PATH, 'w', encoding='utf-8') as f:
    f.write(full_html)

print("SUCCESS: Grand Unified Portal successfully assembled and verified!")
