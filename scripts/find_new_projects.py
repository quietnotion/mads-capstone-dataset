"""Find capstone projects in text input that are not yet in the CSV.

Usage:
    python scripts/find_new_projects.py path/to/slack_paste.txt
    python scripts/find_new_projects.py -                    # read from stdin
    echo "My Project Title" | python scripts/find_new_projects.py -

How it works:
- Looks for lines prefixed with `Project:`, `Project Title:`, `Project Name:`,
  or `Title:` (case insensitive). These are the common formats used in the
  #mads-capstone-gallery channel.
- Falls back to treating every sufficiently long line as a candidate title
  when no prefix lines are found (useful when you paste just a list of
  titles, one per line).
- Normalizes titles (lowercase, parentheticals removed, punctuation
  collapsed) and compares each candidate against every title already in the
  dataset with a fuzzy match threshold of 0.85.
"""
import csv
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "data" / "mads_capstone_projects_by_subject_area.csv"

TITLE_PREFIX = re.compile(
    r"^\s*(?:project(?:\s+title|\s+name)?|title)\s*[:=]\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)

MATCH_THRESHOLD = 0.85
MIN_FALLBACK_LENGTH = 20


def normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if s.startswith("the "):
        s = s[4:]
    return s


def load_existing():
    with open(CSV_PATH) as f:
        return [
            (row["project_title"], normalize(row["project_title"]))
            for row in csv.DictReader(f)
        ]


def extract_candidates(text: str):
    matches = [m.strip() for m in TITLE_PREFIX.findall(text) if m.strip()]
    if matches:
        return matches
    # Fallback: take any reasonably long line
    return [
        line.strip()
        for line in text.splitlines()
        if len(line.strip()) >= MIN_FALLBACK_LENGTH
    ]


def best_match(title_norm: str, existing):
    best_ratio = 0.0
    best_title = None
    for original, norm in existing:
        ratio = SequenceMatcher(None, title_norm, norm).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_title = original
    return best_title, best_ratio


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/find_new_projects.py <path.txt | ->",
            file=sys.stderr,
        )
        sys.exit(1)

    arg = sys.argv[1]
    text = sys.stdin.read() if arg == "-" else Path(arg).read_text()

    existing = load_existing()
    candidates = extract_candidates(text)

    if not candidates:
        print("No candidate titles found in input.", file=sys.stderr)
        sys.exit(1)

    new_titles = []
    dup_titles = []
    for c in candidates:
        match, ratio = best_match(normalize(c), existing)
        if ratio >= MATCH_THRESHOLD:
            dup_titles.append((c, match, ratio))
        else:
            new_titles.append((c, match, ratio))

    print(
        f"Checked {len(candidates)} candidate title(s) against "
        f"{len(existing)} existing rows.\n"
    )

    if dup_titles:
        print(f"Already in dataset ({len(dup_titles)}):")
        for candidate, match, ratio in dup_titles:
            line = f"  - {candidate}"
            if candidate.lower().strip() != match.lower().strip():
                line += f"  (matches '{match}', similarity {ratio:.2f})"
            print(line)
        print()

    if new_titles:
        print(f"Not yet in dataset ({len(new_titles)}):")
        for candidate, closest, ratio in new_titles:
            print(f"  - {candidate}")
            if closest and ratio >= 0.6:
                print(f"      closest existing title: '{closest}' ({ratio:.2f}) — review manually")
    else:
        print("Nothing new. Dataset already covers everything in your input.")


if __name__ == "__main__":
    main()
