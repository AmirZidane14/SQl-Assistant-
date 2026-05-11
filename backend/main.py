from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database.connection import get_db, init_db, get_table_names
from database.seed_data import seed_database
from api.query_routes import router as query_router
from api.schema_routes import router as schema_router
from api.schema_routes import _load_schema
from api.ai_routes import router as ai_router
from api.workflow_routes import router as workflow_router
from api.admin_routes import router as admin_router

from middleware.rate_limit import RateLimiter
from middleware.security_headers import SecurityHeadersMiddleware
from middleware.request_logging import RequestLoggingMiddleware

app = FastAPI(
    title="AI SQL Query Assistant — Backend",
    description="Converts natural language to SQL queries using AI",
    version="0.1.0",
)

# Security middleware — order matters: rate limit first, then logging, then security headers
app.add_middleware(RateLimiter)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# CORS — allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(query_router)
app.include_router(schema_router)
app.include_router(ai_router)
app.include_router(workflow_router)
app.include_router(admin_router)


@app.on_event("startup")
def on_startup():
    init_db()
    db = next(get_db())
    from database.models import Customer
    count = db.query(Customer).count()
    if count == 0:
        print("[startup] Database empty — running seed...")
        seed_database()
    else:
        print("[startup] Database already seeded — skipping.")
    print("[startup] Loading schema cache...")
    _load_schema()
    print("[startup] Schema cache ready.")


@app.get("/health")
def health_check():
    return {"status": "running"}


@app.get("/tables", dependencies=[Depends(get_db)])
def list_tables(db: Session = Depends(get_db)):
    table_names = get_table_names()
    return {"tables": table_names, "count": len(table_names)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
