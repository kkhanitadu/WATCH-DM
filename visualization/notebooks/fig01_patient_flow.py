"""ภาพที่ 1 — Patient Flow Diagram.

CONSORT-style cohort flow showing the exclusion cascade from the full DM
outpatient dataset (n = 13,958) down to the final analytic cohort (n = 2,382).

Exclusions are driven by missing data on WATCH-DM scoring variables.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.style import DPI, save_figure


# ── Flow numbers (hard-coded from cohort QC — verified) ───────────────
MAIN_BOXES = [
    (5.0, 9.2, 5.2, 0.9, "Total patients in dataset\nn = 13,958",  "#dbeafe", "#1d4ed8"),
    (5.0, 7.0, 5.2, 0.9, "After vitals filter\nn = 12,751",         "#dbeafe", "#1d4ed8"),
    (5.0, 4.8, 5.2, 0.9, "After eGFR filter\nn = 10,983",           "#dbeafe", "#1d4ed8"),
    (5.0, 2.6, 5.2, 0.9, "Final analysis cohort\nn = 2,382",        "#dcfce7", "#16a34a"),
]
EXCL_BOXES = [
    (8.4, 8.1, 2.9, 1.0, "Excluded: n = 1,207\n(No vital sign records)",     "#fef3c7", "#d97706"),
    (8.4, 5.9, 2.9, 1.0, "Excluded: n = 1,768\n(No renal function lab)",      "#fef3c7", "#d97706"),
    (8.4, 3.7, 2.9, 1.3, "Excluded: n = 8,592\n(HDL not routinely\nordered)", "#fef3c7", "#d97706"),
]


def build_figure():
    fig, ax = plt.subplots(figsize=(9, 8), dpi=DPI)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    for cx, cy, w, h, label, fc, ec in MAIN_BOXES:
        box = mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.08", linewidth=1.5,
            edgecolor=ec, facecolor=fc, zorder=3,
        )
        ax.add_patch(box)
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="#1e293b", zorder=4)

    for cx, cy, w, h, label, fc, ec in EXCL_BOXES:
        box = mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.08", linewidth=1.2,
            edgecolor=ec, facecolor=fc, zorder=3,
        )
        ax.add_patch(box)
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=8.5, color="#78350f", zorder=4)

    # Down arrows along the main column
    arrow_main = dict(arrowstyle="->", color="#475569", lw=1.8,
                      mutation_scale=16, zorder=2)
    for y_start, y_end in [(8.75, 7.45), (6.55, 5.25), (4.35, 3.05)]:
        ax.annotate("", xy=(5.0, y_end), xytext=(5.0, y_start),
                    arrowprops=arrow_main)

    # Side arrows to exclusion boxes
    arrow_side = dict(arrowstyle="->", color="#94a3b8", lw=1.3,
                      mutation_scale=13, zorder=2)
    for y_arr, y_box in [(8.05, 8.1), (5.85, 5.9), (3.65, 3.7)]:
        ax.annotate("", xy=(6.95, y_box), xytext=(5.0, y_arr),
                    arrowprops=arrow_side)

    ax.set_title("ภาพที่ 1. Patient Flow Diagram", fontsize=13,
                 fontweight="bold", pad=10, color="#1e3a5f", y=0.98)
    plt.tight_layout()
    return fig


def main() -> None:
    fig = build_figure()
    path = save_figure(fig, "fig01_patient_flow.png")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
