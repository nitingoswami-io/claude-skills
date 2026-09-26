# Layout reference

Every `visual` object needs a `type`. Fields below are the complete set — anything else is
ignored. `highlight` is optional everywhere it appears and should be used on at most one
element per slide.

Contents: [flow](#flow) · [stack](#stack) · [compare](#compare) · [steps](#steps) ·
[bars](#bars) · [code](#code) · [hub](#hub) · [stat](#stat) · [themes](#theme-tokens) ·
[troubleshooting](#troubleshooting)

---

## flow

Stages that feed each other, joined by arrows.

```json
{
  "type": "flow",
  "orientation": "vertical",
  "nodes": [
    { "label": "Map side writes", "note": "one file per reducer" },
    { "label": "Fetch over network", "note": "reducers pull every block", "highlight": true }
  ]
}
```

- `orientation`: `"vertical"` (default, 3–5 nodes, arrows point down, each node gets an index
  numeral) or `"horizontal"` (2–3 nodes only — four will not fit at readable size).
- Vertical is the safer default: it gives each label room for a `note` and reads naturally on
  a phone.

## stack

Layers, drawn top-down in array order. The first element is the **top** layer.

```json
{
  "type": "stack",
  "layers": [
    { "label": "Client library", "note": "hashes the key" },
    { "label": "Hash ring", "note": "256 vnodes per node", "highlight": true }
  ]
}
```

3–5 layers. Use when the relationship is "sits on top of", not "happens after" — otherwise
use `flow`.

## compare

Two cards side by side. Cards hug their content and are vertically centred.

```json
{
  "type": "compare",
  "left":  { "heading": "Modulo hashing", "items": ["Every key moves", "Full cache miss"] },
  "right": { "heading": "Ring hashing", "good": true, "items": ["1/N keys move", "Rest stay warm"] }
}
```

- `good`: which side gets the accent border. Defaults to the right side, so put the
  correct/recommended approach on the right and the naive one on the left.
- Keep the two sides parallel — same number of items, same grammatical shape. The comparison
  reads instantly when the rows line up conceptually.

## steps

Numbered procedure with circled numerals.

```json
{
  "type": "steps",
  "items": [
    { "label": "Mark node draining", "note": "stop accepting new writes" }
  ]
}
```

Exactly 3 items is the sweet spot; 4 works, 5 gets tight. Start each label with a verb.

## bars

Horizontal bars, scaled to the largest value.

```json
{
  "type": "bars",
  "unit": " ms",
  "items": [
    { "label": "acks=0", "value": 2 },
    { "label": "acks=all", "value": 24, "highlight": true }
  ]
}
```

- `unit` is appended to each value — include a leading space for word units (`" ms"`,
  `" req/s"`) and none for symbols (`"%"`, `"x"`).
- `display` overrides the printed value for irregular labels: `{"value": 1400, "display": "1.4s"}`.
- 3–5 bars. Order them to make the argument — usually ascending, so the punchline is last.
- Values must be real. Don't invent benchmark numbers; if you don't have measurements, use
  `stat` or `compare` instead.

## code

Monospaced block with line numbers and highlight bands.

```json
{
  "type": "code",
  "lang": "python",
  "lines": ["df = df.repartition(200, \"user_id\")", "df.write.parquet(path)"],
  "highlight": [1]
}
```

- `lines`: one array element per line. Empty strings are blank lines. Indent with real spaces.
- `highlight`: 1-based line numbers, matching the printed gutter numbers.
- `lang` is a label only — there is no syntax colouring, which is deliberate: highlight bands
  direct attention better than rainbow tokens at feed size.
- Hard ceiling ~10 lines / 48 chars. Beyond that the font shrinks below readable. Cut to the
  lines that carry the idea; comments are usually the first thing to go.

## hub

One central concept with satellites around it. Best on slide 3 for "what this buys you".

```json
{
  "type": "hub",
  "center": "Producer ID + sequence",
  "spokes": ["Broker-side dedup", "Safe retries", "Ordering preserved", "No extra topic"]
}
```

- 3–5 spokes; 4 is the most balanced. Spokes can be plain strings or `{"label": "..."}`.
- `center` should be short — 2–4 words. It sits in a circle and will shrink hard if long.

## stat

Headline numbers with context. Values share one font size and the labels align in a column.

```json
{
  "type": "stat",
  "items": [
    { "value": "200", "label": "default shuffle partitions — rarely right for your volume" },
    { "value": "AQE", "label": "coalesces partitions at runtime, free in Spark 3.x" }
  ]
}
```

- 2–3 items. `value` should be ≤ 6 characters — the whole effect depends on it being big.
- `value` doesn't have to be numeric; a short flag or setting name (`AQE`, `acks=all`) works.

---

## Theme tokens

| Theme | Background | Accent | Reads best |
|---|---|---|---|
| `midnight` | deep navy `#0B1220` | cyan `#38BDF8` | Default. High contrast in both LinkedIn light and dark mode |
| `carbon` | near-black `#0E0E11` | violet `#A78BFA` | A moodier alternative when midnight feels overused |
| `paper` | off-white `#F7F6F3` | blue `#1D4ED8` | Print, light-background embeds, or a more corporate register |

Accents are applied automatically to kickers, arrows, highlights, and the takeaway strip.
Don't add colour fields to the spec — the palette is deliberately fixed so a series of decks
looks like a series.

## Troubleshooting

**Type looks tiny on one slide.** Auto-fit shrank it to avoid clipping. Cut words in that
field — see the budgets table in SKILL.md.

**Warning: "visual area is only Npx tall".** The header and takeaway ate the slide. Shorten
the title to ≤ 2 lines, drop the subtitle, or move the takeaway to another slide.

**Bars all look the same length.** One value dwarfs the rest, so everything else floors at the
minimum bar width. Use a log-friendly framing or switch to `stat`.

**Text touching a panel edge.** A single unbreakable token (a long identifier, a URL) can't be
wrapped. Shorten it or break it across two `lines` entries.

**Rendering a different number of slides.** The renderer accepts any count and numbers the
footer accordingly, so a 5-slide deck works if asked. Three remains the default because it is
what fits a single scroll-stop.
