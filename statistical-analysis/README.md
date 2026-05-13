# Statistical Analysis — WATCH-DM

This module contains all code required to reproduce the statistical results reported in the WATCH-DM manuscript (TJPP, May 2026 revision).

## Folder layout

```
statistical-analysis/
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # EHR loaders + most-recent-measurement extraction
│   └── watchdm_scoring.py     # 10-component scoring algorithm + risk classifier
├── notebooks/
│   ├── 01_main_pipeline_table2.py     # data pipeline → ตารางที่ 2
│   └── 02_table3_by_hf_status.py      # sensitivity analysis → ตารางที่ 3
└── results/                   # gitignored — re-generate locally
```

## Pipeline mapped to the manuscript

| Script | Produces |
|---|---|
| `notebooks/01_main_pipeline_table2.py` | Cohort flow (n = 2,382), WATCH-DM scoring, **ตารางที่ 2** (clinical characteristics by risk group, Kruskal–Wallis tests) |
| `notebooks/02_table3_by_hf_status.py`  | **ตารางที่ 3** — WATCH-DM by HF status (Kruskal–Wallis H = 9.33, p = 0.009; Mann–Whitney + Bonferroni × 3) |

`ตารางที่ 1` is the static WATCH-DM scoring reference (no code needed — see Table 1 of the manuscript).

## How to run

```bash
# from repo root, with the conda env activated
python statistical-analysis/notebooks/01_main_pipeline_table2.py
python statistical-analysis/notebooks/02_table3_by_hf_status.py
```

Scripts write CSVs to `results/` (gitignored).

## Reproducibility notes

- All Kruskal–Wallis tests use `scipy.stats.kruskal`; pairwise Mann–Whitney uses `scipy.stats.mannwhitneyu` with two-sided alternative.
- Bonferroni correction multiplies raw p-values by 3 (three pairwise HF comparisons), capped at 1.0.
- Complete-case analysis throughout; all 10 WATCH-DM components must be present.
- α = 0.05, two-sided.
