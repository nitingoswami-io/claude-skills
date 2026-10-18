# Palette, type and layout

arch-doc shares demo-doc's spec-sheet layout and type, with an **indigo** accent instead of teal. A reader can tell a reference architecture from a demo at a glance, and the two still look like one family.

## Standalone HTML

| Token | Light | Dark | Used for |
|---|---|---|---|
| `--bg` | `#f6f7f9` | `#0f141a` | page background |
| `--surface` | `#ffffff` | `#161d25` | figures, tables, CoALA stages, credits |
| `--ink` | `#17202b` | `#e4e9ef` | body text, headings |
| `--muted` | `#5b6676` | `#96a1b0` | lede, captions, TOC, table headers |
| `--rule` | `#dde2e8` | `#2a333e` | borders, hairlines |
| `--accent` | `#4338ca` | `#a5b4fc` | eyebrow, section numbers, stage keys, highlighted figure paths |
| `--accent-soft` | `#e0e7ff` | `#1e1b4b` | maturity pill, TOC hover, working-memory fill |
| `--code-bg` | `#eef1f4` | `#1d2630` | inline code, code blocks, table header row |

| Role | Font | Weight / size |
|---|---|---|
| Display (H1, H2) | Source Serif 4 | 650 |
| Body | IBM Plex Sans | 400/500/600, 16px |
| Mono | IBM Plex Mono | 400/500, 12–13px |
| Figure labels | Kalam | 400 / 700, 11–13px |

The layout is the same as demo-doc: a 1120px shell, a 200px sticky contents rail, one reading column, and a single column at 860px and below.

## Hand-drawn figures

| Class | Light | Dark |
|---|---|---|
| ink (`currentColor`) | `#17202b` | `#e4e9ef` |
| `.sk-accent` | `#4338ca` | `#a5b4fc` |
| `.sk-bg` (label pills) | `#ffffff` | `#161d25` |
| `.sk-fill` | `#e0e7ff` | `#1e1b4b` |

The standalone `.svg` files carry these values in a small `<style>` block. Pages strip that block when they inline the figure and apply their own theme.

## Website (newspaper look)

On the author's site, architectures use the newspaper palette and fonts, like every other section. The site's components render the spec layout, the meta grid (Domain, Level, Key concepts, Related demos), the See it built box and the Credits list. Don't style anything in the MDX.
