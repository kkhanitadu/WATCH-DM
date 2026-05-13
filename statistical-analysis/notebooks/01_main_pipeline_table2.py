"""01 — Main data analysis pipeline + Table 2 (patient characteristics).

Loads four raw EHR exports, extracts the most-recent measurement per patient,
applies the WATCH-DM scoring algorithm to all 10 components, classifies patients
into five risk groups, and runs the descriptive statistics that populate
**ตารางที่ 2** in the manuscript.

Manuscript artefacts produced by this script:
    • ตารางที่ 2 — ลักษณะทางคลินิกของกลุ่มตัวอย่างจำแนกตามระดับความเสี่ยง
    • Cohort flow numbers cited in Results (n = 2,382)
    • Kruskal–Wallis H statistics + p-values for AGE, FPG, eGFR, BMI, SBP, DBP

Cohort: Nakhon Ping Hospital DM outpatient clinic
Study period: January 2019 – December 2024
Final analytic n: 2,382 (complete-case)

Run from the repo root:
    python statistical-analysis/notebooks/01_main_pipeline_table2.py
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# Make `src/` importable when run as a script
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from scipy import stats

from src.data_loader import (
    load_lab_values,
    load_vitals,
    load_cardiac_history,
    load_echo_qrs,
    merge_all,
)
from src.watchdm_scoring import (
    apply_scoring,
    complete_case_and_classify,
    RISK_ORDER,
)


# ─────────────────────────────────────────────────────────────────────────
# File paths (relative to repo root). Adjust if your data lives elsewhere.
# ─────────────────────────────────────────────────────────────────────────
DATA = Path(__file__).resolve().parents[2] / "data"

LAB_FILE  = DATA / "03_Lab_with_Age_and_Treated_Missing.csv"
WHBP_FILE = DATA / "04_WHBP.csv"
DIAG_FILE = DATA / "07 Diag.csv"
ECHO1     = DATA / "06 ECHO1.xlsx"
ECHO2     = DATA / "06 ECHO_21.xlsx"

OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> pd.DataFrame:
    # ── 1. Load each EHR source ─────────────────────────────────────────
    print("Loading lab file…")
    fpg_df, hdl_df, egfr_df, age_df = load_lab_values(LAB_FILE)
    print(f"  FPG:  {len(fpg_df):,} patients")
    print(f"  HDL:  {len(hdl_df):,} patients  (limited availability)")
    print(f"  eGFR: {len(egfr_df):,} patients")
    print(f"  Age:  {len(age_df):,} patients")

    print("\nLoading vital signs file…")
    vitals_df = load_vitals(WHBP_FILE)
    print(f"  Vital signs: {len(vitals_df):,} patients with valid data")

    print("\nLoading diagnosis file…")
    cardiac_df = load_cardiac_history(DIAG_FILE)
    print(f"  MI history:   {cardiac_df['MI_History'].sum():,} patients")
    print(f"  CABG history: {cardiac_df['CABG_History'].sum():,} patients")

    print("\nLoading echo files…")
    qrs_df = load_echo_qrs(ECHO1, ECHO2)
    print(f"  Wide QRS detected: {qrs_df['Wide_QRS'].sum():,} patients")

    # ── 2. Merge + score + complete-case ────────────────────────────────
    print("\nMerging all data sources…")
    merged = merge_all(age_df, fpg_df, hdl_df, egfr_df, vitals_df, cardiac_df, qrs_df)
    print(f"  Total unique patients: {len(merged):,}")

    scored_all = apply_scoring(merged)
    scored = complete_case_and_classify(scored_all)
    print(f"\nComplete scoring dataset: {len(scored):,} patients")

    # ── 3. Risk-group distribution ──────────────────────────────────────
    print("\n=== Risk Group Distribution ===")
    dist = scored["Risk_Group"].value_counts().reindex(RISK_ORDER)
    for grp, n in dist.items():
        pct = 100 * n / len(scored)
        print(f"  {grp:10s}: n={n:5,}  ({pct:.1f}%)")

    # ── 4. WATCH-DM score summary ───────────────────────────────────────
    print("\n=== WATCH-DM Score Summary ===")
    s = scored["WATCH_DM_Score"]
    print(f"  Mean ± SD : {s.mean():.2f} ± {s.std():.2f}")
    print(f"  Median    : {s.median():.1f}")
    print(f"  Range     : {s.min():.0f} – {s.max():.0f}")
    print(f"  IQR       : {s.quantile(0.25):.1f} – {s.quantile(0.75):.1f}")

    # ── 5. Demographics by risk group (Table 2) ─────────────────────────
    print("\n=== Demographics by Risk Group (Table 2) ===")
    for var in ["AGE", "FPG", "eGFR", "BMI", "SBP", "DBP"]:
        row = scored.groupby("Risk_Group")[var].agg(["mean", "std"])
        cells = [
            f"{grp[:4]} {row.loc[grp, 'mean']:.1f}±{row.loc[grp, 'std']:.1f}"
            for grp in RISK_ORDER if grp in row.index
        ]
        print(f"  {var:6s}: " + "  |  ".join(cells))

    # ── 6. Kruskal–Wallis tests + chi-squared for MI history ────────────
    print("\n=== Statistical Tests (Kruskal–Wallis) ===")
    groups_data = [scored[scored["Risk_Group"] == g] for g in RISK_ORDER]
    for var in ["AGE", "FPG", "eGFR", "BMI", "SBP", "DBP"]:
        arrays = [g[var].dropna().values for g in groups_data]
        arrays = [a for a in arrays if len(a) > 0]
        H, p = stats.kruskal(*arrays)
        print(f"  {var:6s}: H={H:.2f}, p={p:.4f}")

    mi_table = pd.crosstab(scored["Risk_Group"], scored["MI_History"])
    chi2, p_chi, _, _ = stats.chi2_contingency(mi_table)
    print(f"  MI Hx : chi2={chi2:.2f}, p={p_chi:.4f}")

    # ── 7. Persist (gitignored — re-run locally) ────────────────────────
    out_path = OUT / "watchdm_scored_patients.csv"
    scored.to_csv(out_path, index=False)
    print(f"\nResults saved to {out_path.relative_to(Path.cwd()) if out_path.is_relative_to(Path.cwd()) else out_path}")
    print(f"Total scored patients: {len(scored):,}")

    return scored


if __name__ == "__main__":
    main()
