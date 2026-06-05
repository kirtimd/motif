# Motif — Plan

## Vision

A personal knowledge tool that captures anything interesting from anywhere, then
uses AI to auto-organize it into a connected knowledge graph — surfacing
patterns, connections, project ideas, and resurfacing things worth revisiting.

Primary goal: solve the "everything stays bookmarked forever and the spark dies"
problem. Secondary goal: a hands-on project to learn AI app development.

## Guiding principles

- **Capture must be frictionless and universal before it is fancy.** One paste
  box beats ten fragile platform integrations. Add native capture later.
- **The brain is the product.** The differentiator is connection & synthesis,
  not the act of saving. Invest there.
- **Always have something running.** Every phase ends with a working app.
- **Provider-agnostic AI.** Never hard-code a vendor; swap behind an interface.

## Architecture (MVP)

```
┌──────────────┐     paste link/text      ┌───────────────────────┐
│  React app   │ ───────────────────────► │   FastAPI backend     │
│  (frontend)  │ ◄─────────────────────── │                       │
└──────────────┘    items, connections     │  - capture/extract    │
                                           │  - embeddings         │
                                           │  - synthesis (LLM)    │
                                           └──────────┬────────────┘
                                                      │
                                           ┌──────────▼────────────┐
                                           │ Postgres + pgvector   │
                                           │  items, tags, links,  │
                                           │  embeddings (vectors) │
                                           └───────────────────────┘
```

Why **Postgres + pgvector**: one store handles relational metadata, vector
similarity search ("find related"), and graph-style link queries. No separate
vector database to operate.

### AI provider abstraction

Two interfaces, each with swappable implementations:

- `EmbeddingProvider.embed(texts) -> vectors` — for semantic search / related items.
- `LLMProvider.complete(prompt) -> text` — for tagging, themes, idea synthesis.

Default is chosen in Phase 2/3 (candidates: local sentence-transformers for
embeddings = free/private; Claude for synthesis). Config via env vars.

## Data model (first cut)

- **item** — id, source_url, source_type, title, content (extracted text),
  image_url, created_at, captured_note.
- **tag** — id, name; **item_tag** — many-to-many.
- **embedding** — item_id, vector (pgvector).
- **link** — from_item, to_item, kind (e.g. "similar", "cites"), score.

## Roadmap

### Phase 0 — Scaffolding  ✅ DONE
- [x] Backend: FastAPI app, `/health` endpoint, dependency setup.
- [x] DB: docker-compose with Postgres + pgvector; connection from backend.
- [x] Frontend: Vite + React + TS + Tailwind; calls `/health`, renders status.
- [ ] One command (or short README) to run all three locally.  ← nice-to-have next
- **Done when:** open the web app, it shows "backend healthy" from a live API call. ✅

### Phase 1 — Capture
- [ ] `POST /items` with a URL or raw text/note.
- [ ] URL fetch + readability extraction (title, main text, lead image, source type).
- [ ] Persist item; `GET /items` list endpoint.
- [ ] Frontend: paste box + reverse-chronological feed of captured items.
- **Done when:** paste a link, see a clean card appear in your feed.

### Phase 2 — The brain (connections)
- [ ] Generate & store an embedding on each capture.
- [ ] "Related items" via vector similarity.
- [ ] Auto-tagging (LLM or keyword extraction).
- **Done when:** opening an item shows genuinely related items.

### Phase 3 — Synthesis (the magic)
- [ ] Periodic/triggered LLM pass: cluster items into themes.
- [ ] Generate project ideas & learning paths from clusters.
- [ ] Resurface forgotten-but-relevant items.
- **Done when:** Motif tells you something useful you didn't ask for.

### Phase 4 — Graph UI
- [ ] Visualize items and their links as an interactive graph.

## Deferred (post-MVP, intentionally)

Browser extension · mobile share sheet · per-platform APIs (LinkedIn/Insta/etc.)
· OCR for handwritten notes · audio/video transcription · auth & multi-user ·
deployment/hosting.

## Open decisions (revisit when relevant)

- Embedding model default (local vs hosted).
- LLM provider default for synthesis.
- Background job mechanism for Phase 3 (inline vs queue/cron).
