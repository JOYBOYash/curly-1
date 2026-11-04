"""Code-drawn charts for the Midnight Bioluminescent carousel — rendered as inline SVG
inside a glass card, so they stay vector-crisp at 2x.

COLOR SYSTEM (validated, not eyeballed)
--------------------------------------
The style sheet forbids a categorical palette: teal is *light* (never paint), and all
type is moon white or fog gray. So identity is never carried by hue here. Every chart
uses one of two validated jobs:

  * EMPHASIS  — the series that matters is lit teal, everything else is fog gray.
                Validated pair #3FBFB2 vs #7C7C82: CVD dE 14.1 (deutan), normal 18.3,
                both >= 3:1 on the glass surface. The muted series also gets a dash
                pattern, so identity survives full CVD and grayscale print.
  * ORDINAL   — a single-hue teal ramp for magnitude:
                #2A6E68 #358F86 #3FBFB2 #72D8CD #A8EBE3 #DCF8F4
                (validate_palette.js --ordinal on surface #14171A: monotone L, all
                adjacent dL >= 0.06, light end 3.02:1, hue spread 2 deg — ALL PASS)

Marks follow the house spec: 2px lines with round caps, >=8px end markers carrying a
2px surface ring, area washes at ~10%, hairline SOLID gridlines one step off surface,
values labelled selectively (the endpoint / the extreme), never one per point, and
text always in ink tokens — never in the series colour.

The medium is a static 1080x1350 image, so there is no hover layer to ship; every
value a reader needs is either directly labelled or carried by the axis.
"""
from __future__ import annotations

import math

# --- themes ---------------------------------------------------------------
# Each style supplies the same slots; the method never changes, only the values.
# Both palettes were checked with the dataviz validator, not by eye.
# "midnight" remains as the internal fallback (and the base for building new
# styles); "activate" is the user's chosen style.
THEMES = {
    # Midnight Bioluminescent: teal is light, type is moon white / fog gray.
    # emphasis pair #3FBFB2 vs #7C7C82 — CVD dE 14.1, normal 18.3, both >= 3:1.
    # ordinal ramp — monotone L, all adjacent dL >= 0.06, light end 3.02:1, hue spread 2 deg.
    "midnight": {
        "ink": "#FFFFFF", "ink2": "#7C7C82", "axis": "#8A8A90",
        "accent": "#3FBFB2", "muted": "rgba(255,255,255,.34)",
        "surface": "#181B1E", "grid": "rgba(255,255,255,.10)",
        "track": "rgba(255,255,255,.07)", "track_line": "rgba(255,255,255,.10)",
        "bar_ctx": "rgba(255,255,255,.22)", "baseline": "rgba(255,255,255,.18)",
        "h_scale": 1.0,
        "glow": "filter:drop-shadow(0 0 12px rgba(63,191,178,.55))",
        "glow_soft": "filter:drop-shadow(0 0 8px rgba(63,191,178,.35))",
        "area_op": ".10",
        "ramp": ["#2A6E68", "#358F86", "#3FBFB2", "#72D8CD", "#A8EBE3", "#DCF8F4"],
    },
    # ACTIVATE (Editorial LinkedIn): charts run on the WHITE card, print-style —
    # no glow, identity by emphasis, magnitude by a single-hue red->rose ramp.
    # The sheet reserves red for display type / chips / fills, which is exactly the
    # chart accent's job; all other type is ink black or silver-gray.
    # Validated numerically (Machado 2009 deutan sim, CIE76 dE, WCAG contrast
    # against surface #FFFFFF), not by eye:
    #   emphasis pair #E41318 vs #8E8E93 — CVD dE 62.3, normal 46.1;
    #   contrast red 4.77:1, silver 3.26:1 — both >= 3:1. ALL PASS.
    #   ordinal ramp #8F0F13 -> #EC6A6E — monotone L, adjacent dL >= 8.6,
    #   light end 3.06:1. ALL PASS. (Lighter rose steps were dropped: their
    #   contrast on white fell under 3:1.)
    # ACTIVATE (The Graphic Effect) — THE registered style. Text-only; charts
    # intentionally unused, but the theme is wired so use_theme never falls back
    # to midnight silently.
    "activate": {
        "ink": "#1A1A1A", "ink2": "#6E6E74", "axis": "#8A8A90",
        "accent": "#E5301A", "muted": "#8E8E93",
        "surface": "#FFFFFF", "grid": "rgba(20,20,20,.10)",
        "track": "rgba(20,20,20,.06)", "track_line": "rgba(20,20,20,.16)",
        "bar_ctx": "#C3C3C3", "baseline": "rgba(20,20,20,.35)",
        "glow": "", "glow_soft": "", "area_op": ".10", "h_scale": 0.88,
        "ramp": ["#8F0F13", "#B61116", "#E41318", "#EC6A6E"],
    },
}
_T = THEMES["midnight"]


def use_theme(name: str):
    """Switch the chart palette. Called by carousel_render from the plan's `theme`."""
    global _T, MOON, FOG, TEAL, SURFACE, GRID, AXIS_INK, MUTED_MARK, RAMP
    global GLOW_STRONG, GLOW_SOFT
    _T = THEMES.get(name) or THEMES["midnight"]
    MOON, FOG, TEAL = _T["ink"], _T["ink2"], _T["accent"]
    SURFACE, GRID, AXIS_INK = _T["surface"], _T["grid"], _T["axis"]
    MUTED_MARK, RAMP = _T["muted"], _T["ramp"]
    GLOW_STRONG, GLOW_SOFT = _T["glow"], _T["glow_soft"]
    return _T


# --- active tokens (rebound by use_theme) ---
MOON = _T["ink"]
FOG = _T["ink2"]
TEAL = _T["accent"]
SURFACE = _T["surface"]
GRID = _T["grid"]
AXIS_INK = _T["axis"]
MUTED_MARK = _T["muted"]
RAMP = _T["ramp"]

W = 852                       # inner width of a glass card at 1080 wide
SANS = "Inter, -apple-system, 'Segoe UI', Roboto, sans-serif"
GLOW_STRONG = _T["glow"]
GLOW_SOFT = _T["glow_soft"]


def _esc(x) -> str:
    return str(x if x is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _fmt(v, unit="", dec=None):
    """Compact, human number: 1284 -> 1,284 · 12900 -> 12.9K · 4.2e6 -> 4.2M."""
    if isinstance(v, str):
        return v + unit
    a = abs(v)
    if a >= 1_000_000:
        s = f"{v/1_000_000:.1f}M".replace(".0M", "M")
    elif a >= 10_000:
        s = f"{v/1000:.1f}K".replace(".0K", "K")
    elif a >= 1000:
        s = f"{v:,.0f}"
    else:
        if dec is None:
            dec = 0 if float(v).is_integer() else (1 if a >= 1 else 2)
        s = f"{v:,.{dec}f}"
    return s + unit


def _nice_ticks(lo, hi, count=4):
    """Round axis ticks to clean numbers (0 / 1,000 / 2,000)."""
    if hi == lo:
        hi = lo + 1
    span = hi - lo
    raw = span / max(1, count)
    mag = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if raw <= step:
            break
    v = math.floor(lo / step) * step
    ticks = []
    # run past `hi` so the top tick always covers the data — otherwise the series
    # draws outside the plot area
    while v < hi - step * 1e-9:
        ticks.append(round(v, 10))
        v += step
    ticks.append(round(v, 10))
    return ticks


def _text(x, y, s, size=19, fill=FOG, weight=400, anchor="start", tabular=False, extra=""):
    tn = "font-variant-numeric:tabular-nums;" if tabular else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{SANS}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'style="{tn}{extra}">{_esc(s)}</text>')


def _title(c):
    t = c.get("title")
    return f'<div class="ctitle">{_esc(t)}</div>' if t else ""


def _notes(c):
    n = c.get("note") or []
    if isinstance(n, str):
        n = [n]
    return "".join(f'<div class="cnote">{_esc(i)}</div>' for i in n)


def _legend(entries):
    """Identity never rides colour alone: a mark key sits beside ink-coloured text."""
    if len(entries) < 2:
        return ""          # a single series needs no legend — the title names it
    out = []
    for label, colour, dashed in entries:
        dash = ' stroke-dasharray="7 6"' if dashed else ""
        out.append(
            f'<span class="lk"><svg width="26" height="10" viewBox="0 0 26 10">'
            f'<line x1="1" y1="5" x2="25" y2="5" stroke="{colour}" stroke-width="3" '
            f'stroke-linecap="round"{dash}/></svg>{_esc(label)}</span>')
    return f'<div class="legend">{"".join(out)}</div>'


def _svg(h, body):
    return (f'<svg class="chart" viewBox="0 0 {W} {h}" width="100%" height="{h}" '
            f'preserveAspectRatio="xMidYMid meet" role="img">{body}</svg>')


# ---------------------------------------------------------------- line / area
def line(c):
    """Trend over time. One series = area wash + lit line. Two = emphasis (lit vs muted)."""
    series = c.get("series") or []
    xs = c.get("x_labels") or []
    unit = c.get("unit", "")
    h = int(c.get("height", 390) * _T.get("h_scale", 1.0))
    pad_l, pad_r, pad_t, pad_b = 74, 132, 20, 50

    vals = [v for s in series for v in s["values"] if v is not None]
    lo = c.get("y_min", min(vals + [0]) if c.get("include_zero", True) else min(vals))
    hi = max(vals)
    ticks = _nice_ticks(lo, hi, c.get("y_ticks", 4))
    lo, hi = ticks[0], ticks[-1]
    n = max(len(s["values"]) for s in series)

    def X(i):
        return pad_l + (W - pad_l - pad_r) * (i / max(1, n - 1))

    def Y(v):
        return pad_t + (h - pad_t - pad_b) * (1 - (v - lo) / (hi - lo or 1))

    g = []
    # gridlines: hairline, solid, one step off surface — plus the y ticks they carry
    for t in ticks:
        y = Y(t)
        g.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{W-pad_r}" y2="{y:.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        g.append(_text(pad_l - 16, y + 7, _fmt(t, unit), 18, AXIS_INK, 400, "end", True))

    # x labels: ends + middle only, so they never collide
    idxs = sorted({0, n // 2, n - 1}) if n > 2 else list(range(n))
    for i in idxs:
        if i < len(xs):
            g.append(_text(X(i), h - pad_b + 32, xs[i], 18, AXIS_INK, 400,
                           "start" if i == 0 else ("end" if i == n - 1 else "middle")))

    legend = []
    for s in series:
        muted = s.get("muted")
        colour = MUTED_MARK if muted else TEAL
        pts = [(X(i), Y(v)) for i, v in enumerate(s["values"]) if v is not None]
        d = " ".join(f"{'M' if k == 0 else 'L'}{x:.1f},{y:.1f}" for k, (x, y) in enumerate(pts))
        if not muted and len(series) == 1:      # area wash ~10%, single series only
            g.append(f'<path d="{d} L{pts[-1][0]:.1f},{Y(lo):.1f} L{pts[0][0]:.1f},{Y(lo):.1f} Z" '
                     f'fill="{TEAL}" fill-opacity="{_T["area_op"]}"/>')
        dash = ' stroke-dasharray="9 7"' if muted else ""          # secondary encoding
        g.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="2" '
                 f'stroke-linejoin="round" stroke-linecap="round"{dash} '
                 f'style="{"" if muted else GLOW_STRONG}"/>')
        # end marker: r>=4 with a 2px surface ring so it stays legible on crossings
        ex, ey = pts[-1]
        g.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="5.5" fill="{colour}" '
                 f'stroke="{SURFACE}" stroke-width="2" style="{"" if muted else GLOW_STRONG}"/>')
        # ONE direct label per series, at the end — never a number on every point
        lv = [v for v in s["values"] if v is not None][-1]
        g.append(_text(ex + 16, ey - 2, _fmt(lv, unit), 27, MOON, 600))
        if s.get("label"):
            g.append(_text(ex + 16, ey + 24, s["label"], 18, FOG, 400))
        legend.append((s.get("label", ""), colour, bool(muted)))

    return f'<div class="card">{_title(c)}{_svg(h, "".join(g))}{_legend(legend)}{_notes(c)}</div>'


# ---------------------------------------------------------------- columns
def column(c):
    """Magnitude across ordered categories. Emphasis: the one that matters is lit."""
    items = c["items"]
    unit = c.get("unit", "")
    h = int(c.get("height", 380) * _T.get("h_scale", 1.0))
    pad_l, pad_r, pad_t, pad_b = 66, 24, 46, 56
    hi = max(i["value"] for i in items)
    ticks = _nice_ticks(0, hi, 3)
    top = ticks[-1]
    plot_h = h - pad_t - pad_b
    band = (W - pad_l - pad_r) / len(items)
    # cap the thickness so the band keeps its air, but let a 2-3 column chart
    # breathe a little wider or it reads spindly across a full-width card
    bw = min(46 + max(0, 4 - len(items)) * 14, band * 0.44)

    g = []
    for t in ticks:
        y = pad_t + plot_h * (1 - t / top)
        g.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{W-pad_r}" y2="{y:.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        g.append(_text(pad_l - 16, y + 7, _fmt(t, unit), 18, AXIS_INK, 400, "end", True))

    for k, it in enumerate(items):
        cx = pad_l + band * (k + 0.5)
        bh = max(3, plot_h * it["value"] / top)
        y = pad_t + plot_h - bh
        hi_bar = it.get("highlight")
        fill = TEAL if hi_bar else _T["bar_ctx"]
        r = 4                                  # 4px rounded data-end, square at baseline
        d = (f'M{cx-bw/2:.1f},{pad_t+plot_h:.1f} V{y+r:.1f} Q{cx-bw/2:.1f},{y:.1f} '
             f'{cx-bw/2+r:.1f},{y:.1f} H{cx+bw/2-r:.1f} Q{cx+bw/2:.1f},{y:.1f} '
             f'{cx+bw/2:.1f},{y+r:.1f} V{pad_t+plot_h:.1f} Z')
        g.append(f'<path d="{d}" fill="{fill}" style="{GLOW_STRONG if hi_bar else ""}"/>')
        g.append(_text(cx, y - 16, _fmt(it["value"], unit), 25 if hi_bar else 22,
                       MOON if hi_bar else FOG, 600 if hi_bar else 500, "middle"))
        # a label may carry "\n" to break onto a second line (SVG ignores raw newlines)
        lines = str(it["label"]).split("\n")
        ink = MOON if hi_bar else AXIS_INK
        wgt = 500 if hi_bar else 400
        for li, ln in enumerate(lines):
            g.append(_text(cx, h - pad_b + 34 + li * 24, ln, 19, ink, wgt, "middle"))

    g.append(f'<line x1="{pad_l}" y1="{pad_t+plot_h:.1f}" x2="{W-pad_r}" y2="{pad_t+plot_h:.1f}" '
             f'stroke="{_T["baseline"]}" stroke-width="1"/>')
    return f'<div class="card">{_title(c)}{_svg(h, "".join(g))}{_notes(c)}</div>'


# ---------------------------------------------------------------- meter
def meter(c):
    """A single ratio against a limit — the honest form for one number vs a cap."""
    v, mx = float(c["value"]), float(c.get("max", 100))
    unit = c.get("unit", "")
    pct = max(0.0, min(1.0, v / mx if mx else 0))
    h = 132
    x0, x1 = 4, W - 4
    ty = 74
    th = 34
    fw = (x1 - x0) * pct
    g = [
        _text(x0, 34, c.get("value_label") or _fmt(v, unit), 44, MOON, 600),
        _text(x1, 34, c.get("cap_label") or f"of {_fmt(mx, unit)}", 21, FOG, 400, "end"),
        # track = a lighter step of the same ramp, so state reads across the whole bar
        f'<rect x="{x0}" y="{ty}" width="{x1-x0}" height="{th}" rx="{th/2}" '
        f'fill="{_T["track"]}" stroke="{_T["track_line"]}" stroke-width="1"/>',
        f'<rect x="{x0}" y="{ty}" width="{max(th, fw):.1f}" height="{th}" rx="{th/2}" '
        f'fill="{TEAL}" fill-opacity=".92" style="{GLOW_STRONG}"/>',
    ]
    if c.get("left") or c.get("right"):
        g.append(_text(x0, ty + th + 30, c.get("left", ""), 19, FOG))
        g.append(_text(x1, ty + th + 30, c.get("right", ""), 19, FOG, 400, "end"))
        h += 22
    return f'<div class="card">{_title(c)}{_svg(h, "".join(g))}{_notes(c)}</div>'


# ---------------------------------------------------------------- dumbbell
def dumbbell(c):
    """Before -> after per item. One hue, two shades: the 'after' is the lit one.

    Position is the encoding, so both ends are direct-labelled where they sit — no
    separate value column, which would fight the left-to-right read when the value
    falls. When the two ends crowd, the labels split above/below instead of colliding.
    """
    items = c["items"]
    unit = c.get("unit", "")
    row = int(88 * _T.get("h_scale", 1.0))
    lab_w = int(c.get("label_width", 224))
    h = 40 + row * len(items) + 44          # + x-axis band
    x0, x1 = lab_w, W - 46
    vals = [v for i in items for v in (i["from"], i["to"])]
    hi = max(vals)
    ticks = _nice_ticks(0, hi, 3)
    top = ticks[-1]

    def X(v):
        return x0 + (x1 - x0) * (v / (top or 1))

    plot_bottom = 40 + row * len(items) - 22
    g = []
    # recessive vertical grid + the scale the reader needs
    for t in ticks:
        x = X(t)
        g.append(f'<line x1="{x:.1f}" y1="14" x2="{x:.1f}" y2="{plot_bottom}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        g.append(_text(x, plot_bottom + 32, _fmt(t, unit), 18, AXIS_INK, 400, "middle", True))

    for k, it in enumerate(items):
        y = 46 + row * k
        g.append(_text(0, y + 8, it["label"], 24, "rgba(255,255,255,.86)", 400))
        xa, xb = X(it["from"]), X(it["to"])
        g.append(f'<line x1="{xa:.1f}" y1="{y}" x2="{xb:.1f}" y2="{y}" '
                 f'stroke="{_T["baseline"]}" stroke-width="2" stroke-linecap="round"/>')
        # 'before' — de-emphasised, with a 2px surface ring
        g.append(f'<circle cx="{xa:.1f}" cy="{y}" r="7" fill="{MUTED_MARK}" '
                 f'stroke="{SURFACE}" stroke-width="2"/>')
        # 'after' — lit
        g.append(f'<circle cx="{xb:.1f}" cy="{y}" r="8.5" fill="{TEAL}" '
                 f'stroke="{SURFACE}" stroke-width="2" style="{GLOW_STRONG}"/>')
        crowded = abs(xa - xb) < 96          # split the labels rather than overlap them
        g.append(_text(xa, y - 22, _fmt(it["from"], unit), 21, FOG, 500, "middle"))
        g.append(_text(xb, y + (34 if crowded else -22), _fmt(it["to"], unit), 25, MOON, 600, "middle"))
    return (f'<div class="card">{_title(c)}{_svg(h, "".join(g))}'
            f'{_legend([(c.get("from_label", "before"), MUTED_MARK, False), (c.get("to_label", "after"), TEAL, False)])}'
            f'{_notes(c)}</div>')


# ---------------------------------------------------------------- sparkline
def sparkline(values, w=150, h=42):
    """12-point trend for a stat tile: de-emphasised line, lit current point."""
    if not values or len(values) < 2:
        return ""
    lo, hi = min(values), max(values)
    def X(i): return 3 + (w - 6) * i / (len(values) - 1)
    def Y(v): return h - 5 - (h - 12) * ((v - lo) / ((hi - lo) or 1))
    d = " ".join(f"{'M' if i == 0 else 'L'}{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(values))
    ex, ey = X(len(values) - 1), Y(values[-1])
    return (f'<svg class="spark" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<path d="{d}" fill="none" stroke="{MUTED_MARK}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{TEAL}" '
            f'stroke="{SURFACE}" stroke-width="2" style="{GLOW_SOFT}"/></svg>')


RENDERERS = {"line": line, "column": column, "meter": meter, "dumbbell": dumbbell}
