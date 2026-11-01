"""
The Spatial-Genomic Oncology Continuum (spatial-continuum)
Universal biophysical reaction-diffusion transport framework and Bedside Composite Resistance Index (CRI).
Native scverse AnnData interoperability for spatial biology and precision oncology.
"""

__version__ = "1.0.3"
__author__ = "Luca Celebrano"
__email__ = "l.celebrano@studenti.unina.it"

from .cri_calc import calculate_cri
from .audit import K0_integral, run_deep_audit
from .anndata_adapter import (
    to_anndata,
    annotate_anndata,
    from_anndata,
    BESSEL_TRANSPORT_METRICS,
    SCIENTIFIC_ANCHORS,
)

__all__ = [
    "calculate_cri",
    "K0_integral",
    "run_deep_audit",
    "to_anndata",
    "annotate_anndata",
    "from_anndata",
    "BESSEL_TRANSPORT_METRICS",
    "SCIENTIFIC_ANCHORS",
    "__version__",
]
