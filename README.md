# AI Engineer Daily

An AI-powered daily briefing platform built with Next.js, FastAPI, and SQLAlchemy to help software engineers stay up to date with AI in just a few minutes a day.

---

## Live Demo

- Frontend: `<your Vercel URL>` (e.g. `https://ai-engineer-daily.vercel.app`)
- Backend API: `<your Render URL>` (e.g. `https://ai-engineer-daily-api.onrender.com`)

> Fill these in after completing [Production Setup](#production-setup) below. The backend runs on Render's free tier, so the first request after a period of inactivity can take 30-50s while the instance wakes up.

---

## Overview

Instead of manually browsing dozens of AI blogs every day, AI Engineer Daily automatically ingests articles from trusted AI organizations, stores them in a database, and serves them through a REST API.

The current version focuses on building a production-style data pipeline:

- Collect articles from RSS feeds
- Store them in a PostgreSQL database
- Enrich each article with OpenAI-generated summaries, takeaways, concepts, and background
- Expose them through a FastAPI backend, including search
- Display them with a modern Next.js frontend

---

## Architecture

```text
Internet (RSS)

        │

        ▼

 RSS Ingestion

        │

        ▼

PostgreSQL Database

        │

        ▼

 SQLAlchemy ORM

        │

        ▼

 FastAPI REST API

        │

        ▼

 Next.js Frontend
```

---

## Current Features

### Data Pipeline

- Automatic RSS ingestion from major AI organizations
- Duplicate detection using stable article IDs
- SQLAlchemy ORM with PostgreSQL persistence
- FastAPI REST API

### Frontend

- Apple-inspired responsive UI
- Homepage with latest articles
- Individual news detail pages
- Reusable React components

### Backend

- Layered architecture
- CRUD abstraction
- SQLAlchemy ORM
- Pydantic schemas
- RESTful API

---

## RSS Sources

Current RSS feeds include:

- OpenAI
- Google AI
- Hugging Face

(The Anthropic RSS feed is currently unavailable.)

---

## Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL (via the `psycopg` driver)

### AI

- OpenAI API

---

## Current Features

- Homepage
- Daily Brief
- News Detail Page
- AI Takeaways
- Concepts
- Background
- Related News
- Sources
- RESTful API
- PostgreSQL Database
- SQLAlchemy ORM
- Pydantic API Schemas
- Apple-inspired Design System

---

## Architecture

```text
     Browser
        │
        ▼
 Next.js Frontend
        │
    REST API
        │
        ▼
 FastAPI Backend
        │
        ▼
   CRUD Layer
        │
        ▼
  SQLAlchemy ORM
        │
        ▼
 PostgreSQL Database
```

---

## Project Structure

```text
app/                 # Next.js frontend

backend/
├── app/             # FastAPI routers
├── config.py
├── crud.py
├── database.py
├── ingest_rss.py    # RSS ingestion
├── init_db.py       # Development seed data
├── models.py
├── schemas.py
└── main.py

components/
services/
types/

backend/
├── app/
│   └── news.py
├── config.py
├── crud.py
├── database.py
├── models.py
├── schemas.py
├── init_db.py
├── test_db.py
├── main.py
```

---

## Database Setup

The backend uses PostgreSQL, accessed entirely through SQLAlchemy — the same models, CRUD layer, and API routes work unchanged regardless of which PostgreSQL instance you point them at.

### 1. Install PostgreSQL (local development)

On macOS, using Homebrew:

```bash
brew install postgresql@16
brew services start postgresql@16
```

Then create a local database and a role matching your setup (adjust to taste):

```bash
createdb ai_engineer_daily
```

### 2. Required environment variables

**Backend** (`backend/.env.example`):

| Variable          | Required | Purpose                                                        | Default (if unset)                                                        |
| ----------------- | -------- | --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `DATABASE_URL`    | No       | Full SQLAlchemy connection string — the single source of truth for which database the app uses | `postgresql+psycopg://postgres:postgres@localhost:5432/ai_engineer_daily` |
| `OPENAI_API_KEY`  | Yes, for AI generation | Used by `generate_ai.py` to call the OpenAI API                | none — required, no default                                               |
| `OPENAI_MODEL`    | No       | Overrides the OpenAI model used for AI metadata generation      | `gpt-4o-mini`                                                              |
| `ALLOWED_ORIGINS` | No       | Comma-separated list of origins allowed to call the API (CORS) | `http://localhost:3000`                                                    |

**Frontend** (`.env.example`, repo root):

| Variable                     | Required | Purpose                                                                                   | Default (if unset)      |
| ----------------------------- | -------- | ------------------------------------------------------------------------------------------ | ------------------------ |
| `NEXT_PUBLIC_API_BASE_URL`    | No       | Base URL of the FastAPI backend, used for server-side fetches and the `/api/search` proxy | `http://127.0.0.1:8000` |

No credentials are hardcoded anywhere in the codebase — everything comes from the environment. For the frontend, copy `.env.example` → `.env.local` (Next.js loads it automatically, already git-ignored). The backend has no dotenv loader by design (keeps the dependency list minimal) — use `backend/.env.example` as a reference and `export` the variables in your shell, as shown below.

### 3. Local development setup

```bash
cd backend
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/ai_engineer_daily"
pip install -r requirements.txt
```

If your local PostgreSQL doesn't use the `postgres`/`postgres` user and password, adjust `DATABASE_URL` accordingly (or just don't set it, and instead create a role/database that matches the default above).

### 4. Database initialization

Tables are created automatically from the existing SQLAlchemy models — there's no separate migration step or SQL schema file to maintain.

```bash
python init_db.py     # creates tables (if needed) + inserts development seed articles
python ingest_rss.py  # pulls real articles from RSS_FEEDS in config.py
python generate_ai.py # generates AI summary/takeaway/concepts/background (requires OPENAI_API_KEY)
```

`init_db.py` remains the development seed script; `ingest_rss.py` and `generate_ai.py` are additive and safe to re-run (both skip records that already exist).

### 5. Switching between development and production databases

Because `DATABASE_URL` is the only place the database connection is configured, switching environments is just changing that one environment variable — no code changes required:

```bash
# Local development
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/ai_engineer_daily"

# Production (example — use your actual hosted Postgres credentials)
export DATABASE_URL="postgresql+psycopg://user:password@your-db-host:5432/ai_engineer_daily"
```

Then run the backend as usual:

```bash
uvicorn main:app --reload
```

---

## Deployment Architecture

```text
GitHub repo (this monorepo)
   │
   ├─ Vercel          → Next.js frontend (build + deploy on push to main)
   │
   ├─ Render          → FastAPI backend (Web Service, uvicorn)
   │
   ├─ Neon            → managed PostgreSQL (free tier)
   │
   └─ GitHub Actions   → scheduled workflow: ingest_rss.py + generate_ai.py
                          (cron, against production DATABASE_URL / OPENAI_API_KEY)
```

| Layer | Choice | Why |
|---|---|---|
| Frontend | [Vercel](https://vercel.com) | Zero-config Next.js hosting with a generous free tier, automatic HTTPS/CDN, and a verified deployment adapter for this Next.js version. |
| Backend | [Render](https://render.com) (free Web Service) | Deploys the existing `uvicorn` process straight from GitHub, no Dockerfile needed. Free tier; automatic HTTPS. Free instances sleep after 15 minutes of inactivity, so the first request afterward takes ~30-50s to wake up — acceptable for an MVP, see [Limitations](#limitations). |
| Database | [Neon](https://neon.tech) | Serverless PostgreSQL with a generous free tier. Standard `postgresql://` wire protocol, so it works with the existing `psycopg` + SQLAlchemy setup unmodified — just a `DATABASE_URL`. |
| Scheduled ingestion / AI generation | GitHub Actions (`.github/workflows/ingest.yml`) | `ingest_rss.py` and `generate_ai.py` are scripts, not API endpoints. A scheduled Actions workflow (free) runs them against the production database on a cron schedule instead of standing up a separate cron service. |

This keeps the original architecture (`RSS → PostgreSQL → SQLAlchemy → FastAPI → Next.js`) completely unchanged — deployment is purely a matter of *where* each piece runs and how it's configured, not a redesign.

---

## Production Setup

Set these up in order — each step's output feeds the next.

### 1. Database (Neon)

1. Create a free project at [neon.tech](https://neon.tech).
2. Copy the connection string it gives you (it already includes `?sslmode=require`). This is your production `DATABASE_URL`.

### 2. Backend (Render)

1. Push this repo to GitHub (if you haven't already).
2. In the Render dashboard, choose **New → Blueprint** and point it at this repo — it will read `render.yaml` at the repo root and create the API service with the correct build/start commands automatically.
3. In the service's **Environment** tab, set:
   - `DATABASE_URL` — the Neon connection string from step 1
   - `OPENAI_API_KEY` — your OpenAI API key
   - `OPENAI_MODEL` — optional, defaults to `gpt-4o-mini`
   - `ALLOWED_ORIGINS` — your Vercel frontend URL (set after step 3; you can update this later)
4. Deploy. Note the public URL Render gives you (e.g. `https://ai-engineer-daily-api.onrender.com`) — this is your production backend URL.
5. Seed the production database once, from your machine, pointed at the Neon `DATABASE_URL`:
   ```bash
   cd backend
   export DATABASE_URL="<your Neon connection string>"
   export OPENAI_API_KEY="<your OpenAI key>"
   python ingest_rss.py
   python generate_ai.py
   ```
   Do **not** run `init_db.py` against production — it inserts development seed articles.

### 3. Frontend (Vercel)

1. Import this repo into [Vercel](https://vercel.com/new).
2. Set the environment variable `NEXT_PUBLIC_API_BASE_URL` to your Render backend URL from step 2.
3. Deploy. Note the public URL Vercel gives you (e.g. `https://ai-engineer-daily.vercel.app`).
4. Go back to Render and update `ALLOWED_ORIGINS` to this Vercel URL, then redeploy the backend so CORS allows requests from it.

### 4. Scheduled ingestion (GitHub Actions)

1. In the GitHub repo, go to **Settings → Secrets and variables → Actions**.
2. Add repository secrets: `DATABASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL` (same values as the Render service).
3. The `.github/workflows/ingest.yml` workflow runs every 6 hours automatically, and can also be triggered manually from the **Actions** tab (`workflow_dispatch`).

### 5. Fill in the Live Demo links

Update the [Live Demo](#live-demo) section above with your Vercel and Render URLs.

---

## Limitations

- **Cold starts**: Render's free tier sleeps the backend after 15 minutes of inactivity; the first request afterward can take 30-50s. Upgrading to a paid Render instance removes this.
- **No migrations tooling**: tables are created via `Base.metadata.create_all`, which is fine for the current schema but doesn't handle future schema changes — a migration tool (e.g. Alembic) would be needed before altering `models.py` in production.
- **`init_db.py` is dev-only**: it inserts fixed seed articles and must never be run against the production database.
- **Ingestion cadence**: the GitHub Actions cron runs every 6 hours, not in real time — acceptable for a daily-briefing product, but news can lag by up to that window.
- **Single environment**: there's no separate staging deployment; testing happens locally against a local or scratch Postgres database before pushing to `main`.

---


## Roadmap

### Completed

- ✅ Next.js frontend
- ✅ FastAPI backend
- ✅ REST API
- ✅ SQLAlchemy ORM
- ✅ Pydantic schemas
- ✅ RSS ingestion
- ✅ AI-generated summaries, takeaways, concepts, and background
- ✅ Article search
- ✅ PostgreSQL
- ✅ Deployment

### Future

- Personalized recommendations
- User accounts

---


## Design Philosophy

AI Engineer Daily is inspired by Apple's simplicity, OpenAI's clarity, and Linear's information hierarchy.

The goal is not to replicate their interfaces, but to create a focused reading experience that helps engineers understand AI rather than simply consume news.

---

## Status

🚧 Active Development

The project now includes a complete frontend-backend architecture with:

- Next.js frontend
- FastAPI backend
- RESTful API
- PostgreSQL database
- SQLAlchemy ORM
- Pydantic schemas

RSS ingestion, AI-generated summaries, and article search are all functional.
