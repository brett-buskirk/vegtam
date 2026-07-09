# CLAUDE.md — Vegtam Build Brief
### A single-repo swiss-army CLI — the wanderer that walks into any repo, anywhere

> `huginn new` scaffolded this repo (guardrails, ruleset, labels, the full docs suite, a signed genesis
> commit). This file is the build brief for the agent that builds Vegtam. Read it top to bottom first.
> **The pack's tools are your structural reference — read `~/github-repos/huginn/huginn` for the
> dispatcher/help/color idioms — but Vegtam is deliberately NOT one of the beasts (see "How it differs").**

---

## The concept

In the estate, Odin sits in the **high seat** ([`grimnir`](https://github.com/brett-buskirk/grimnir)) and
sees all his own realms at once — the whole `~/github-repos` estate, through the ravens
([`huginn`](https://github.com/brett-buskirk/huginn), [`muninn`](https://github.com/brett-buskirk/muninn))
and wolves ([`geri`](https://github.com/brett-buskirk/geri),
[`freki`](https://github.com/brett-buskirk/freki)). That whole pack is **estate-scoped**: it scans every
repo under one root and acts across all of them.

**Vegtam is the other mode.** *Vegtam* ("the wanderer") is the name Odin travels under when he leaves
Asgard and walks Midgard in disguise, visiting one realm at a time. This tool is that: it operates on
**exactly one repository — whichever one you're standing in when you call it** — derived from the local
`.git` and its remote. You run it *inside* a repo, anywhere on the machine, and it gives you a fast lay of
the land plus a few safe actions. It is all the beasts' most useful views, folded into one command,
scoped to a single repo.

**The whole point is portability:** Vegtam is meant for the repos that *aren't* your estate — client
work, a contribution to someone else's project, a repo you just cloned. The pack is overkill and
wrong-shaped for those. Vegtam fits in your pocket and goes anywhere.

## The governing design decision: it runs in OTHER PEOPLE'S repos

Read this before writing a single command. Vegtam's default context is a repository **Brett does not
own**. That inverts the pack's risk posture completely, and three rules follow from it. They are not
negotiable:

1. **Read-first, act-light.** The value is 90% in the *views* (fast aggregation), and the views are safe
   everywhere. Actions are scoped to "help me work *in* this repo," never "clean up someone's repo."
   Safe actions only: fetch/sync, prune **merged local** branches (dry-run by default), create a branch,
   open a PR from HEAD. **Never** delete remote branches, close others' PRs, or delete artifacts/releases.
   The whole `freki` "reaper" instinct is *wrong* in a foreign repo. (This is Brett's own managed-policy
   rule: propose-don't-presume on irreversible, outward-facing actions.)
2. **Convention-neutral.** Vegtam **reports what is**; it does not audit against Brett's estate standard.
   `huginn doctor` flags deviations from *our* conventions — that is presumptuous and useless in a repo
   whose owner never agreed to them. Do not port `doctor`. (An optional, off-by-default "does this match
   my own conventions?" check could exist later; it is not the point and not in v1.)
3. **Permission-aware, degrades gracefully.** Brett is often a contributor without admin, or read-only.
   Every capability must handle "you lack rights to see/do that" cleanly — a quiet, informative line, not
   a crash or a stack trace. Never assume ownership or write access.

## Scope — v1 (read/aggregate + safe local actions)

Everything is derived live from the **current repo** via `git` (local) and `gh` (its remote). No estate
model, no scanning sibling directories, no stored state.

### Views (the heart of v1 — safe everywhere)
- **`vegtam` / `vegtam status`** — the flagship one-screen briefing (the repo-local `survey`): repo name +
  description + visibility, default branch, your relationship to it (fork? upstream? ahead/behind of the
  remote?), current branch + dirty state, a count of open PRs and open issues, CI status of the latest
  commit, and last activity. One glance, you know where you stand.
- **`vegtam branches`** — local + remote branches: current, dirty, ahead/behind, merged, and stale ones.
- **`vegtam prs`** — open PRs with their CI/check status; highlight the ones authored by the current user.
- **`vegtam log`** (or `activity`) — recent commits / merged PRs / releases; a "what changed since I last
  looked" delta is a nice touch (muninn-flavored).
- **`vegtam health`** (or `hunt`) — security & freshness *if the remote grants access*: Dependabot alerts,
  outdated dependencies, unpinned actions (geri-flavored). Degrade gracefully when access is denied.

### Actions (deliberately minimal — safe, local, gated)
- **`vegtam sync`** — fetch + fast-forward the current branch. Never clobbers uncommitted work.
- **`vegtam tidy`** — prune **merged local** branches. **Dry-run by default; `--apply` required** (borrow
  freki's safe-by-default spine). Never touches remote branches or the default/current branch.
- **`vegtam branch <name>`** — create + switch to a branch.
- **`vegtam pr`** — open a PR from the current branch (thin wrapper over `gh pr create`).

Anything destructive or remote-mutating beyond the above is **out of v1.** If it's ever added, it must be
gated on a proven ownership check, and even then dry-run by default.

## Tech & architecture

- **Single Bash script** named `vegtam`, `set -uo pipefail`. Deps: `bash`, `git`, `gh`, `jq`.
- **Dispatcher + two-level help** (`vegtam help`, `vegtam <cmd> help`) — mirror huginn's structure and its
  terse, lowercase, lightly-wry voice. Respect `NO_COLOR` and non-TTY output.
- **Fully self-contained and zero-config — this is a hard requirement and the main way it differs from the
  pack.** Vegtam must NOT depend on the estate, on `$HUGINN_ROOT`, on huginn's config, or on
  `exemptions.json`. It derives everything from the current working directory's `.git` and `gh`. Someone
  should be able to `curl` this one file into `~/.local/bin`, run it in any repo on any machine, and have
  it just work with nothing else installed. Keep it a standalone script; do not reuse the beasts' estate
  helpers (`repos()`, `is_exempt`, the config-fallback chain).
- **Resolve the repo from `pwd`.** Confirm you're inside a git work tree (`git rev-parse
  --is-inside-work-tree`); find the repo root; resolve the GitHub `owner/name` from the `origin` remote.
  Fail clearly and early when not in a repo, or when there's no GitHub remote (git-only views still work).
- **Graceful degradation is the spine.** Every `gh` call may fail on permissions or a non-GitHub remote.
  Wrap them; on failure, print a short informative note and keep going. A view that can't fetch one
  section still renders the rest.

## Code quality — comment for humans (Brett's explicit ask)

This tool is the **most adoptable** thing in the collection precisely because it isn't estate-tied — which
means it will get the most outside eyes and scrutiny. Write it accordingly:

- **Comment like a good, senior developer would** — enough that a stranger reading the source understands
  *why* a block exists and what a non-obvious `git`/`gh`/`jq` incantation does. Explain intent and the
  gotchas, not the obvious.
- **Not over-the-top.** No comment on every line, no restating what the code plainly says. Aim for the
  density of a well-kept open-source Bash tool: a short header block per function, a line where a
  reader would otherwise pause and squint.
- Keep functions small and named for what they do. Readability is a feature here, not a nicety.

## Working conventions (non-negotiable)

- **No direct commits to `main`.** Branch → PR → green checks → **stop at the PR and let Brett merge**
  (don't self-merge unless told). One focused change per PR.
- **Signed commits** (Verified); end messages with `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **AgentGate + GitGuardian on every PR** (scaffolded). Its `dangerous_patterns` rule matches risky tokens
  even in prose/comments — if a comment needs to name one, describe it in words rather than the literal
  token, or have Brett bypass. **`brett-buskirk` must be the active gh account.**
- Follow the estate's issue/PR conventions (assignee, labels, milestone, project membership) — see the
  parent `~/github-repos/CLAUDE.md`, which auto-loads here.

## Docs suite

`huginn new` scaffolded README / LICENSE / CHANGELOG / ROADMAP / CONTRIBUTING. Flesh out the **README**
with the wanderer framing, a "works in any repo, owns nothing" promise, the safe-by-default action
contract, and an install one-liner (`curl` the script → `~/.local/bin/vegtam`). Since this is aimed at a
public audience, the README is a first-class deliverable — write it to be adopted. Grow CHANGELOG/ROADMAP.

## Phased plan (each phase → a version milestone; create them when you start)

- **v0.1.0 — Scaffold + repo resolution + `status`.** Dispatcher, help, color, the pwd→repo resolver with
  clean failure modes, and the flagship one-screen briefing.
- **v0.2.0 — Views.** `branches`, `prs`, `log`/`activity`.
- **v0.3.0 — `health`/`hunt`.** Security + freshness, with graceful degradation on access.
- **v0.4.0 — Safe actions.** `sync`, `tidy` (dry-run/`--apply`), `branch`, `pr`.
- **v0.5.0 — Polish + docs.** `shellcheck` gate, README written for adoption, `--json` where it helps.
- **v1.0.0 — Release.** `curl`-installable to `~/.local/bin/vegtam`, tagged `v1.0.0`, DoD met. Consider
  public from the start (unlike the estate-tied beasts, this one is genuinely for everyone).

## Definition of Done

`vegtam status`, `branches`, `prs`, `log`, and `health` all render a clean, useful view of **the current
repo** from anywhere on the machine, degrading gracefully on missing permissions or a non-GitHub remote;
the safe actions (`sync`, `tidy` dry-run-by-default, `branch`, `pr`) work and never touch remote state or
uncommitted work; zero-config and self-contained (no estate dependency); two-level help; `shellcheck`-clean
in CI; source is human-readable and sensibly commented; README written for outside adoption. Shipped as a
single installable script.

## Deferred (do NOT build in v1)

- **Any remote-mutating or destructive action** beyond the safe local set (see the governing design
  decision). If ever added: ownership-gated and dry-run by default.
- **Optional "match my conventions" check** (off by default) for when Brett *is* in one of his own repos.
- **`--json` everywhere**, shell completions, a Homebrew tap or other package distribution.
- **Multi-repo** anything. That's the pack's job; Vegtam is single-repo by definition.

## Reference repos

- **`~/github-repos/huginn/huginn`** — the dispatcher / two-level help / color / voice reference. Match the
  *structure and feel*, not the estate scoping.
- **`~/github-repos/freki/freki`** — the safe-by-default `--apply`/dry-run spine to borrow for `tidy`.
- **`~/github-repos/grimnir`** — the "high seat" counterpart; Vegtam is its away-from-home complement.
