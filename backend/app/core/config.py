from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DevMate AI"
    app_version: str = "0.1.0"
    environment: str = "development"

    api_prefix: str = "/api"

    database_url: str = (
        "postgresql+asyncpg://devmate:devmate_password@localhost:5432/devmate"
    )

    redis_url: str = "redis://localhost:6379/0"

    allowed_origins: str = "http://localhost:3000"

    model_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"

    model_name: str = "qwen3:1.7b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()