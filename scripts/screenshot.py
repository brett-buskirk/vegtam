#!/usr/bin/env python3
# screenshot.py — regenerate the README images under docs/.
#
# Renders REPRESENTATIVE vegtam output (illustrative fake acme-* data, NOT live
# runs — the GitHub-backed views need a readable remote, and a real run would bake
# in a real repo's changing state) into clean terminal-window PNGs matching the
# rest of the toolkit. The four shots share one coherent story: the acme/webapp
# fork you're contributing to, mid-work on feat/checkout-v2 (PR #128), with a
# dependabot next bump (#126) that recurs in both `prs` and `health`.
#
# Dev-only.  pip3 install --user rich cairosvg  &&  python3 scripts/screenshot.py
import os, tempfile
from rich.console import Console
from rich.text import Text
import cairosvg

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")


def render(title, filename, lines):
    """rich markup lines -> terminal-window SVG -> PNG @2x, sized to the content."""
    texts = [Text.from_markup(line) for line in lines]
    con = Console(record=True, width=max(t.cell_len for t in texts) + 2)
    for t in texts:
        con.print(t)
    svg = tempfile.mktemp(suffix=".svg")
    con.save_svg(svg, title=title)
    out = os.path.join(DOCS, filename)
    cairosvg.svg2png(url=svg, write_to=out, scale=2)
    os.unlink(svg)
    print("wrote", out)


# ── status — the flagship, showing every signal at once ──
# fork · dirty · ahead/behind · stash · CI · PR/issue counts.
STATUS = [
    "",
    "  [bold]vegtam[/]  [dim]·[/]  [bold]acme/webapp[/]",
    "  [dim]Acme's storefront — Next.js, deployed on Vercel.[/]",
    "",
    "    [green]● public[/]   [dim]·[/]   default [bold]main[/]   [dim]·[/]   [magenta]fork of acme-labs/webapp[/]",
    "    branch    [bold cyan]feat/checkout-v2[/]  [yellow]● 3 changed[/]  [yellow]↑2[/]  [yellow]↓1[/]  [magenta]⚑1[/]",
    "    head      [bold]a1b2c3d[/]  [green]✓ checks pass[/]  [dim]· 2h ago[/]",
    "    open      [bold]4[/] PRs   [dim]·[/]   [bold]12[/] issues",
    "",
]

# ── prs — open PRs with CI glyph, source branch, author; your own tagged ──
PRS = [
    "",
    "  [bold]vegtam prs[/]  [dim]·  acme/webapp  ·  open pull requests[/]",
    "",
    "  [green]✓[/] [bold]#128[/]  Add Apple Pay to checkout  [cyan](you)[/]",
    "       [dim]feat/checkout-v2 ← @you · 2h ago[/]",
    "  [yellow]●[/] [bold]#126[/]  build(deps): bump lodash from 4.17.19 to 4.17.21",
    "       [dim]dependabot/npm/lodash-4.17.21 ← @app/dependabot · 1d ago[/]",
    "  [red]✗[/] [bold]#124[/]  Refactor the cart reducer",
    "       [dim]fix/cart-state ← @jsmith · 3d ago[/]",
    "  [dim]·[/] [bold]#119[/]  WIP: gift-card redemption  [dim]\\[draft][/]",
    "       [dim]feat/gift-cards ← @mchen · 5d ago[/]",
    "",
    "  [bold]4 open[/]  [dim]·[/]  [cyan]1 yours[/]",
    "",
]


def _alert(sev, style, num, pkg, summary):
    return f"    [{style}]{sev.ljust(8)}[/] [dim]#{num}[/] {pkg.ljust(16)} {summary}"


def _action(ref, wf, info_style, info):
    return f"    [yellow]∙[/] {ref.ljust(38)} [dim]{wf.ljust(22)}[/] [{info_style}]{info}[/]"


# ── health — the security & freshness view (alerts · deps · actions) ──
HEALTH = [
    "",
    "  [bold]vegtam health[/]  [dim]·  acme/webapp  ·  security & freshness[/]",
    "",
    "  [bold]alerts[/]  [dim]open Dependabot security advisories[/]",
    "    [bold]2 open[/]  [red]1 high[/]  [yellow]1 medium[/]",
    _alert("high", "red", 7, "lodash", "Prototype pollution in lodash before 4.17.21"),
    _alert("medium", "yellow", 4, "axios", "SSRF via unexpected 3xx redirect in axios"),
    "",
    "  [bold]deps[/]  [dim]dependency freshness[/]",
    "    [yellow]∙[/] manifests present, nothing watching them for updates [dim](npm)[/]",
    "",
    "  [bold]actions[/]  [dim]third-party Actions not pinned to a commit SHA[/]",
    _action("actions/checkout@v4", "ci.yml", "yellow", "outdated → v7.0.0"),
    _action("actions/setup-node@v4", "ci.yml", "yellow", "outdated → v6.4.0"),
    "",
    "  [bold]5 signals[/] [dim]to look at across alerts · deps · actions[/]",
    "",
]


def _merged(branch, age):
    return f"    [dim]∙[/] {branch.ljust(30)} [green]merged[/] [dim]· {age}[/]"


# ── tidy — the safe action: dry-run by default, nothing deleted ──
TIDY = [
    "",
    "  [bold]vegtam tidy[/]  [dim]·  acme/webapp  ·  merged local branches · dry-run[/]",
    "",
    _merged("feat/old-navbar", "2w"),
    _merged("fix/footer-typo", "5d"),
    _merged("chore/bump-eslint", "3d"),
    "",
    "  [dim]3 merged branches · 'vegtam tidy --apply' deletes them (git branch -d — never the default or current branch, never anything on the remote)[/]",
    "",
]


if __name__ == "__main__":
    render("vegtam status", "vegtam-status.png", STATUS)
    render("vegtam prs", "vegtam-prs.png", PRS)
    render("vegtam health", "vegtam-health.png", HEALTH)
    render("vegtam tidy", "vegtam-tidy.png", TIDY)
