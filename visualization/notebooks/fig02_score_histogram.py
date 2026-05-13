"""ภาพที่ 2 — Distribution of WATCH-DM scores (histogram).

Histogram of the integer WATCH-DM scores across all 2,382 patients, colour-coded
by risk group with dashed cut-off lines at the 4 risk-group boundaries.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.style import COLORS, DPI, save_figure


COHORT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data" / "watchdm_full_master_cohort.csv"
)


def risk_idx(s: int) -> int:
    """Return colour index 0..4 matching the risk-group cut-offs."""
    if s <= 7:  return 0   # Very Low
    if s <= 9:  return 1   # Low
    if s == 10: return 2   # Average
    if s <= 13: return 3   # High
    return 4               # Very High


def build_figure(hist_scores, hist_counts):
    bar_colors = [COLORS[risk_idx(s)] for s in hist_scores]

    fig, ax = plt.subplots(figsize=(10, 5), dpi=DPI)
    ax.bar(hist_scores, hist_counts, color=bar_colors,
           edgecolor="white", linewidth=0.8, width=0.8, zorder=3)

    # Risk-group bands behind the bars (alpha via 8-digit hex)
    zones = [
        (0,  7,  "Very Low",  "#4ade8018"),
        (8,  9,  "Low",       "#86efac18"),
        (10, 10, "Average",   "#fbbf2418"),
        (11, 13, "High",      "#f9731618"),
        (14, 18, "Very High", "#ef444418"),
    ]
    for lo, hi, lbl, col in zones:
        ax.axvspan(lo - 0.4, hi + 0.4, color=col, zorder=1)
        ax.text((lo + hi) / 2, max(hist_counts) * 0.94, lbl,
                ha="center", fontsize=7.5, color="#6b7280", fontstyle="italic")

    # Cut-off lines
    for cut in [7.5, 9.5, 10.5, 13.5]:
        ax.axvline(cut, color="#d1d5db", linewidth=1, linestyle="--", zorder=2)

    ax.set_xlabel("WATCH-DM Score", fontsize=11)
    ax.set_ylabel("Number of Patients", fontsize=11)
    ax.set_title("ภาพที่ 2. Distribution of WATCH-DM Scores (n=2,382)",
                 fontsize=13, fontweight="bold", pad=12, color="#1e3a5f")
    ax.set_xticks(hist_scores); ax.set_xlim(-0.6, 18.6)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    return fig


def main() -> None:
    df = pd.read_csv(COHORT_FILE)
    counts = df["watchdm_score"].value_counts().sort_index()
    hist_scores = counts.index.tolist()
    hist_counts = counts.values.tolist()

    fig = build_figure(hist_scores, hist_counts)
    path = save_figure(fig, "fig02_score_histogram.png")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
