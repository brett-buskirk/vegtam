# Roadmap

_What's planned for vegtam — check items off as they ship. Each phase is a version milestone and a
focused PR._

## Shipped
- [x] **v0.1.0 — scaffold + `status`** · dispatcher, two-level help, color, the pwd→repo resolver
  with clean failure modes, and the flagship one-screen briefing.
- [x] **v0.2.0 — views** · `branches`, `prs`, `log`/`activity`.

## Next
- [ ] **v0.3.0 — `health`** · Dependabot alerts, outdated deps, unpinned actions; graceful
  degradation when access is denied.
- [ ] **v0.4.0 — safe actions** · `sync` (ff-only), `tidy` (dry-run by default), `branch`, `pr`.
- [ ] **v0.5.0 — polish + docs** · shellcheck CI gate, README written for adoption, `--json`
  where it helps.
- [ ] **v1.0.0 — release** · curl-installable to `~/.local/bin/vegtam`, tagged, public.

## Out of scope (by design)
- Any remote-mutating or destructive action beyond the safe local set — and if ever added, it must
  be ownership-gated and dry-run by default.
- Auditing a repo against external conventions.
- Anything multi-repo — that's the pack's job; Vegtam is single-repo by definition.
