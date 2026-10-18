# arch-doc

A Claude skill that writes **reference architectures as concept explainers**: *What is an agent harness?*, *What is AI Ops?*, *CoALA: how language agents remember, decide and act*. Each is taught the way a good textbook chapter would teach it, with two or three hand-drawn diagrams. Every one **credits the original sources** it draws on.

It's the sibling of [`demo-doc`](../demo-doc/):
- **demo-doc** documents one running demo: its repo, run steps and contributions.
- **arch-doc** explains an idea, never links a repository, and points to the demos that implement it.

On a site with both, each architecture shows **See it built** links to its demos, and each demo shows clickable **Follows** tags back to the architectures.

## The format

Seven short sections:

1. **In one picture**: the definition, Fig. 1 and "the key idea".
2. **Why it matters**: the problem, and the questions the concept makes easy to answer.
3. **The building blocks**: each part, with an everyday example.
4. **How it works**: a numbered walkthrough and Fig. 2, plus an optional worked example mapping a demo onto the concept (Fig. 3).
5. **Patterns & variations**
6. **Pitfalls**
7. **Go further**: See it built, what to read, what's next.

Then **Credits & sources**, which is mandatory. Every entry says what was taken, URLs are verified, and nothing is invented.

## Outputs

1. `ARCHITECTURE.md` + `figures/*.svg`
2. A standalone HTML page (indigo spec-sheet look)
3. An MDX post (`content/architectures/<slug>.mdx`) with `demos: [slug]`. The author's site refuses architectures without `sources`, and any that carry repo links.

## When to use it

- *"Reference architecture: agent harness."*
- *"Explain AI Ops as a reference architecture and link my eval demo."*
- *"What is CoALA? Write it up for the site."*

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | The workflow and the three hard rules (credit sources, no repos, a concept rather than a codebase) |
| `references/format.md` | The section-by-section contract |
| `references/credits.md` | How to credit sources |
| `references/diagrams.md` | Hand-drawn figure style; the three figure types |
| `references/palette.md`, `references/checklist.md` | Tokens and type; pre-handover checks |
| `assets/` | `ARCHITECTURE.template.md`, `template.html`, `architecture.template.mdx` |
| `scripts/figures.py` | Lints figures and inlines them into the HTML |
| `examples/coala-cognitive-architecture/` | The reference example in all formats, with 3 figures |

## Install

```bash
git clone https://github.com/nitingoswami-io/claude-skills.git
cp -r claude-skills/arch-doc ~/.claude/skills/arch-doc
```

In Claude Desktop, drag the folder into a chat and say *"Please install this as a skill."*, or run `./build.sh` and upload `dist/arch-doc.skill`.

## License

MIT. See [LICENSE](LICENSE).
