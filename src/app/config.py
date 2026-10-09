import os
from dataclasses import dataclass


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True, slots=True)
class Settings:
    environment: str
    log_level: str
    max_content_length: int
    rate_limit: str
    rate_limit_storage_uri: str
    trust_proxy: bool

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            environment=os.getenv("APP_ENV", "production"),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            max_content_length=int(os.getenv("MAX_CONTENT_LENGTH", "1048576")),
            rate_limit=os.getenv("RATE_LIMIT", "60 per minute"),
            rate_limit_storage_uri=os.getenv("RATELIMIT_STORAGE_URI", "memory://"),
            trust_proxy=_as_bool(os.getenv("TRUST_PROXY", "false")),
        )
