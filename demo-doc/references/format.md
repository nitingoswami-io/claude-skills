# demo-doc format specification

This file is the contract. Each rule holds in all three outputs unless a format-specific note says otherwise.

## Header

| Part | Rule | Example |
|---|---|---|
| Eyebrow | `DESIGN DOCUMENT · <slug>`, monospace, accent colour | `DESIGN DOCUMENT · rag-demo` |
| Title (H1) | `<Name>: <what it does, as a verb phrase>`, no trailing period | `RAG Demo: upload documents, chat with them` |
| Lede | 1–2 sentences, at most 62 characters per line on screen. Says what it shows and why it's worth looking at. Mentions CoALA if the demo maps to it. | — |
| Meta grid | Four cells in this order: **Stack** (` · `-separated), **Models** (each in `code`), **Date** (`17 Oct 2026`), **Status** (pill) | — |
| Status pill | One of `Draft`, `Approved`, `Approved · built` | — |
| GitHub links | Under the meta grid: **View code · Fork · Report an issue · Contribute**, linking to `<repo>`, `<repo>/fork`, `<repo>/issues/new` and `<repo>/blob/main/CONTRIBUTING.md`. Leave them out (and list `TBD`) when there is no repo URL. Add `Live demo` first when a deployed URL exists | — |

## Sections (fixed order, always 10)

Section titles are fixed. Use exactly these strings:

1. `Purpose & scope`
2. `Use cases`
3. `Architecture`
4. `Key flows`
5. `Backend design`
6. `Data model`
7. `Frontend design`
8. `Project layout`
9. `Run & verify`
10. `Next steps`

Sub-headings (H3) are sentence case. Under Key flows they are numbered `4.1`, `4.2` and so on, and named `<Flow>: <a → b → c>` (e.g. `4.1 Ingestion: upload → chunk → embed → store`). Under Purpose & scope they are exactly `In scope` and `Out of scope`. Under Backend design they are exactly `System prompt` and `API contract`, when present.

### 1. Purpose & scope
- Opening paragraph: what the app teaches and which CoALA memories and actions it exercises. **Bold** the CoALA terms.
- **CoALA pipeline strip**: exactly 5 stages, left to right in data-flow order. Each stage has:
  - `k`: the code key (route, function, class or store), in monospace accent colour;
  - `t`: what happens, in 2–4 words (`Chunk · embed · store`);
  - role: the CoALA concept (`Semantic memory (long-term)`, `Retrieval action`, `Working memory`, `Learning action`, `Reasoning → external action`, `Episodic memory`, `Procedural memory`, `Decision procedure`).
- `In scope`: 3–6 bullets, each starting with a verb.
- `Out of scope`: a single paragraph naming what's deliberately left out, ending with "Section 10 lists these as follow-ups."

### 2. Use cases
- Figure: a stick-figure actor, use cases as ellipses inside a dashed system boundary, and external systems as double-bordered boxes joined by dashed, labelled arrows.
- Table `ID | Use case | Behaviour`, with IDs `UC1…UCn` and the behaviour written as system responses.

### 3. Architecture
- One paragraph: the number of runtime parts and what each one owns.
- Figure: a component diagram, with one dashed group per runtime titled `Name · tech :port`, a cylinder for each database, and a double box for each third-party API.
- Figure: a deployment view, with nested groups for machine and container, host:port sub-labels, and arrows labelled with the protocol.

### 4. Key flows
- One sequence figure per main flow, with numbered message labels (`1 …`), solid call arrows, **dashed return arrows** and a dotted `loop · …` frame. The retrieval and LLM steps are highlighted in the accent colour.
- A state figure for any UI component that has loading or error states.
- Captions name the CoALA concept where one applies: `Sequence: ingestion (CoALA learning action).`

### 5. Backend design
- Figure: a class diagram covering modules (as 3-part boxes with `+public` / `-private` members) and the request/response models.
- Table `File | Responsibility`: one row per module, with file paths in code.
- `System prompt`: verbatim, monospace, left accent rule.
- `API contract`: table `Method | Path | Request | Response`. The method cell is monospace in the accent colour (HTML `td.method`).
- One sentence listing error codes and their causes.

### 6. Data model
- One sentence on who creates the schema (ORM, migrations, library on first use).
- Figure: an ER diagram, with table boxes showing columns on the left and notes on the right (`PK`, `FK`, `1536 dims`), joined by a crow's-foot line labelled with the relationship verb.

### 7. Frontend design
- Figure: a component tree, with boxes sub-labelled by the state each one owns and arrows from parent to child.
- 2–4 bullets: rendering model, how it calls the API, one UX detail that makes the demo's point visible.

### 8. Project layout
- Fenced tree with `├──`/`└──` and right-aligned comments. Keep it to 3 levels at most, and collapse leaf lists with ` · `.

### 9. Run & verify
- One fenced block of commands that work when pasted in order. **The first line is `git clone <repo>.git && cd <slug>`.** Add trailing `# comments` for ports and manual steps.
- Table `Check | Expected`, 4–6 rows. It must include a health check, the main happy path, **one grounded answer** with its citation, and **one refusal or validation error**.

### 10. Next steps
- Table `Idea | What it teaches`, 3–6 rows, ordered by learning value. Name the CoALA concept when the idea adds one.
- Then an H3 `Contribute` with one paragraph: "Fork the repo, pick an idea from the table, and open a pull request. Bugs and unclear steps go in issues." Link the fork, issues and CONTRIBUTING.md URLs. Omit it only when there is no repo URL.

## Credits & sources

Unnumbered, after section 10. A numbered list in the form *authors, linked title, year*, followed by what was taken. Follow `references/credits.md`. In MDX it isn't written in the body: the site renders it from the frontmatter `sources`.

## Figures

- Every diagram is a **hand-drawn SVG**, following `references/diagrams.md` and the `artifact-diagramming` skill. No Mermaid.
- Files are named `docs/figures/fig-NN-short-name.svg`, and numbering runs from 1 to N across the whole document; it never restarts per section.
- Caption: `Fig. N` in bold monospace, then `<Diagram type>: <one line>.` or `<Diagram type> for <subject>.` The SVG's `aria-label` says the same thing as a full sentence.
- Diagram types: `Use case diagram`, `Component diagram`, `Deployment view`, `Sequence`, `State diagram`, `Class diagram`, `Entity-relationship diagram`, `Frontend component tree`.
- Exactly one highlighted path per figure, using the `sk-accent` class. Everything else is `currentColor`.

## Writing

- Plain, short sentences. One idea per sentence, and no marketing language.
- Identifiers, paths, routes, env vars and model ids go in `code`.
- Numbers come from the code or config (`k = 4`, `1000 chars, 150 overlap`), never from rounding.
- The footer reads: `<slug> · design document · source of truth: docs/DESIGN.md in the repository.`

## Format-specific notes

**DESIGN.md**
- Headings are `## N. Title`.
- The header is an H1, then the eyebrow line in backticks, the lede in italics, and the meta grid as a 4-column table.
- The CoALA strip is a table `Stage | Key | Does | CoALA role`.
- A figure is `![Fig. N: Caption](figures/fig-NN-name.svg)` followed by `*Fig. N: Caption*`.
- The GitHub links go on one line under the meta table: `[View code](…) · [Fork](…/fork) · [Report an issue](…/issues/new) · [Contribute](…/blob/main/CONTRIBUTING.md)`.

**HTML** (`assets/template.html`)
- Copy the `<style>` block unchanged.
- The TOC `<ol>` has exactly 10 items whose anchors match the section ids `purpose, usecases, architecture, flows, backend, data, frontend, structure, run, next`.
- Each figure's canvas holds a `<!-- figure: fig-NN-name.svg -->` placeholder. `scripts/figures.py inline` replaces it with the SVG; the page CSS (`.sketch …`) themes it.
- The header has a `.links` row, and section 10 ends with a `.contribute` box. Delete both when there's no repo URL.

**MDX** (`assets/demo.template.mdx`)
- No numbers in `##` headings. The site numbers sections and figures with CSS counters, and builds the contents rail from the `##` headings.
- Use `<Figure caption="Type: text." src="/images/demos/<slug>/fig-NN-name.svg" />`, with the files copied to `public/images/demos/<slug>/`.
- Set `repoUrl` in the frontmatter. The site builds the Fork / Issues / Contribute links and the closing "Build on this demo" box from it.
- Use `<PipelineStrip>` containing `<Stage k="…" t="…">role</Stage>` ×5.
- Use `<PromptBlock text={`…`} />` for the system prompt.
- GFM tables and fenced code are supported. Keep `{`, `}` and `<` out of prose.
