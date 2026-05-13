"""Shared plot style for all WATCH-DM figures.

Single source of truth for colors, group labels, output paths, and DPI so that
every figure in the manuscript has a consistent look.
"""

from __future__ import annotations

from pathlib import Path

# ── Output directory (relative to repo root) ───────────────────────────
OUT = Path(__file__).resolve().parents[2] / "visualization" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


# ── DPI for all exports ────────────────────────────────────────────────
DPI = 300


# ── Risk-group labels ──────────────────────────────────────────────────
GROUPS_FULL  = ["Very Low", "Low", "Average", "High", "Very High"]
GROUPS_SHORT = GROUPS_FULL  # alias kept for backward compatibility with the
                            # supplemental code

# ── Color palette per risk group ───────────────────────────────────────
# Green → Yellow → Orange → Red gradient, colorblind-tested
COLORS = [
    "#4ade80",  # Very Low  — green
    "#86efac",  # Low       — light green
    "#fbbf24",  # Average   — amber
    "#f97316",  # High      — orange
    "#ef4444",  # Very High — red
]


# ── HF-status palette (used in Figure 4 of the manuscript) ─────────────
HF_COLORS = {
    "No HF":     "#94a3b8",  # slate
    "Incident":  "#3b82f6",  # blue
    "Prevalent": "#dc2626",  # crimson
}


def save_figure(fig, filename: str, **kwargs) -> Path:
    """Save a figure to the canonical figures/ directory at the right DPI."""
    path = OUT / filename
    fig.savefig(
        path,
        dpi=DPI,
        bbox_inches=kwargs.pop("bbox_inches", "tight"),
        facecolor=kwargs.pop("facecolor", "white"),
        **kwargs,
    )
    return path
