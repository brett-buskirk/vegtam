# vegtam cheat sheet

Quick reference for every command, option, and behavior. `vegtam` operates on the **one repo you're
standing in**, read live from its `.git` and GitHub remote — no config, no stored state.

For the narrative version see the [README](README.md); for per-command detail in the terminal, run
`vegtam <command> help`.

---

## At a glance

| Command | Aliases | What it does | Options |
|---------|---------|--------------|---------|
| [`status`](#status) | *(default)* | One-screen briefing on the current repo | `-f`/`--fetch`, `--json` |
| [`branches`](#branches) | `br` | Local + remote branches: tracking, merged, stale | `-f`/`--fetch`, `--json` |
| [`prs`](#prs) | `pulls` | Open pull requests with CI status | `--json` |
| [`log`](#log) | `activity` | Timeline of commits, merged PRs, releases | `--since <window>`, `--json` |
| [`health`](#health) | `hunt` | Security & freshness: alerts, deps, unpinned actions | `--json` |
| [`sync`](#sync) | | Fast-forward the current branch to its upstream | |
| [`tidy`](#tidy) | | Delete merged local branches (**dry-run by default**) | `--apply`, `-y`/`--yes` |
| [`branch`](#branch-name) | | Create + switch to a branch | |
| [`pr`](#pr) | | Open a PR from the current branch | *(passes flags to `gh pr create`)* |
| [`help`](#help--version) | `-h`, `--help` | The command menu | |
| `version` | `-V`, `--version` | Print the version | |

- **Inspect** views (`status` `branches` `prs` `log` `health`) are read-only and safe anywhere. Each
  takes `--json`.
- **Act** commands (`sync` `tidy` `branch` `pr`) are the only ones that change anything — all local
  and self-scoped. `tidy` is dry-run by default.
- Running `vegtam` with no command is the same as `vegtam status`.

---

## Requirements & global behavior

- **Requires** `bash` + `git`. `gh` (GitHub CLI) unlocks the GitHub-backed sections; `jq` enables
  `--json`. Missing any of these degrades gracefully — the local git views still work.
- **`NO_COLOR`** — set it (`NO_COLOR=1 vegtam …`) to disable color. Output is also automatically plain
  when piped or redirected (not a TTY).
- **`--json`** — needs `jq`; without it the flag refuses cleanly (exit 1) and the human views are
  unaffected. Fields you can't read come through as `null` (tell "no access" from "none found").
- **Two-level help** — `vegtam help` for the menu, `vegtam <command> help` (or `-h`/`--help`) for one
  command.
- **Exit codes** — `0` on success; `1` on error (not in a git repo, unknown command, bad `--since`,
  `--json` without `jq`, or an action's guard refusing).

---

## Inspect

### `status`

One-screen briefing: name · description · visibility · default branch · fork relationship ·
ahead/behind upstream · current branch + dirty state + stashes · latest commit + CI · open PR/issue
counts. Fast and local by default; the GitHub lines degrade to a note without `gh`/access.

```sh
vegtam                 # status is the default command
vegtam status
vegtam status --fetch  # git fetch first, for fresh ahead/behind (network)
vegtam status -f
vegtam status --json   # machine-readable (needs jq)
```

| Option | Effect |
|--------|--------|
| `-f`, `--fetch` | `git fetch --all` first so ahead/behind is fresh (network) |
| `--json` | Emit one JSON object instead of the human view |

**`--json` fields:** `repo, name, root, description, visibility, defaultBranch, branch, isFork,
parent, dirty, stashes, hasUpstream, ahead, behind, head{sha, ci, lastCommitRelative}, openPRs,
openIssues, remoteAvailable`

---

### `branches`

Local branches (newest commit first) with upstream tracking (`↑ahead`/`↓behind`, `[gone]`,
`local-only`), merged-into-default status, and age — then the branches on `origin` you don't have
locally. Purely descriptive; it never deletes (that's [`tidy`](#tidy)).

```sh
vegtam branches
vegtam br               # alias
vegtam branches --fetch # git fetch --prune first, for fresh tracking + remote branches
vegtam branches --json
```

| Option | Effect |
|--------|--------|
| `-f`, `--fetch` | `git fetch --prune --all` first (network) |
| `--json` | Emit the branches as JSON |

**`--json` shape:** `{ defaultBranch, local[], remoteOnly[] }` where each `local` item is
`{ name, upstream, track, committed, merged, current, default }` and each `remoteOnly` item is
`{ name, committed }`.

---

### `prs`

Open pull requests, each with a CI glyph, source branch, author, and age. Your own are tagged
`(you)`.

CI glyphs: `✓` pass · `✗` fail · `●` running · `·` none.

```sh
vegtam prs
vegtam pulls            # alias
vegtam prs --json
```

| Option | Effect |
|--------|--------|
| `--json` | Emit the open PRs as a JSON array |

**`--json` item fields:** `number, title, author, branch, draft, createdAt, checks, mine`
(`checks` is one of `pass`/`fail`/`pending`/`none`; `mine` is a bool).

Degrades to a note (human) or `[]` + a stderr reason (`--json`) when there's no GitHub remote or no
`gh`. Distinguishes "no open PRs" from "couldn't read the repo".

---

### `log`

Newest-first timeline of what changed: commits on the current branch (`●`), merged PRs (`⑃`), and
releases (`⚑`). Commits always work; the GitHub events need `gh`.

```sh
vegtam log                 # default window: 2w
vegtam activity            # alias
vegtam log --since 6h
vegtam log --since 3d
vegtam log --since 1mo
vegtam log --since 2w --json
```

| Option | Effect |
|--------|--------|
| `--since <window>` | How far back to look. Format: `<n><unit>`, unit ∈ `h` `d` `w` `mo`. Default `2w`. |
| `--json` | Emit the timeline as a JSON array |

**`--since` examples:** `6h` · `3d` · `2w` (default) · `1mo`. A malformed window errors (exit 1).

**`--json` events** (array, newest first), by `type`:
- `{ type:"commit",  ts, sha, title }`
- `{ type:"pr",      ts, number, title }`
- `{ type:"release", ts, tag, name }`

---

### `health`

Security & freshness — three neutral, best-effort, access-aware signals. Reports what *is*; changes
nothing.

```sh
vegtam health
vegtam hunt            # alias
vegtam health --json
```

| Section | Shows |
|---------|-------|
| **alerts** | Open Dependabot advisories by severity. Needs security read — a contributor usually can't see these, so it degrades to a note. |
| **deps** | Dependency manifests with nothing watching them, and open Dependabot update PRs. |
| **actions** | Third-party Actions not pinned to a commit SHA (the supply-chain hardening rec), flagged `outdated` when a newer major exists. |

| Option | Effect |
|--------|--------|
| `--json` | Emit the three signals as one structured object (`null` where a section can't be read) |

**`--json` shape:**
```
{
  alerts:  { available, open, bySeverity{critical,high,medium,low}, items[] },
  deps:    { dependabotConfigured, ecosystems[], unmonitored, updatePRsChecked, updatePRs[] },
  actions: { workflows, unpinned[] },
  signals: <count>
}
```

---

## Act — safe, local, self-scoped

These are the only commands that change anything. None touch remote branches, close others' PRs, or
rewrite history.

### `sync`

Fetch, then **fast-forward** the current branch to its upstream — nothing more.

```sh
vegtam sync
```

- **Diverged** (you have local commits the remote doesn't) → reports it and stops. It won't
  rebase/merge for you.
- **No upstream** → clean no-op with a hint to set one.
- **Dirty tree** → a clean fast-forward still proceeds; git itself refuses to overwrite uncommitted
  changes, so your work is never clobbered.
- **Behind only** → fast-forwards and reports `+N commits`.

### `tidy`

Delete local branches already merged into the default branch. **Dry-run by default** — lists what it
*would* delete and changes nothing until `--apply`.

```sh
vegtam tidy               # dry-run: list merged branches, delete nothing
vegtam tidy --apply       # delete them (confirms once for the batch)
vegtam tidy --apply --yes # delete without the confirmation prompt
vegtam tidy --apply -y
```

| Option | Effect |
|--------|--------|
| `--apply` | Actually delete the merged branches |
| `-y`, `--yes` | Skip the one batch-confirmation prompt (with `--apply`) |

Safety: never the **default** branch, never the **current** branch, never anything on the **remote**;
deletes only via `git branch -d` (which itself refuses a not-fully-merged branch). Refuses entirely
if it can't resolve a real default branch to measure "merged" against. The confirmation reads
`/dev/tty` directly, so a piped `--apply` won't silently auto-delete — pass `--yes` for that.

### `branch <name>`

Create a branch and switch to it — or just switch, if it already exists (safe to run twice). Purely
local; nothing is pushed.

```sh
vegtam branch fix/typo-in-readme
vegtam branch feat/new-thing
```

### `pr`

Open a pull request from the current branch — a thin wrapper over `gh pr create`. Any extra flags
pass straight through.

```sh
vegtam pr                  # interactive — gh prompts for title/body
vegtam pr --fill           # title/body from the commits
vegtam pr --fill --web     # …then open it in the browser
vegtam pr --draft          # open as a draft
vegtam pr --base develop   # target a non-default base
```

**Refuses early** (before handing off to `gh`) when:
- you're on a **detached HEAD**,
- you're on the **default branch** (make a feature branch first),
- the branch has **no commits beyond the base** (nothing to open),
- there's **no GitHub remote**, or **`gh` isn't installed**.

Otherwise it hands off to `gh pr create`, which pushes the branch if needed (via a fork when you
can't push to origin) and prompts for the rest.

---

## `help` & version

```sh
vegtam help            # the command menu
vegtam -h              # same
vegtam <command> help  # detail for one command (e.g. vegtam tidy help)
vegtam --version       # print the version
vegtam -V              # same
```

---

## Recipes

```sh
# Where do I stand in this repo? (the flagship, default command)
vegtam

# Am I behind the remote before I start work?
vegtam status --fetch

# What are the open PRs, and which are mine?
vegtam prs

# Just my open PRs, as data
vegtam prs --json | jq '[.[] | select(.mine)]'

# Am I behind my upstream? (scriptable)
vegtam status --json | jq '.behind'

# How many open Dependabot alerts? (null → 0 when you can't read them)
vegtam health --json | jq '.alerts.open // 0'

# What shipped here in the last month?
vegtam log --since 1mo

# Catch my branch up to the remote (fast-forward only)
vegtam sync

# See which merged branches I could clean up (deletes nothing)
vegtam tidy

# Actually delete them, no prompt
vegtam tidy --apply --yes

# Start a feature branch and open a PR from it
vegtam branch feat/checkout-v2
#   … commit some work …
vegtam pr --fill --web

# Plain output for a log/pipe (no color)
NO_COLOR=1 vegtam status
```
