import os
from functools import lru_cache

from pydantic_settings import BaseSettings

CONF_FILE = os.environ.get("CONFFILE", "/app/conf/pdf-service.env")


class Settings(BaseSettings):
    db_host: str
    db_password: str
    db_master_name: str
    db_slave_name: str
    db_user: str
    db_master_port: int
    db_slave_port: int
    db_app_name: str = "pdf"
    image_max_width: int = 1200
    image_max_height: int = 1600

    class Config:
        env_file = CONF_FILE
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()
