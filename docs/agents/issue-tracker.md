# Issue Tracker: Local Markdown

This project uses local markdown files in `.scratch/` as the issue tracker.

## Location

Issues are stored as individual markdown files under `.scratch/`. Each issue should be in a feature-specific subdirectory, e.g., `.scratch/<feature-name>/`.

## Workflow

- New issues are created as markdown files with a descriptive name
- Issues can be triaged by adding labels and updating their status
- Agent skills like `to-tickets`, `triage`, `to-spec`, and `qa` read from and write to this location
- PRs as a request surface: **off** (can be enabled by editing this file if needed)

## File Format

Each issue file should contain:
- Title
- Description
- Labels
- Status
- Blocking edges (if any)
