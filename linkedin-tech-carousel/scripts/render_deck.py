#!/usr/bin/env python3
"""
render_deck.py — render a LinkedIn-ready technical carousel from a JSON spec.

Usage:
    python3 render_deck.py spec.json --out-dir ./out --basename my-topic

Outputs:
    <basename>.pdf        multi-page, for a LinkedIn *document* post (native swipe)
    <basename>-1..N.png   one image per slide, for an image carousel or other platforms

Everything is drawn on a fixed pixel canvas (1080x1350 for 4:5, 1080x1080 for 1:1),
so what you see is exactly what LinkedIn shows. Font sizes below are specified in
PIXELS and converted to points internally — do not mix units.
"""

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, FancyArrow, Circle, Rectangle
from matplotlib.lines import Line2D

DPI = 100
SANS = "Liberation Sans"
MONO = "Liberation Mono"

matplotlib.rcParams["pdf.fonttype"] = 42   # embed real TrueType, keeps text selectable
matplothack = matplotlib.rcParams
matplothack = None
matplotlib.rcParams["font.family"] = SANS

# ---------------------------------------------------------------- themes

THEMES = {
    "midnight": {
        "bg": "#0B1220", "panel": "#152234", "panel_edge": "#24374F",
        "text": "#F1F5F9", "muted": "#8FA3BC",
        "accent": "#38BDF8", "accent_ink": "#04121E", "accent2": "#FBBF24",
        "rule": "#24374F",
    },
    "carbon": {
        "bg": "#0E0E11", "panel": "#1A1A20", "panel_edge": "#2E2E38",
        "text": "#F5F5F7", "muted": "#9C9CA8",
        "accent": "#A78BFA", "accent_ink": "#140A26", "accent2": "#34D399",
        "rule": "#2E2E38",
    },
    "paper": {
        "bg": "#F7F6F3", "panel": "#FFFFFF", "panel_edge": "#DFDCD4",
        "text": "#14181F", "muted": "#61697A",
        "accent": "#1D4ED8", "accent_ink": "#FFFFFF", "accent2": "#B45309",
        "rule": "#DFDCD4",
    },
}

ASPECTS = {"4:5": (1080, 1350), "1:1": (1080, 1080)}

M = 76          # side margin
RADIUS = 18     # default corner rounding


# ---------------------------------------------------------------- text engine

def pt(px_size):
    """Convert a pixel font size to points for the current DPI."""
    return px_size * 72.0 / DPI


class Canvas:
    def __init__(self, w, h, theme):
        self.w, self.h, self.t = w, h, theme
        self.fig = plt.figure(figsize=(w / DPI, h / DPI), dpi=DPI)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(0, h)
        self.ax.axis("off")
        self.fig.patch.set_facecolor(theme["bg"])
        self.ax.add_patch(Rectangle((0, 0), w, h, color=theme["bg"], zorder=-10))
        self._r = self.fig.canvas.get_renderer()

    # -- measurement -------------------------------------------------
    def measure(self, s, size_px, weight="normal", family=SANS):
        t = self.ax.text(0, 0, s, fontsize=pt(size_px), fontweight=weight,
                         family=family, alpha=0)
        bb = t.get_window_extent(renderer=self._r)
        t.remove()
        return bb.width, bb.height

    def wrap(self, s, size_px, max_w, weight="normal", family=SANS):
        """Greedy word wrap using real glyph metrics."""
        words, lines, cur = s.split(), [], ""
        for wd in words:
            trial = f"{cur} {wd}".strip()
            if self.measure(trial, size_px, weight, family)[0] <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def fit(self, s, max_w, max_lines, size_px, min_px, weight="normal", family=SANS):
        """Shrink font until the string wraps into max_lines within max_w."""
        size = size_px
        while size > min_px:
            lines = self.wrap(s, size, max_w, weight, family)
            if len(lines) <= max_lines:
                return lines, size
            size -= 2
        return self.wrap(s, min_px, max_w, weight, family)[:max_lines], min_px

    # -- drawing -----------------------------------------------------
    def text(self, x, y, s, size_px, color=None, weight="normal", ha="left",
             va="baseline", family=SANS, alpha=1.0, spacing=1.22, zorder=5):
        return self.ax.text(x, y, s, fontsize=pt(size_px), color=color or self.t["text"],
                            fontweight=weight, ha=ha, va=va, family=family,
                            alpha=alpha, linespacing=spacing, zorder=zorder)

    def block(self, x, y_top, lines, size_px, leading=1.32, **kw):
        """Draw wrapped lines downward from y_top. Returns y of the last baseline."""
        step = size_px * leading
        y = y_top - size_px * 0.82
        for ln in lines:
            self.text(x, y, ln, size_px, **kw)
            y -= step
        return y + step

    def line(self, x0, y0, x1, y1, color=None, lw=1.5, alpha=1.0, zorder=3):
        self.ax.add_line(Line2D([x0, x1], [y0, y1], color=color or self.t["rule"],
                                lw=lw, alpha=alpha, zorder=zorder))

    def panel(self, x, y, w, h, fill=None, edge=None, radius=RADIUS, lw=1.6, zorder=1):
        p = FancyBboxPatch((x + radius, y + radius), w - 2 * radius, h - 2 * radius,
                           boxstyle=f"round,pad={radius}",
                           facecolor=fill or self.t["panel"],
                           edgecolor=edge or self.t["panel_edge"],
                           linewidth=lw, zorder=zorder)
        self.ax.add_patch(p)
        return p

    def save_png(self, path):
        self.fig.savefig(path, dpi=DPI, facecolor=self.t["bg"], pad_inches=0)

    def close(self):
        plt.close(self.fig)


# ---------------------------------------------------------------- visuals
# Each visual fills the rect (x, y, w, h). y is the BOTTOM of the region.

def v_flow(c, r, spec):
    x, y, w, h = r
    nodes = spec["nodes"]
    n = len(nodes)
    horiz = spec.get("orientation", "vertical") == "horizontal"
    t = c.t

    if horiz:
        gap, arrow = 26, 34
        bw = (w - gap * (n - 1) - arrow * (n - 1)) / n
        bh = min(h, 340)
        by = y + (h - bh) / 2
        cx = x
        for i, nd in enumerate(nodes):
            hl = nd.get("highlight")
            c.panel(cx, by, bw, bh,
                    fill=t["accent"] if hl else t["panel"],
                    edge=t["accent"] if hl else t["panel_edge"])
            ink = t["accent_ink"] if hl else t["text"]
            lines, sz = c.fit(nd["label"], bw - 36, 3, 34, 20, "bold")
            note = nd.get("note")
            blk_h = len(lines) * sz * 1.3 + (26 if note else 0)
            top = by + bh / 2 + blk_h / 2
            end = c.block(cx + bw / 2, top, lines, sz, weight="bold",
                          color=ink, ha="center")
            if note:
                nl, ns = c.fit(note, bw - 36, 2, 21, 15)
                c.block(cx + bw / 2, end - sz * 0.7, nl, ns, ha="center",
                        color=t["accent_ink"] if hl else t["muted"], alpha=0.95)
            if i < n - 1:
                ax0 = cx + bw + gap * 0.35
                c.ax.add_patch(FancyArrow(ax0, by + bh / 2, arrow + gap * 0.3, 0,
                                          width=3, head_width=16, head_length=14,
                                          color=t["accent"], zorder=4,
                                          length_includes_head=True))
            cx += bw + gap + arrow
    else:
        arrow = 40
        bh = (h - arrow * (n - 1)) / n
        cy = y + h - bh
        for i, nd in enumerate(nodes):
            hl = nd.get("highlight")
            c.panel(x, cy, w, bh,
                    fill=t["accent"] if hl else t["panel"],
                    edge=t["accent"] if hl else t["panel_edge"])
            ink = t["accent_ink"] if hl else t["text"]
            note = nd.get("note")
            lines, sz = c.fit(nd["label"], w - 200, 2, 40, 24, "bold")
            nl, ns = (c.fit(note, w - 200, 2, 23, 16) if note else ([], 0))
            blk = len(lines) * sz * 1.28 + (len(nl) * ns * 1.3 + 10 if nl else 0)
            top = cy + bh / 2 + blk / 2
            end = c.block(x + 40, top, lines, sz, weight="bold", color=ink)
            if nl:
                c.block(x + 40, end - sz * 0.55, nl, ns,
                        color=t["accent_ink"] if hl else t["muted"], alpha=0.95)
            # step index on the right
            c.text(x + w - 40, cy + bh / 2, f"{i + 1}", 46,
                   color=ink, weight="bold", ha="right", va="center", alpha=0.28)
            if i < n - 1:
                c.ax.add_patch(FancyArrow(x + w / 2, cy - 8, 0, -(arrow - 16),
                                          width=3, head_width=16, head_length=13,
                                          color=t["accent"], zorder=4,
                                          length_includes_head=True))
            cy -= bh + arrow


def v_stack(c, r, spec):
    x, y, w, h = r
    layers = spec["layers"]
    n = len(layers)
    gap = 14
    bh = (h - gap * (n - 1)) / n
    cy = y + h - bh
    t = c.t
    for lyr in layers:
        hl = lyr.get("highlight")
        c.panel(x, cy, w, bh,
                fill=t["accent"] if hl else t["panel"],
                edge=t["accent"] if hl else t["panel_edge"])
        ink = t["accent_ink"] if hl else t["text"]
        c.ax.add_patch(Rectangle((x, cy + 10), 7, bh - 20,
                                 color=t["accent_ink"] if hl else t["accent"],
                                 zorder=3, alpha=0.9 if hl else 1))
        note = lyr.get("note")
        lines, sz = c.fit(lyr["label"], w - 90, 2, 36, 22, "bold")
        nl, ns = (c.fit(note, w - 90, 2, 22, 15) if note else ([], 0))
        blk = len(lines) * sz * 1.28 + (len(nl) * ns * 1.3 + 8 if nl else 0)
        top = cy + bh / 2 + blk / 2
        end = c.block(x + 36, top, lines, sz, weight="bold", color=ink)
        if nl:
            c.block(x + 36, end - sz * 0.55, nl, ns,
                    color=t["accent_ink"] if hl else t["muted"], alpha=0.95)
        cy -= bh + gap


def v_compare(c, r, spec):
    x, y, w, h = r
    t = c.t
    gap = 26
    cw = (w - gap) / 2

    # Pre-measure both columns so the cards hug their content instead of
    # leaving a dead zone at the bottom of a full-height box.
    plan = {}
    needed = 0
    for side in ("left", "right"):
        d = spec[side]
        hl, hs = c.fit(d["heading"], cw - 56, 2, 32, 20, "bold")
        rows = [c.fit(i, cw - 76, 3, 24, 17) for i in d["items"]]
        ph = (len(hl) * hs * 1.3 + 46
              + sum(len(r_) * sz * 1.34 + sz * 0.9 for r_, sz in rows) + 30)
        plan[side] = (hl, hs, rows, d)
        needed = max(needed, ph)
    ch = min(h, needed)
    cby = y + (h - ch) / 2

    for idx, side in enumerate(("left", "right")):
        hl, hs, rows, d = plan[side]
        cx = x + idx * (cw + gap)
        good = d.get("good", idx == 1)
        edge = t["accent"] if good else t["panel_edge"]
        c.panel(cx, cby, cw, ch, edge=edge, lw=2.2 if good else 1.6)
        yy = c.block(cx + 28, cby + ch - 30, hl, hs, weight="bold",
                     color=t["accent"] if good else t["muted"])
        c.line(cx + 28, yy - 22, cx + cw - 28, yy - 22, lw=1.4)
        yy -= 54
        for (lines, sz) in rows:
            c.text(cx + 28, yy - sz * 0.75, "\u25aa", sz, color=edge, weight="bold")
            yy = c.block(cx + 54, yy, lines, sz, leading=1.34) - sz * 0.9


def v_bars(c, r, spec):
    x, y, w, h = r
    t = c.t
    items = spec["items"]
    unit = spec.get("unit", "")
    n = len(items)
    gap = 22
    bh = min((h - gap * (n - 1)) / n, 92)
    total = n * bh + (n - 1) * gap
    cy = y + h - (h - total) / 2 - bh
    vmax = max(abs(i["value"]) for i in items) or 1
    label_w = 0
    for i in items:
        label_w = max(label_w, c.measure(i["label"], 24, "bold")[0])
    label_w = min(label_w, w * 0.34)
    track_x = x + label_w + 26
    track_w = w - label_w - 26 - 130
    for it in items:
        hl = it.get("highlight")
        col = t["accent"] if hl else t["muted"]
        lines, sz = c.fit(it["label"], label_w, 2, 24, 16, "bold")
        c.block(x, cy + bh / 2 + len(lines) * sz * 1.25 / 2, lines, sz,
                weight="bold", color=t["text"] if hl else t["muted"])
        c.ax.add_patch(FancyBboxPatch((track_x + 8, cy + bh / 2 - 15), track_w - 16, 30,
                                      boxstyle="round,pad=8",
                                      facecolor=t["panel"], edgecolor="none", zorder=2))
        bw = max(track_w * abs(it["value"]) / vmax, 46)
        c.ax.add_patch(FancyBboxPatch((track_x + 8, cy + bh / 2 - 15), bw - 16, 30,
                                      boxstyle="round,pad=8",
                                      facecolor=col, edgecolor="none", zorder=3))
        val = it.get("display") or f"{it['value']:g}{unit}"
        c.text(track_x + track_w + 18, cy + bh / 2, val, 30,
               color=t["text"] if hl else t["muted"], weight="bold", va="center")
        cy -= bh + gap


def v_steps(c, r, spec):
    x, y, w, h = r
    t = c.t
    items = spec["items"]
    n = len(items)
    gap = 20
    bh = (h - gap * (n - 1)) / n
    cy = y + h - bh
    for i, it in enumerate(items):
        c.panel(x, cy, w, bh)
        d = min(bh * 0.44, 62)
        ccx, ccy = x + 34 + d / 2, cy + bh / 2
        c.ax.add_patch(Circle((ccx, ccy), d / 2, facecolor=t["accent"],
                              edgecolor="none", zorder=3))
        c.text(ccx, ccy, str(i + 1), d * 0.52, color=t["accent_ink"],
               weight="bold", ha="center", va="center", zorder=4)
        tx = ccx + d / 2 + 26
        tw = w - (tx - x) - 34
        note = it.get("note")
        lines, sz = c.fit(it["label"], tw, 2, 32, 21, "bold")
        nl, ns = (c.fit(note, tw, 3, 22, 15) if note else ([], 0))
        blk = len(lines) * sz * 1.28 + (len(nl) * ns * 1.3 + 8 if nl else 0)
        end = c.block(tx, cy + bh / 2 + blk / 2, lines, sz, weight="bold")
        if nl:
            c.block(tx, end - sz * 0.55, nl, ns, color=t["muted"])
        cy -= bh + gap


def v_code(c, r, spec):
    x, y, w, h = r
    t = c.t
    lines = spec["lines"]
    hi = set(spec.get("highlight", []))
    c.panel(x, y, w, h, fill=t["panel"])
    lang = spec.get("lang")
    top = y + h - 26
    if lang:
        c.text(x + 28, top - 20, lang.upper(), 20, color=t["accent"],
               weight="bold", family=MONO)
        top -= 52
    n = len(lines)
    avail_h = top - y - 26
    size = 26
    while size > 13:
        longest = max(lines, key=len) if lines else ""
        if (c.measure(longest, size, family=MONO)[0] <= w - 108
                and n * size * 1.62 <= avail_h):
            break
        size -= 1
    step = size * 1.62
    cy = top - size * 0.85
    for i, ln in enumerate(lines, start=1):
        if i in hi:
            c.ax.add_patch(Rectangle((x + 14, cy - size * 0.42), w - 28, step * 0.92,
                                     facecolor=t["accent"], alpha=0.16,
                                     edgecolor="none", zorder=2))
            c.ax.add_patch(Rectangle((x + 14, cy - size * 0.42), 5, step * 0.92,
                                     facecolor=t["accent"], edgecolor="none", zorder=3))
        c.text(x + 34, cy, f"{i:>2}", size, color=t["muted"],
               family=MONO, alpha=0.55, zorder=4)
        c.text(x + 78, cy, ln, size,
               color=t["text"] if i in hi else t["text"],
               family=MONO, alpha=1.0 if i in hi else 0.86, zorder=4)
        cy -= step


def v_hub(c, r, spec):
    import math
    x, y, w, h = r
    t = c.t
    spokes = spec["spokes"]
    n = len(spokes)
    cx, cy = x + w / 2, y + h / 2

    bw = min(252, (w - 40) / 2 if n > 2 else w * 0.6)
    bh = min(92, h / (n / 2 + 1.4))
    # Elliptical placement: a wide, short region should spread sideways rather
    # than shrink to the smaller of the two axes.
    rx, ry = w / 2 - bw / 2, h / 2 - bh / 2
    cr = min(w, h) * 0.17

    for i, sp in enumerate(spokes):
        ang = math.pi / 2 + i * 2 * math.pi / n
        sx, sy = cx + rx * math.cos(ang), cy + ry * math.sin(ang)
        label = sp if isinstance(sp, str) else sp["label"]
        c.line(cx, cy, sx, sy, color=t["accent"], lw=2.2, alpha=0.5, zorder=2)
        c.panel(sx - bw / 2, sy - bh / 2, bw, bh, radius=14, zorder=3)
        lines, sz = c.fit(label, bw - 30, 2, 24, 14, "bold")
        c.block(sx, sy + len(lines) * sz * 1.26 / 2, lines, sz,
                weight="bold", ha="center", zorder=4)

    c.ax.add_patch(Circle((cx, cy), cr, facecolor=t["accent"],
                          edgecolor=t["bg"], lw=7, zorder=5))
    cl, cs = c.fit(spec["center"], cr * 1.7, 3, 26, 14, "bold")
    c.block(cx, cy + len(cl) * cs * 1.24 / 2, cl, cs, weight="bold",
            color=t["accent_ink"], ha="center", zorder=6)


def v_stat(c, r, spec):
    x, y, w, h = r
    t = c.t
    items = spec["items"]
    n = len(items)
    gap = 22
    bh = (h - gap * (n - 1)) / n

    # One value size for every card, and one shared label column, so the
    # numbers read as a set instead of three unrelated headlines.
    vsize = min(bh * 0.5, 96)
    for it in items:
        vsize = min(vsize, c.fit(it["value"], w * 0.38, 1, vsize, 34, "bold")[1])
    vcol = max(c.measure(it["value"], vsize, "bold")[0] for it in items)
    tx = x + 40 + vcol + 34

    cy = y + h - bh
    for it in items:
        c.panel(x, cy, w, bh)
        c.text(x + 40, cy + bh / 2, it["value"], vsize, color=t["accent"],
               weight="bold", va="center")
        lines, sz = c.fit(it["label"], w - (tx - x) - 36, 3, 26, 16)
        c.block(tx, cy + bh / 2 + len(lines) * sz * 1.3 / 2, lines, sz,
                color=t["muted"])
        cy -= bh + gap


VISUALS = {"flow": v_flow, "stack": v_stack, "compare": v_compare, "bars": v_bars,
           "steps": v_steps, "code": v_code, "hub": v_hub, "stat": v_stat}


# ---------------------------------------------------------------- slide

def render_slide(slide, idx, total, deck, size, theme):
    w, h = size
    c = Canvas(w, h, theme)
    t = theme

    # --- header
    y = h - 74
    kicker = slide.get("kicker")
    if kicker:
        c.text(M, y, kicker.upper(), 22, color=t["accent"], weight="bold")
        # letter-spaced feel via small caps kicker + rule
        y -= 40

    title = slide["title"]
    tlines, tsize = c.fit(title, w - 2 * M, 3, 66, 38, "bold")
    y = c.block(M, y, tlines, tsize, weight="bold", leading=1.16)

    sub = slide.get("subtitle")
    if sub:
        y -= tsize * 0.55
        slines, ssize = c.fit(sub, w - 2 * M - 40, 3, 28, 20)
        y = c.block(M, y, slines, ssize, color=t["muted"], leading=1.34)

    header_bottom = y - 46
    c.line(M, header_bottom, w - M, header_bottom, lw=1.5, zorder=2)

    # --- footer
    foot_y = 56
    footer = deck.get("footer", "")
    if footer:
        c.text(M, foot_y, footer, 21, color=t["muted"], alpha=0.9)
    c.text(w - M, foot_y, f"{idx}/{total}", 21, color=t["muted"],
           weight="bold", ha="right", alpha=0.9)
    floor = foot_y + 46

    # --- takeaway strip (optional, sits above footer)
    take = slide.get("takeaway")
    if take:
        lines, sz = c.fit(take, w - 2 * M - 76, 3, 27, 18, "bold")
        bh = len(lines) * sz * 1.34 + 46
        c.panel(M, floor, w - 2 * M, bh, fill=t["panel"], edge=t["accent"], lw=2.0)
        c.ax.add_patch(Rectangle((M, floor + 12), 7, bh - 24,
                                 color=t["accent"], zorder=3))
        c.block(M + 34, floor + bh - 22, lines, sz, weight="bold", leading=1.34)
        floor += bh + 30

    # --- visual
    vis = slide.get("visual")
    if vis:
        region = (M, floor, w - 2 * M, header_bottom - 34 - floor)
        if region[3] < 120:
            print(f"  ! slide {idx}: visual area is only {region[3]:.0f}px tall — "
                  f"trim the title, subtitle, or takeaway.", file=sys.stderr)
        VISUALS[vis["type"]](c, region, vis)

    return c


def render(spec, out_dir, basename):
    theme = THEMES[spec.get("theme", "midnight")]
    size = ASPECTS[spec.get("aspect", "4:5")]
    slides = spec["slides"]
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = out_dir / f"{basename}.pdf"
    pngs = []
    with PdfPages(pdf_path) as pdf:
        for i, s in enumerate(slides, start=1):
            c = render_slide(s, i, len(slides), spec, size, theme)
            png = out_dir / f"{basename}-{i}.png"
            c.save_png(png)
            pdf.savefig(c.fig, facecolor=theme["bg"])
            c.close()
            pngs.append(png)
    return pdf_path, pngs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--basename", default="carousel")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text())
    pdf, pngs = render(spec, a.out_dir, a.basename)
    print(f"PDF : {pdf}")
    for p in pngs:
        print(f"PNG : {p}")


if __name__ == "__main__":
    main()
