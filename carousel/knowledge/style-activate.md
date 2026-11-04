# style-activate — "The Graphic Effect" (Activate)

Source: the user's two reference posters ("The Graphic Effect" by Gagan Singh Gill,
pasted in chat 2026-11-04 — no local sheet file; do not delete any asset to make room).
Registered 2026-11-04. This is the kit's ONLY template.

Plan settings: `"template":"template-activate.html"`, `"theme":"activate"`.

## What this style is

**One thought per card.** A giant bold grotesque headline IS the slide — a complete,
punchy sentence stacked one phrase per line — with exactly ONE red moment, oceans of
whitespace, and nothing else. No cards, charts, stickers, ghost words or avatars.
Copy always written with `knowledge/copywriting.md`; the set must flow as one
continuous story (hook → proof → mechanism → recognition → fix → CTA).

## Fixed type scale (exactly three sizes — never auto-fitted)

| element | size | notes |
|---|---|---|
| Headline | **84px** | Inter 800, sentence case, stacked flush-left `\n` lines, line-height 1.07, tracking -.028em |
| Subtitle | **28px** | gray `#8A8A90`, sentence case, line-height 1.5 |
| Source citation | **20px micro-caps** | UPPERCASE, tracked (+.14em), lighter gray `#9A9AA0` — visibly distinct from the subtitle |

Because the size is fixed, keep every headline line short enough to fit the 928px
plate (~16–17 characters max per line). Rebreak the sentence across more `\n` lines
rather than shrinking text. The `fitSlide` wrapper is a safety net only — if it ever
triggers, the copy is too long: fix the copy, not the size.

## Default words per card

**One sentence per card, 12 words max** (hook and CTA can go shorter). If a thought
needs more, it needs two cards. Numbers only inside plain sentences.

## Palette

| token | hex | job |
|---|---|---|
| Paper | `#F1F1F0` | off-white field, the faintest grain |
| Ink | `#1A1A1A` | headline type |
| Red | `#E5301A` | the ONE red moment per slide |
| Gray | `#8A8A90` | subtitle, source note, italic tagline |

## Rules (enforced by the template)

1. **Top rail**: zero-padded page number top-left ("01"), "© 2026" top-right. Small.
2. **The headline is the whole slide**: fixed 84px, stacked flush-left lines.
3. **Exactly one red moment per slide**, two flavours via plan markers:
   - `**text**` → white type on a red block
   - `*text*` → plain red type
   A single `**span**` must not cross a `\n` line break — give each line its own
   `**…**`; stacked marks read as one continuous block.
4. **Source citation** in gray 28px under the headline (via `content.note`) —
   facts verified from primary sources.
5. **Footer bottom-left**: bold `handle` line + italic gray `tagline`.
6. Nothing else is painted but the paper. `lines`-type rows are hidden; use
   `content` only to carry the source `note`.

## Per-slide fields

`headline` (with `\n` + one red moment) · `subtitle` (optional gray line) ·
`content.note` (source) · `bg_seed` · `index`. `kicker`, `hero_word`, `ghost_word`,
`cta_pill` are unused in this style.
