# Roadmap

_What's planned for vegtam — check items off as they ship. Each phase is a version milestone and a
focused PR._

## Shipped
- [x] **v0.1.0 — scaffold + `status`** · dispatcher, two-level help, color, the pwd→repo resolver
  with clean failure modes, and the flagship one-screen briefing.
- [x] **v0.2.0 — views** · `branches`, `prs`, `log`/`activity`.
- [x] **v0.3.0 — `health`** · Dependabot alerts, outdated deps, unpinned actions; graceful
  degradation when access is denied.
- [x] **v0.4.0 — safe actions** · `sync` (ff-only), `tidy` (dry-run by default), `branch`, `pr`.
- [x] **v0.5.0 — polish + docs** · shellcheck CI gate, README written for adoption, `--json` on
  every inspect view.
- [x] **v1.0.0 — release** · single self-contained script, curl-installable to `~/.local/bin/vegtam`,
  tagged, DoD met.

## Out of scope (by design)
These aren't backlog — they're deliberately not what Vegtam is for.

- **Anything remote-mutating or destructive** beyond the safe local set (`sync`, `tidy`, `branch`,
  `pr`). If ever added, it must be ownership-gated and dry-run by default.
- **Auditing a repo against conventions** — Vegtam reports what *is*. (An optional, off-by-default
  "does this match *my own* conventions?" check for your own repos is the only version that could
  ever fit, and it's not a priority.)
- **Anything multi-repo** — that's the pack's job; Vegtam is single-repo by definition.

## Maybe someday (nice-to-have, not planned)
- Shell completions, and package distribution (a Homebrew tap or similar).
