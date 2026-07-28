# AI Engineer Daily

An AI-powered news platform that automatically ingests AI news from trusted sources, enriches each article with LLM-generated insights, and delivers concise daily briefings for software engineers. Instead of overwhelming users with dozens of AI news articles every day, AI Engineer Daily automatically aggregates trusted sources and uses LLMs to generate concise, actionable briefings in just a few minutes.

**Tech Stack:** Next.js · React · TypeScript · FastAPI · PostgreSQL · OpenAI

[![CI](https://github.com/tia-he/ai-engineer-daily/actions/workflows/ci.yml/badge.svg)](https://github.com/tia-he/ai-engineer-daily/actions/workflows/ci.yml)

🌐 **Live Demo:**  https://ai-engineer-daily.vercel.app

> **Note:** The backend is hosted on Render's free tier and may take a few seconds to wake up on the first request.

---

## Architecture

```text
                  RSS Sources
(OpenAI · Anthropic · Google AI · Hugging Face)
                         │
                         ▼
              GitHub Actions (Cron, daily)
                         │
              ingest_rss.py
        (select top stories, then
         synthesize each with the
              OpenAI API)
                         │
                         ▼
                 PostgreSQL (Neon)
                         │
                         ▼
              FastAPI (Render)
                         │
                    REST API
                         │
                         ▼
             Next.js (Vercel)
                         │
                         ▼
                      Users
```

Once a day, a scheduled GitHub Actions workflow runs `ingest_rss.py`,
which pulls new posts from every feed, asks the OpenAI API to pick the
day's most significant stories (merging any that cover the same event
across sources), and asks it again per story to write one fully-formed
article from the combined source material. Every article is complete
by the time it's written to the database, so serving requests never
waits on ingestion or the OpenAI API — the backend stays stateless and
responsive.

---

## Core Features

- **Daily AI Briefing** — a handful of the day's most significant stories, not a firehose of every post
- **Cross-source synthesis** — stories covered by more than one source are merged into a single article instead of duplicated
- **AI-generated Metadata** — summary, takeaway, key concepts, and background for every article
- **Full-text Search** — search across titles, summaries, takeaways, and concepts
- **Responsive UI** — optimized for desktop and mobile
- **Automated RSS ingestion** that skips any post already covered by an existing article

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js (App Router), React, TypeScript, Tailwind CSS |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL (Neon) |
| AI | OpenAI API (`gpt-4o-mini`) |
| Testing | pytest, Vitest, React Testing Library, Playwright |
| Deployment | Vercel, Render, GitHub Actions |

---

## Project Structure

```text
app/                    # Next.js routes (App Router)
├── page.tsx             # Homepage
├── news/[id]/page.tsx   # Article detail
└── search/page.tsx      # Search

components/              # Reusable UI components
services/                # API client
types/                   # Shared TypeScript types

backend/
├── main.py               # FastAPI app + CORS, creates tables on startup
├── app/                  # Routers (health, news, search)
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── crud.py                # Data access layer
├── config.py               # Environment-driven config
├── openai_client.py        # Story selection + article synthesis (OpenAI calls)
└── ingest_rss.py           # Daily brief pipeline: fetch, select, synthesize, publish

.github/workflows/       # CI + scheduled ingestion
```

---

## How It Works

1. **Fetch** — `ingest_rss.py` pulls entries from every configured RSS feed, skipping any whose link is already used as a source on an existing article.
2. **Select** — one OpenAI call groups that day's new entries by real-world story (multiple sources covering the same event become one group) and picks at most `MAX_DAILY_STORIES` (5) most significant — fewer is fine, it never pads the list.
3. **Synthesize** — one OpenAI call per selected story combines all of its sources into a single article: a full, normal-length body deduped across sources (never padded or invented beyond what the sources say), plus a takeaway and background that are allowed more editorial latitude.
4. **Schedule** — the whole pipeline runs once a day on a GitHub Actions cron, so the database stays fresh without a long-running worker.
5. **Serve** — FastAPI exposes the data through a REST API, while Next.js renders pages using the App Router and performs client-side search. Since ingestion and synthesis are handled asynchronously by a scheduled GitHub Actions workflow, API requests remain lightweight and stateless.

---

## Getting Started

**Prerequisites:** Node 20+, Python 3.11+, PostgreSQL

```bash
git clone https://github.com/<your-username>/ai-engineer-daily.git
cd ai-engineer-daily
```

**Frontend**

```bash
npm install
cp .env.example .env.local   # set NEXT_PUBLIC_API_BASE_URL
npm run dev
```

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/ai_engineer_daily"
uvicorn main:app --reload   # creates tables on startup if they don't exist
```

**(Optional) Populate the database**

```bash
python init_db.py       # dev seed articles
python ingest_rss.py    # real RSS articles, selected + synthesized (requires OPENAI_API_KEY)
```

| Variable | Where | Purpose |
|---|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | frontend | Backend API base URL |
| `DATABASE_URL` | backend | PostgreSQL connection string |
| `OPENAI_API_KEY` | backend | Required for story selection and article synthesis |
| `OPENAI_MODEL` | backend | Defaults to `gpt-4o-mini` |
| `ALLOWED_ORIGINS` | backend | CORS-allowed frontend origin(s) |

---

## Testing

**Frontend unit tests** ([Vitest](https://vitest.dev/) + React Testing Library):

```bash
npm run test          # run once
npm run test:watch    # watch mode
```

**Backend tests** (pytest, against a real Postgres database — not
SQLite, since search relies on Postgres-specific JSON-cast behavior):

```bash
cd backend
pip install -r requirements-dev.txt
createdb ai_engineer_daily_test   # one-time setup
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/ai_engineer_daily_test"
pytest
```

**End-to-end test** (Playwright — covers the two async Server
Component routes Vitest can't render). Requires the backend running
and seeded (`python init_db.py`) first. Not run in CI — run it
locally before deploying if you've touched those routes:

```bash
npx playwright install --with-deps chromium   # one-time setup
npm run test:e2e
```

Frontend and backend unit tests run in CI on every push/PR — see `.github/workflows/ci.yml`.

---

## Deployment

| Layer | Platform |
|---|---|
| Frontend | [Vercel](https://vercel.com) |
| Backend | [Render](https://render.com) |
| Database | [Neon](https://neon.tech) |
| Scheduled jobs | GitHub Actions (`.github/workflows/ingest.yml`) |

Backend deploys from `render.yaml` (Render Blueprint); tables are created automatically on startup if missing. Frontend uses Vercel's zero-config Next.js detection — no config file needed. Both build on push to `main`.

---

## Roadmap

### Planned

- Semantic search with pgvector
- AI-powered news chat
- Personalized recommendations
- Daily digest email

---

## License

MIT — see [LICENSE](LICENSE).
