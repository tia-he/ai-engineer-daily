# AI Engineer Daily

An AI-powered news platform that automatically ingests AI news from trusted sources, enriches each article with LLM-generated insights, and delivers concise daily briefings for software engineers. Instead of overwhelming users with dozens of AI news articles every day, AI Engineer Daily automatically aggregates trusted sources and uses LLMs to generate concise, actionable briefings in just a few minutes.

**Tech Stack:** Next.js · React · TypeScript · FastAPI · PostgreSQL · OpenAI

[![CI](https://github.com/tia-he/ai-engineer-daily/actions/workflows/ci.yml/badge.svg)](https://github.com/tia-he/ai-engineer-daily/actions/workflows/ci.yml)

🌐 **Live Demo:** https://ai-engineer-daily-p09kjojte-ti-a.vercel.app

> **Note:** The backend is hosted on Render's free tier and may take a few seconds to wake up on the first request.

---

## Architecture

```text
                  RSS Sources
(OpenAI · Google AI · Hugging Face)
                         │
                         ▼
              GitHub Actions (Cron)
                         │
              ingest_rss.py
                         │
                         ▼
                 PostgreSQL (Neon)
                         │
              generate_ai.py
               (OpenAI API)
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

The ingestion and AI enrichment pipelines run asynchronously on scheduled GitHub Actions workflows rather than during API requests, keeping the backend stateless and responsive.

---

## Core Features

- **Daily AI Briefing** — curated AI news from trusted sources
- **AI-generated Metadata** — summary, takeaway, key concepts, and background for every article
- **Full-text Search** — search across titles, summaries, takeaways, and concepts
- **Responsive UI** — optimized for desktop and mobile
- **Automated RSS ingestion** with content-hash deduplication
- **Scheduled AI enrichment** powered by the OpenAI API

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

## Screenshots

### Homepage

![Homepage](docs/home.jpg)

### Article Detail (Top)

![Article](docs/article_1.jpg)

### Article Detail (Bottom)

![Article](docs/article_2.jpg)

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
├── ingest_rss.py           # RSS ingestion
└── generate_ai.py          # AI metadata generation

.github/workflows/       # CI + scheduled ingestion
```

---

## How It Works

1. **Ingest** — `ingest_rss.py` pulls articles from configured RSS feeds and inserts new ones, skipping duplicates by a stable content hash.
2. **Enrich** — `generate_ai.py` finds articles missing AI metadata and calls the OpenAI API to generate a summary, takeaway, concepts, and background.
3. **Schedule** — both scripts run on a GitHub Actions cron, so the database stays fresh without a long-running worker.
4. **Serve** — FastAPI exposes the data through a REST API, while Next.js renders pages using the App Router and performs client-side search. Since ingestion and AI enrichment are handled asynchronously by scheduled GitHub Actions workflows, API requests remain lightweight and stateless.

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
python ingest_rss.py    # real RSS articles
python generate_ai.py   # AI metadata (requires OPENAI_API_KEY)
```

| Variable | Where | Purpose |
|---|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | frontend | Backend API base URL |
| `DATABASE_URL` | backend | PostgreSQL connection string |
| `OPENAI_API_KEY` | backend | Required for AI metadata generation |
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
