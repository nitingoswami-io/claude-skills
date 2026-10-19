# demo-doc

A Claude skill that writes the **design document for a software demo** in one fixed house format, so every demo you publish looks and reads the same.

**Status:** a learning template, shared as-is under MIT. Read it, run it, adapt it. No API keys or environment variables needed.

You get a technical spec sheet with:
- a numbered contents rail and a header meta grid (Stack, Models, Date, Status);
- a **CoALA pipeline strip** that maps the demo onto the Cognitive Architectures for Language Agents framework;
- ten numbered sections, from purpose to next steps;
- numbered **hand-drawn SVG figures** (wobbly lines, handwriting labels, one highlighted path) that follow light and dark mode;
- **View code · Fork · Report an issue · Contribute** links, so readers can build on the demo;
- a **Credits & sources** list that credits the tutorials, templates, papers and projects the demo builds on.

## What you get

The same content in every format:

1. **`docs/DESIGN.md` + `docs/figures/*.svg`** in the demo repo. This is the source of truth, and GitHub renders the figures inline.
2. **`CONTRIBUTING.md`** in the demo repo, if it doesn't have one yet: the fork → branch → PR workflow, tied to the design doc's *Next steps*.
3. **A standalone HTML page** with the spec-sheet styling: teal accent, Source Serif 4 and IBM Plex. You can publish it as a Claude artifact or open it locally.
4. **An MDX post** for a Next.js site that has the matching components (`PipelineStrip`, `Stage`, `Figure`, `PromptBlock`). This is how demos are published at the author's site.

The ten sections, always in this order:

1. Purpose & scope
2. Use cases
3. Architecture
4. Key flows
5. Backend design
6. Data model
7. Frontend design
8. Project layout
9. Run & verify
10. Next steps

The full contract is in [`references/format.md`](references/format.md). How to draw the figures is in [`references/diagrams.md`](references/diagrams.md); it builds on the `artifact-diagramming` skill, and `scripts/figures.py` lints the figures and inlines them into the HTML. The palette and type are in [`references/palette.md`](references/palette.md), and the pre-handover checks are in [`references/checklist.md`](references/checklist.md). [`examples/rag-demo/`](examples/rag-demo/) is the reference document in all three formats, with its nine figures.

## When to use it

- *"Document this demo."*
- *"Write the design doc for the RAG app and publish it."*
- *"Build a demo of agentic RAG with episodic memory."* The skill writes the design doc first as a draft, then updates it as the build progresses.

## Install

### Claude Code

```bash
git clone https://github.com/nitingoswami-io/claude-skills.git
cp -r claude-skills/demo-doc ~/.claude/skills/demo-doc
```

Restart Claude Code. The skill fires on prompts like the ones above.

### Claude Desktop

Either:
- drag the whole `demo-doc/` folder into a chat and say *"Please install this as a skill."*, or
- run `./build.sh` and upload `dist/demo-doc.skill` under **Settings → Capabilities → Skills**.

## Adapt it

- **Your own palette:** change the token values in `assets/template.html` and `references/palette.md` together. Keep the token names.
- **Your own site:** the MDX output expects the four components above. If your site has none, ask for the HTML or Markdown output only.
- **Figures in another style:** change the skeleton in `references/diagrams.md`. Drop the `rough` filter for clean lines, or swap the Kalam font. Keep `currentColor` and the `sk-*` classes so theming still works.
- **No CoALA:** the strip is a 5-stage data-flow map. You can relabel the role line, but keep exactly five stages so the layout holds.

## Known limits

- It documents what the code does; it can't verify claims the code doesn't show. Unknowns are marked TBD.
- The figure check catches long labels, not layout mistakes. Look at the rendered figures.
- The website MDX targets the author's site components; elsewhere, use DESIGN.md or the HTML page.

## Contributing

Issues and pull requests are welcome: fork the repo, branch, run `python3 scripts/check_skills.py` from the repo root, and open a PR. See [CONTRIBUTING.md](../CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
