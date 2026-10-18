---
name: demo-doc
description: >-
  Write the design document for a software demo in one fixed house format:
  a technical spec sheet with a numbered contents rail, a header meta grid,
  GitHub view/fork/contribute links, a CoALA pipeline strip, ten numbered
  sections (purpose, use cases, architecture, flows, backend, data model,
  frontend, layout, run & verify, next steps) and numbered hand-drawn SVG
  figures. Produces from one source: docs/DESIGN.md plus docs/figures/ and a
  CONTRIBUTING.md in the demo repo, a styled standalone HTML page, and an
  MDX post for the author's website. Use this skill whenever the user asks
  to document, write up, explain, publish or "make a design doc" for a demo,
  prototype, sample app, proof of concept or learning project — and also
  when they ask Claude to build a new demo, so the design doc is written in
  this format from the start. Trigger on short asks like "document this
  demo", "design doc for the RAG app", "write up what we built", "publish
  this demo", or "build a demo of X".
---

# demo-doc: design documents for demos, one house format

Every demo gets the same document: same headings in the same order, same layout, same palette, same hand-drawn figures. Readers learn the format once and can then skim any demo. The approved reference is the **RAG Demo** (`examples/rag-demo/`).

The format has three jobs:
- show **how the demo works**: architecture, flows and contracts;
- show **how to prove it works**: run steps and a check table;
- make it easy to **build on**: clone, fork and contribute links to the GitHub repo.

Every demo is also mapped to the **CoALA** agent framework (working, semantic, episodic and procedural memory; retrieval, reasoning, learning and external actions). That mapping is what makes a set of demos read as one body of work.

---

**Never link the author's website repository** in any output. Demos link their *own* repo only.

## Step 1: Gather facts from the code. Don't invent them.

If the demo exists, read it before writing anything:

- **GitHub repo URL**:
  - Run `git remote get-url origin` and convert `git@github.com:owner/repo.git` to `https://github.com/owner/repo`.
  - If there's no GitHub remote, **ask the user** for the URL, or whether they want you to create one. Creating a public repo is a public action: get an explicit yes before running `gh repo create`.
  - Until a URL exists, write `TBD` and leave the GitHub links out. Never guess a URL.
- **Stack and models**: package files, `requirements.txt`, `.env.example`, config modules. Use exact model ids.
- **Entry points and routes**: HTTP routes, CLI commands, UI pages.
- **Modules**: one line on each module's responsibility.
- **Data model**: tables, collections, vector dimensions.
- **Prompts**: the system prompt, verbatim.
- **Run steps**: README, docker-compose, scripts. Run them if you can and record what actually happens.
- **Folder tree**: `tree -L 3 -I node_modules` or similar.
- **License and CONTRIBUTING.md**: note whether they exist.
- **Architectures it follows**: check `content/architectures/` in the site repo for concept explainers this demo implements (e.g. `coala-cognitive-architecture` for an agent with memory). List their slugs in the MDX frontmatter as `architectures: [slug]`. The site shows them as clickable **Follows** tags. An architecture that lists this demo in its own `demos:` is linked automatically.
- **Sources to credit**: tutorials, starter templates, library examples, papers or other demos this one builds on. Read `references/credits.md`. Every source states what was taken, and URLs are verified or left out (never invented).

If you are **building** the demo in the same session, write the doc first, with `docStatus: draft`, as the design you get approved. Update it to `approved` or `built` as the work progresses.

If a fact is unknown, write `TBD` and list it for the user at the end. A wrong port, model, URL or table name is worse than a gap.

## Step 2: Fill the ten sections, in order

Read `references/format.md` for the exact rules. In short:

| # | Section | Must contain |
|---|---|---|
| 1 | Purpose & scope | Purpose paragraph, the **CoALA pipeline strip** (exactly 5 stages), In scope bullets, an Out of scope paragraph |
| 2 | Use cases | Use-case figure, ID / Use case / Behaviour table |
| 3 | Architecture | Overview paragraph, component figure, deployment figure |
| 4 | Key flows | `4.1`, `4.2`… sequence figures; a state figure where the UI has states |
| 5 | Backend design | Class figure, File / Responsibility table, **System prompt** verbatim, **API contract** table, error codes |
| 6 | Data model | Who creates the schema, ER figure |
| 7 | Frontend design | Component-tree figure, 2–4 bullets |
| 8 | Project layout | Annotated folder tree |
| 9 | Run & verify | Commands **starting with `git clone <repo>`**, then a Check / Expected table with at least one grounded success case and one refusal or error case |
| 10 | Next steps | Idea / What it teaches table, then a **Contribute** paragraph: fork, pick an idea, open a PR (links to fork, issues, CONTRIBUTING.md) |
| — | **Credits & sources** | Numbered list: authors, linked title, year, and what was taken (unnumbered, always last). Inline attribution where the idea is used |

A section that doesn't apply stays in place with one line: "Not applicable: <reason>." That keeps the numbering identical across all demos.

## Step 3: Draw the figures by hand

**Load the `artifact-diagramming` skill first.** Then follow `references/diagrams.md`:
- Every figure is a hand-authored SVG at `docs/figures/fig-NN-short-name.svg`, drawn on the house skeleton: a rough-line filter, handwriting labels, `currentColor`, and one accent path.
- Draw the mechanism, label every arrow, and make one claim per figure. The caption and the `aria-label` state that claim.
- Start from the matching drawing in `examples/rag-demo/figures/`. Don't start from a blank canvas.
- Run `python3 -I scripts/figures.py check docs/figures` and fix every `FIX` line.

Figures are numbered 1…N across the whole document, never restarting per section.

## Step 4: Produce the outputs

All outputs carry the same content. Write `DESIGN.md` first, then derive the rest.

1. **`docs/DESIGN.md` + `docs/figures/`** in the demo repo, from `assets/DESIGN.template.md`. This is the source of truth; GitHub renders the SVG figures inline.
2. **`CONTRIBUTING.md`** at the repo root, from `assets/CONTRIBUTING.template.md`, if the repo doesn't have one. Link it from the README. If the repo has no LICENSE, ask the user which one they want; don't pick one for them.
3. **Standalone HTML**, from `assets/template.html`:
   - Keep the CSS exactly as it is.
   - Put `<!-- figure: fig-NN-name.svg -->` placeholders inside each figure.
   - Run `python3 -I scripts/figures.py inline <page>.html docs/figures`.
   - Publish it as an Artifact when that tool is available, or save it as `docs/design.html`.
4. **Website post**, from `assets/demo.template.mdx`:
   - Save it as `content/demos/<slug>.mdx` in the author's local site checkout when it's on disk.
   - Copy the figures to `public/images/demos/<slug>/`.
   - Otherwise, hand the files to the user.
   - The frontmatter must validate: `title, dek, date, tags, stack, models, docStatus, layout: spec, sources` (the site renders Credits from `sources`), plus `repoUrl` (the site derives the Fork / Issues / Contribute links from it) and `demoUrl`, `designDocUrl` and `artifactUrl` when known. `demoUrl` is the hosted live demo: the site turns it into a "Try it live" button on the page and the front-page card, and shows a "Live demo: coming soon" placeholder when it is missing. When a live demo exists, also say so at the top of **Run & verify** ("No install needed to try it: …") and near the top of the demo repo's README.

Conversion rules between formats (details in `references/format.md`):

| Element | DESIGN.md | HTML | MDX |
|---|---|---|---|
| Section heading | `## 1. Purpose & scope` | `<h2><span class="num">1</span>Purpose &amp; scope</h2>` | `## Purpose & scope` (the site numbers headings) |
| Figure | `![Fig. N: caption](figures/fig-NN-x.svg)` + `*Fig. N: caption*` | `<figure class="uml">` + `<!-- figure: fig-NN-x.svg -->` + `<figcaption><b>Fig. N</b> …` | `<Figure caption="…" src="/images/demos/<slug>/fig-NN-x.svg" />` (the site numbers figures) |
| GitHub links | line under the meta table | `.links` row in the header + `.contribute` box in section 10 | from `repoUrl`, automatic |
| CoALA strip | 5-row table: Stage / Key / Does / CoALA role | `.pipeline` with 5 `.stage` divs | `<PipelineStrip>` with 5 `<Stage k="…" t="…">role</Stage>` |
| System prompt | fenced `text` block | `<blockquote class="prompt">` | `<PromptBlock text={`…`} />`, which keeps `{placeholders}` safe |

MDX escaping: outside code, `{`, `}` and `<` are JSX. Keep braces inside backticks, fenced blocks or `PromptBlock text`.

## Step 5: Check before handing over

Go through `references/checklist.md`. The checks that fail most often:
- The section count isn't exactly 10, or the order changed.
- `figures.py check` reports a `FIX`: a missing `aria-label`, a literal colour, a long label, or a numbering gap.
- The repo URL is guessed, or the clone command and the GitHub links point to different repos.
- Credits are missing or vague, or a source URL wasn't verified.
- The CoALA strip doesn't have exactly 5 stages.
- The run commands weren't actually run, or ports and env var names don't match the code.

Finish with three short lines:
- where each output was written, or the Artifact link;
- the list of `TBD`s, including the repo URL if it's missing and any unverified source;
- the one thing you couldn't verify.
