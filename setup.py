from setuptools import setup, find_packages

setup(
    name="spatial-continuum",
    version="1.0.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "cri-calc = spatial_continuum.cri_calc:main",
            "spatial-continuum-audit = spatial_continuum.audit:main",
        ],
    },
)
