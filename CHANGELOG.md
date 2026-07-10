# Changelog

All notable changes to vegtam are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **`LICENSE`** now carries the full MIT text (the scaffold shipped only the title + copyright line,
  so GitHub reported the license as "Other" despite the README/CHANGELOG saying MIT).
- **`.gitignore`** actually ignores `.env` files and keys now, matching what `CONTRIBUTING.md` promises.

### Changed
- Pre-public docs pass: `CLAUDE.md` rewritten from the (completed) build brief into a maintenance
  manual for future agents; `CONTRIBUTING.md` expanded for outside contributors; `ROADMAP.md`'s two
  overlapping "out of scope" sections consolidated; README install snippet creates `~/.local/bin` first.

## [1.0.0] - 2026-07-10

First stable release. Vegtam is a single, self-contained Bash script that walks into any one repo —
including repos you don't own — and gives you a fast, read-first lay of the land plus a few safe,
local actions. Feature-complete for v1: five inspect views (each with `--json`), four safe actions
(`sync`, `tidy`, `branch`, `pr`), two-level help, graceful degradation on missing `gh`/`jq`/access,
`shellcheck`-gated CI, and a `curl`-to-`~/.local/bin` install. Needs only `bash` + `git`; `gh` and
`jq` enhance.

### Added
- **`--json` on every inspect view** (`status`, `branches`, `prs`, `log`, `health`) — machine-readable
  output for piping into other tools, built with `jq` so escaping is always correct. Fields that
  can't be read (alerts you lack access to, a repo with no GitHub remote) come through as `null`, so
  a consumer can tell "no access" from "none found". Needs `jq`; without it, `--json` refuses cleanly
  and the human views are unaffected.
- **Shellcheck CI gate** — `.github/workflows/shellcheck.yml` runs `bash -n` + `shellcheck` on every
  push and pull request, matching the pack's convention. README carries the status badge.

### Changed
- `status`, `prs`, and `health` factored their data-gathering so the human and `--json` renders share
  one set of API calls (`status`/`prs`) or a single emitter (`health`).

## [0.4.0]

### Added
- **`vegtam sync`** — fetch, then fast-forward the current branch to its upstream. Never merges or
  rewrites history: a diverged branch is reported and left alone, and git's own `--ff-only` refuses
  to overwrite uncommitted work.
- **`vegtam tidy`** — delete local branches already merged into the default branch. **Dry-run by
  default; `--apply` required** (`--yes` skips the batch confirmation). Never the default or current
  branch, never anything on the remote; deletes only via `git branch -d`.
- **`vegtam branch <name>`** — create + switch to a branch (switches if it already exists). Local
  only.
- **`vegtam pr`** — open a PR from the current branch; a thin wrapper over `gh pr create` that
  guards against a detached HEAD or the default branch and passes extra flags through.

## [0.3.0]

### Added
- **`vegtam health`** (alias `hunt`) — a security & freshness view: open Dependabot alerts by
  severity, dependency freshness (unwatched manifests + open Dependabot update PRs), and
  third-party GitHub Actions not pinned to a commit SHA (flagged outdated when a newer major
  exists). Best-effort and access-aware — every remote piece degrades to a note; the local scans
  always run. Convention-neutral: it reports, it doesn't audit or change anything.

## [0.2.0]

### Added
- **`vegtam branches`** — local branches (newest first) with upstream tracking, merged-into-default
  status, and age, plus the branches on `origin` you don't have locally. Read-only. `--fetch`
  refreshes tracking + remote branches.
- **`vegtam prs`** — open pull requests with a per-PR CI rollup glyph, source branch, author, and
  age; the ones you authored are tagged `(you)`.
- **`vegtam log`** — a newest-first timeline of commits (current branch), merged PRs, and releases,
  windowed by `--since` (default `2w`). Commits work offline; the GitHub events need `gh`.

### Changed
- Factored the CI verdict logic into a shared `classify_ci` helper used by both `status` and `prs`.

## [0.1.0]

### Added
- **`vegtam status`** — the flagship one-screen briefing on the current repo: name, description,
  visibility, default branch, fork/ahead-behind relationship, current branch + dirty state +
  stashes, latest commit with its CI rollup, and open PR/issue counts. `--fetch` refreshes
  ahead/behind from the remote first.
- **Repo resolution from the working directory** — confirms it's inside a git work tree, finds the
  root, and parses a github.com `owner/name` from the remotes (ssh, https, and `ssh://` forms).
- **Graceful degradation** — the git-only views work with no `gh`/`jq`, no GitHub remote, or no
  access; each missing remote section prints a short note instead of failing.
- **Dispatcher + two-level help** (`vegtam help`, `vegtam <cmd> help`), `--version`, and
  `NO_COLOR` / non-TTY plain-text output.
- Initial scaffold.
