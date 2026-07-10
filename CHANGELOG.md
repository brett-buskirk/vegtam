# Changelog

All notable changes to vegtam are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
