# RAG Demo: ask real-world documents, see the evidence

`DESIGN DOCUMENT · rag-demo`

*A minimal web app that shows semantic Retrieval-Augmented Generation end to end. Pick a knowledge base (HR policies, a lease, a router manual), ask a question, and see the passages, similarity scores and database rows behind every answer. Each stage maps to the CoALA framework.*

| Stack | Models | Date | Status |
|---|---|---|---|
| FastAPI · LangChain · pgvector · Next.js | `gpt-4o-mini` · `text-embedding-3-small` | 17 Oct 2026 | Approved · built |

[View code](https://github.com/nitingoswami-io/rag-demo) · [Fork](https://github.com/nitingoswami-io/rag-demo/fork) · [Report an issue](https://github.com/nitingoswami-io/rag-demo/issues/new) · [Contribute](https://github.com/nitingoswami-io/rag-demo/blob/main/CONTRIBUTING.md)

---

## 1. Purpose & scope

The app is a learning tool. The ingestion pipeline fills a long-term **semantic memory** (pgvector). Each chat turn runs a **retrieval action** that copies the most relevant chunks into the model's **working memory** (the prompt).

**CoALA pipeline**

| Stage | Key | Does | CoALA role |
|---|---|---|---|
| 1 | `samples.seed()` | Chunk · embed · store | CoALA learning action |
| 2 | `pgvector` | Vector collection | Semantic memory (long-term) |
| 3 | `similarity_search` | Top-4 chunks in one pack | Retrieval action |
| 4 | `ChatPromptTemplate` | Context + history | Working memory |
| 5 | `ChatOpenAI` | Grounded answer | Reasoning → external action |

### In scope

- Three sample knowledge bases ("packs") of fictional documents, indexed at startup: HR & Policies, Contracts & Legal, and Customer Support.
- A chat agent that searches only the selected pack, answers only from it, and cites its sources.
- Evidence views: the pipeline steps with timings and tokens, a sources table (document, page, chunk, similarity, cited), and a read-only view of the pgvector rows.
- Short chat history per pack, kept on the client and sent with each request.
- Local mode only (`ALLOW_UPLOADS=true`): upload `.pdf`, `.txt` and `.md` files, de-duplicate re-uploads, and delete documents.

### Demo safety and privacy

Uploads are off by default, so visitors can't store anything and there is no user data to protect. Sample documents are read-only, and uploads can't reuse a sample filename. `/chat` is rate-limited to 20 requests per minute per IP, which caps OpenAI spend. Request sizes are limited too: a message can be up to 1,000 characters and the history up to 20 turns. Question text and the retrieved passages are sent to OpenAI to generate the answer.

| | Demo mode (default) | Local mode (`ALLOW_UPLOADS=true`) |
|---|---|---|
| Sample knowledge bases | Read-only | Read-only |
| Upload and delete your own files | Disabled (`403`) | Yes, in a shared "Your documents" set |
| Limits | 20 chats per minute per IP | Also 5 files and 5 MB per upload, 10 uploads per minute |

### Out of scope

Authentication, per-user upload isolation, streaming, reranking, hybrid search and production deployment. Section 10 lists these as follow-ups.

## 2. Use cases

![Fig. 1: Use case diagram: a visitor picks a knowledge base, asks, and inspects the evidence; uploads are local-mode only.](figures/fig-01-use-cases.svg)

*Fig. 1: Use case diagram: a visitor picks a knowledge base, asks, and inspects the evidence; uploads are local-mode only.*

| ID  | Use case               | Behaviour                                                                                                         |
| --- | ---------------------- | ----------------------------------------------------------------------------------------------------------------- |
| UC1 | Upload documents (local mode) | The user picks files. The system chunks, embeds and stores them, then shows how many chunks were indexed per file. Re-uploading the same file is skipped; a changed file with the same name replaces its old chunks. |
| UC2 | Pick a knowledge base  | Shows each pack's problem, value and documents (chunk and page counts). In local mode, uploaded documents can be deleted, which removes their chunks and embeddings from pgvector. |
| UC3 | Ask a question         | Retrieves the top-4 chunks from the selected pack. The LLM answers from them only, or replies "I don't know based on the uploaded documents." |
| UC4 | Inspect evidence       | Clicking an answer shows its pipeline timings, a sources table with similarity scores and cited flags, and the matching rows in the pgvector table. |

## 3. Architecture

The system has three runtime parts: a Next.js client, a FastAPI service that owns all LangChain logic, and Postgres with the pgvector extension. OpenAI provides the embedding and chat models.

![Fig. 2: Component diagram: the panels, the FastAPI modules, and the chat path to pgvector and OpenAI.](figures/fig-02-components.svg)

*Fig. 2: Component diagram: the panels, the FastAPI modules, and the chat path to pgvector and OpenAI.*

![Fig. 3: Deployment view for local development.](figures/fig-03-deployment.svg)

*Fig. 3: Deployment view for local development.*

## 4. Key flows

### 4.1 Ingestion: hash → chunk → embed → store

At startup the backend indexes every sample file; in local mode, uploads take the same path. A file whose hash is already stored in that pack is skipped, so restarts are cheap, and a changed file replaces its old chunks only after the new ones are stored.

![Fig. 4: Sequence: ingestion with de-duplication (CoALA learning action).](figures/fig-04-seq-ingest.svg)

*Fig. 4: Sequence: ingestion with de-duplication (CoALA learning action).*

### 4.2 Query: question → retrieve → generate

![Fig. 5: Sequence: one chat turn within a pack (retrieval → working memory → reasoning).](figures/fig-05-seq-query.svg)

*Fig. 5: Sequence: one chat turn within a pack (retrieval → working memory → reasoning).*

### 4.3 Chat request lifecycle

![Fig. 6: State diagram for the chat panel.](figures/fig-06-state-chat.svg)

*Fig. 6: State diagram for the chat panel.*

## 5. Backend design

![Fig. 7: Class diagram: Python modules and Pydantic models.](figures/fig-07-classes.svg)

*Fig. 7: Class diagram: Python modules and Pydantic models.*

| File                  | Responsibility                                                                                                                               |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `app/config.py`       | Loads `.env` and exposes a frozen `Settings` dataclass: models, chunking, `top_k`, `ALLOW_UPLOADS` and the rate and size limits. |
| `app/samples.py`      | Reads `samples/packs.json` and indexes every sample file at startup (`seed()`), skipping unchanged files. |
| `app/vectorstore.py`  | Cached `PGVector` (collection `docs`, JSONB metadata) using `OpenAIEmbeddings`, plus SQL for pack documents, rows, de-duplication and delete. |
| `app/ingest.py`       | Hashes the file, skips it if unchanged, picks a loader by extension, splits with `RecursiveCharacterTextSplitter`, tags `source`, `page`, `chunk`, `pack` and `file_hash`, then calls `add_documents` with stable ids. |
| `app/rag.py`          | Runs `similarity_search_with_score(k=4)` filtered to the pack, builds the prompt with `ChatPromptTemplate` and `MessagesPlaceholder`, calls `ChatOpenAI(temperature=0)`, and returns the answer, sources with similarity scores, and timings. |
| `app/main.py`         | FastAPI routes, startup seeding, CORS, request and response models, per-IP rate limits, upload guards and error mapping. |

### System prompt

```text
You are a helpful assistant for a document Q&A demo.
Answer the question using ONLY the context below.
If the answer is not in the context, reply exactly:
"I don't know based on the uploaded documents."
Cite sources inline as [filename p.N] (omit p.N when there is no page).

Context:
{context}
```

### API contract

| Method | Path | Request | Response |
| ------ | ---- | ------- | -------- |
| GET    | `/health` | n/a | `{"status":"ok"}` |
| GET    | `/config` | n/a | `{"allow_uploads","chat_model","embedding_model","chunk_size","chunk_overlap","top_k",…}` |
| GET    | `/packs` | n/a | `[{"id","title","audience","problem","value","questions","readonly","documents":[{"filename","chunks","pages"}]}]` |
| GET    | `/packs/{id}/rows` | n/a | `{"limit":100,"rows":[{"id","source","page","chunk","file_hash","dims","embedding_preview","text"}]}` |
| POST   | `/chat` | `{"message","pack","history":[{"role","content"}]}` | `{"answer","sources":[{"rank","id","source","page","chunk","score",…}],"stats":{"retrieve_ms","generate_ms","chunks_searched","prompt_tokens",…}}` |
| POST   | `/upload` | multipart, field `files` (1..5), local mode | `[{"filename","chunks","status"}]`, status is `added`, `updated` or `unchanged` |
| DELETE | `/documents/{filename}` | n/a, local mode | `{"filename","chunks_deleted"}` |

Errors: `400` for an unsupported file type or an empty message, `403` for uploads in demo mode or deleting a sample, `404` for an unknown pack or document, `409` for an upload that reuses a sample filename, `413` for a file that is too large, `429` when a rate limit is hit. `500` with a readable `detail` for OpenAI or database failures.

## 6. Data model

`langchain-postgres` creates the `vector` extension and both tables on first use, so no migrations are needed. Each chunk is one row: its text, its 1536-dimension embedding and JSONB metadata. The `pack` key in that metadata is what keeps each knowledge base separate; the evidence panel reads these rows directly.

![Fig. 8: Entity-relationship diagram of the vector store tables.](figures/fig-08-er.svg)

*Fig. 8: Entity-relationship diagram of the vector store tables.*

## 7. Frontend design

![Fig. 9: Frontend component tree.](figures/fig-09-frontend.svg)

*Fig. 9: Frontend component tree.*

- A full-page layout: knowledge bases on the left, the chat in the centre, "How this answer was built" on the right, and an evidence panel along the bottom. On mobile the panels stack.
- Each pack keeps its own chat thread, so switching packs never mixes answers.
- Clicking an answer selects it: the insight panel shows retrieve and generate timings and token counts; the evidence panel shows the **Answer sources** table (rank, document, page, chunk, similarity, cited) and **Database rows** from `langchain_pg_embedding`.
- `UploadPanel` appears only when `/config` reports `allow_uploads`.
- Client components (`"use client"`) with Tailwind v4 and plain `fetch` to `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`). No extra packages beyond the `create-next-app` defaults.

## 8. Project layout

```text
rag-demo/
├── docker-compose.yml        pgvector/pgvector:pg16
├── README.md
├── docs/DESIGN.md            this document (Markdown + Mermaid)
├── backend/
│   ├── requirements.txt
│   ├── .env.example          OPENAI_API_KEY, DATABASE_URL
│   ├── samples/              packs.json + fictional docs (hr/, legal/, support/)
│   └── app/  config · samples · vectorstore · ingest · rag · main
└── frontend/
    ├── lib/api.ts
    └── app/  page.tsx · components/{KnowledgeBase, ChatPanel, InsightPanel,
              EvidencePanel, UploadPanel, MessageBubble, Header, Panel}.tsx
```

## 9. Run & verify

```bash
git clone https://github.com/nitingoswami-io/rag-demo.git && cd rag-demo
docker compose up -d
cd backend && python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && cp .env.example .env   # add OPENAI_API_KEY
uvicorn app.main:app --reload                              # :8000, docs at /docs
cd ../frontend && cp .env.local.example .env.local         # NEXT_PUBLIC_API_URL
npm install && npm run dev                                 # :3000
```

| Check                                           | Expected                                                                                  |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `GET /health`                                   | `{"status":"ok"}`                                                                         |
| Start the backend                               | Log shows each sample file `added` (first run) or `unchanged`.                            |
| HR pack: "How many weeks of parental leave do I get?" | 18 weeks for the primary caregiver and 6 for the secondary, cited as `[acme-employee-handbook.md]` |
| Legal pack: "Can I keep a dog in the flat?"     | One cat or one dog under 15 kg with written consent, plus a 300 EUR pet deposit, cited to the lease. |
| "Who won the 2022 World Cup?"                   | "I don't know based on the uploaded documents."                                           |
| `POST /upload` in demo mode                     | `403`                                                                                     |
| Upload a `.csv` (local mode)                    | `400` with "only .pdf, .txt and .md are supported."                                       |

## 10. Next steps

| Idea                                                  | What it teaches                                          |
| ----------------------------------------------------- | -------------------------------------------------------- |
| Hybrid search (BM25 + vector) and a reranker          | The largest retrieval-quality gain in real systems       |
| Agentic RAG: let the agent decide when to retrieve    | CoALA decision procedure instead of a fixed pipeline     |
| Persist chat history in Postgres and retrieve it      | Episodic memory alongside semantic memory                |
| Streaming answers over SSE                            | Responsive UX for long answers                           |
| Per-user upload collections with auth                 | Memory isolation and access control                      |

### Contribute

Fork the repo, pick an idea from the table, and open a pull request. Bugs and unclear steps go in [issues](https://github.com/nitingoswami-io/rag-demo/issues/new); the workflow is in [CONTRIBUTING.md](../CONTRIBUTING.md).

## Credits & sources

1. Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, Thomas L. Griffiths. [*Cognitive Architectures for Language Agents*](https://arxiv.org/abs/2309.02427) (2023). The CoALA vocabulary (semantic and working memory, retrieval and learning actions) used to map each RAG stage.
2. [*pgvector — open-source vector similarity search for Postgres*](https://github.com/pgvector/pgvector). The vector store behind ingestion and similarity search.

---

rag-demo · design document · source of truth: `docs/DESIGN.md` in the repository.
