from typing import List

from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "HubSpot Clone"
    debug: bool = True
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    postgres_user: str = "hubspot"
    postgres_password: str = "hubspot"
    postgres_db: str = "hubspot"
    postgres_host: str = "db"
    postgres_port: int = 5432

    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    hubspot_access_token: str
    hubspot_base_url: str = "https://api.hubapi.com"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
