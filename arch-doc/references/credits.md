# Credits & sources: give credit to the original source

Every explainer builds on someone's work: the paper that named the concept, a vendor's docs, an open-source project, a talk, a book. **Credit is not optional.** A document with an empty credits list does not ship.

## What to credit

Credit anything the design **takes** from:

| Kind | Example | Credit it when you… |
|---|---|---|
| Paper | Sumers et al., *Cognitive Architectures for Language Agents* (2023) | use its model, taxonomy, terms or diagrams |
| Vendor or cloud reference architecture | A cloud provider's "RAG on X" pattern | follow its structure or component choices |
| Open-source project | pgvector, LangChain | depend on it or copy its approach |
| Article, talk or book | A conference talk on agent memory | reuse its argument, numbers or framing |
| Diagram | Fig. 1 of a paper | redraw or adapt it (never paste it) |
| Prior internal or personal work | Your own earlier post or demo | build on it (link it) |
| Original work | Your own design | nothing else applies (say so explicitly) |

## How to credit

1. **Frontmatter `sources`** (site MDX). Each entry has:
   - `title` (required);
   - `authors`, `year`, `url`;
   - `note`, saying **what you took** ("memory taxonomy and decision cycle", "Fig. 2 adapted from the paper's Fig. 1");
   - `license`, when you reuse text, code or images under a license.

   The site renders these as the **Credits & sources** list on the page. Architectures fail the build without at least one entry.
2. **The Credits & sources section** closes `ARCHITECTURE.md` and the HTML page, after section 10 and unnumbered. Use the same list in the same order.
3. **Inline attribution** where the idea is used:
   - in prose: "organised around the CoALA framework (after Sumers et al., 2023)";
   - in figure captions: "adapted from Sumers et al. (2023)".
4. **Original work** gets one entry: `title: Original work`, with a `note` naming what is new and what it was inspired by.

## Rules that keep credit honest

- **Verify every URL.** Use only URLs you opened in this session or that the user gave you. If you can't verify one, keep the title, authors and year, leave the URL out, and list it as `TBD` in the handover.
- **Never invent** authors, years, titles or DOIs. A partial credit is better than a fabricated one.
- **Redraw, don't copy.** Figures from sources are redrawn in the house hand-drawn style and captioned "adapted from …". Copy an original image only if its license allows it, and record the license.
- **Quote sparingly.** Paraphrase. Any direct quote stays under ~25 words, in quotation marks, with the source credited.
- **Credit the specific thing.** "Inspired by the internet" is not a credit. Name the paper, repo or talk, and what you took from it.
- **Keep credits when you edit.** When you revise an explainer, never drop a source whose idea is still in it.

## Format examples

Frontmatter:
```yaml
sources:
  - title: Cognitive Architectures for Language Agents
    authors: Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, Thomas L. Griffiths
    year: 2023
    url: https://arxiv.org/abs/2309.02427
    note: Memory taxonomy, action space and decision cycle; Fig. 2 adapted from the paper's framework.
  - title: Original work
    note: The human-gated learning loop (Fig. 5) is new in this design.
```

ARCHITECTURE.md:
```markdown
## Credits & sources

1. Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, Thomas L. Griffiths. [*Cognitive Architectures for Language Agents*](https://arxiv.org/abs/2309.02427) (2023). Memory taxonomy, action space and decision cycle; Fig. 2 adapted from the paper's framework.
```
