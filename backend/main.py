from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database.connection import get_db, init_db, get_table_names
from database.seed_data import seed_database

app = FastAPI(
    title="AI SQL Query Assistant — Backend",
    description="Converts natural language to SQL queries using AI",
    version="0.1.0",
)

# Allow the Next.js frontend running on port 3000 to call these APIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """
    On every startup:
    1. Create the DB schema (all tables)
    2. Seed with sample data (only if tables are empty)
    """
    init_db()
    # Check if tables are already seeded by checking if customers exist
    db = next(get_db())
    from database.models import Customer
    count = db.query(Customer).count()
    if count == 0:
        print("[startup] Database empty — running seed...")
        seed_database()
    else:
        print("[startup] Database already seeded — skipping.")


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Frontend and load balancers use this to verify the server is up.
    """
    return {"status": "running"}


@app.get("/tables", dependencies=[Depends(get_db)])
def list_tables(db: Session = Depends(get_db)):
    """
    Returns a list of all table names in the connected database.
    The frontend uses this to build the schema browser sidebar.
    """
    table_names = get_table_names()
    return {"tables": table_names, "count": len(table_names)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)