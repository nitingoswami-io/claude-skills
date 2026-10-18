# Pre-handover checklist

## Blocking
- [ ] **No repository links**: no `repoUrl`, `demoUrl`, fork or clone links. **The author's website repository appears nowhere.**
- [ ] **Credits:** at least one source. Every idea taken from a source is credited with what was taken, plus inline attribution where it's used.
- [ ] Every URL was opened in this session or given by the user. Nothing about a source is invented.
- [ ] Every figure that adapts a source says "adapted from …" and is redrawn, not pasted.

## Structure
- [ ] Exactly 7 sections, in order: In one picture · Why it matters · The building blocks · How it works · Patterns & variations · Pitfalls · Go further. Then Credits & sources.
- [ ] The header has an eyebrow, an H1, a lede, and a meta grid of Domain / Level / Key concepts / Related demos.
- [ ] "In one picture" has a definition, Fig. 1 and a "The key idea" SideNote.

## Teaching quality
- [ ] It's a concept, not a codebase: generic component names, with specific systems only as examples or linked demos.
- [ ] Every term is defined on first use, and each building block has an everyday example.
- [ ] "How it works" is a numbered walkthrough with bold verbs.
- [ ] Each pattern says when to use it, and each pitfall names an observable symptom.

## Figures
- [ ] `artifact-diagramming` was loaded before drawing.
- [ ] 2–3 figures; `python3 -I scripts/figures.py check figures` prints only `ok`.
- [ ] One accent path per figure, every arrow labelled, no line crossing a shape.

## Links to demos
- [ ] `demos:` lists the slugs of existing demos on the site (checked in `content/demos/`), or "None yet" is stated in Go further with a suggested demo.

## Outputs
- [ ] `ARCHITECTURE.md` + `figures/` exist, ending with Credits & sources.
- [ ] The HTML has every figure inlined and Credits filled in.
- [ ] The MDX frontmatter has `title, dek, date, tags, domain, level, concepts, demos, layout: spec, sources`.
- [ ] Figures are copied to `public/images/architectures/<slug>/`.
