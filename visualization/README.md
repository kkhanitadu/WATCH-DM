# Visualization — WATCH-DM

This module produces every figure that appears in the WATCH-DM manuscript (TJPP, May 2026 revision).

## Folder layout

```
visualization/
├── src/
│   ├── __init__.py
│   └── style.py               # shared colors, DPI, group labels, save helper
├── notebooks/
│   ├── fig01_patient_flow.py            # ภาพที่ 1
│   ├── fig02_score_histogram.py         # ภาพที่ 2
│   ├── fig03_risk_group_distribution.py # ภาพที่ 3 (A+B donut + bar)
│   ├── fig04_hf_status_by_risk.py       # ภาพที่ 4 (added in revision)
│   ├── fig05_age_egfr_by_risk.py        # ภาพที่ 5 (dual-axis Age + eGFR)
│   └── fig06_egfr_distribution.py       # ภาพที่ 6 (eGFR box + CKD bands)
└── figures/                   # PNG/PDF outputs
```

## Figure inventory

| File | Manuscript figure | Description |
|---|---|---|
| `fig01_patient_flow.py`            | **ภาพที่ 1** | Cohort flow 13,958 → 2,382 with exclusion boxes |
| `fig02_score_histogram.py`         | **ภาพที่ 2** | WATCH-DM score histogram, colour-coded by risk band |
| `fig03_risk_group_distribution.py` | **ภาพที่ 3** | (A) Donut % + (B) Horizontal bar count |
| `fig04_hf_status_by_risk.py`       | **ภาพที่ 4** | Stacked bar — HF status (No / Incident / Prevalent) within each risk group |
| `fig05_age_egfr_by_risk.py`        | **ภาพที่ 5** | Dual-axis line: mean Age + mean eGFR ± SD by risk group |
| `fig06_egfr_distribution.py`       | **ภาพที่ 6** | Box plot of eGFR by risk group with KDIGO CKD bands + 45 mL/min cut-off |

Numbering note: `fig04` and `Table 3` were inserted in the May 2026 revision (HF-status sensitivity analysis), which shifts the supplemental's original "Figure 4" → ภาพที่ 5 and original "Figure 5" → ภาพที่ 6.

## Style conventions

All figures pull from `src/style.py`:

- **DPI:** 300 (publication quality)
- **Palette:** colorblind-safe green→yellow→orange→red gradient for risk groups
- **HF palette:** slate / blue / crimson for No-HF / Incident / Prevalent
- **Font sizes:** ≥8 pt labels, 11–13 pt titles
- **Output:** PNG (with optional PDF/SVG by editing the `save_figure` call)

## How to run

```bash
# from repo root, with the conda env activated
python visualization/notebooks/fig01_patient_flow.py
python visualization/notebooks/fig02_score_histogram.py
python visualization/notebooks/fig03_risk_group_distribution.py
python visualization/notebooks/fig04_hf_status_by_risk.py
python visualization/notebooks/fig05_age_egfr_by_risk.py
python visualization/notebooks/fig06_egfr_distribution.py
```

Outputs land in `figures/` and are versioned with the repo.
