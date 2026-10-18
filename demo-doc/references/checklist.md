# Pre-handover checklist

Check every item. Fix any failure before you share the output.

## Structure
- [ ] Exactly 10 `##` sections, titled exactly as in `format.md` and in that order.
- [ ] Any section that doesn't apply says "Not applicable: <reason>." It isn't deleted.
- [ ] Key flows sub-headings are numbered `4.1`, `4.2`, …
- [ ] The header has an eyebrow, an H1 `<Name>: <verb phrase>`, a lede of up to 2 sentences, and a meta grid of Stack / Models / Date / Status.

## CoALA
- [ ] The pipeline strip has exactly 5 stages, each with a code key, a 2–4 word action and a CoALA role.
- [ ] The opening paragraph bolds the CoALA memories and actions it mentions.
- [ ] At least one figure caption or Next-steps row names a CoALA concept.

## Figures
- [ ] `artifact-diagramming` was loaded before drawing.
- [ ] `python3 -I scripts/figures.py check docs/figures` prints only `ok` lines.
- [ ] Each figure shows a mechanism, with every arrow labelled and one accent path.
- [ ] The captions and `aria-label`s state each figure's claim. Labels inside the drawings are 1–4 words.
- [ ] Figures are numbered 1…N across the whole document, and the file numbers match the caption numbers.

## GitHub
- [ ] The repo URL comes from `git remote` or the user, never from a guess.
- [ ] The header links (View code · Fork · Report an issue · Contribute) all point to that repo.
- [ ] Section 9 starts with `git clone <repo>.git`.
- [ ] Section 10 ends with the Contribute paragraph.
- [ ] `CONTRIBUTING.md` exists in the repo (created from the template if it was missing) and the README links to it.

## Credits
- [ ] Every tutorial, template, library example, paper or demo this one builds on is credited, with what was taken.
- [ ] Every URL was verified or left out, and nothing about a source is invented.
- [ ] `DESIGN.md` and the HTML end with Credits & sources. The MDX frontmatter has `sources`.

## Links
- [ ] `architectures:` lists the concept explainers this demo follows (checked in `content/architectures/`).
- [ ] The author's website repository is never linked.

## Facts
- [ ] Model ids, ports, env var names, routes and table names match the code exactly.
- [ ] The system prompt is quoted verbatim.
- [ ] The run commands were actually run, or the user is told they weren't.
- [ ] The check table includes a grounded success case and a refusal or error case.
- [ ] Every `TBD` is listed in the handover message.

## Outputs
- [ ] `docs/DESIGN.md` and `docs/figures/*.svg` are written in the demo repo.
- [ ] The HTML uses the template CSS unchanged, has 10 TOC entries whose anchors resolve, and has every figure inlined (no `<!-- figure:` placeholders left).
- [ ] The MDX frontmatter has `title, dek, date, tags, stack, models, docStatus, layout: spec`, plus any known URLs.
- [ ] The MDX prose has no bare `{`, `}` or `<`. The system prompt uses `PromptBlock text={`…`}`.
- [ ] The MDX `##` headings have no numbers. Each `<Figure>` has a `src` under `/images/demos/<slug>/`, and the files are copied there.
- [ ] The MDX frontmatter has `repoUrl`, so the site renders the Fork and Contribute links.
