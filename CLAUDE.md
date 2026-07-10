# CLAUDE.md — Vegtam

Working manual for a Claude Code agent editing **this** repo. Two parent files auto-load above it via
the directory walk and own the universal rules — this file does **not** restate them:

- **`/etc/claude-code/CLAUDE.md`** (machine policy) — the chain of command (branch → PR → **Brett
  merges**; never self-merge, never commit to `main`), signed commits, the safety floors, brand
  positioning, NIST AI RMF.
- **`~/github-repos/CLAUDE.md`** (estate manual) — issue/PR wiring (assignee `brett-buskirk`, labels,
  milestone, Estate board **#17**), the `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`
  trailer, the AgentGate `dangerous_patterns`-fires-in-prose quirk, the `brett-buskirk`-must-be-the-
  active-gh-account gotcha, the pack, and the estate memory.

Everything below is Vegtam-specific.

## What Vegtam is

`vegtam` ("the wanderer") is a single-file CLI that operates on **exactly one repo — whichever one
you're standing in** — read live from the local `.git` and its GitHub remote. It is deliberately **not**
estate-scoped; that's the pack (huginn/muninn/geri/freki/grimnir), which scans every repo under one
root. Vegtam is the away-from-home mode: zero config, no stored state, goes anywhere.

## The governing design decision — never violate

Vegtam's default context is a repo **Brett does not own** (client work, an OSS contribution, a fresh
clone). That inverts the pack's risk posture, and three invariants follow. They are not negotiable:

1. **Read-first, act-light.** The value is the *views*; they're safe everywhere. Actions help you work
   *in* the repo, never "clean up" someone else's. The `freki` reaper instinct is *wrong* here.
2. **Convention-neutral.** Report what *is*. Never audit a repo against anyone's house style — do not
   port `huginn doctor`.
3. **Permission-aware, degrades gracefully.** Assume contributor-without-admin / read-only / a
   non-GitHub remote. Every `gh`/`jq` call is wrapped; on failure print a short note — never a crash
   or a stack trace.

## The script, at a glance

One file, `vegtam`, `set -uo pipefail`. Deps: **`bash` + `git` required, `gh` + `jq` optional.** Read
top→bottom: palette → small helpers (`have` / `note` / `age_short` / `since_to_gitdate` /
`classify_ci` / `num` / `json_ok` …) → `resolve_repo` + `github_slug` → the five view `cmd_*` (status,
branches, prs, log, health, with a separate `health_json` emitter) → the four safe-action `cmd_*`
(sync, tidy, branch, pr) with `confirm` → the `help_*` block → the `case` dispatcher at the bottom.

Surface: **5 inspect views** (each takes `--json`) + **4 safe actions**. Two-level help
(`vegtam help`, `vegtam <cmd> help`). Respects `NO_COLOR` and non-TTY output.

## Invariants specific to Vegtam

- **Self-contained & zero-config.** No estate dependency: no `$HUGINN_*`, no config file, no
  `exemptions.json`, no scanning sibling directories, none of the pack's `repos()`/`is_exempt`
  helpers. It must stay `curl`-one-file-into-`~/.local/bin`-and-run.
- **Safe-actions contract.** Only `sync` / `tidy` / `branch` / `pr`. `tidy` is **dry-run by default**
  (`--apply` to act, and only `git branch -d`). Never delete remote branches, never force, never
  rewrite history, never touch uncommitted work. Anything beyond this set is out of scope unless it is
  ownership-gated **and** dry-run by default.
- **`jq` only behind `--json`.** The human views must run without system `jq` (they use `gh`'s
  embedded `--jq`); `--json` output is gated by `json_ok` and refuses cleanly when `jq` is absent.
- **Comment for humans.** This is the most-scrutinized thing in the collection because it isn't
  estate-tied — explain the non-obvious *why* of a `git`/`gh`/`jq` incantation, not the obvious *what*.

## Gotchas (each cost real debugging)

- **`def` is a reserved jq keyword** — never name a jq variable `$def` (use `$defbranch`). It's a
  compile error that produces *empty* stdout, so a test must assert non-empty JSON or the failure hides.
- **The field separator is `\x1f`, not tab.** `IFS=$'\t' read` collapses adjacent tabs (tab is
  IFS-whitespace) and silently drops empty fields, shifting everything after. In a jq `join`, write it
  as the readable `\u001f`, not a raw control byte.
- **`/dev/tty` can exist yet not be openable** in sandboxes — `[ -r /dev/tty ]` passes but the
  redirection fails. `confirm()` probes with `{ : < /dev/tty; }` and never leaves `reply` unset under
  `set -u`. That's `tidy --apply`'s safety gate; don't regress it.
- **shellcheck `SC2059`** (variables in a printf format string) is disabled file-level on purpose — the
  color-escapes-in-format idiom, matching the pack. Keep the script otherwise shellcheck-clean.

## Editing & shipping

- Every change must be `bash -n vegtam` + `shellcheck vegtam` clean — the CI gate
  (`.github/workflows/shellcheck.yml`) runs both on every push and PR.
- **Test the way it was built:** real repos for populated views (`huginn` / `geri`; `day-one` has a
  live Dependabot alert), a **foreign** repo for the core case (point a throwaway repo's `origin` at,
  say, `cli/cli`), throwaway git fixtures for the write actions (`sync`/`tidy`/`branch`), plus
  `NO_COLOR`/piped output (zero escape bytes) and `--json | jq empty` on every view.
- Bump `VERSION`; keep `README` / `CHANGELOG` / `ROADMAP` in sync with the change. After a PR merges,
  refresh Brett's installed copy: `install -m 0755 vegtam ~/.local/bin/vegtam`.

## Status

**v1.0.0** shipped, tagged (signed), and released. Two things remain Brett's to do, on his own timing —
do not do them for him:

- **Flip the repo public.** He does this himself after testing. The README `curl` line only works for
  outsiders once the repo is public.
- **After it's public,** enable secret scanning + push protection (free on public repos; the estate's
  hardening standard when a repo flips public).

## Reference

- `~/github-repos/huginn/huginn` — dispatcher / two-level help / color / the terse, lightly-wry voice.
- `~/github-repos/freki/freki` — the `--apply`/dry-run safety spine that `tidy` borrows.
