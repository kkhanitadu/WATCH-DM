"""ภาพที่ 4 — HF status distribution by WATCH-DM risk group (stacked bars).

Sensitivity-analysis figure added in revision (TJPP minor revision, May 2026).
Shows the percentage breakdown of three HF-status categories (No HF, Incident HF,
Prevalent HF) within each of the five WATCH-DM risk groups.

The Very-High risk group has very small (<5%) Prevalent-HF slivers, so those
labels are rendered as a callout box sized 12 pt to stay legible.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.style import DPI, GROUPS_SHORT, HF_COLORS, save_figure


COHORT_FILE = (
    Path(__file__).resolve().parents[2]
    / "data" / "watchdm_full_master_cohort.csv"
)

HF_ORDER = ["No HF", "Incident", "Prevalent"]


def compute_percentages(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame indexed by Risk_Group with HF_status columns (%)."""
    xtab = pd.crosstab(df["risk_group"], df["HF_status"], normalize="index") * 100
    return xtab.reindex(index=GROUPS_SHORT, columns=HF_ORDER).fillna(0.0)


def build_figure(pct: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(11, 6), dpi=DPI)
    x = np.arange(len(GROUPS_SHORT))

    # ── Stacked bars ────────────────────────────────────────────────────
    bottoms = np.zeros(len(GROUPS_SHORT))
    for hf in HF_ORDER:
        vals = pct[hf].values
        ax.bar(x, vals, bottom=bottoms, label=hf,
               color=HF_COLORS[hf], edgecolor="white", linewidth=1.0, zorder=3)

        # In-bar % labels (skip the Very-High row for the tiny Prevalent slice;
        # we render that via callout further down).
        for i, (b, v) in enumerate(zip(bottoms, vals)):
            if v >= 2.0:  # only label segments large enough to fit text
                ax.text(x[i], b + v / 2, f"{v:.1f}%",
                        ha="center", va="center",
                        fontsize=9.5, color="white", fontweight="bold", zorder=4)
        bottoms += vals

    # ── Callout for Very-High Prevalent sliver (visibility tweak) ───────
    vh_idx = GROUPS_SHORT.index("Very High")
    prev_val = pct.loc["Very High", "Prevalent"]
    inc_val  = pct.loc["Very High", "Incident"]
    if prev_val > 0 and prev_val < 6:
        # Find the centre of the orange (Incident) band to drop the box into
        callout_x = vh_idx
        callout_y = pct.loc["Very High", "No HF"] + inc_val / 2
        ax.annotate(
            f"Prevalent\n{prev_val:.1f}%",
            xy=(vh_idx, 100 - prev_val / 2),
            xytext=(callout_x + 0.45, callout_y),
            fontsize=12, fontweight="bold",
            color="#7f1d1d", ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.4",
                      facecolor="#fee2e2", edgecolor="#dc2626", lw=1.5),
            arrowprops=dict(arrowstyle="-", color="#dc2626", lw=1.2),
            zorder=5,
        )

    # ── Axis cosmetics ──────────────────────────────────────────────────
    ax.set_xticks(x)
    ax.set_xticklabels(GROUPS_SHORT, fontsize=11)
    ax.set_xlabel("WATCH-DM Risk Group", fontsize=12)
    ax.set_ylabel("Percentage within risk group (%)", fontsize=12)
    ax.set_ylim(0, 105)
    ax.yaxis.grid(True, linestyle="--", alpha=0.4, color="grey")
    ax.set_axisbelow(True)
    ax.set_title(
        "ภาพที่ 4. HF status distribution by WATCH-DM risk group\n"
        "(No HF / Incident HF / Prevalent HF)",
        fontsize=13, fontweight="bold", pad=12, color="#1e3a5f",
    )
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.10),
              ncol=3, frameon=False, fontsize=10)
    plt.tight_layout()
    return fig


def main() -> None:
    df = pd.read_csv(COHORT_FILE)
    pct = compute_percentages(df)
    fig = build_figure(pct)
    path = save_figure(fig, "fig04_hf_status_by_risk.png")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
