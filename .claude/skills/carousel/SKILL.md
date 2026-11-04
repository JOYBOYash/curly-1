---
name: carousel
description: >
  Generate a branded Instagram carousel (1080×1350, 4:5) in the user's single
  registered style: "Activate" (The Graphic Effect — one giant bold-grotesque
  thought per card, one red moment, oceans of whitespace, fixed type scale).
  All copy is written with the copywriting operating system
  (knowledge/copywriting.md). Everything is painted LOCALLY and procedurally
  (no API, no key, no cost); every element is code-rendered. Use when the user
  asks to "make a carousel", "make an Instagram carousel", "turn this into a
  carousel", or "/carousel".
---

# Carousel generator — Activate ("The Graphic Effect")

Makes a scroll-stopping Instagram carousel that stays perfectly on-brand across
every slide. **The headline is the whole slide**: one complete, punchy thought in
huge bold grotesque type on off-white paper, with exactly ONE red moment.
The style is replicated from the user's reference posters ("The Graphic Effect");
full spec: `carousel/knowledge/style-activate.md`.

Self-contained in `carousel/`. **Runs fully offline — no API key required.**

## The registered style (the only one)
| style | plan settings | reference | look |
|---|---|---|---|
| **Activate** (The Graphic Effect) | `"template":"template-activate.html"`, `"theme":"activate"` | user's reference posters (spec in `style-activate.md`) | one giant bold-grotesque thought per card, stacked flush-left lines, ONE red moment (`**word**` = white on red block, `*word*` = red text), page number top-left, © year top-right, tiny brand footer |

No other templates exist. When the user shares a new reference design, build it
as a SECOND template from their sheet (see `knowledge/new-style-from-a-sheet.md`)
— never modify Activate.

## Fixed type scale (locked by the user)
Exactly three font sizes on every card, in every set — no auto-fitting:
- **Headline: 84px** (Inter 800, stacked `\n` lines, flush left, line-height 1.07)
- **Sub content: 28px** (subtitle line, gray, sentence case)
- **Source citation: 20px micro-caps** (UPPERCASE, tracked, lighter gray — visibly
  distinct from the subtitle)

Because the size is fixed, keep every headline line ≤ ~17 characters — rebreak
into more lines instead of resizing. Keep citations short enough for one line
(≤ ~58 characters); "Wohl et al., 2010, <journal>" is the pattern.

## Default words per card (locked by the user)
**One sentence per card, 12 words max** (hook and CTA can go shorter).

## Highlight markers (headline, subtitle or note text)
- `**text**` → white type on a red block
- `*text*` → plain red type

Escape nothing — the renderer handles it. A single `**span**` must not cross a
`\n` line break (the browser closes the mark mid-span); if two consecutive lines
need the red block, give each line its own `**…**` — stacked marks read as one
continuous block.

## COPY IS ALWAYS WRITTEN WITH THE COPYWRITING OS
Before writing any slide copy, hooks, captions or CTAs, read
**`carousel/knowledge/copywriting.md`** (the user's copywriting skill, copied
into the kit) and follow it: decode the brief → find the angle → design the hook
(call-out + value condition) → structure the arc → draft → edit.

**The set must flow as one continuous story**: it starts with an action/hook/pain
point and every card hands the reader to the next, ending with a CTA/takeaway
that rounds everything off. Arc = hook → proof → mechanism → recognition →
counterintuitive fix → CTA. Each headline should make the reader *need* the next
card; the last card should feel inevitable, not bolted on.

Specific beats vague; every promise is paid off; never invent proof.
**Numbers go inside plain sentences** ("a meta-analysis of 691 studies") — never
as statistical notation (`r = .62`, `n = 119`), which reads as jargon.
This is mandatory for every carousel.

### Golden rules (Activate)
- **One thought per card.** The headline is a complete sentence worth stopping
  for — like the reference's "If the alignment looks wrong to the eye, it is
  wrong, even if the grid says otherwise." One sentence, 12 words max per card.
- **Exactly ONE red moment per slide** — either a red block (`**…**`) or red
  type (`*…*`), never both flavours competing on one slide.
- **The field is off-white paper** (`#F1F1F0`, painted by the template's seeded
  canvas with faint grain — set a unique `bg_seed` per slide). Nothing else is
  painted but the paper: no cards, charts, stickers, ghost words or avatars.
- **Headline**: Inter 800, sentence case, stacked flush-left lines (`\n` in the
  plan), tight leading, auto-fitted HUGE.
- **Top rail**: zero-padded page number top-left ("01"), © year top-right.
- **Source citations** go in the tiny gray note under the headline (via
  `content.note`) — kept quiet, never loud. Facts verified from primary sources.
- **Footer bottom-left**: bold `handle` + italic gray `tagline`.
- **Free by default.** Everything runs locally; nothing here costs money.
- **Facts:** if researching, verify from a primary source. Never invent numbers.

## Setup (once)
```
pip install playwright && playwright install chromium
```
That's it. (Fonts load from Google Fonts on first render; everything else is local.)

## Workflow (all local, all free)
1. **Init** — `python carousel/scripts/carousel_run.py init "<topic>"` → a run folder + starter plan.
2. **Content** — FIRST read `carousel/knowledge/copywriting.md` (mandatory), then
   write the copy so the set flows as one continuous story (see above). 5–6 slides.
3. **Build** — `python carousel/scripts/carousel_run.py build <run-folder>` =
   render 1080×1350 PNGs → export to `carousel/output/<slug>/`.
4. **Open every slide for review** (look at each PNG); fix overflow/flow, rebuild.
5. Draft a caption + hashtags (also flowing, also per the copywriting OS).

## plan.json
**Plan level:** `slug, topic, template` (`template-activate.html`), `handle`
(footer bold line, e.g. `@activ8`), `tagline` (footer italic line), `brand_label`,
`canvas`, `slides`.

**Per slide:** `index, role (hook|body|cta), headline` (the whole slide — `\n`
splits stacked lines, one red moment inside), `subtitle` (optional small gray
line), `content` — in this style used **only** to carry the source note:
`{"type":"lines","items":[],"note":["Steel, 2007, Psychological Bulletin"]}`,
`bg_seed`, `out_file`. `kicker`, `hero_word`, `ghost_word`, `cta_pill`,
`cta_soft`, `microcopy` are unused in this style.

## Brand / look (`carousel/scripts/template-activate.html`)
Paper `#F1F1F0`, ink `#1A1A1A`, red `#E5301A` (the only accent), gray `#8A8A90`.
Fixed type scale: headline 84px (Inter 800), sub content 28px.
Full spec: `carousel/knowledge/style-activate.md`.

The chart theme `activate` is registered in `carousel_charts.py` so no chart
code ever silently falls back — but this style does not use charts.
`midnight` stays as an internal fallback theme only.

## Reference assets — never delete
`carousel/assets/styles/*.png` and the original reference images in
`carousel/assets/` are the user's permanent style sheets. Never delete or
overwrite them.
