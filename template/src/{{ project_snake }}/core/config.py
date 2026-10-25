"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        frozen=True,
    )

    app_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    uvicorn_host: str = "0.0.0.0"  # noqa: S104 - bind all interfaces inside containers
    uvicorn_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True


def get_settings() -> Settings:
    """Load settings from environment."""
    return Settings()
