---
name: arch-doc
description: >-
  Write a reference architecture as a conceptual explainer in one fixed house
  format, the sibling of demo-doc. It explains an idea such as "what is an
  agent harness", "what is AI Ops" or "what is CoALA", tutorial-style:
  seven short sections (In one picture, Why it matters, The building blocks,
  How it works, Patterns & variations, Pitfalls, Go further), two or three
  hand-drawn SVG diagrams, links to demos that implement the idea, and a
  mandatory Credits & sources list that gives credit to every paper, pattern
  or project it draws on. It is not a write-up of a codebase and never links
  a repository. Produces ARCHITECTURE.md + figures, a standalone HTML page
  and an MDX post for the author's website. Use this skill whenever the user
  asks for a reference architecture, a concept explainer, "what is X" for a
  system or engineering concept, or "explain the architecture of X", even
  when the request is short, like "reference architecture: agent harness".
---

# arch-doc: reference architectures as concept explainers, always credited

A reference architecture on this site is a **concept**, explained the way a good textbook chapter would: what the thing is, why it exists, its parts, how they work together, the common variations, and how it goes wrong. It's taught with **two or three hand-drawn diagrams** and plain prose.

It is **not** documentation of a codebase. That's `demo-doc`'s job. The two link to each other:
- an architecture lists the demos that implement it (`demos: [slug]`), shown as **See it built**;
- each demo shows clickable **Follows** tags pointing back to the architectures it implements.

Examples of good topics:
- *What is an agent harness?*
- *What is AI Ops?*
- *CoALA: how language agents remember, decide and act*
- *Retrieval-augmented generation*
- *Evaluation loops for LLM apps*

The reference example is `examples/coala-cognitive-architecture/`.

---

## Hard rules

1. **Give credit to the original source.** Every explainer ends with Credits & sources, and every idea taken from a paper, vendor pattern, talk or project is credited, with what was taken. Read `references/credits.md`. Never invent authors, years or URLs.
2. **No repositories.** An architecture never carries `repoUrl`, `demoUrl`, Fork or Clone links. **Never link the author's website repository anywhere.** It is private to the author, and the site's build rejects it.
3. **Conceptual, not specific.** Use generic names ("vector store", "tool router"), not one project's file names. Specific systems appear only as examples or linked demos.

## Step 1: Frame the concept

- **One-sentence definition.** If you can't write it, the scope is too wide; narrow it.
- **The reader's question.** What would someone type into a search box to land here? Answer it in the first paragraph.
- **Sources.** The paper that named the idea, the vendor docs that popularised it, and talks or books. Use only URLs opened in this session or given by the user.
- **Related demos.** Check whether the author has a demo that implements the idea: look in `content/demos/` of the site repo. List the slugs. If there are none, say "None yet" and suggest one in Go further.

## Step 2: Write the seven sections, in order

Use the exact headings. See `references/format.md`.

| # | Section | Must contain |
|---|---|---|
| 1 | In one picture | A one- or two-sentence definition, with the source credited inline; **Fig. 1**, the concept at a glance; a `SideNote` titled "The key idea" |
| 2 | Why it matters | The problem the concept solves, then the 2–3 questions it makes easy to answer |
| 3 | The building blocks | Each part in plain words, as tables or short paragraphs, each with an everyday example |
| 4 | How it works | A numbered walkthrough of one cycle or request; **Fig. 2**. Optional `### A worked example` mapping a real demo onto the concept (**Fig. 3**) |
| 5 | Patterns & variations | Pattern / What changes / When to use it table, crediting named patterns inline |
| 6 | Pitfalls | Pitfall / What you'll notice / Remedy table |
| 7 | Go further | **See it built** (links to demos on the site), the paper to read, and related explainers |
| — | Credits & sources | Rendered from frontmatter on the site; written out in `ARCHITECTURE.md` and the HTML |

Voice: a patient senior engineer teaching a smart newcomer. Use short sentences, define every term the first time it appears, and include no code beyond a tiny illustrative snippet.

## Step 3: Draw two or three diagrams by hand

**Load the `artifact-diagramming` skill first**, then follow `references/diagrams.md`. Use hand-drawn SVGs in the indigo palette, with one highlighted path per figure:
1. **At a glance**: the concept's parts and how they connect. This is required.
2. **How it works**: the cycle or flow. This is required.
3. **Worked example**: a real demo mapped onto the concept. This is optional, but strongly preferred when a demo exists.

When a figure adapts a source's diagram, redraw it and caption it "adapted from …". Run `python3 -I scripts/figures.py check figures`.

## Step 4: Produce the outputs

1. **`ARCHITECTURE.md` + `figures/`**, from `assets/ARCHITECTURE.template.md`, saved in the user's architecture notes folder, or handed over as files.
2. **Standalone HTML**, from `assets/template.html`. Inline the figures with `python3 -I scripts/figures.py inline <page>.html figures`, then publish as an Artifact when available.
3. **Website post**, from `assets/architecture.template.mdx`:
   - Save it as `content/architectures/<slug>.mdx` in the author's site repo when it's on disk.
   - Copy the figures to `public/images/architectures/<slug>/`.
   - Frontmatter: `title, dek, date, tags, domain, level, concepts, demos, layout: spec, sources`. Never `repoUrl` or `demoUrl`.
   - If a listed demo should show the Follows tag, no edit to the demo is needed: the site works it out from `demos`.

## Step 5: Check before handing over

Go through `references/checklist.md`. The checks that fail most often:
- **No repo links**, and especially not the author's website repo.
- **Credits:** every idea taken from a source is credited, every URL verified, nothing invented.
- **The 7 headings exactly**, with 2–3 figures and every arrow labelled.
- **A concept, not a codebase**: generic component names, with specific systems only as examples or demos.

Finish with three short lines:
- where the outputs went;
- `TBD`s, including unverified sources;
- which demos were linked, or "none yet" plus a suggested demo.
