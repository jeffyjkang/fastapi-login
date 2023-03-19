from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    github_client_id: str
    github_client_secret: str
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
