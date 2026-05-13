"""Data loading and cleaning helpers for the WATCH-DM cohort.

Loads four source EHR exports (lab, vitals, diagnoses, echo) and extracts the
most-recent measurement per patient for each WATCH-DM variable.

Manuscript reference: Methods — "กระบวนการคัดเลือกกลุ่มตัวอย่าง" and "การจัดการข้อมูล"
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


# ── Lab codes used in this study ────────────────────────────────────────
LAB_CODES = {
    "FPG":  "40382",   # fasting plasma glucose
    "HDL":  "40324",   # HDL-cholesterol
    "eGFR": "308B",    # estimated GFR (CKD-EPI)
}

# ── ICD-10 / operation codes for cardiovascular history ────────────────
MI_CODES   = ["I21", "I22", "I252"]   # myocardial infarction
CABG_CODES = ["Z951"]                  # CABG / bypass history

# ── Free-text keywords used to detect wide-QRS on echocardiography ─────
WIDE_QRS_KEYWORDS = [
    "wide qrs", "lbbb", "rbbb", "pacemaker", "ppm",
    "left bundle", "right bundle",
]


# ─────────────────────────────────────────────────────────────────────────
# Generic helpers
# ─────────────────────────────────────────────────────────────────────────

def clean_numeric(series: pd.Series) -> pd.Series:
    """Strip non-numeric suffixes (e.g. '46.22 Repeated') and coerce to float."""
    return pd.to_numeric(
        series.astype(str).str.extract(r"([\d.]+)")[0],
        errors="coerce",
    )


def most_recent_lab(lab: pd.DataFrame, labcode: str) -> pd.DataFrame:
    """Return the most-recent numeric result per HN for a given LABCODE."""
    subset = lab[lab["LABCODE"] == labcode].dropna(subset=["RESULT_NUM", "DATE"])
    subset = subset.sort_values("DATE", ascending=False)
    return subset.groupby("HN")["RESULT_NUM"].first().reset_index()


def _has_code(row: pd.Series, cols: Iterable[str], code_list: Iterable[str]) -> bool:
    """Return True if any of the given columns contains one of the codes (prefix match)."""
    for col in cols:
        val = str(row.get(col, "")).upper().replace(".", "")
        for code in code_list:
            if val.startswith(code):
                return True
    return False


def _has_wide_qrs(memo: str) -> bool:
    if pd.isna(memo):
        return False
    memo_lower = str(memo).lower()
    return any(kw in memo_lower for kw in WIDE_QRS_KEYWORDS)


# ─────────────────────────────────────────────────────────────────────────
# Source-specific loaders
# ─────────────────────────────────────────────────────────────────────────

def load_lab_values(lab_file: str | Path) -> tuple[pd.DataFrame, ...]:
    """Load lab export and return (fpg_df, hdl_df, egfr_df, age_df).

    Each returned DataFrame has columns ``[HN, <variable>]`` with the most-recent
    measurement per patient.
    """
    lab = pd.read_csv(lab_file, encoding="utf-8-sig", low_memory=False)
    lab["DATE"] = pd.to_datetime(lab["RECEIVESPECIMENDATETIME"], errors="coerce")
    lab["RESULT_NUM"] = clean_numeric(lab["LABRESULT"])

    fpg_df  = most_recent_lab(lab, LAB_CODES["FPG"]);  fpg_df.columns  = ["HN", "FPG"]
    hdl_df  = most_recent_lab(lab, LAB_CODES["HDL"]);  hdl_df.columns  = ["HN", "HDL"]
    egfr_df = most_recent_lab(lab, LAB_CODES["eGFR"]); egfr_df.columns = ["HN", "eGFR"]

    # Age comes pre-calculated as a column
    age_df = lab.dropna(subset=["AGE"]).groupby("HN")["AGE"].first().reset_index()
    age_df.columns = ["HN", "AGE"]

    return fpg_df, hdl_df, egfr_df, age_df


def load_vitals(whbp_file: str | Path) -> pd.DataFrame:
    """Load vitals (SBP, DBP, BMI) with physiologic-range filtering and BMI calc."""
    whbp = pd.read_csv(whbp_file, encoding="utf-8-sig", low_memory=False)
    whbp["DATE"] = pd.to_datetime(whbp["DATETIME"], errors="coerce")
    whbp["SBP"] = pd.to_numeric(whbp["SYSTOLIC"],   errors="coerce")
    whbp["DBP"] = pd.to_numeric(whbp["DIASTOLIC"],  errors="coerce")
    whbp["WT"]  = pd.to_numeric(whbp["BODYWEIGHT"], errors="coerce")
    whbp["HT"]  = pd.to_numeric(whbp["HEIGHT"],     errors="coerce")

    whbp = whbp[
        whbp["SBP"].between(60, 300) &
        whbp["DBP"].between(30, 200) &
        whbp["WT"].between(20, 250)  &
        whbp["HT"].between(100, 220)
    ].copy()

    whbp["BMI"] = whbp["WT"] / (whbp["HT"] / 100) ** 2
    whbp = whbp[whbp["BMI"].between(10, 70)]

    return (
        whbp.sort_values("DATE", ascending=False)
            .groupby("HN")[["SBP", "DBP", "BMI"]]
            .first()
            .reset_index()
    )


def load_cardiac_history(diag_file: str | Path) -> pd.DataFrame:
    """Flag prior MI and CABG using ICD-10 / operation codes."""
    diag = pd.read_csv(diag_file, encoding="utf-8-sig", low_memory=False)
    diag_cols = [c for c in diag.columns if c.startswith("DIAG")]
    oper_cols = [c for c in diag.columns if c.startswith("OPER")]

    diag["MI_History"] = diag.apply(
        lambda r: _has_code(r, diag_cols, MI_CODES), axis=1)
    diag["CABG_History"] = diag.apply(
        lambda r: _has_code(r, diag_cols + oper_cols, CABG_CODES), axis=1)

    return diag.groupby("HN")[["MI_History", "CABG_History"]].any().reset_index()


def load_echo_qrs(*echo_files: str | Path) -> pd.DataFrame:
    """Flag wide-QRS from free-text echo reports (LBBB / RBBB / pacemaker / etc)."""
    parts = [pd.read_excel(f) for f in echo_files]
    echo = pd.concat(parts, ignore_index=True)
    echo["Wide_QRS"] = echo["RESULTMEMO"].apply(_has_wide_qrs)
    return echo.groupby("HN")["Wide_QRS"].any().reset_index()


def merge_all(age_df, fpg_df, hdl_df, egfr_df, vitals_df, cardiac_df, qrs_df) -> pd.DataFrame:
    """Outer-style left-merge against the age cohort. Fill missing binary flags with False."""
    merged = age_df.copy()
    for df_to_merge in [fpg_df, hdl_df, egfr_df, vitals_df, cardiac_df, qrs_df]:
        merged = merged.merge(df_to_merge, on="HN", how="left")

    for flag in ["MI_History", "CABG_History", "Wide_QRS"]:
        merged[flag] = merged[flag].fillna(False)

    return merged
