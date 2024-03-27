import sys
import logging
from typing import Any, Dict, List
from pydantic_settings import BaseSettings

# Define logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["console"], "level": "INFO"},
        "ktltat": {"handlers": ["console"], "level": "INFO", "propagate": True},
    },
}
class Settings(BaseSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "KTLTAT"
    version: str = "0.0.0"
    database_url: str = ""
    echo_sql: bool = False
    test: bool = False
    allowed_hosts: List[str] = ["*"]
    base_domain: str = "127.0.0.1"
    base_url: str = "http://127.0.0.1:9000"
    salt: str = "salt"
    cookie_session_timeout: int = 60*10 #seconds

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

settings = Settings()
