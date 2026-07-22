# AI Engineer Daily

An AI-powered daily briefing platform built with Next.js, FastAPI, and SQLAlchemy to help software engineers stay up to date with AI in just a few minutes a day.

---

## Overview

AI Engineer Daily delivers a concise daily briefing instead of overwhelming users with dozens of news articles.

Each story includes:

- AI-generated summary
- Full article
- Key takeaway
- Technical concepts
- Background knowledge
- Related news
- Trusted sources

The long-term goal is to help engineers stay current in just a few minutes every day.

---

## Tech Stack

### Frontend

- Next.js
- React
- Tailwind CSS
- TypeScript

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
app/
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
