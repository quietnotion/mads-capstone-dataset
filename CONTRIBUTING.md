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

Open an issue via [the issue form](https://github.com/quietnotion/mads-capstone-dataset/issues/new/choose), or email [quiet@umich.edu](mailto:quiet@umich.edu). Include:

- Cohort and team number (or project title)
- What should change
- Optional: why

## Requesting redaction

If you want your team's row removed, open an issue or email [quiet@umich.edu](mailto:quiet@umich.edu). Turnaround is 48 hours. No explanation required.

## Adding a new project

Follow the existing row format. Fields: `cohort,team_number,project_title,team_size,subject_category,has_report,has_video,has_code_repo,has_live_app,notes`.

If you are unsure which subject category applies, pick your best guess and say so in the PR description. A reviewer will push back if another category fits better.

## Ground rules

- **Never add individual names, Slack handles, emails, mentor names, or URLs.** That's the privacy boundary. Anything at that level goes through UMSI's own channels, not this repo.
- Keep notes brief. One sentence.
- If you think a category boundary needs to move, open an issue before PRing a mass recategorization. We'll talk it through.
