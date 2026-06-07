# Motif — Plan

## Vision

Motif owns the compounding, intent-rich record of what sparks you, and a
proactive loop that turns it into things you actually make. The reasoning is
rented from Claude; the corpus, the intent, and the loop are owned. Full thesis
in [`vision.md`](vision.md).

Primary goal: close the gap between consuming and creating — today the spark dies
in a bookmark graveyard. Success = things *made*, not items stored. Secondary
goal: a hands-on project to learn AI app development.

## Guiding principles

- **Rent the model, own what compounds.** Reasoning is commodity (Claude); the
  moat is the intent-rich corpus + the spark→artifact loop + the initiative.
  Test every feature: does a *better* model strengthen it, or obsolete it?
- **Capture must be frictionless, and capture intent.** One paste box + the *why
  this sparked me*. The intent note is the highest-value signal — catch it early.
- **The loop is the product.** Spark → suggestion → tracked artifact. Don't be a
  thin wrapper: the loop must close to real output, not lost chat replies.
- **Always have something running.** Every phase ends with a working app.
- **Provider-agnostic, Claude-first.** Swap behind an interface, but build for Claude.

## Architecture (MVP)

```
   paste link/text + spark note
┌──────────────┐  ───────────────►  ┌───────────────────────┐      ┌──────────────┐
│  React app   │                    │   FastAPI backend     │ ───► │  Claude API  │
│  (frontend)  │  ◄───────────────  │  capture/extract,     │ ◄─── │ (rented brain)│
└──────────────┘  feed, suggestions │  assemble corpus,     │      └──────────────┘
                                    │  run the loop         │
                                    └──────────┬────────────┘
                                               │
                                    ┌──────────▼─────────────────┐
                                    │ Postgres (+pgvector ready,  │
                                    │  unused until scale)        │
                                    │  items, suggestions         │
                                    └─────────────────────────────┘
```

**Claude-first, corpus-in-context.** While the corpus is small, hand the whole
intent-rich corpus to Claude (prompt-cached) and let it cluster + suggest —
qualitatively richer than vector similarity, and cheap at small N. pgvector stays
installed but unused until the corpus outgrows the context window (~few hundred
items), at which point embeddings return as a **retrieval (RAG)** layer that
feeds Claude only the relevant slice and keeps cost flat.

> Similarity / auto-organize (the original goal) is delivered by **Claude now**,
> and by **embeddings + RAG at scale** — preserved throughout, not dropped.

### AI provider abstraction

- `LLMProvider.complete(prompt) -> text` — **Claude-first**; clustering,
  suggestions, drafting. The core engine from V1.
- `EmbeddingProvider.embed(texts) -> vectors` — added at scale (Phase 4) for RAG
  retrieval. Candidate: local sentence-transformers (free) or hosted (~$0.02/1M).

## Data model

### `items` (Phase 1 — signed off)

| Column | Type | Notes |
|---|---|---|
| `id` | UUID (PK) | non-enumerable, URL-safe |
| `user_id` | UUID, not-null, indexed | defaults to `SEED_USER_ID`; multi-tenant-ready |
| `source_type` | varchar | `url` \| `text` \| `note` (validated string, not a DB enum) |
| `source_url` | text, nullable | original link |
| `title` | text, nullable | |
| `content` | text, nullable | extracted body / note text |
| `excerpt` | text, nullable | short preview for cards |
| `image_url` | text, nullable | lead image |
| `spark_note` | text, nullable | **the intent** — why this sparked you (highest-value signal) |
| `status` | varchar, default `ready` | `pending` \| `ready` \| `failed` |
| `extra` | JSONB, default `{}` | author, site_name, published_at, word_count… |
| `created_at` / `updated_at` | timestamptz | |

Index: `(user_id, created_at)` — the feed query.

**Design decisions (with rationale):**
- **UUID PK** — non-enumerable & URL-safe for a future public multi-user app.
- **Seed-constant `user_id`** — every row owned + every query scoped by `user_id`
  now, without building auth. Add real `users` table + FK later (see checklist).
- **Flexible string + JSONB** — evolve sources/metadata without migrations while
  the model is still moving; promote a field to a real column when we must query it.

### Coming later (by phase)
- **suggestion** (Phase 2) — id, user_id, kind (build/write/learn), title, body,
  status (suggested/making/done/dismissed), source spark ids (provenance).
- **embedding** (Phase 4, at scale) — item_id, vector (pgvector) for RAG retrieval.
- **tag / link** (later) — auto-tags and explicit item links if they earn their keep.

### ⚠️ Auth-migration checklist (do ALL when real auth lands)

The seed-constant `user_id` is a training wheel. When adding multi-user auth:
1. Create a `users` table; insert your real account.
2. Backfill: `UPDATE items SET user_id = <your real id>` (was `SEED_USER_ID`).
3. Add the foreign key `items.user_id -> users.id`.
4. **Drop the `user_id` default** so inserts MUST supply the logged-in user —
   otherwise new users' data silently lands under the seed id (cross-user leak).
5. Confirm every query filters by the authenticated `user_id` (already the habit).

## Roadmap

### Phase 0 — Scaffolding  ✅ DONE
- [x] Backend: FastAPI app, `/health` endpoint, dependency setup.
- [x] DB: docker-compose with Postgres + pgvector; connection from backend.
- [x] Frontend: Vite + React + TS + Tailwind; calls `/health`, renders status.
- [ ] One command (or short README) to run all three locally.  ← nice-to-have next
- **Done when:** open the web app, it shows "backend healthy" from a live API call. ✅

### Phase 1 — Capture with intent + provenance  ← we are here
- [x] Data model: `items` table + SQLAlchemy model + Alembic migration.
- [ ] `POST /items` — URL or text/note + `spark_note`; auto-record provenance.
- [ ] URL fetch + readability extraction (title, excerpt, lead image, source type).
- [ ] `GET /items` list endpoint.
- [ ] Frontend: paste box + spark-note field + reverse-chronological feed.
- **Done when:** paste a link with a why-note, see a clean card in your feed.

### Phase 2 — The loop (the differentiator, pulled early)
- [ ] `suggestion` table + provider-agnostic `LLMProvider` (Claude-first).
- [ ] "What can I make?" → Claude reads the corpus → suggestions citing sparks.
- [ ] Accept a suggestion → tracked artifact (status suggested→making→done).
- [ ] Prompt-cache the corpus; structured outputs for suggestions.
- **Done when:** Motif proposes something to make from your sparks, and you can
  accept it into tracked work.

### Phase 3 — Proactivity (the engine)
- [ ] Motif *initiates* the loop: scheduled/triggered nudges.
- [ ] Resurface forgotten-but-relevant sparks.
- **Done when:** Motif tells you something useful you didn't ask for.

### Phase 4 — Scale the brain (embeddings return as RAG)
- [ ] Embeddings on each item; pgvector retrieval of the relevant slice.
- [ ] Keeps Claude cost flat + corpus searchable once it outgrows the context window.
- **Done when:** suggestions stay fast/cheap with a large corpus.

### Phase 5 — Later
- [ ] Graph UI · richer capture sources · "context wallet" export.

## Deferred (post-MVP, intentionally)

Browser extension · mobile share sheet · per-platform APIs (LinkedIn/Insta/etc.)
· OCR for handwritten notes · audio/video transcription · auth & multi-user ·
deployment/hosting.

## Open decisions (revisit when relevant)

- Claude model tier for the loop (Haiku / Sonnet / Opus) — cost vs quality.
- Embedding model default when Phase 4 arrives (local vs hosted).
- Background job mechanism for Phase 3 (inline vs queue/cron).
