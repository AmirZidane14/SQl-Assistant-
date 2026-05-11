from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

from core.config import settings

# Engine is created once at module load time.
# StaticPool keeps connections alive in-memory so SQLite works correctly.
# check_same_thread=False allows multi-threaded access (FastAPI runs each request on a separate thread).
connect_args = {"check_same_thread": False}
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    poolclass=StaticPool,
    echo=settings.is_development,
)

# SessionLocal creates database sessions bound to this engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the declarative class — all SQLAlchemy models inherit from it.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that injects a database session into route handlers.
    Ensures the session is closed after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Creates all tables defined in the models.
    Import all models here so SQLAlchemy's Base.metadata knows about them.
    Call this once at startup to ensure the schema exists.
    """
    # Import all models so Base.metadata registers them before create_all
    from database import models  # noqa: F401
    Base.metadata.create_all(bind=engine)


def get_table_names():
    """
    Inspects the database and returns a list of all table names.
    Used by the /tables endpoint.
    """
    inspector = inspect(engine)
    return inspector.get_table_names()