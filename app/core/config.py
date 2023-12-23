import os
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    API_V1: str = "/v1"
    sqlite_file_name: str = "vdm.db"
    DB_URL: str = f"sqlite:///{sqlite_file_name}"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.environ['JWT_SECRET_KEY']     # should be kept secret
    JWT_REFRESH_SECRET_KEY: str = os.environ['JWT_REFRESH_SECRET_KEY']      # should be kept secret
