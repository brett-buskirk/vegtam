# Changelog

All notable changes to vegtam are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
