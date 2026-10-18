# Palette, type and layout

## Standalone HTML (spec-sheet look)

The values below are taken from the approved RAG Demo document. Don't change them per demo.

| Token | Light | Dark | Used for |
|---|---|---|---|
| `--bg` | `#f6f7f9` | `#0f141a` | page background |
| `--surface` | `#ffffff` | `#161d25` | figures, tables, CoALA stages, prompt block |
| `--ink` | `#17202b` | `#e4e9ef` | body text, headings |
| `--muted` | `#5b6676` | `#96a1b0` | lede, captions, TOC links, table headers |
| `--rule` | `#dde2e8` | `#2a333e` | borders, hairlines |
| `--accent` | `#0f766e` | `#4fd1c0` | eyebrow, section numbers, stage keys, method cells, prompt rule |
| `--accent-soft` | `#e3f2ef` | `#15302d` | status pill, TOC hover |
| `--code-bg` | `#eef1f4` | `#1d2630` | inline code, code blocks, table header row |

Dark mode follows `prefers-color-scheme`. It can be forced with `data-theme="dark"` or `data-theme="light"` on `<html>`.

| Role | Font | Weight / size |
|---|---|---|
| Display (H1, H2) | Source Serif 4 | 650; H1 `clamp(2rem, 4.5vw, 2.9rem)`, H2 `1.65rem` |
| Body | IBM Plex Sans | 400/500/600, 16px, line-height 1.6 |
| Mono (eyebrow, numbers, code) | IBM Plex Mono | 400/500, 12–13px |
| Figures (hand-drawn labels) | Kalam | 400 for labels, 700 for titles, 11–13px |

Hand-drawn figures take their colours from the page:

| Class | Light | Dark |
|---|---|---|
| ink (`currentColor`) | `--ink` | `--ink` |
| `.sk-accent` (the highlighted path) | `--accent` `#0f766e` | `--accent` `#4fd1c0` |
| `.sk-bg` (label pills) | `--surface` | `--surface` |
| `.sk-fill` (rare tint) | `--accent-soft` | `--accent-soft` |

Each standalone `.svg` file carries the same values in its own small `<style>` block, so it reads correctly on GitHub and when opened on its own. Pages strip that block when they inline the figure.

Layout:
- The shell is 1120px wide, with a 200px sticky contents rail and one reading column (56px gap).
- At 860px and below, the rail turns into wrapped chips above the content.
- Paragraphs are capped at 68ch.
- At 720px and below, the CoALA strip stacks into 1 column.
- Labels (meta keys, TOC heading, table headers) are 11px, uppercase, tracked `.12em`, muted, weight 600.

## Website (newspaper look)

The site keeps the same structure (and the same hand-drawn figures, inlined so they follow its day and night themes) and swaps in its own tokens (paper `#f6f1e7`, ink `#141414`, newsprint red `#a4161a`; the night edition is `#111110` / `#ece6d9` / `#e0574f`) with Playfair Display, Source Serif 4, Libre Franklin and JetBrains Mono. You don't style anything yourself in the MDX: the components `SpecHeader`, `PipelineStrip`, `Stage`, `Figure`, `PromptBlock` and the contents rail apply the theme.
