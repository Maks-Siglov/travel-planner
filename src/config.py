from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
PROJECT_ROOT = Path(__file__).parent.parent
env_path = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    @property
    def db_uri(self) -> str:
        return ...

# Create global settings instance
settings = Settings()
