# AI Engineer Daily

An AI-powered daily briefing platform that helps software engineers stay up to date with AI in just a few minutes each day.

Built with Next.js, FastAPI, PostgreSQL, and OpenAI.

🌐 **Live Demo:** https://ai-engineer-daily-p09kjojte-ti-a.vercel.app

---

## Architecture

```text
User
    │
    ▼
Next.js (Vercel)
    │
REST API
    ▼
FastAPI (Render)
    │
SQLAlchemy
    ▼
PostgreSQL (Neon)

RSS Sources
(OpenAI / Google AI / Hugging Face)
    │
    ▼
RSS ingestion ──────┐
                     │ GitHub Actions
OpenAI API           │ (scheduled)
    │                │
    ▼                │
AI metadata gen ─────┘
```

Ingestion and AI metadata generation run as scheduled jobs, not request-time work — the API stays fast and stateless.

---

## Core Features

- **Daily briefing homepage** — latest AI news, curated and deduplicated
- **AI-generated metadata** — summary, takeaway, key concepts, and background for every article
- **Search** — full-text search across title, summary, takeaway, and concepts
- **RSS ingestion pipeline** — pulls from OpenAI, Google AI, and Hugging Face, deduplicated by content hash
- **REST API** — FastAPI with typed Pydantic schemas
- **Scheduled automation** — ingestion and AI generation run on a cron via GitHub Actions

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js (App Router), React, TypeScript, Tailwind CSS |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL (Neon) |
| AI | OpenAI API (`gpt-4o-mini`) |
| Infra | Vercel, Render, GitHub Actions |

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
├── main.py               # FastAPI app + CORS
├── app/                  # Routers (news, search)
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── crud.py                # Data access layer
├── config.py               # Environment-driven config
├── ingest_rss.py           # RSS ingestion
└── generate_ai.py          # AI metadata generation

.github/workflows/       # Scheduled ingestion + AI generation
```

---

## How It Works

1. **Ingest** — `ingest_rss.py` pulls articles from configured RSS feeds and inserts new ones, skipping duplicates by a stable content hash.
2. **Enrich** — `generate_ai.py` finds articles missing AI metadata and calls the OpenAI API to generate a summary, takeaway, concepts, and background.
3. **Schedule** — both scripts run on a GitHub Actions cron, so the database stays fresh without a long-running worker.
4. **Serve** — FastAPI exposes the data through a REST API; Next.js renders it server-side and proxies client-side search.

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
uvicorn main:app --reload
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

## Deployment

| Layer | Platform |
|---|---|
| Frontend | [Vercel](https://vercel.com) |
| Backend | [Render](https://render.com) |
| Database | [Neon](https://neon.tech) |
| Scheduled jobs | GitHub Actions (`.github/workflows/ingest.yml`) |

Backend deploys from `render.yaml` (Render Blueprint). Frontend uses Vercel's zero-config Next.js detection — no config file needed. Both build on push to `main`.

---

## Roadmap

- Semantic search
- Related articles
- AI-generated timelines
- Daily digest email
- Personalized feeds

---

## License

MIT — see [LICENSE](LICENSE).
