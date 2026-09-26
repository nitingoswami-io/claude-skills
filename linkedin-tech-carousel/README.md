# linkedin-tech-carousel

A Claude skill that turns **one technical concept** into a 3-slide LinkedIn carousel — delivered as a swipeable PDF plus PNGs, sized exactly for the feed, with ready-to-paste post copy.

The skill is opinionated. It refuses to shrink a conference talk into three slides and insists on one mechanism per deck. That constraint — plus a fixed slide-1 / slide-2 / slide-3 contract — is the difference between a carousel someone swipes and one they scroll past.

## What you get

Every run produces:

- **`<name>.pdf`** — 3 pages at 1080×1350 (4:5) or 1080×1080 (1:1). Upload it as a LinkedIn *document post* and the platform renders it as a native swipeable carousel.
- **`<name>-1.png`, `-2.png`, `-3.png`** — the same slides as images. Use these for an image carousel, X/Twitter, or a Substack embed.
- **Post copy** — a hook line, 2–4 mechanism lines, an invitation, and 3–5 targeted hashtags. Plus posting instructions.

Both formats come out at exact feed dimensions, so LinkedIn never resizes your text.

## When to use it

Trigger the skill on anything technical you want to publish as slides:

- *"Turn this Spark shuffle explanation into 3 slides for LinkedIn."*
- *"Explain Kafka idempotence (acks=all + producer IDs) as a carousel."*
- *"Make a LinkedIn deck on consistent hashing vs modulo — 4:5."*

The skill's description matches on phrases like *carousel*, *deck*, *swipe post*, *slides*, *mini-tutorial*, *explainer*, or any technical topic paired with a request for something postable. You don't need to describe the format.

## The two-phase workflow

This skill is not prompt-only. It has two phases you should understand before running it:

**Phase 1 — Claude writes the content and a JSON spec.**
Claude picks one mechanism (narrowing broad topics silently), drafts titles/subtitles/labels/notes to strict word budgets, chooses a layout for each of the three slides (`flow`, `stack`, `compare`, `steps`, `bars`, `code`, `hub`, `stat`), and writes a `spec.json` file.

**Phase 2 — Claude runs the renderer and inspects the output.**
Claude invokes:
```bash
python3 scripts/render_deck.py spec.json --out-dir out --basename kafka-idempotence
```

Then — and this is not optional — Claude opens every rendered PNG with the `view` tool. matplotlib's auto-fit *shrinks* text rather than clipping it, so overflow shows up as a single slide with awkwardly tiny type. The only way to catch it is to look. If a slide looks cramped, Claude cuts words and re-renders.

You get the PDF + PNGs + post copy at the end.

## Setup

The renderer needs **Python 3.6+** and **matplotlib**. Everything else is standard library.

```bash
# From this folder (linkedin-tech-carousel/):
python3 -m pip install -r requirements.txt
```

Or, if you prefer an isolated environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

**Font fallback**: the renderer requests *Liberation Sans* / *Liberation Mono* by default. If those aren't installed, matplotlib silently substitutes system fonts (Helvetica/DejaVu on macOS, DejaVu on Linux). The output still looks good — don't panic if the fonts differ slightly from the spec.

Try the included example to confirm everything works:

```bash
python3 scripts/render_deck.py examples/spark-shuffle.json --out-dir out --basename spark-shuffle
```

You should get `out/spark-shuffle.pdf` plus three PNGs at 1080×1350.

## Install

This skill works in both **Claude Code** (the CLI) and **Claude Desktop** (the app). Pick the one you use. In both cases, install matplotlib first (see [Setup](#setup)).

### 1) Claude Code

Copy the skill folder into your local skills directory:

```bash
git clone https://github.com/<your-username>/claude-skills.git
cp -r claude-skills/linkedin-tech-carousel ~/.claude/skills/linkedin-tech-carousel
```

Restart Claude Code. It auto-discovers the skill — no separate enable step. Test with one of the trigger prompts under [When to use it](#when-to-use-it).

### 2) Claude Desktop

Two easy paths — Option A is the fastest.

**Option A — Ask Claude to install it for you.**

1. Open a new chat in Claude Desktop.
2. **Drag this whole `linkedin-tech-carousel/` folder into the chat** — or attach it with the paperclip / `+` button. Make sure you attach the folder itself, not just `SKILL.md` — this skill relies on files under `references/`, `scripts/`, and `examples/`, and pasting `SKILL.md` alone will drop them.
3. Say: *"Please install this as a skill."*

Claude will validate the frontmatter, show you a review card, and save it with one click.

**Option B — Upload the zip yourself.**

1. Build the `.skill` archive using this skill's own build script:
   ```bash
   git clone https://github.com/<your-username>/claude-skills.git
   cd claude-skills/linkedin-tech-carousel
   ./build.sh
   ```
   That produces `dist/linkedin-tech-carousel.skill` inside this folder.
2. In Claude Desktop, go to **Settings → Capabilities → Skills**, click **Upload skill**, and choose the file. (Menu names may vary slightly by app version.)
3. Wait ~1–2 minutes for the security scan.
4. When the skill turns green, toggle it on.
5. Test it in a new chat with one of the example prompts above.

If the skill doesn't fire, check that **Code execution and file creation** is enabled in Settings — the skill needs to run Python to render, and this capability is required. Updating a skill you already uploaded? Just upload the new `.skill` file in its place; it replaces the previous version.

## Adapt it to your work

**Your name in the footer.** Every slide has a small footer strip. Set it in the spec: `"footer": "Your Name · yoursite.com"`. Or leave it out and Claude will ask.

**Theme choice.** Three built-in themes — `midnight` (dark navy + cyan, default), `carbon` (near-black + violet), `paper` (off-white + blue, best for print or corporate). Pick one at the spec level; the palette is fixed on purpose so a series of decks looks like a series.

**Different aspect ratios.** `4:5` (default, 1080×1350 — claims more vertical space in the feed) or `1:1` (1080×1080 — for cross-posting to squares).

**Writing your own spec directly.** If you want to bypass Phase 1 entirely, write a spec JSON against the schema in [`references/layouts.md`](references/layouts.md) and just run the renderer. The schema is complete — every layout, every field, every constraint is documented there.

**More than 3 slides.** The renderer accepts any slide count and numbers the footer accordingly. Three remains the default because it's what fits a single scroll-stop on a phone; go longer only if the topic genuinely earns it.

## Why the discipline works

Two paragraphs on the shape, because it explains the constraints.

**One mechanism per deck.** Three slides is a brutal constraint. If you spend slide 1 on "what is Kafka", slide 2 on "topics and partitions", and slide 3 on "producers and consumers", you've written three definitions — which nobody swipes. The skill silently narrows broad requests ("explain Kafka") to a single mechanism with a payoff ("why `acks=all` alone doesn't stop duplicates"). That's the shape people finish, and it's the shape they follow you for.

**The 3-slide contract.** Each slide has exactly one job. Slide 1 is a hook — a diagnostic pain, a claim that sounds slightly wrong, a specific misconception. Slide 2 is the mechanism — real config keys, real phases, real numbers. Slide 3 is the payoff — what the reader does differently tomorrow morning, expressed as a knob or a threshold or a decision rule. Word budgets are keyed to how matplotlib's renderer wraps and shrinks type, so staying inside them is the difference between a slide that looks designed and one that looks cramped. Everything else in the skill — the layout variety rule, the highlight-one-thing rule, the visual-verification step — is downstream of these two commitments.

## Example

See [`examples/spark-shuffle.json`](examples/spark-shuffle.json) for a complete spec against a real technical topic (Spark shuffle mechanics). It demonstrates three different visual layouts across the deck (`compare` for the hook, `flow` for the mechanism, `stat` for the payoff), a diagnostic slide-1 hook, and a takeaway strip on slide 3.

The schema itself lives in [`references/layouts.md`](references/layouts.md) — every layout type, every field, every constraint.

## Attribution

This skill is adapted from an internal one used to produce technical LinkedIn carousels. It's now MIT-licensed and open for anyone to use, adapt, or extend.
