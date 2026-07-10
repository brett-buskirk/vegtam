# vegtam

**The wanderer — a pocket CLI for whatever repo you're standing in.**

Odin walks Midgard in disguise under the name *Vegtam*. This tool is that mode: it works on
**exactly one repository — the one your shell is in right now** — reading everything live from the
local `.git` and its GitHub remote. No config, no stored state, no assumptions about who owns the
repo. Run it inside any repo, anywhere on the machine, and get a fast lay of the land.

```
  vegtam  ·  brett-buskirk/geri
  The hunter of your GitHub estate — outdated deps, security advisories, and drift.

    ● public   ·   default main
    branch    main  ✓ clean  (up to date)
    head      121b5b4  ✓ checks pass  · 5d ago
    open      0 PRs   ·   0 issues
```

## Works in any repo. Owns nothing.

Vegtam is built for the repos that *aren't* yours — client work, an open-source contribution,
something you just cloned. That inverts the usual risk posture, so three rules hold throughout:

- **Read-first, act-light.** The value is in the *views*, and views are safe everywhere. The
  handful of actions are scoped to "help me work *in* this repo," never "clean up someone else's."
- **Convention-neutral.** Vegtam reports *what is*. It doesn't audit your repo against anyone's
  house style.
- **Permission-aware.** Contributor without admin? Read-only? Non-GitHub remote? Every remote call
  degrades to a quiet, informative line — never a crash or a stack trace.

Nothing Vegtam does touches remote state or your uncommitted work unless you explicitly ask — and
even then, the destructive-adjacent bits are dry-run by default.

## Install

Vegtam is a single, self-contained Bash script. Drop it on your `PATH`:

```sh
curl -fsSL https://raw.githubusercontent.com/brett-buskirk/vegtam/main/vegtam -o ~/.local/bin/vegtam
chmod +x ~/.local/bin/vegtam
```

**Requires** `bash` and `git`. The GitHub CLI (`gh`) and `jq` unlock the GitHub-backed sections;
without them, the local git views still work.

## Usage

```
vegtam [status]      one-screen briefing on the current repo (the default)
vegtam branches      local + remote branches: tracking, merged, stale
vegtam prs           open pull requests with their CI status
vegtam log           timeline of commits, merged PRs, and releases
vegtam help          the menu
vegtam <cmd> help    detail & options for any command
vegtam --version     print the version
```

### `status` — the flagship

One glance tells you where you stand:

- repo name, description, visibility, and default branch
- your relationship to it — a fork of whom, and how far ahead/behind its upstream you are
- current branch, dirty state, and stashes
- the latest commit, its CI status, and how long ago
- open PR and issue counts

Fast and local by default; add `--fetch` to refresh ahead/behind from the remote first. Respects
`NO_COLOR` and prints plain text when piped.

### `branches`

Your local branches, newest commit first — each with its upstream tracking state (`↑ahead`/
`↓behind`, `[gone]`, or `local-only`), whether it's merged into the default branch, and its age —
followed by the branches on `origin` you don't have locally. Purely descriptive; it never deletes
anything (that's `tidy`, later). `--fetch` refreshes tracking and remote branches first.

### `prs`

Open pull requests, each with a CI glyph (`✓` pass · `✗` fail · `●` running · `·` none), its
source branch, author, and age. The ones you authored are tagged `(you)`.

### `log`

A newest-first timeline of what changed: commits on the current branch (`●`), merged PRs (`⑃`),
and releases (`⚑`). `--since <window>` sets how far back to look — `6h`, `3d`, `2w` (default),
`1mo`. Commits always work; the GitHub events need `gh`.

## Roadmap

The views ship today. The rest arrives one safe, reviewable piece at a time:

- **security & freshness** — `health`: Dependabot alerts, outdated dependencies, unpinned actions,
  degrading gracefully where access is denied
- **safe local actions** — `sync` (fast-forward only), `tidy` (prune merged local branches,
  dry-run by default), `branch`, `pr`

See [ROADMAP.md](ROADMAP.md). Anything remote-mutating or destructive beyond that safe local set is
deliberately out of scope — that's not what a wanderer is for.

## License

MIT — see [LICENSE](LICENSE).
