# Hand-drawn figures

Every arch-doc figure is a **hand-authored inline SVG**. It follows the `artifact-diagramming` skill, plus the hand-drawn house style described here. Mermaid is no longer used.

**Load `artifact-diagramming` before you draw.** It decides *what* to draw. This file decides *how it looks*.

## What to draw (summary of artifact-diagramming)

- **Show the mechanism, not just its name.** Draw the path a request takes, which boundary it crosses, and which store it writes to. Leave out parts the section doesn't need.
- **Label every arrow** with what moves along it: `POST /chat`, `embed`, `SQL + vector search`, `200 OK`. An unlabelled arrow says nothing.
- **One figure, one claim.** The caption and the `aria-label` state that claim in a sentence. Labels inside the drawing are 1–4 words; explanations go in the caption.
- **Match complexity to the stakes.** Use a three-box figure for a one-hop idea. A sequence diagram can have 15 messages if the flow really has 15 steps.
- **Highlight one path** in the accent colour: the path the section is about, such as the chat path in the component diagram or the retrieval steps in the query sequence. Everything else stays in ink.

## Files

- Save figures as `figures/fig-NN-short-name.svg` next to `ARCHITECTURE.md`, numbered 01…N in document order, e.g. `fig-02-how-it-works.svg`.
- These files are the single source for all three outputs:
  - **ARCHITECTURE.md** shows them as images: `![Fig. 3 …](figures/fig-02-how-it-works.svg)`.
  - **HTML**: put `<!-- figure: fig-02-how-it-works.svg -->` inside the figure, then run `python3 -I scripts/figures.py inline architecture.html figures`.
  - **Site MDX**: copy them to `public/images/architectures/<slug>/` and use `<Figure caption="…" src="/images/architectures/<slug>/fig-02-how-it-works.svg" />`. The site inlines the file so it follows the site's theme.
- Run `python3 -I scripts/figures.py check figures` before handing over.

## The house style (copy this skeleton)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 330" role="img"
     aria-label="<One sentence: what the figure shows.>"
     class="sketch" font-family="Kalam, 'Segoe Print', 'Comic Sans MS', cursive" font-size="13"
     fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
<style>/* standalone viewing only — stripped when the figure is inlined into a page */
svg{color:#17202b} .sk-bg{fill:#ffffff} .sk-fill{fill:#e0e7ff} .sk-accent{stroke:#4338ca} text.sk-accent{fill:#4338ca;stroke:none}
@media (prefers-color-scheme:dark){svg{color:#e4e9ef} .sk-bg{fill:#161d25} .sk-fill{fill:#1e1b4b} .sk-accent{stroke:#a5b4fc} text.sk-accent{fill:#a5b4fc}}
</style>
<defs>
<filter id="rough" x="-3%" y="-3%" width="106%" height="106%"><feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G"/></filter>
<marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1.5 1.5 L8.5 5 L1.5 8.5" fill="none" stroke="currentColor" stroke-width="1.4"/></marker>
<marker id="arrow-accent" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path class="sk-accent" d="M1.5 1.5 L8.5 5 L1.5 8.5" fill="none" stroke="currentColor" stroke-width="1.4"/></marker>
</defs>
<g filter="url(#rough)">
  <!-- shapes and arrows only: they wobble -->
</g>
<g fill="currentColor" stroke="none">
  <!-- label backgrounds (class="sk-bg") and text: these stay crisp -->
</g>
</svg>
```

Rules:
- **Two layers.** Shapes go inside `<g filter="url(#rough)">`, which gives the wobbly hand-drawn line. Text goes in the unfiltered group, because wobbly text is hard to read.
- **Colour.** Use `currentColor` everywhere. Add `class="sk-accent"` to the highlighted path's shapes and labels, and use `marker-end="url(#arrow-accent)"` on its arrows. Use `sk-fill` for a light tint, rarely. Hex colours appear **only** inside the `<style>` block. Pages strip that block and apply their own theme.
- **Handwriting.** Use the Kalam font: 13px for labels, 11–12px for sub-labels and arrow labels, and `font-weight="700"` for group and class titles.
- **Grid.** Put coordinates on a 2px grid with even gaps. Standard sizes:
  - boxes are 36–48 px tall;
  - gaps between boxes are 24–40 px;
  - group padding is 30 px;
  - box corners are `rx="6"`, states `rx="18"`, groups `rx="10"`, classes and tables `rx="4"`.
- **Arrow labels** sit at the midpoint, about 6 px above the line, on a background pill: `<rect class="sk-bg" … rx="3"/>` followed by the `<text>`. Size the pill at about 6.7 px per character + 8, by 17 px tall.
- **Seeds.** Give each figure its own `seed` (3, 4, 5, …) so the wobble differs between figures.
- **Width.** 640–800 for most figures. Sequence diagrams use as much width as their participants need, at about 120–140 px per lifeline.
- **Self-contained.** No `<script>`, `<foreignObject>`, `<image>` or external `href`. All ids live in this fragment. The inliner prefixes them.

## The two or three figures

| Figure | Required | What it shows | Shapes |
|---|---|---|---|
| 1 · At a glance | yes | The concept's parts and how they connect | Dashed groups for families of parts (e.g. "Long-term memory"); one `sk-fill` box for the centre of the idea; labelled arrows naming the relationship (`retrieval`, `learning`, `act`) |
| 2 · How it works | yes | One cycle or flow, step by step | A row of step boxes inside dashed stage groups (e.g. Planning / Execution); the loop-back arrow labelled with its stopping rule |
| 3 · Worked example | when a demo exists | A demo on the site mapped onto the concept | The demo's real components, labelled with their concept role as sub-labels; a **dashed box** for anything the demo is missing |

Use generic labels in figures 1–2 ("vector store", not `vectorstore.py`). Only figure 3 uses a specific system's names.

The reference drawings in `examples/coala-cognitive-architecture/figures/` show all three. Start from the matching one.
