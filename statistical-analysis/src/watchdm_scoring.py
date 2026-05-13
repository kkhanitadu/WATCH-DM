"""WATCH-DM 10-component scoring algorithm.

Implements the integer-point WATCH-DM score (Segar et al. 2019) as adapted for
this study, where serum creatinine is replaced by eGFR. Maximum score = 32.
Five risk groups are defined by the original publication's cut-offs.

Manuscript reference: Methods — "การคำนวณคะแนน WATCH-DM" (Table 1).
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ── Ordered risk-group labels (used for plotting and categorical sort) ──
RISK_ORDER = ["Very Low", "Low", "Average", "High", "Very High"]


# ─────────────────────────────────────────────────────────────────────────
# Component-level scoring functions (return NaN if input is missing)
# ─────────────────────────────────────────────────────────────────────────

def score_age(age):
    """Age (0–6 pts): <50=0, 50–54=1, 55–59=2, 60–64=3, 65–69=4, 70–74=5, ≥75=6."""
    if pd.isna(age): return np.nan
    if age < 50: return 0
    if age < 55: return 1
    if age < 60: return 2
    if age < 65: return 3
    if age < 70: return 4
    if age < 75: return 5
    return 6


def score_bmi(bmi):
    """BMI (0–3 pts): <25=0, 25–34=1, 35–39=2, ≥40=3."""
    if pd.isna(bmi): return np.nan
    if bmi < 25: return 0
    if bmi < 35: return 1
    if bmi < 40: return 2
    return 3


def score_sbp(sbp):
    """Systolic BP (0–3 pts): <100=0, 100–139=1, 140–159=2, ≥160=3."""
    if pd.isna(sbp): return np.nan
    if sbp < 100: return 0
    if sbp < 140: return 1
    if sbp < 160: return 2
    return 3


def score_dbp(dbp):
    """Diastolic BP (0–2 pts, INVERSE): <60=2, 60–79=1, ≥80=0."""
    if pd.isna(dbp): return np.nan
    if dbp < 60: return 2
    if dbp < 80: return 1
    return 0


def score_fpg(fpg):
    """FPG (0–3 pts): <125=0, 125–199=1, 200–299=2, ≥300=3."""
    if pd.isna(fpg): return np.nan
    if fpg < 125: return 0
    if fpg < 200: return 1
    if fpg < 300: return 2
    return 3


def score_hdl(hdl):
    """HDL-C (0–2 pts, INVERSE): <30=2, 30–59=1, ≥60=0."""
    if pd.isna(hdl): return np.nan
    if hdl < 30: return 2
    if hdl < 60: return 1
    return 0


def score_egfr(egfr):
    """eGFR proxy (0, 2, or 5 pts): >60=0, 30–60=2, <30=5.

    NOTE: substitutes Serum creatinine in the original Segar model. This
    substitution is discussed as a study limitation in the manuscript.
    """
    if pd.isna(egfr): return np.nan
    if egfr > 60: return 0
    if egfr >= 30: return 2
    return 5


# ─────────────────────────────────────────────────────────────────────────
# Whole-cohort scoring + classification
# ─────────────────────────────────────────────────────────────────────────

SCORE_COLS = [
    "Age_Score", "BMI_Score", "SBP_Score", "DBP_Score", "FPG_Score",
    "HDL_Score", "eGFR_Score", "QRS_Score", "MI_Score", "CABG_Score",
]


def apply_scoring(merged: pd.DataFrame) -> pd.DataFrame:
    """Compute per-row component scores and the total WATCH-DM score.

    Input must contain columns: AGE, BMI, SBP, DBP, FPG, HDL, eGFR,
    Wide_QRS (bool), MI_History (bool), CABG_History (bool).
    """
    df = merged.copy()
    df["Age_Score"]  = df["AGE"].apply(score_age)
    df["BMI_Score"]  = df["BMI"].apply(score_bmi)
    df["SBP_Score"]  = df["SBP"].apply(score_sbp)
    df["DBP_Score"]  = df["DBP"].apply(score_dbp)
    df["FPG_Score"]  = df["FPG"].apply(score_fpg)
    df["HDL_Score"]  = df["HDL"].apply(score_hdl)
    df["eGFR_Score"] = df["eGFR"].apply(score_egfr)
    df["QRS_Score"]  = df["Wide_QRS"].astype(int) * 3      # wide-QRS = 3 pts
    df["MI_Score"]   = df["MI_History"].astype(int) * 3    # prior MI = 3 pts
    df["CABG_Score"] = df["CABG_History"].astype(int) * 2  # prior CABG = 2 pts

    df["WATCH_DM_Score"] = df[SCORE_COLS].sum(axis=1)
    return df


def classify_risk(score: float) -> str:
    """WATCH-DM risk groups per the original publication's cut-offs.

    Very Low: ≤7   Low: 8–9   Average: 10   High: 11–13   Very High: ≥14
    """
    if score <= 7:  return "Very Low"
    if score <= 9:  return "Low"
    if score == 10: return "Average"
    if score <= 13: return "High"
    return "Very High"


def complete_case_and_classify(scored: pd.DataFrame) -> pd.DataFrame:
    """Drop incomplete rows (any of the 10 components missing) and add Risk_Group."""
    complete = scored.dropna(subset=SCORE_COLS).copy()
    complete["Risk_Group"] = complete["WATCH_DM_Score"].apply(classify_risk)
    complete["Risk_Group"] = pd.Categorical(
        complete["Risk_Group"], categories=RISK_ORDER, ordered=True
    )
    return complete
