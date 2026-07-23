# AI Engineer Daily

An AI-powered daily briefing platform built with Next.js, FastAPI, and SQLAlchemy to help software engineers stay up to date with AI in just a few minutes a day.

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

| Variable          | Required | Purpose                                                        | Default (if unset)                                                        |
| ----------------- | -------- | --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `DATABASE_URL`    | No       | Full SQLAlchemy connection string — the single source of truth for which database the app uses | `postgresql+psycopg://postgres:postgres@localhost:5432/ai_engineer_daily` |
| `OPENAI_API_KEY`  | Yes, for AI generation | Used by `generate_ai.py` to call the OpenAI API                | none — required, no default                                               |
| `OPENAI_MODEL`    | No       | Overrides the OpenAI model used for AI metadata generation      | `gpt-4o-mini`                                                              |

No credentials are hardcoded anywhere in the codebase — everything comes from the environment.

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

### Future

- Personalized recommendations
- User accounts
- Deployment

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
