# arch-doc format specification (concept explainer)

## Header

| Part | Rule | Example |
|---|---|---|
| Eyebrow | `REFERENCE ARCHITECTURE · <slug> · <date>` | `REFERENCE ARCHITECTURE · coala-cognitive-architecture · 17 Oct 2026` |
| Title (H1) | `<Concept>: <what it lets you understand or do>`, or `What is <concept>?` | `CoALA: how language agents remember, decide and act` |
| Lede | 1–2 sentences: the definition, plus "explained with N diagrams and …" | — |
| Meta grid | **Domain** · **Level** (pill: Beginner / Intermediate / Advanced) · **Key concepts** (` · `-separated) · **Related demos** (links, or "None yet") | — |
| Links | **None.** No repo, fork, clone or live-demo links. **Never the author's website repository** | — |

## Sections (fixed order, always 7, then Credits)

1. `In one picture`
2. `Why it matters`
3. `The building blocks`
4. `How it works`
5. `Patterns & variations`
6. `Pitfalls`
7. `Go further`

Then **`Credits & sources`**, unnumbered and always last. On the site it's rendered from the frontmatter, so don't write it in the MDX body.

### 1. In one picture
- The definition in 1–2 sentences, with inline attribution of who named or described it: "(Sumers et al., 2023)".
- Fig. 1, the concept at a glance.
- `<SideNote title="The key idea">`: one or two sentences the reader should remember.

### 2. Why it matters
- One paragraph on the problem: the confusion or failure that exists without this concept.
- 2–3 bold questions the concept makes easy to answer.

### 3. The building blocks
- Each part with a one-line definition and an everyday example. Tables work well (`Part | Holds or does | Everyday example`).
- Bold each term the first time it appears.

### 4. How it works
- A numbered walkthrough, 4–7 steps, each starting with a **bold verb**.
- Fig. 2, the cycle or flow.
- Optional `### A worked example: <demo name>`: one paragraph and Fig. 3, mapping a demo on the site onto the concept and pointing out what that demo leaves out.

### 5. Patterns & variations
- Table `Pattern | What changes | When to use it`, 3–6 rows. Named patterns credit their source inline: "ReAct (Yao et al., 2022)".

### 6. Pitfalls
- Table `Pitfall | What you'll notice | Remedy`, 3–6 rows. "What you'll notice" is an observable symptom.

### 7. Go further
- **See it built:** links to the demos on the site (`/demos/<slug>`), or "None yet", plus the demo you'd build.
- **Read:** the primary source.
- **Next:** related explainers, published or planned.

## Figures
- **2 or 3** hand-drawn SVGs (`references/diagrams.md`, indigo palette), numbered 1…N.
- Captions use the form `<Type>: <one line>.`, adding "adapted from <source>" when the figure adapts someone's work.
- Use generic labels ("vector store", "tool router"), never one project's file names, except in the worked-example figure.

## Writing
- Write for a smart newcomer. Define each term on first use, and use one idea per sentence.
- Don't write code beyond a tiny illustrative snippet.
- The architecture explains the idea; the linked demos prove it.

## Format-specific notes

**ARCHITECTURE.md**
- Headings are `## N. Title`, and the last section is `## Credits & sources`.
- The meta grid is a 4-column table (Domain | Level | Key concepts | Related demos).
- Figures are `![Fig. N: Caption](figures/fig-NN-name.svg)` followed by `*Fig. N: Caption*`.

**HTML** (`assets/template.html`)
- The TOC has 7 numbered items plus "Credits & sources".
- Section ids are `picture, why, blocks, how, patterns, pitfalls, further, credits`.

**MDX** (`assets/architecture.template.mdx`)
- No numbers in the `##` headings and no Credits heading.
- Use `<Figure caption="…" src="/images/architectures/<slug>/fig-NN-name.svg" />` and `<SideNote title="The key idea">…</SideNote>`.
- Frontmatter has `demos: [slug]` for See it built. Demos get the Follows tags automatically.
