# WATCH-DM

**Data Analysis of Diabetes Mellitus (DM) Patients**

[![DOI](https://zenodo.org/badge/DOI/PLACEHOLDER.svg)](https://doi.org/PLACEHOLDER)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> Source code accompanying the WATCH-DM study — a retrospective cohort analysis of diabetes mellitus patients at Nakornping Hospital.

---

## Overview

This repository contains the complete reproducible analysis pipeline for the WATCH-DM study, split into two stages:

| Module | Purpose |
|---|---|
| `statistical-analysis/` | Data cleaning, cohort definition, descriptive statistics, hypothesis testing, survival analysis (KM, Cox PH), and predictive modeling. |
| `visualization/` | Publication-quality figures, dashboards, and supplementary visual outputs. |

## Repository structure

```
WATCH-DM/
├── statistical-analysis/      # Stage 1 — analytic pipeline
│   ├── src/                   # reusable .py modules
│   ├── notebooks/             # Jupyter notebooks (exploratory + final)
│   └── results/               # tables, model outputs (gitignored if PHI)
├── visualization/             # Stage 2 — figure generation
│   ├── src/                   # plotting modules
│   ├── notebooks/             # figure-building notebooks
│   └── figures/               # exported .png / .pdf / .svg
├── data/                      # (empty by design — see data/README.md)
├── docs/                      # study protocol, data dictionary, methods
├── CITATION.cff               # how to cite this software
├── .zenodo.json               # Zenodo deposit metadata
├── LICENSE                    # MIT
├── requirements.txt           # pip dependencies
└── environment.yml            # conda environment
```

## Data availability

Patient-level data are **not** included in this repository due to confidentiality (PHI). De-identified datasets may be obtained from the corresponding author upon reasonable request and IRB approval. See [`data/README.md`](data/README.md) for details.

## Getting started

```bash
# Clone
git clone https://github.com/<your-username>/WATCH-DM.git
cd WATCH-DM

# Option A — conda
conda env create -f environment.yml
conda activate watch-dm

# Option B — pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Reproducibility

Each module ships with its own `README.md` describing inputs, outputs, and the order in which scripts/notebooks must be run. Random seeds are fixed where applicable. Software versions are pinned in `environment.yml`.

## Citation

If you use this code, please cite both the software (Zenodo DOI) and the associated publication. See [`CITATION.cff`](CITATION.cff) or click "Cite this repository" on GitHub.

## License

Released under the [MIT License](LICENSE).

## Contact

Khanita Duangchaemkarn — University of Phayao
kkhanita.du@up.ac.th