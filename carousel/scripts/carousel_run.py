"""Orchestrator for the Instagram carousel generator.

Subcommands:
  init <slug>       create a fresh run folder + starter plan.json, print its path
  localbg <run>     paint backgrounds locally (procedural — Activate paints its
                    own paper, so this is a fast no-op kept for pipeline parity)
  render <run>      overlay the template on each background -> 1080x1350 PNGs
  export <run>      copy final numbered slides into output/<slug>/
  build <run>       localbg + render + export  (fully offline, costs nothing,
                    no API key)

Everything here is free and local.
"""
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import carousel_config as cfg


def _slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:48] or "carousel"


def _slide(index, role, headline, subtitle="", note=None, bg_seed=2042):
    return {
        "index": index,
        "role": role,                       # hook | body | cta (labels for you)
        "headline": headline,               # the whole slide: \n splits stacked lines,
                                            # **text** = white on red block, *text* = red type
        "subtitle": subtitle,               # optional gray line; "" hides it
        "content": {"type": "lines", "items": [], "note": note or []},
        "bg_seed": bg_seed,                 # unique per slide — never repeat a sheet
        "out_file": f"{index:02d}.png",
    }


def _starter_plan(slug: str, stamp: str) -> dict:
    """A 6-slide ACTIVATE starter (hook -> proof -> mechanism -> recognition ->
    fix -> CTA). Replace the copy with the real thing (one sentence per card,
    12 words max, ONE red moment, every headline line <= ~17 chars), keep a
    unique bg_seed per slide, then `build`."""
    plan = {
        "slug": f"{stamp}-{slug}",
        "topic": "",
        "created": stamp,
        "template": "template-activate.html",   # the ONLY template (The Graphic Effect)
        "theme": "activate",
        "handle": "@activ8",                     # footer bold line
        "tagline": "activate your own potential",  # footer italic line
        "brand_label": "@v8",
        "canvas": [cfg.CANVAS_W, cfg.CANVAS_H],
        "slides": [
            _slide(1, "hook", "Hook headline goes\n*here* —\nunder 12 words.",
                   bg_seed=2041),
            _slide(2, "body", "Card two hands the\nreader *here*.",
                   "optional gray subtitle line",
                   note=["Author, Year, Publication - keep under 58 chars"],
                   bg_seed=2078),
            _slide(3, "body", "Card three continues\nthe **same story**.",
                   bg_seed=2115),
            _slide(4, "body", "Card four deepens it\n**one step further**.",
                   bg_seed=2152),
            _slide(5, "body", "Card five turns\nthe corner *here*.",
                   bg_seed=2189),
            _slide(6, "cta", "Close it.\nStart **now**.",
                   "takeaway that rounds the set off",
                   bg_seed=2226),
        ],
    }
    # the CTA slide carries the bright frosted button from the style sheet
    plan["slides"][-1].update({
        "cta_pill": "Save this", "cta_soft": "for later",
        "microcopy": "Follow @justjay.md for the full build.",
    })
    plan["slides"][0]["microcopy"] = "A carousel painted, laid out and rendered locally."
    return plan


def cmd_init(slug: str):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    slug = _slugify(slug)
    run_dir = cfg.RUNS_DIR / f"{stamp}-{slug}"
    (run_dir / "media").mkdir(parents=True, exist_ok=True)
    (run_dir / "plan.json").write_text(json.dumps(_starter_plan(slug, stamp), indent=2))
    print(str(run_dir))


def cmd_localbg(run_dir: str):
    """FREE: paint every background procedurally (no API key, no network)."""
    import carousel_localbg
    carousel_localbg.generate(run_dir, force="--force" in sys.argv)


def cmd_render(run_dir: str):
    import carousel_render
    carousel_render.render(run_dir)


def cmd_export(run_dir: str):
    run_dir = Path(run_dir)
    plan = json.loads((run_dir / "plan.json").read_text(encoding="utf-8"))
    dest = cfg.OUTPUT_DIR / plan["slug"]
    dest.mkdir(parents=True, exist_ok=True)
    n = 0
    for slide in plan["slides"]:
        src = slide.get("out_file")
        if src and Path(src).exists():
            shutil.copy2(src, dest / f"{slide['index']:02d}.png")
            n += 1
    print(f"Exported {n} slide(s) -> {dest}")


def cmd_build(run_dir: str):
    """The fully offline path: local backgrounds -> render -> export. Costs nothing."""
    cmd_localbg(run_dir)
    cmd_render(run_dir)
    cmd_export(run_dir)


_CMDS = {
    "init": cmd_init,
    "localbg": cmd_localbg,
    "render": cmd_render,
    "export": cmd_export,
    "build": cmd_build,
}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in _CMDS:
        print(__doc__)
        raise SystemExit(1)
    _CMDS[sys.argv[1]](sys.argv[2])
