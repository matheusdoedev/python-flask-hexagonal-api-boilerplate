from typing import Protocol
from app.domain.health import HealthStatus


class HealthQuery(Protocol):
    def execute(self) -> HealthStatus: ...
