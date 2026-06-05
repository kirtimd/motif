# Motif

Capture everything that piques your attention — links, posts, articles, videos,
notes — into one place, and let AI auto-organize it into a connected knowledge
graph that surfaces patterns, connections, and ideas you'd otherwise forget.

> We consume information at a terrifying rate. Most of it gets bookmarked,
> drafted, or screenshotted — and the spark dies. Motif exists to retain and
> build on the things that genuinely interest you.

## Status

🚧 Early development — building the MVP. See [`docs/plan.md`](docs/plan.md).

## MVP scope

1. **Capture** — paste any link, text, or note; Motif fetches and extracts it.
2. **Connect** — embeddings + auto-tagging organize items into a knowledge graph.
3. **Surface** — AI finds relationships, project ideas, and resurfaces forgotten gems.

Fancy per-platform capture (browser extension, mobile share sheet, OCR for
handwritten notes, audio transcription) comes *after* the core brain works.

## Stack

| Layer    | Tech                                          |
|----------|-----------------------------------------------|
| Backend  | Python 3.12 + FastAPI                          |
| Database | Postgres + pgvector (Docker)                  |
| Frontend | React + Vite + TypeScript + Tailwind          |
| AI       | Provider-agnostic embeddings + synthesis      |

## Getting started

_Coming in Phase 0 — scaffolding in progress._

## Repo layout

```
backend/      FastAPI app, DB models, AI providers
frontend/     React + Vite web app
experiments/  Throwaway spikes & notebooks (AI prompts, extraction tests)
docs/         Plan, architecture, session notes
```
