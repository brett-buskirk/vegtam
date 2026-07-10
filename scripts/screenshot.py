#!/usr/bin/env python3
# screenshot.py — regenerate the README hero (docs/vegtam-status.png).
#
# Renders a REPRESENTATIVE `vegtam status` (illustrative fake acme-* data, NOT a
# live run — the flagship's richest lines need a readable GitHub remote, and a real
# run would bake in a real repo's changing state) into a clean terminal-window PNG
# matching the rest of the toolkit's shots.
#
# Dev-only.  pip3 install --user rich cairosvg  &&  python3 scripts/screenshot.py
import os, tempfile
from rich.console import Console
from rich.text import Text
import cairosvg

# One busy-but-realistic snapshot: a fork you're contributing to, mid-work on a
# feature branch — so every signal status can surface is on screen at once
# (visibility · default · fork · dirty · ahead/behind · stash · CI · PRs/issues).
# Markup styles mirror vegtam's own palette: green/yellow/cyan/magenta/dim/bold.
LINES = [
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

texts = [Text.from_markup(line) for line in LINES]
con = Console(record=True, width=max(t.cell_len for t in texts) + 2)
for t in texts:
    con.print(t)

svg = tempfile.mktemp(suffix=".svg")
con.save_svg(svg, title="vegtam status")
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "vegtam-status.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
cairosvg.svg2png(url=svg, write_to=out, scale=2)
os.unlink(svg)
print("wrote", out)
