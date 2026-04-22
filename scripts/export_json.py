"""Export the CSV to JSON for agent and tool consumption.

Usage:
    python scripts/export_json.py
"""
import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "data" / "mads_capstone_projects_by_subject_area.csv"
JSON_PATH = REPO_ROOT / "data" / "mads_capstone_projects_by_subject_area.json"

BOOL_FIELDS = {"has_report", "has_video", "has_code_repo", "has_live_app"}
INT_FIELDS = {"team_number", "team_size"}


def coerce(row):
    out = {}
    for k, v in row.items():
        if k in BOOL_FIELDS:
            out[k] = v.strip().lower() == "true"
        elif k in INT_FIELDS:
            try:
                out[k] = int(v)
            except (ValueError, TypeError):
                out[k] = v
        else:
            out[k] = v
    return out


def main():
    with open(CSV_PATH) as f:
        rows = [coerce(r) for r in csv.DictReader(f)]
    with open(JSON_PATH, "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {JSON_PATH} ({len(rows)} projects)")


if __name__ == "__main__":
    main()
