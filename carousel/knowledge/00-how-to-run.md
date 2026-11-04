# 00 — How to run (read this first, Claude)

This is the master flow for the Carousel Generator kit. When the user asks for a
carousel, follow this exactly. The user should do almost nothing.

**Default mode is LOCAL: no API, no key, no cost.** The paper is painted
procedurally by `template-activate.html` itself; all type is code-rendered.

## Flow
1. **Read the knowledge base**: `copywriting.md` (MANDATORY for all copy), then
   `structure.md`, `hooks.md`, `ctas.md`. Apply them.
2. **No key needed.** Nothing here is paid.
3. **One style only — Activate (The Graphic Effect)**:
   `template-activate.html` + `"theme":"activate"`. One giant grotesque thought
   per card, ONE red moment, oceans of whitespace. Spec: `style-activate.md`.
   There are no other templates. When the user shares a new reference design,
   build it as a SECOND template from their sheet
   (`knowledge/new-style-from-a-sheet.md`) — never modify Activate.
4. **Ask the user 3 questions** and wait: (1) topic or full script, (2) slide
   count 5–6, (3) @handle + footer tagline.
5. **Write the copy** — following `copywriting.md` — so the set flows as ONE
   continuous story: it opens with an action/hook/pain point, every card hands
   the reader to the next (each headline makes them need the next card), and the
   last card closes with a CTA/takeaway that rounds everything off. Arc =
   hook → proof → mechanism → recognition → counterintuitive fix → CTA.
   **Defaults: one sentence per card, 12 words max** (hook/CTA can go shorter);
   fixed type scale — headline 84px, subtitle 28px, source 20px micro-caps — so
   keep every headline line ≤ ~17 characters (rebreak into more lines, never resize).
   Build the plan and **show it for approval**.
6. **Build it** — all free, all local:
   - `python carousel/scripts/carousel_run.py init "<topic>"` → run folder + plan.json
   - Edit `plan.json`: per slide set `headline` (stacked `\n` lines + one red
     moment — `**word**` = white on red block, `*word*` = red text; never let a
     `**span**` cross a `\n`), optional `subtitle`, `content.note` (gray source
     citation), a unique `bg_seed`. Set `handle` + `tagline` once on the plan.
   - `python carousel/scripts/carousel_run.py build <run-folder>`
     (= `render` → `export`; nothing paid, nothing downloaded)
   - **Look at every PNG** in `carousel/output/<slug>/` before showing the user;
     fix overflow or flow and rebuild if needed.
   - Draft a caption + hashtags (also flowing, also per `copywriting.md`).

   Repaint a slide's paper: change its `bg_seed`, then rebuild.

## Hard rules
- Titles are code-rendered by the template — never AI text.
- ONE style: Activate. Full spec in `style-activate.md`.
- One thought per card; one sentence, 12 words max; exactly ONE red moment per slide.
- The field is off-white paper `#F1F1F0` — no cards, charts, stickers, ghost
  words or avatars. Nothing painted but the paper.
- 5–6 slides; the set must flow as one continuous story (hook → CTA).
- **No statistical notation, ever** (user rule): no `r = .62`, `n = 119`, p-values.
  Numbers appear only inside plain sentences ("a meta-analysis of 691 studies").
- Unique `bg_seed` per slide — never repeat a paper sheet.
- Verify facts from a primary source; cite them in the tiny gray note.
- Never delete `carousel/assets/styles/*` or the original reference images.

## Plan fields (per slide)
`index, role (hook|body|cta), headline` (the whole slide — `\n` splits stacked
lines, one red moment inside), `subtitle` (optional gray line),
`content` — in this style used only to carry the source `note`
(`{"type":"lines","items":[],"note":["Steel, 2007, Psychological Bulletin"]}`),
`bg_seed`, `out_file`.
Plan-level: `slug, topic, template` (`template-activate.html`), `handle`
(footer bold line), `tagline` (footer italic line), `brand_label`, `canvas`, `slides`.
`kicker`, `hero_word`, `ghost_word`, `cta_pill`, `cta_soft`, `microcopy`,
`sticker`, `topic_tag` are unused in this style.
