# market-teardown

A Claude skill that turns your research on a market, product, or startup idea into a **data-dense, verdict-driven teardown** — around 1,500 words, argued from figures you can actually cite, with a bold conclusion at the end and a dated reference list. Ships alongside a companion short post that drives readers to the teardown without spoiling the verdict.

The skill is opinionated about *how* to write the piece — that's the point. It enforces a seven-step discipline (verdict-first, source-traceable, one currency per comparison, verdict withheld from the teaser) that separates a competent analytical writeup from another market-map think-piece.

## What you get

Two files per topic:

1. **The teardown** (~1,500 words). Six sections in a fixed order: title, narrative opening, four analytical sections, verdict, "what I'd validate next," references.
2. **A companion feed post** (400–800 characters). A short piece that names the collision, states what's withheld, and links to the teardown. Never states the verdict.

Both are plain Markdown, formatted for LinkedIn articles, Substack, Medium, or a personal blog.

## When to use it

Trigger this skill when you want to publish an analytical take on something you've already researched:

- *"Turn my notes on vertical SaaS in construction procurement into a teardown."*
- *"Write up the on-device inference economics research as an article."*
- *"Teardown of the consumer subscription unbundling thesis, 1,500 words."*

You don't need to describe the format — the skill's description matches on phrases like *teardown*, *idea breakdown*, *market analysis writeup*, *newsletter edition*, *write this research up*. As soon as it fires, it will read your project files and any relevant prior chats to find the numbers before drafting.

## Install

### Claude Code

```bash
git clone https://github.com/<your-username>/claude-skills.git
cp -r claude-skills/market-teardown ~/.claude/skills/market-teardown
```

Restart Claude Code and it will pick up the skill automatically.

### Claude Desktop

From the repo root:

```bash
./scripts/build-skill.sh market-teardown
```

That produces `dist/market-teardown.skill`. In Claude Desktop, go to **Settings → Capabilities → Skills → Add skill** (or the equivalent for your app version) and select the built file.

## Adapt it to your work

The skill is written to work out of the box, but two things are worth tuning to your setup:

**Where your research lives.** Step 1 tells Claude to read project files and prior chats before drafting. If you keep your research in a specific place — a Claude Project, an Obsidian vault mounted via MCP, a folder of PDFs — mention it in your prompt (*"my research on this is in the project files"*) and Claude will look there.

**Which publishing platform you target.** Step 5 (formatting) is written for the LinkedIn / Substack / Medium subset of Markdown: no tables, H2 subheads only, 3–4 sentence paragraphs. If you're publishing somewhere that renders more (a personal blog with full Markdown, Notion, etc.), you can loosen these rules in your prompt.

**Currency and locale conventions.** The example teardown uses USD/INR figures from an India-focused analysis. The skill's underlying rules — one currency per comparison, date every figure, don't convert historical fundraises in headlines — apply to any market.

## Why the discipline works

Two paragraphs on the shape, because it explains the constraints.

**Verdict-first, not verdict-last.** Most analytical writing is a survey that ends with "so what?". This skill flips it: decide the verdict before writing the opening, then let every section lay track toward it. This does two things at once. It kills the writer's temptation to hedge (there is nothing to hedge into — the conclusion is already fixed), and it lets the reader half-know where they're heading by section three, which is the difference between "I skimmed it" and "I finished it."

**The payer question is the sharpest lens.** Somewhere in the middle of every teardown is the section titled "The economics, and who actually pays." That question — *who pays, and from when?* — is the fastest way to falsify a plausible market. A category can have real demand, obvious utility, and a clear TAM, and still not have anyone whose budget line the money comes out of. When the payer is ambiguous, the model is broken. When the payer is clear, everything else is scoping.

Everything else in the skill — the source-traceability rule, the "one bulleted run per section" limit, the ban on rhetorical question stacks, the specific way the feed post withholds — is downstream of these two commitments.

## Example

See [`references/example-teardown.md`](references/example-teardown.md) for a full worked teardown against a real (public) market: mid-term furnished rentals in India. It runs ~1,450 words, carries around 30 dated figures and 15 references, and ends on a bold "Conditional go" with four numbered conditions.

## Attribution

This skill is adapted from an internal one used to produce a weekly analytical newsletter. It's now MIT-licensed and open for anyone to use, adapt, or extend.
