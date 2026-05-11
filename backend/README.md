# AI SQL Query Assistant — Backend (Phase 1)

## Setup

```bash
cd backend
cp .env.example .env          # Optional: copy and fill in values
pip install -r requirements.txt
python main.py               # or: uvicorn main:app --reload
```

The server starts on **http://localhost:8000**.

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/health` | Server health check |
| `GET` | `/tables` | List all database table names |

## Database

- SQLite file: `sqlassistant.db` (created automatically in the `backend/` folder)
- On first startup, tables are created and seeded with ~25 customers, 20 products, 40 orders, and 40 payments

## To re-seed the database

Delete `sqlassistant.db` and restart the server, or run:

```bash
python database/seed_data.py
```

## Next Phase

Phase 2 adds the AI-powered SQL generation endpoint (`POST /api/generate`), a SQL safety validator, and a schema inspector that returns full column/relationship information.