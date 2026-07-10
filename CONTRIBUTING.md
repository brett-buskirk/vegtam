# Contributing

Thanks for taking a look. Vegtam is a single, self-contained Bash script — there's no build step
and no dependencies to install beyond what you already have.

## Working on it

- Everything lives in one file: **`vegtam`**. Edit it, then run it from the repo (`./vegtam …`).
- **Requires** `bash` and `git`; `gh` and `jq` are optional (they light up the GitHub-backed views
  and `--json`).
- Before you push, run what CI runs:
  ```sh
  bash -n vegtam       # syntax
  shellcheck vegtam    # lint — must be clean
  ```
  Every push and PR is `shellcheck`-gated.

## What to keep true

Vegtam runs inside repositories its user doesn't own, so a few things are non-negotiable:

- **Read-first.** New views are welcome. New *actions* must be safe and local — never delete remote
  branches, close others' PRs, rewrite history, or touch uncommitted work. Anything
  destructive-adjacent is dry-run by default.
- **Zero-config and self-contained.** No config files, no environment assumptions — someone should be
  able to `curl` the one file and run it anywhere.
- **Degrade gracefully.** Every `gh`/`jq` call can fail (no access, non-GitHub remote, tool missing);
  handle it with a short note, never a crash or a stack trace.
- Match the surrounding style, and comment the non-obvious *why* (not the obvious *what*).

## Pull requests

- **No direct commits to `main`** — branch → PR → green checks → merge.
- Keep changes focused and reviewable; update `README` / `CHANGELOG` / `ROADMAP` alongside code.
- Never commit secrets — `.env` files and keys are gitignored; keep it that way.
