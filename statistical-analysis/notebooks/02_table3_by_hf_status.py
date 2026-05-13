"""02 — Table 3: WATCH-DM scores stratified by HF status.

Sensitivity analysis added in revision (TJPP minor revision, May 2026).
Compares the WATCH-DM score across three HF-status strata defined from the
patient's HF diagnosis history relative to the index date.

Strata
------
    No HF         — no ICD-10 I50 diagnosis ever recorded
    Incident HF   — first I50 recorded AFTER the index date
    Prevalent HF  — I50 recorded BEFORE the index date

Manuscript artefacts produced by this script:
    • ตารางที่ 3 — คะแนน WATCH-DM และการกระจายของระดับความเสี่ยงจำแนกตามสถานะ HF
    • Methods paragraph reporting Kruskal–Wallis + Mann–Whitney + Bonferroni

Verified numbers (must match the manuscript):
    Kruskal–Wallis: H = 9.33, p = 0.009
    No HF vs Prevalent HF  : Bonferroni-adjusted p = 0.009
    No HF vs Incident HF   : Bonferroni-adjusted p = 1.000
    Incident vs Prevalent  : Bonferroni-adjusted p = 0.406

Run from the repo root:
    python statistical-analysis/notebooks/02_table3_by_hf_status.py
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

import pandas as pd
from scipy import stats

# Make `src/` importable when run as a script (not strictly needed here, but
# kept for consistency with notebook 01).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


# ─────────────────────────────────────────────────────────────────────────
# Input file
# ─────────────────────────────────────────────────────────────────────────
# Master cohort table with HF flags added in the revision sub-analysis.
# Required columns: HN, watchdm_score, risk_group, HF_status
COHORT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data" / "watchdm_full_master_cohort.csv"
)

OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(parents=True, exist_ok=True)

HF_GROUPS = ["No HF", "Incident", "Prevalent"]
N_COMPARISONS = 3  # Bonferroni divisor — three pairwise tests


# ─────────────────────────────────────────────────────────────────────────
def descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute n, mean ± SD, and median [IQR] of WATCH-DM score per HF stratum."""
    rows = []
    for g in HF_GROUPS:
        s = df.loc[df["HF_status"] == g, "watchdm_score"].dropna()
        rows.append({
            "HF_status": g,
            "n":         len(s),
            "mean":      s.mean(),
            "sd":        s.std(),
            "median":    s.median(),
            "q1":        s.quantile(0.25),
            "q3":        s.quantile(0.75),
        })
    return pd.DataFrame(rows)


def dominant_risk_group(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-tabulate HF status × risk_group (proportions within each HF stratum)."""
    xtab = pd.crosstab(df["HF_status"], df["risk_group"], normalize="index") * 100
    return xtab.round(1)


def pairwise_mannwhitney_bonferroni(df: pd.DataFrame) -> pd.DataFrame:
    """Pairwise Mann–Whitney U with Bonferroni correction over 3 comparisons."""
    arrays = {
        g: df.loc[df["HF_status"] == g, "watchdm_score"].dropna().values
        for g in HF_GROUPS
    }
    rows = []
    for g1, g2 in combinations(HF_GROUPS, 2):
        U, p_raw = stats.mannwhitneyu(arrays[g1], arrays[g2], alternative="two-sided")
        rows.append({
            "comparison": f"{g1} vs {g2}",
            "U":          U,
            "p_raw":      p_raw,
            "p_bonf":     min(p_raw * N_COMPARISONS, 1.0),
        })
    return pd.DataFrame(rows)


def main() -> None:
    df = pd.read_csv(COHORT_FILE)
    required = {"HF_status", "watchdm_score", "risk_group"}
    missing = required - set(df.columns)
    if missing:
        raise KeyError(f"Cohort file is missing required columns: {missing}")

    # ── 1. Descriptive stats ────────────────────────────────────────────
    desc = descriptive_stats(df)
    print("=== Table 3 — descriptive stats ===")
    for _, r in desc.iterrows():
        print(
            f"  {r['HF_status']:10s}: n={int(r['n']):4d}  "
            f"mean±SD = {r['mean']:.2f} ± {r['sd']:.2f}  "
            f"median [IQR] = {r['median']:.1f} [{r['q1']:.1f}–{r['q3']:.1f}]"
        )

    # ── 2. Dominant risk group within each HF stratum ───────────────────
    xtab = dominant_risk_group(df)
    print("\n=== Risk-group distribution within each HF stratum (%) ===")
    print(xtab)

    # ── 3. Kruskal–Wallis ───────────────────────────────────────────────
    arrays = [df.loc[df["HF_status"] == g, "watchdm_score"].dropna().values
              for g in HF_GROUPS]
    H, p_kw = stats.kruskal(*arrays)
    print(f"\nKruskal–Wallis: H = {H:.2f}, p = {p_kw:.4f}")

    # ── 4. Pairwise Mann–Whitney + Bonferroni ───────────────────────────
    pw = pairwise_mannwhitney_bonferroni(df)
    print("\n=== Pairwise Mann–Whitney U (Bonferroni × 3) ===")
    for _, r in pw.iterrows():
        sig = " ✱" if r["p_bonf"] < 0.05 else ""
        print(f"  {r['comparison']:30s} U={int(r['U']):>6d}  "
              f"p_raw={r['p_raw']:.4f}  p_bonf={r['p_bonf']:.3f}{sig}")

    # ── 5. Persist (gitignored) ─────────────────────────────────────────
    desc.to_csv(OUT / "table3_descriptive.csv", index=False)
    xtab.to_csv(OUT / "table3_dominant_risk.csv")
    pw.to_csv(OUT / "table3_pairwise.csv", index=False)
    print(f"\nResults saved under {OUT}")


if __name__ == "__main__":
    main()
