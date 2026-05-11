from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Build the absolute path to the database file relative to this file's location
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "sqlassistant.db"


class Settings:
    """
    Application-wide settings loaded from environment variables.
    Centralizes all configuration so it can be imported anywhere.
    """

    # Database connection string
    # Default to SQLite in the project root; can be overridden for MySQL/PostgreSQL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DATABASE_PATH.as_posix()}"
    )

    # Gemini API key for AI features
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Environment mode (development / production)
    ENV: str = os.getenv("ENV", "development")

    @property
    def is_development(self) -> bool:
        return self.ENV == "development"


# Singleton instance — import this throughout the app instead of creating new Settings()
settings = Settings()