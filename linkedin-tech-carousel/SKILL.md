---
name: linkedin-tech-carousel
description: Turn one purely technical topic into a 3-slide LinkedIn carousel with a real infographic on every slide, delivered as a swipeable PDF plus PNGs and ready-to-paste post copy. Use this whenever someone wants slides, a carousel, a deck, a "swipe post", a document post, a mini-tutorial, or an explainer to share on LinkedIn about an engineering subject — distributed systems, databases, data pipelines, cloud architecture, ML/AI internals, networking, security, algorithms, language internals, or DevOps. Also use it when they say things like "make this into slides for LinkedIn", "explain X in 3 slides", "turn this concept into a carousel", or paste a technical explanation and ask for something postable, even if they never say the word "carousel".
---

# LinkedIn technical carousel

Three slides is a brutal constraint, and that is the point. A LinkedIn reader gives slide 1
about two seconds. If it earns a swipe, they will read slide 2 properly. Slide 3 is what they
remember and what makes them follow. Everything below exists to protect that arc.

Do not hand the reader a shrunk-down conference talk. Pick **one** mechanism and explain it
until it clicks.

## Output

`scripts/render_deck.py` takes a JSON spec and produces:

- **`<name>.pdf`** — 3 pages. This is the primary deliverable: LinkedIn renders a PDF as a
  native swipeable document post, no third-party tool needed.
- **`<name>-1.png`, `-2.png`, `-3.png`** — same slides as images, for an image carousel,
  X/Twitter, or a Substack embed.

Both come out at exact feed dimensions (1080×1350 for 4:5, 1080×1080 for 1:1), so text is
never resized by LinkedIn.

## Workflow

1. **Narrow the topic.** If the request is broad ("explain Kafka"), silently narrow it to one
   mechanism with a payoff ("why acks=all alone doesn't stop duplicates") and say which slice
   you picked. Broad topics produce three slides of definitions, which nobody swipes.
2. **Write the content first, as plain text**, following the slide contract and word budgets
   below. Getting the words right is the whole job; the renderer is just typesetting.
3. **Choose a layout per slide** from the table below. Read `references/layouts.md` for the
   exact JSON fields of the layouts you picked.
4. **Write the spec JSON** and render:
   ```bash
   python3 scripts/render_deck.py spec.json --out-dir out --basename kafka-idempotence
   ```
5. **Look at every PNG with the `view` tool.** This is not optional. Auto-fit shrinks text
   rather than clipping it, so overflow shows up as one slide with awkwardly tiny type — you
   will only catch it by looking. Fix by cutting words, not by fighting the renderer.
6. **Deliver** with `present_files` (PDF first, then PNGs) and include the post copy.

## The 3-slide contract

Each slide has exactly one job. Do not let them blur together.

**Slide 1 — the hook.** Name a specific, recognisable pain or a claim that sounds slightly
wrong. State the mechanism-level reason it happens. Never open with a definition, never open
with "In today's data-driven world". The strongest hooks are diagnostic: *"Your Spark job
isn't slow. It's shuffling."* Good visuals here: `compare` (the wrong vs right mental model),
`code` (the innocent-looking line), `flow` (where it breaks).

**Slide 2 — the mechanism.** This slide carries the teaching. Show the thing happening step
by step, at the level of detail a working engineer would actually need. This is where you earn
credibility: name the real config keys, the real phases, the real numbers. Good visuals:
`flow`, `stack`, `steps`, `bars`.

**Slide 3 — the payoff.** What the reader does differently tomorrow morning. Concrete
knobs, thresholds, or a decision rule — not "it depends" and not a summary of slides 1–2.
Add a `takeaway` strip with the one sentence you want quoted back to you. Good visuals:
`stat`, `steps`, `hub`, `compare`.

## Word budgets

These are measured against the renderer. Staying inside them is the difference between a
slide that looks designed and one that looks cramped.

| Field | Budget |
|---|---|
| `kicker` | ≤ 5 words. Topic + position, e.g. `Spark internals · 2 of 3` |
| `title` | ≤ 12 words. Prefer a full sentence with a verb over a noun phrase |
| `subtitle` | ≤ 25 words, and only when slide 1 needs setup. Usually omit on 2 and 3 |
| `takeaway` | ≤ 22 words, one sentence, opinionated |
| node / layer / step `label` | ≤ 5 words |
| `note` on those | ≤ 12 words |
| `compare` items | 3–4 per side, ≤ 8 words each |
| `code` lines | ≤ 10 lines, ≤ 48 characters per line |
| `bars` / `steps` / `stat` items | 3–5, 3, and 2–3 respectively |

Total words across all three slides should land around 120–160. If you are over, you are
explaining two topics.

## Choosing a layout

| Layout | Use it for |
|---|---|
| `flow` | A sequence where each stage feeds the next — request lifecycle, shuffle phases, commit path |
| `stack` | Layers of a system — protocol stack, storage engine tiers, an architecture diagram |
| `compare` | Two mental models, before/after, or the naive vs correct approach |
| `steps` | An ordered procedure the reader will follow — migration, tuning, debugging |
| `bars` | Numbers that make the point — latency, throughput, cost per setting |
| `code` | The one config or snippet that matters, with the key lines highlighted |
| `hub` | One central mechanism and what it buys you — good for slide 3 |
| `stat` | 2–3 headline numbers or knobs with a line of context each |

Vary them across the three slides. Three `flow` slides in a row is monotonous, and it usually
means the topic was never narrowed.

Set `highlight: true` on exactly the one node, layer, bar, or code line the reader should look
at first. Highlighting everything highlights nothing.

## Spec shape

```json
{
  "theme": "midnight",
  "aspect": "4:5",
  "footer": "Your Name · yoursite.com",
  "slides": [
    {
      "kicker": "Spark internals · 1 of 3",
      "title": "Your Spark job isn't slow. It's shuffling.",
      "subtitle": "A wide transformation writes every partition to disk first.",
      "visual": { "type": "compare", "left": {}, "right": {} },
      "takeaway": "Optional. Strongest on slide 3."
    }
  ]
}
```

- `theme`: `midnight` (dark navy + cyan, the default and best-performing in feed), `carbon`
  (near-black + violet), `paper` (off-white + blue, for slides that will also be printed
  or embedded in a light-background doc).
- `aspect`: `4:5` claims more vertical space in the feed and is the default. Use `1:1` only
  when asked or when the deck will be cross-posted somewhere square.
- `footer`: ask for a name/handle if it isn't obvious from context, or leave it out.

Full field reference for every layout: `references/layouts.md`.

## Post copy

Ship the caption with the deck — a carousel with no hook text underperforms. Use this shape:

```
[One-line version of the slide 1 hook, as a statement.]

[2–4 short lines expanding the mechanism. Line breaks, not paragraphs —
LinkedIn truncates after ~3 lines, so the first line does the work.]

[One question that invites a real reply, e.g. "What's the worst shuffle
you've inherited?"]

#hashtags — 3 to 5, specific ones (#ApacheSpark #DataEngineering) over
generic ones (#tech #coding)
```

Also tell them how to post it: **Start a post → Add a document → upload the PDF → give it a
title** (the title becomes the swipe-card label, so make it the hook, not "deck-final-v2").

## Quality check before delivering

- Would an engineer who already knows this topic learn one thing? If no, add specificity —
  real config keys, real numbers, real failure modes.
- Does slide 1 work as a standalone image? It's the only one shown in the feed.
- Is every claim on the slides correct? A wrong threshold in a confident infographic is worse
  than no post. If you're unsure of a current default or version-specific number, verify it or
  phrase it without the number.
- Any slide where the type auto-shrank noticeably? Cut words.
- Three visually distinct slides, not three variations of one layout?
