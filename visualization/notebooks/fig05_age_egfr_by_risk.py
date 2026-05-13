"""ภาพที่ 5 — Mean Age and eGFR by WATCH-DM risk group (dual-axis line + error bars).

Dual-axis line chart showing how mean age (left y-axis) and mean eGFR (right
y-axis) change across the five risk groups. Error bars are ±1 SD. The visual
contrast (age rising; eGFR falling) underpins the Discussion paragraph that
identifies Age and eGFR as the two strongest discriminators.

Originally "Figure 4" in the supplemental — renumbered to ภาพที่ 5 in the
revision (Table 3 + ภาพที่ 4 inserted ahead of it).
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.style import DPI, GROUPS_SHORT, save_figure


COHORT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data" / "watchdm_full_master_cohort.csv"
)

COLOR_AGE  = "#4472C4"
COLOR_EGFR = "#1B9E8A"


def compute_group_stats(df: pd.DataFrame) -> tuple[np.ndarray, ...]:
    """Return (age_mean, age_sd, egfr_mean, egfr_sd) ordered by GROUPS_SHORT."""
    g = df.groupby("risk_group")
    age_mean  = g["age"].mean().reindex(GROUPS_SHORT).round(1).values
    age_sd    = g["age"].std().reindex(GROUPS_SHORT).round(1).values
    egfr_mean = g["eGFR"].mean().reindex(GROUPS_SHORT).round(1).values
    egfr_sd   = g["eGFR"].std().reindex(GROUPS_SHORT).round(1).values
    return age_mean, age_sd, egfr_mean, egfr_sd


def build_figure(age_mean, age_sd, egfr_mean, egfr_sd):
    x = np.arange(len(GROUPS_SHORT))
    fig, ax1 = plt.subplots(figsize=(10, 6.5), dpi=DPI)

    # ── Left axis: Age ─────────────────────────────────────────────────
    ax1.errorbar(x, age_mean, yerr=age_sd,
                 color=COLOR_AGE, marker="o", markersize=9,
                 linewidth=2.5, capsize=6, capthick=1.8, elinewidth=1.5,
                 label="Mean Age ± SD (years)", zorder=3)
    for xi, yi, si in zip(x, age_mean, age_sd):
        ax1.annotate(f"{yi}\n(±{si})", xy=(xi, yi),
                     xytext=(-22, 10), textcoords="offset points",
                     ha="center", va="bottom",
                     color=COLOR_AGE, fontsize=8.5, fontweight="bold")

    ax1.set_xlabel("WATCH-DM Risk Group", fontsize=12, labelpad=10)
    ax1.set_ylabel("Mean Age (years)", color=COLOR_AGE, fontsize=12)
    ax1.tick_params(axis="y", labelcolor=COLOR_AGE)
    ax1.set_xticks(x); ax1.set_xticklabels(GROUPS_SHORT, fontsize=11)
    ax1.set_ylim(30, 105)
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(10))

    # ── Right axis: eGFR ───────────────────────────────────────────────
    ax2 = ax1.twinx()
    ax2.errorbar(x, egfr_mean, yerr=egfr_sd,
                 color=COLOR_EGFR, marker="s", markersize=9,
                 linewidth=2.5, linestyle="--",
                 capsize=6, capthick=1.8, elinewidth=1.5,
                 label="Mean eGFR ± SD (mL/min/1.73m²)", zorder=3)
    for i, (xi, yi, si) in enumerate(zip(x, egfr_mean, egfr_sd)):
        offset = -22 if i <= 1 else 10
        ax2.annotate(f"{yi}\n(±{si})", xy=(xi, yi),
                     xytext=(22, offset), textcoords="offset points",
                     ha="center", va="bottom",
                     color=COLOR_EGFR, fontsize=8.5, fontweight="bold")

    ax2.set_ylabel("Mean eGFR (mL/min/1.73m²)", color=COLOR_EGFR, fontsize=12)
    ax2.tick_params(axis="y", labelcolor=COLOR_EGFR)
    ax2.set_ylim(0, 140)
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(20))

    ax1.yaxis.grid(True, linestyle="--", alpha=0.5, color="grey")
    ax1.set_axisbelow(True)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2,
               loc="upper left", fontsize=10, framealpha=0.9)

    plt.title("ภาพที่ 5. Mean Age and eGFR by WATCH-DM Risk Group\n(p < 0.001)",
              fontsize=13, fontweight="bold", pad=15)
    fig.text(0.12, 0.01,
             "Error bars represent ±1 SD. p < 0.001 for both Age and eGFR across "
             "risk groups (Kruskal-Wallis test).",
             fontsize=8.5, style="italic", color="#444444")
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    return fig


def main() -> None:
    df = pd.read_csv(COHORT_FILE)
    age_mean, age_sd, egfr_mean, egfr_sd = compute_group_stats(df)
    fig = build_figure(age_mean, age_sd, egfr_mean, egfr_sd)
    path = save_figure(fig, "fig05_age_egfr_by_risk.png")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
