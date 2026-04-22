"""Regenerate chart.png from the CSV.

Usage:
    python scripts/make_chart.py
"""
import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "data" / "mads_capstone_projects_by_subject_area.csv"
OUT_PATH = REPO_ROOT / "chart.png"

# UMich brand palette (brand.umich.edu)
MICH_BLUE = "#00274C"
MAIZE = "#FFCB05"
TAPPAN_RED = "#D86018"
BODY = "#333333"
SUPPORT_GRAY = "#999999"

COHORT_ORDER = ["SS25", "F25", "W26"]
COHORT_LABEL = {
    "SS25": "Spring/Summer 2025",
    "F25": "Fall 2025",
    "W26": "Winter 2026",
}
COHORT_COLOR = {
    "SS25": MICH_BLUE,
    "F25": TAPPAN_RED,
    "W26": MAIZE,
}


def load():
    with open(CSV_PATH) as f:
        return list(csv.DictReader(f))


def make_chart():
    rows = load()
    cross = Counter((r["cohort"], r["subject_category"]) for r in rows)
    totals = Counter(r["subject_category"] for r in rows)

    categories = sorted(totals.keys(), key=lambda c: -totals[c])
    values = {
        c: np.array([cross.get((c, cat), 0) for cat in categories])
        for c in COHORT_ORDER
    }
    cohort_totals = {c: int(values[c].sum()) for c in COHORT_ORDER}
    grand_total = sum(cohort_totals.values())

    fig = plt.figure(figsize=(12, 8.5))
    ax = fig.add_axes([0.28, 0.13, 0.68, 0.72])

    left = np.zeros(len(categories))
    for c in COHORT_ORDER:
        ax.barh(
            categories,
            values[c],
            left=left,
            color=COHORT_COLOR[c],
            label=f"{COHORT_LABEL[c]} (n={cohort_totals[c]})",
            linewidth=0,
        )
        left += values[c]

    ax.invert_yaxis()
    ax.set_xlabel("Number of Projects", fontsize=11, color=BODY)

    for i, cat in enumerate(categories):
        ax.text(totals[cat] + 0.18, i, str(totals[cat]),
                va="center", fontsize=10.5, color=BODY, fontweight="bold")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(SUPPORT_GRAY)
    ax.spines["bottom"].set_color(SUPPORT_GRAY)
    ax.tick_params(colors=BODY, labelsize=10)
    ax.grid(axis="x", alpha=0.25, linestyle=":", color=SUPPORT_GRAY)
    ax.set_xlim(0, max(totals.values()) + 2)

    ax.legend(loc="lower right", frameon=False, fontsize=9.5,
              title="Capstone Cohort", title_fontsize=10)

    fig.text(0.02, 0.945,
             f"MADS Capstone Projects by Subject Area   (n = {grand_total})",
             fontsize=16, fontweight="bold", color=MICH_BLUE)
    fig.text(0.02, 0.905,
             "Posting in #mads-capstone-gallery is mandatory for MADS capstones. Channel opened May 17, 2025.",
             fontsize=10.5, color=BODY, style="italic")

    plt.savefig(OUT_PATH, dpi=160, facecolor="white")
    print(f"Saved {OUT_PATH} (n = {grand_total})")


if __name__ == "__main__":
    make_chart()
