# Hand-drawn figures

Every demo-doc figure is a **hand-authored inline SVG**. It follows the `artifact-diagramming` skill, plus the hand-drawn house style described here. Mermaid is no longer used.

**Load `artifact-diagramming` before you draw.** It decides *what* to draw. This file decides *how it looks*.

## What to draw (summary of artifact-diagramming)

- **Show the mechanism, not just its name.** Draw the path a request takes, which boundary it crosses, and which store it writes to. Leave out parts the section doesn't need.
- **Label every arrow** with what moves along it: `POST /chat`, `embed`, `SQL + vector search`, `200 OK`. An unlabelled arrow says nothing.
- **One figure, one claim.** The caption and the `aria-label` state that claim in a sentence. Labels inside the drawing are 1–4 words; explanations go in the caption.
- **Match complexity to the stakes.** Use a three-box figure for a one-hop idea. A sequence diagram can have 15 messages if the flow really has 15 steps.
- **Highlight one path** in the accent colour: the path the section is about, such as the chat path in the component diagram or the retrieval steps in the query sequence. Everything else stays in ink.

## Files

- Save figures as `docs/figures/fig-NN-short-name.svg`, numbered 01…N in document order, e.g. `fig-04-seq-ingest.svg`.
- These files are the single source for all three outputs:
  - **DESIGN.md** shows them as images: `![Fig. 4 …](figures/fig-04-seq-ingest.svg)`.
  - **HTML**: put `<!-- figure: fig-04-seq-ingest.svg -->` inside the figure, then run `python3 -I scripts/figures.py inline design.html docs/figures`.
  - **Site MDX**: copy them to `public/images/demos/<slug>/` and use `<Figure caption="…" src="/images/demos/<slug>/fig-04-seq-ingest.svg" />`. The site inlines the file so it follows the site's theme.
- Run `python3 -I scripts/figures.py check docs/figures` before handing over.

## The house style (copy this skeleton)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 330" role="img"
     aria-label="<One sentence: what the figure shows.>"
     class="sketch" font-family="Kalam, 'Segoe Print', 'Comic Sans MS', cursive" font-size="13"
     fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
<style>/* standalone viewing only — stripped when the figure is inlined into a page */
svg{color:#17202b} .sk-bg{fill:#ffffff} .sk-fill{fill:#e3f2ef} .sk-accent{stroke:#0f766e} text.sk-accent{fill:#0f766e;stroke:none}
@media (prefers-color-scheme:dark){svg{color:#e4e9ef} .sk-bg{fill:#161d25} .sk-fill{fill:#15302d} .sk-accent{stroke:#4fd1c0} text.sk-accent{fill:#4fd1c0}}
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

## Shapes by diagram type

| Diagram | Elements |
|---|---|
| Use case | Stick-figure actor (circle r=9 plus a body path); system boundary as a dashed group (`stroke-dasharray="7 5"`); use cases as ellipses; external systems as **double-bordered** boxes; dashed labelled arrows to the external systems |
| Component | Dashed group per runtime, titled `Name · tech :port`; one box per module; a cylinder (`path` with two arcs) for databases; double box for third-party APIs |
| Deployment | Nested dashed groups (machine ⊃ Docker); boxes with a sub-label for host:port; arrows labelled with the protocol |
| Sequence | Participant boxes at the top (or a stick figure for the user); dotted lifelines (`stroke-dasharray="3 6"`, width 1); solid arrows for calls; **dashed arrows for returns**; labels numbered `1 …`, `2 …`; self-calls as a small loop to the right; a `loop · each item` frame as a dotted rectangle |
| State | Filled start dot; states as `rx="18"` boxes; labelled transitions; routes that go back to an earlier state run around the outside |
| Class | 3-part box (`rx="4"`): bold title above a rule, then members at 11.5px (`+public`, `-private`). Arrows mean "depends on". Show only the members the doc mentions |
| ER | Table boxes with a bold title, columns on the left and notes on the right (`PK`, `FK`, `1536 dims`). A crow's-foot line labelled with the relationship verb |
| Component tree | Boxes with a sub-label for the state each one owns; arrows go parent → child; an arrow to the API module is labelled with the function called |

The reference drawings in `examples/rag-demo/figures/` cover every type above. Open the matching one and adapt its coordinates. Don't start from a blank canvas.
