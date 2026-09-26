---
name: market-teardown
description: >-
  Draft a data-dense, verdict-driven teardown of a market, product idea, or
  startup — around 1,500 words, sourced from research the user already has,
  opening with narrative, arguing from figures, ending with a bold verdict and
  a dated reference list. Also produces a short companion post that drives
  readers to the teardown without spoiling the verdict. Use this skill when
  the user asks for a teardown, an idea breakdown, a market analysis
  writeup, a newsletter edition, a LinkedIn/Substack/Medium article, or says
  things like "write this research up", "turn this into an article", "publish
  the analysis on X", or names a topic and asks to publish it. Trigger even
  when the request is as short as "teardown of on-device inference economics"
  or "write up the vertical SaaS thing" — don't wait for the user to describe
  the format.
---

# Market teardown — data-driven verdict writeup

Produces one long-form teardown of a market or startup idea, plus the companion short-form post that distributes it.

The teardown's reason to exist is that it prints numbers other writers won't and reaches a verdict other writers won't. Two failure modes destroy it: fabricated statistics and hedged conclusions. Most of what follows exists to prevent those two things.

The skill assumes the user has done research on the topic already — this is a *compression* of that research into a shareable artifact, not a fresh opinion.

---

## Step 1 — Find the research before writing a word

Never generate a statistic. Every number must trace to research already done. A teardown is a compression of prior work, not a new opinion.

Before drafting:

1. Read whatever project files, uploads, or attached documents relate to the topic. If the user has anchored the request in a specific document, treat that as authoritative and read it first.
2. Search the user's prior chats and drafts for the same topic using **content words**, not meta-words. Content words are the specific nouns and numbers of the domain — e.g. `vertical SaaS construction procurement`, `on-device inference hardware economics`, `consumer subscription unbundling`. Meta-words like `research` or `we discussed` return everything and nothing.
3. Web-search only to date-check a figure or fill a specific gap the prior research left open — and flag anything that has moved since the original session.

**Gate:** a teardown of this length needs 15–25 sourced figures. If the available research yields fewer than about ten, stop and say so. Offer to pick a different topic or run the underlying research first.

**Traceability rule:** if a number cannot be pointed back to a project doc, a past research session, or a source found in this session, cut it. Do not estimate from general knowledge and do not round up from memory. Where a figure genuinely is the author's own modelling, label it — `Author's model — [what it estimates], directional only`.

---

## Step 2 — Fix the verdict before drafting

Decide the conclusion first, then write toward it. Exactly one of:

- **No-go** — the model is structurally broken; name the constraint that kills it.
- **Conditional go** — viable only if a named condition holds; state the condition and the number attached to it.
- **Go** — rare; reserve it, and still name the kill risk.

The verdict appears at the *end* of the piece, but it governs everything before it. Each section lays track toward it. If the verdict is unclear after reading the research, the teardown isn't ready — say so rather than writing a survey.

---

## Step 3 — Write the teardown

**Length: 1,400–1,600 words.** Long enough to argue properly, short enough to finish on a phone.

Structure, in this order:

**1. Title** — ≤100 characters. Lead with the number, the collision, or the killed assumption.

**2. Opening — 150–250 words, no heading.** This is the narrative block and the only place prose runs free. Set the situation: what is happening in the market, why the opportunity looks obvious, and the first number that complicates it. Narrative here means *flowing analytical prose*, not a personal anecdote — statistics beat stories, so the scene is set with facts, not with "last week I met a founder". End the opening on the turn: the reason to be suspicious.

**3. Four headed sections, 250–350 words each.** Adapt the headings to the topic; the underlying job of each is stable:

- *What's actually real* — the demand, sized and dated. Also name what has **no** published figure; that absence is often the finding.
- *Why the obvious version fails* — the structural blocker, or the graveyard of companies that already tried it.
- *The economics, and who pays* — unit economics, take rate, cost to serve, and the named paying counterparty with the month or milestone at which revenue starts.
- *What would have to be true* — the conditions, and the risks with an owner attached to each.

Prose paragraphs carry the argument. Use bullets only where a list genuinely is a list — a run of comparable figures, a set of conditions. Roughly one bulleted run per section at most.

**4. The verdict — 150–220 words, final heading.** Bold one-liner: No-go / Conditional go / Go. Then the conditions, numbered where there is more than one, each with a figure attached. Then the single risk most likely to kill it.

**5. What I'd validate next — 60–100 words.** Two or three specific, cheap, time-boxed actions with numeric gates.

**6. References** — see Step 4.

Title formulas that work:
- The number that kills it: `2.5%: the ceiling that ends the directory business`
- The collision: `$110M raised, $11M sold`
- The killed assumption: `A billion users is not a data moat`
- The absence: `Nobody owns the 1–6 month furnished flat. There's a reason.`
- The outcome gap: `$237M raised across four companies, one survivor — and it changed its model`

**The title carries the turn or the number — never the opportunity alone.** An opportunity headline attracts the audience this format is differentiating itself from, and it sets up a bait-and-switch when the reader arrives at a conditional or a no-go. `A billion-dollar gap that nobody has filled` is the counter-example: it promises a market, where `a gap this size is usually not an oversight — it is a structural refusal` promises analysis. Include at least one topic keyword so the title is findable in search and legible to a scrolling reader.

Do not promote a phrase from the body into the title without rewriting the body line. The echo makes the original land flat 200 words later.

Read `references/voice.md` before drafting, and `references/example-teardown.md` for a full worked teardown to write against.

---

## Step 4 — The reference section

Every teardown ends with a dated source list. This is the credibility mechanism — it is what separates the piece from an opinion post, and it is what makes the numbers reusable later.

Format: a flat list, one line per source, grouped only if there are more than about ten.

```
**References**

- Industry report name — what it supports (FY26)
- Regulatory filing / analyst brief — what it supports (Q1 2026)
- Trade press article — what it supports (Nov 2023)
```

Rules:
- Name the source, then what it supports, then the date of the data.
- No bare URLs in the body. If a link belongs anywhere it is here, and most publishing platforms render it inline.
- If a figure came from the author's own modelling, list it as such: `Author's model — [what it estimates] (Jul 2026), directional only`.
- If a source could not be verified, either cut the claim or mark it: `unverified — flagged in text`.

---

## Step 5 — Publishing-platform formatting

Most target platforms (LinkedIn articles, Substack, Medium, personal blogs) render a limited markdown subset. Get this wrong and the piece renders as garbage.

- **No tables.** Research docs are table-heavy; convert every table to prose or one-line bullets.
- Subheads only (rendered as H2) — no deeper nesting.
- Paragraphs of 3–4 sentences. At 1,500 words, wall-of-text is the main way to lose a mobile reader.
- Bold reserved for the verdict line and a handful of pivotal figures.
- No emoji in the title or opening; at most one in the body, and only if it's doing work.

Numbers, formatted consistently:
- **Date every figure**: `(FY26)`, `(Jul 2026)`, `(Q1 2027)`. A statistics-driven piece that doesn't date its statistics ages into a liability.
- **One currency per comparison.** Never write `$110M raised, ₹90 Cr sold` — mixing units inside a single collision forces the reader to do arithmetic before the point lands. Pick the unit that fits the audience and convert the other. Default to the native currency of the market being analyzed; convert to a comparison unit only when the point requires it, and mark converted figures as such.
- **Converting historical figures is defensible in a reference line, not in a headline.** Exchange rates move; a five-year-old fundraise converted at today's rate is a directional figure, not a fact.
- Percentages and multiples exact as sourced; don't smooth them.
- **Keep haircut denominators straight.** Raised-versus-sold and peak-valuation-versus-sold are different claims with different multiples. State which one you mean; never let a title pull the body into conflating them.

---

## Step 6 — Companion feed post

Every teardown ships with a separate short post that links to it. Newsletter platforms and long-form articles rarely distribute themselves — this short post is the entire distribution mechanism.

**Length: 400–800 characters.** Short, and deliberately incomplete.

The job is not to summarise the teardown — it is to open a question the teardown answers. A feed post that delivers the argument and the verdict has given the reader no reason to click; they have already got the value, and the piece gets a like instead of a subscriber. Withhold on purpose.

Shape:

1. **Line one: the hardest collision in the piece, in under 140 characters.** That is all that shows above the fold on mobile. A number against a number is best — `$110M raised. $11M sold.`
2. **Two or three short lines establishing the contradiction.** The demand is real *and* the attempts died. The market is large *and* nobody owns it. Two or three figures maximum — the teardown has thirty, and spending them here is what kills the click.
3. **One line naming what is withheld, specifically.** The verdict and its conditions, the constraint that killed the model, the identity of the payer. Name the shape of the answer, never the answer.
4. **One line pointing to the teardown.**
5. Hashtags: three at most, precise, or none.

**Suspense, not clickbait.** The withheld thing must be real, specific and delivered in full by the teardown. `The verdict, and the four conditions attached to it, are in the piece` is right. `You won't believe what I found` is wrong, and so is any rhetorical question stack. If the piece would disappoint someone who clicked on the promise, rewrite the promise.

Never state the verdict in the feed post. That is the single rule that separates this from a summary.

**Example — the shape working:**

```
NestAway raised over $110M to fix Indian rental housing. It sold for $11M.

The gap it was chasing is still open. Every year, several hundred thousand
professionals need a furnished flat for one to six months. Airbnb is built
for nights. NoBroker is built for 11-month leases. Nobody sells the middle.

Zeus, Landing and OYO Life all raised nine figures against that same gap.
All four died the same death — and it is the same reason a corporate
travel desk cannot book an Airbnb in India today.

The verdict, and the four conditions it depends on, are in this week's
teardown.
```

Note what that does not contain: the verdict, the mechanism, the unit economics, or the name of the payer. Three figures, one contradiction, one specific withheld answer.

---

## Step 7 — Deliver

Save both files to the user's chosen output folder (ask if it isn't obvious from context — common choices are `./out/`, `~/Documents/`, or a Claude Desktop file drop):

- `<slug>.md` — the teardown
- `<slug>-feedpost.md` — the companion feed post

Where a sequence number helps the author track drafts (e.g. `03-vertical-saas-construction.md`), use one — but this is a naming preference, not a rule.

Then report four lines only: word count, count of sourced figures, number of references, the verdict. No prose summary — the user is about to read it.

---

## Guardrails

**Aim the knife at models, not at people.** Published financials, traffic declines, and shutdowns are fair game. Character judgments about named founders are not. A teardown that reads as a hit piece against a person costs more than it earns, and it undermines the analytical positioning of everything else the author publishes.

**Don't leak the author's own live plans.** If the topic touches something the author is actively building, write about it only when they ask explicitly, and only at the level of detail they set.

**Honest uncertainty is on-brand; hedging is not.** "No published figure exists for annual X — that gap is why the wedge is unowned" is right. "This could be interesting, but there are challenges" is wrong.

**Statistics over stories, always.** If a sentence could be replaced by a number, replace it. The narrative opening is a structural setup, not an anecdote.

---

## Files

- `references/voice.md` — voice rules and banned constructions. Read before drafting.
- `references/example-teardown.md` — a full worked ~1,500-word teardown. Read before drafting.
- `assets/teardown-template.md` — the skeleton to fill in.
