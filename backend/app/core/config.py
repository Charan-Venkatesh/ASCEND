from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "ASCEND OS"
    environment: str = "local"
    debug: bool = False
    secret_key: str = Field(min_length=16)
    access_token_expire_minutes: int = 45
    refresh_token_expire_days: int = 14
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "ascend_memory"
    frontend_origin: str = "http://localhost:3000"
    nvidia_api_key: str = ""
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_model: str = "meta/llama-3.1-70b-instruct"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    otel_exporter_otlp_endpoint: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
