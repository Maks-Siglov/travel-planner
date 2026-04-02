from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent
env_path = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DB_PATH: str
    ARTIC_BASE_URL: str

    LOG_LEVEL: str
    LOG_IN_CONSOLE: bool
    LOG_FILE: str

    @property
    def db_uri(self) -> str:
        return f"sqlite:///{self.DB_PATH}"


settings = Settings()
