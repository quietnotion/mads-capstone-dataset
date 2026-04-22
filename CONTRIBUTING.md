# Contributing

The point of this repo is to stay useful as more cohorts finish capstones. That means other people adding to it.

## What kind of changes are welcome

- A new cohort's worth of data, once projects wrap and get shared
- Fixes to team number, title, team size, booleans
- Re tagging a project into a different subject category (see [`taxonomy.md`](taxonomy.md) for the current rules)
- New subject categories, with reasoning
- Typos, missing projects, anything else that's wrong

## Easiest way to contribute

1. Go to [`data/mads_capstone_projects_by_subject_area.csv`](data/mads_capstone_projects_by_subject_area.csv) on GitHub.
2. Click the pencil icon on the top right ("Edit this file").
3. Make your change.
4. Scroll down, write a short message describing what you changed.
5. Click "Propose changes." GitHub creates a pull request automatically.

No local git setup required. No forking. Browser only.

## If you don't have a GitHub account

Open an issue via [the issue form](https://github.com/quietnotion/mads-capstone-dataset/issues/new/choose). GitHub sign up is free. Include:

- Cohort and team number (or project title)
- What should change
- Optional: why

## Requesting redaction

If you want your team's row removed, open an issue. No explanation required.

## Adding a new project

Follow the existing row format. Fields: `cohort,team_number,project_title,team_size,subject_category,has_report,has_video,has_code_repo,has_live_app,notes`.

If you are unsure which subject category applies, pick your best guess and say so in the PR description. A reviewer will push back if another category fits better.

## Avoiding duplicates

Every project title in the CSV is unique. Before adding a row, check whether your project is already listed.

### Checking one project (your team)

Easiest path: open [the CSV on GitHub](data/mads_capstone_projects_by_subject_area.csv), hit `Cmd+F` or `Ctrl+F`, and search for a distinctive word from your title. If nothing comes up, it's safe to add.

### Checking a batch (e.g. a whole cohort paste from Slack)

Use the helper script. It takes a text file or stdin, extracts project titles, and tells you which are already in the dataset and which are new.

```
python scripts/find_new_projects.py path/to/my_paste.txt
```

Or pipe directly:

```
echo "My New Capstone Project" | python scripts/find_new_projects.py -
```

The script looks for lines prefixed with `Project:`, `Project Title:`, `Project Name:`, or `Title:` (the common formats used in `#mads-capstone-gallery`). If none are found, it falls back to treating long input lines as titles. Matches against the existing CSV use fuzzy comparison with an 85% similarity threshold, which catches minor variations like different capitalization or an added subtitle. Anything below the threshold is shown as "not yet in dataset," with the closest existing title noted when it's a close call (60% similarity or higher). Use your judgment on borderline cases.

### Typical cohort workflow

When Spring/Summer 2026 wraps and you want to batch add projects:

1. Scroll the channel to the first SS26 post.
2. Copy the channel text into a file (any plain text format works).
3. Run `python scripts/find_new_projects.py your_file.txt`.
4. Copy the "not yet in dataset" titles into new CSV rows with their cohort, team number, category, and flags.
5. Open a PR. The maintainer merges, the GitHub Action regenerates chart and JSON, and a new release tag can be cut to mark the cutoff.

## Ground rules

- **Never add individual names, Slack handles, emails, mentor names, or URLs.** That's the privacy boundary. Anything at that level goes through UMSI's own channels, not this repo.
- Keep notes brief. One sentence.
- If you think a category boundary needs to move, open an issue before PRing a mass recategorization. We'll talk it through.
