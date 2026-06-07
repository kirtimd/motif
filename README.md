# Motif

> **Motif owns the compounding, intent-rich record of what sparks you, and a
> proactive loop that turns it into things you actually make. The reasoning is
> rented from Claude; the corpus, the intent, and the loop are owned — and they
> get more valuable every month and every model upgrade.**

We consume information at a terrifying rate. Most of what grabs us gets
bookmarked, drafted, or screenshotted — and the spark dies in a graveyard of
tabs. Motif exists to keep that spark alive and turn it into output.

Motif is **not** a note app or a personal wiki, and it doesn't try to out-think
Claude. The intelligence is *rented* (and improves for free as models do). What
Motif *owns* is the part that compounds: a proprietary, intent-rich,
provenance-tracked corpus of what catches your attention, and a closed loop from
**spark → suggestion → artifact**.

> Guiding principle: **rent the model, own what compounds.**

See [`docs/vision.md`](docs/vision.md) for the full thesis and
[`docs/plan.md`](docs/plan.md) for the build roadmap.

🚧 Early development.

## What V1 proves

1. **Capture with intent** — save any link / text / note in seconds, plus the
   *why it sparked you*. Provenance (source, time) is recorded automatically.
2. **Close the loop** — grounded in your corpus, Claude proposes things you
   could *make* (build / write / learn), citing the sparks behind each.
3. **Track the artifact** — accept a suggestion and it becomes tracked work, so
   progress compounds and nothing gets re-suggested.

Proactive nudges, semantic clustering at scale, and richer capture sources come
*after* the loop works.

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
