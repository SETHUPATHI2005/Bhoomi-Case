import pathlib
from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    app_name: str = "Land Cases Search API"
    debug: bool = False
    admin_username: str = "admin"
    admin_password: str = "devtoken123"
    jwt_secret: str = "your-secret-key-change-in-prod"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    database_url: str = "sqlite:///./land_cases.db"
    redis_url: str = ""

    max_upload_size_mb: int = 50
    rate_limit_per_minute: int = 60

    # Email Configuration
    resend_api_key: str = ""
    sendgrid_api_key: str = ""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    sender_email: str = "noreply@bhoomi.local"
    sender_name: str = "Bhoomi Land Cases"
    enable_email: bool = True

    # Email Verification
    email_verification_expiry_hours: int = 24
    password_reset_expiry_hours: int = 24

    cors_origins: list = ["*"]

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=str(pathlib.Path(__file__).resolve().parents[3] / ".env"),
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("debug", "enable_email", mode="before")
    @classmethod
    def _parse_flexible_bool(cls, value):
        """Accept flexible boolean-like env values such as 'release'/'dev'."""
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        normalized = str(value).strip().lower()
        return normalized in {"1", "true", "yes", "on", "debug", "development", "dev"}


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
