# AI Engineer Daily

An AI-powered daily briefing platform built with Next.js, FastAPI, and SQLAlchemy to help software engineers stay up to date with AI in just a few minutes a day.

---

## Overview

Instead of manually browsing dozens of AI blogs every day, AI Engineer Daily automatically ingests articles from trusted AI organizations, stores them in a database, and serves them through a REST API.

The current version focuses on building a production-style data pipeline:

- Collect articles from RSS feeds
- Store them in a relational database
- Expose them through a FastAPI backend
- Display them with a modern Next.js frontend

Future versions will enrich every article using OpenAI.

---

## Architecture

```text
Internet (RSS)

        │

        ▼

 RSS Ingestion

        │

        ▼

SQLite Database

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
- SQLAlchemy ORM with SQLite persistence
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
- SQLite

### AI (Planned)

- OpenAI API

### Database (Future Upgrade)

- PostgreSQL
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
- SQLite Database
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
 SQLite Database
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


## Roadmap

### Completed

- ✅ Next.js frontend
- ✅ FastAPI backend
- ✅ REST API
- ✅ SQLite integration
- ✅ SQLAlchemy ORM
- ✅ Pydantic schemas

### In Progress

- RSS ingestion
- AI-generated summaries
- AI-generated takeaways
- Background knowledge generation

### Future

- PostgreSQL
- Search
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
- SQLite database
- SQLAlchemy ORM
- Pydantic schemas

RSS ingestion and AI-generated summaries are currently under development.
