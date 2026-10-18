# {{Name}}: {{what it does}}

`DESIGN DOCUMENT · {{slug}}`

*{{Lede: 1–2 sentences on what the demo shows and why. Mention CoALA if it applies.}}*

| Stack | Models | Date | Status |
|---|---|---|---|
| {{FastAPI · LangChain · pgvector · Next.js}} | `{{model-id}}` · `{{embedding-model-id}}` | {{17 Oct 2026}} | {{Draft \| Approved \| Approved · built}} |

[View code]({{REPO_URL}}) · [Fork]({{REPO_URL}}/fork) · [Report an issue]({{REPO_URL}}/issues/new) · [Contribute]({{REPO_URL}}/blob/main/CONTRIBUTING.md)

---

## 1. Purpose & scope

{{What the app teaches. **Bold** the CoALA memories and actions it exercises.}}

**CoALA pipeline**

| Stage | Key | Does | CoALA role |
|---|---|---|---|
| 1 | `{{POST /upload}}` | {{Chunk · embed · store}} | {{Learning action}} |
| 2 | `{{pgvector}}` | {{Vector collection}} | {{Semantic memory (long-term)}} |
| 3 | `{{similarity_search}}` | {{Top-4 chunks}} | {{Retrieval action}} |
| 4 | `{{ChatPromptTemplate}}` | {{Context + history}} | {{Working memory}} |
| 5 | `{{ChatOpenAI}}` | {{Grounded answer}} | {{Reasoning → external action}} |

### In scope

- {{Verb-first capability}}

### Out of scope

{{Deliberately excluded items}}. Section 10 lists these as follow-ups.

## 2. Use cases

![Fig. 1: Use case diagram: {{one line}}.](figures/fig-01-use-cases.svg)

*Fig. 1: Use case diagram: {{one line}}.*

| ID | Use case | Behaviour |
|---|---|---|
| UC1 | {{Use case}} | {{System behaviour}} |

## 3. Architecture

{{Runtime parts and what each owns.}}

![Fig. 2: Component diagram: modules and their dependencies.](figures/fig-02-components.svg)

*Fig. 2: Component diagram: modules and their dependencies.*

![Fig. 3: Deployment view for {{environment}}.](figures/fig-03-deployment.svg)

*Fig. 3: Deployment view for {{environment}}.*

## 4. Key flows

### 4.1 {{Flow}}: {{a → b → c}}

![Fig. 4: Sequence: {{flow}} (CoALA {{concept}}).](figures/fig-04-seq-flow.svg)

*Fig. 4: Sequence: {{flow}} (CoALA {{concept}}).*

## 5. Backend design

![Fig. 5: Class diagram: {{modules and models}}.](figures/fig-05-classes.svg)

*Fig. 5: Class diagram: {{modules and models}}.*

| File | Responsibility |
|---|---|
| `{{path}}` | {{responsibility}} |

### System prompt

```text
{{VERBATIM SYSTEM PROMPT}}
```

### API contract

| Method | Path | Request | Response |
|---|---|---|---|
| `{{GET}}` | `{{/path}}` | {{request}} | `{{response}}` |

Errors: {{codes and causes}}.

## 6. Data model

{{Who creates the schema; what one row is.}}

![Fig. 6: Entity-relationship diagram of {{store}}.](figures/fig-06-er.svg)

*Fig. 6: Entity-relationship diagram of {{store}}.*

## 7. Frontend design

![Fig. 7: Frontend component tree.](figures/fig-07-frontend.svg)

*Fig. 7: Frontend component tree.*

- {{Rendering model}}
- {{How it calls the API}}
- {{The UX detail that makes the demo's point visible}}

## 8. Project layout

```text
{{slug}}/
├── {{file}}        {{comment}}
└── {{dir}}/
```

## 9. Run & verify

```bash
git clone {{REPO_URL}}.git && cd {{slug}}
{{commands, one per line, with # comments}}
```

| Check | Expected |
|---|---|
| {{health check}} | {{expected}} |
| {{grounded question}} | {{answer + citation}} |
| {{out-of-scope question or bad input}} | {{refusal or 4xx}} |

## 10. Next steps

| Idea | What it teaches |
|---|---|
| {{idea}} | {{lesson, naming the CoALA concept if any}} |

### Contribute

Fork the repo, pick an idea from the table, and open a pull request. Bugs and unclear steps go in issues.
[Fork]({{REPO_URL}}/fork) · [Report an issue]({{REPO_URL}}/issues/new) · [How to contribute](../CONTRIBUTING.md)

## Credits & sources

1. {{Authors}}. [*{{Title}}*]({{verified URL}}) ({{Year}}). {{What this demo takes from it.}}

---

{{slug}} · design document · source of truth: `docs/DESIGN.md` in the repository.
