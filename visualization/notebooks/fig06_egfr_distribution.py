"""ภาพที่ 6 — eGFR distribution across WATCH-DM risk groups (box plot with CKD shading).

Visualises the wide eGFR spread within each WATCH-DM risk group, illustrating
the *score dilution effect* discussed in the manuscript: patients with low eGFR
can fall into Low/Average WATCH-DM groups if their other components are normal.
Background bands show KDIGO CKD stages G1–G5 for clinical interpretation.

Originally "Figure 5" in the supplemental — renumbered to ภาพที่ 6 in revision.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.style import COLORS, DPI, GROUPS_SHORT, save_figure


COHORT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data" / "watchdm_full_master_cohort.csv"
)


def compute_box_stats(df: pd.DataFrame) -> dict[str, np.ndarray]:
    """Return median, Q1, Q3, min, max, n for eGFR within each risk group."""
    g = df.groupby("risk_group")["eGFR"]
    return {
        "median": g.median().reindex(GROUPS_SHORT).round(1).values,
        "q1":     g.quantile(0.25).reindex(GROUPS_SHORT).round(1).values,
        "q3":     g.quantile(0.75).reindex(GROUPS_SHORT).round(1).values,
        "lo":     g.min().reindex(GROUPS_SHORT).values,
        "hi":     g.max().reindex(GROUPS_SHORT).values,
        "n":      g.size().reindex(GROUPS_SHORT).astype(int).values,
    }


CKD_STAGES = [
    (90, 148, "G1\n(≥90)",   "#bbf7d0"),
    (60, 90,  "G2\n(60–89)", "#d1fae5"),
    (45, 60,  "G3a\n(45–59)", "#fef9c3"),
    (30, 45,  "G3b\n(30–44)", "#fed7aa"),
    (0,  30,  "G4–G5\n(<30)", "#fecaca"),
]


def build_figure(stats: dict[str, np.ndarray]):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=DPI)

    # ── CKD stage background bands ──────────────────────────────────────
    for lo_ckd, hi_ckd, lbl, fc in CKD_STAGES:
        ax.axhspan(lo_ckd, hi_ckd, xmin=0, xmax=1,
                   color=fc, alpha=0.25, zorder=0)
        ax.text(4.75, (lo_ckd + hi_ckd) / 2, lbl,
                ha="right", va="center", fontsize=7.5,
                color="#6b7280", fontstyle="italic")

    # ── Per-group manual box plot from summary stats ────────────────────
    for i, col in enumerate(COLORS):
        med = stats["median"][i]
        q1, q3 = stats["q1"][i], stats["q3"][i]
        lo, hi = stats["lo"][i], stats["hi"][i]
        n = stats["n"][i]

        # Whisker line (min–max)
        ax.plot([i, i], [lo, hi], color="#94a3b8", linewidth=1.2, zorder=1)
        # IQR box
        box = mpatches.FancyBboxPatch(
            (i - 0.28, q1), 0.56, q3 - q1,
            boxstyle="round,pad=0.02", linewidth=1.5,
            edgecolor="#475569", facecolor=col + "bb", zorder=2,
        )
        ax.add_patch(box)
        # Median line
        ax.plot([i - 0.28, i + 0.28], [med, med],
                color="#1e293b", linewidth=2.2, zorder=3)
        # Whisker caps
        for cap_y in [lo, hi]:
            ax.plot([i - 0.14, i + 0.14], [cap_y, cap_y],
                    color="#94a3b8", linewidth=1.2, zorder=1)
        # Median label
        ax.text(i + 0.32, med, f"{med}", va="center",
                fontsize=9, color="#1e293b", fontweight="bold")
        # n label
        ax.text(i, q3 + 3, f"n={n:,}",
                ha="center", fontsize=8.5, color="#374151")

    # ── Suggested screening cutoff line (eGFR = 45) ─────────────────────
    ax.axhline(45, color="#dc2626", linewidth=1.4, linestyle=":", zorder=4)
    ax.text(0.02, 47, "Suggested supplementary cutoff: eGFR = 45 mL/min/1.73m²",
            transform=ax.get_yaxis_transform(), color="#7f1d1d",
            fontsize=8.5, fontweight="bold")

    # ── Axis cosmetics ──────────────────────────────────────────────────
    ax.set_xticks(range(len(GROUPS_SHORT)))
    ax.set_xticklabels(GROUPS_SHORT, fontsize=11)
    ax.set_xlabel("WATCH-DM Risk Group", fontsize=12)
    ax.set_ylabel("eGFR (mL/min/1.73m²)", fontsize=12)
    ax.set_ylim(-5, 158)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
    ax.yaxis.grid(True, linestyle="--", alpha=0.4, color="grey")
    ax.set_axisbelow(True)
    ax.set_title(
        "ภาพที่ 6. eGFR Distribution across WATCH-DM Risk Groups\n"
        "(Kruskal–Wallis p < 0.001)",
        fontsize=13, fontweight="bold", pad=12, color="#1e3a5f",
    )
    fig.text(0.12, 0.01,
             "Boxes represent IQR (Q1–Q3); horizontal line = median; "
             "whiskers = min/max.\n"
             "CKD stage shading based on KDIGO 2012 classification.",
             fontsize=8.5, style="italic", color="#444444")
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    return fig


def main() -> None:
    df = pd.read_csv(COHORT_FILE)
    stats = compute_box_stats(df)
    fig = build_figure(stats)
    path = save_figure(fig, "fig06_egfr_distribution.png")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
