"""
The Spatial-Genomic Oncology Continuum (spatial-continuum)
Universal biophysical reaction-diffusion transport framework and Bedside Composite Resistance Index (CRI).
Pure standard library / zero external dependencies.
"""

__version__ = "1.0.2"
__author__ = "Luca Celebrano"
__email__ = "l.celebrano@studenti.unina.it"

from .cri_calc import calculate_cri
from .audit import K0_integral, run_deep_audit

__all__ = ["calculate_cri", "K0_integral", "run_deep_audit", "__version__"]
