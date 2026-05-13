"""ภาพที่ 3 — Risk group distribution: (A) Proportion (donut) + (B) Absolute count.

Two-panel figure summarising how the 2,382 patients distribute across the five
WATCH-DM risk groups.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.style import COLORS, DPI, GROUPS_SHORT, save_figure


COHORT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data" / "watchdm_full_master_cohort.csv"
)


def build_figure(n_patients, pct_patients):
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=DPI)
    fig.suptitle("ภาพที่ 3. Risk Group Distribution by WATCH-DM Score (n=2,382)",
                 fontsize=13, fontweight="bold", color="#1e3a5f", y=1.01)

    # ── Panel A — Donut chart ───────────────────────────────────────────
    wedges, _, autotexts = axA.pie(
        pct_patients, labels=None, colors=COLORS,
        autopct="%1.1f%%", startangle=90, pctdistance=0.75,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2.2),
    )
    for at in autotexts:
        at.set_fontsize(9); at.set_fontweight("bold"); at.set_color("white")
    axA.text(0, 0, "n=2,382", ha="center", va="center",
             fontsize=10, fontweight="bold", color="#374151")
    axA.set_title("(A) Proportion (%)", fontsize=11, fontweight="bold",
                  color="#374151", pad=10)
    legend_labels = [f"{g}  ({p:.1f}%)" for g, p in zip(GROUPS_SHORT, pct_patients)]
    axA.legend(wedges, legend_labels, loc="lower center",
               bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False, fontsize=9)

    # ── Panel B — Horizontal bar chart ──────────────────────────────────
    ypos = np.arange(5)
    bars = axB.barh(ypos, n_patients, color=[c + "cc" for c in COLORS],
                    edgecolor="white", linewidth=0.5, height=0.6)
    for bar, n in zip(bars, n_patients):
        axB.text(bar.get_width() + 15, bar.get_y() + bar.get_height() / 2,
                 f"n = {n:,}", va="center", fontsize=9.5, color="#374151")
    axB.set_yticks(ypos)
    axB.set_yticklabels(GROUPS_SHORT, fontsize=10)
    axB.set_xlabel("Number of Patients", fontsize=11)
    axB.set_xlim(0, max(n_patients) * 1.22)
    axB.invert_yaxis()
    axB.set_title("(B) Absolute Count", fontsize=11, fontweight="bold",
                  color="#374151", pad=10)
    axB.text(0.98, 0.03, "Total n = 2,382", transform=axB.transAxes,
             ha="right", va="bottom", fontsize=9, color="#6b7280", fontstyle="italic")

    plt.tight_layout()
    return fig


def main() -> None:
    df = pd.read_csv(COHORT_FILE)
    counts = (
        df["risk_group"]
        .value_counts()
        .reindex(GROUPS_SHORT)
        .astype(int)
    )
    n_patients   = counts.values.tolist()
    pct_patients = (100 * counts / counts.sum()).round(1).values.tolist()

    fig = build_figure(n_patients, pct_patients)
    path = save_figure(fig, "fig03_risk_group_distribution.png")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
