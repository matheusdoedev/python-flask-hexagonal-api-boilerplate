from app.domain.health import HealthStatus
from app.ports.outbound.clock import Clock


class HealthService:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock

    def execute(self) -> HealthStatus:
        return HealthStatus(status="healthy", timestamp=self._clock.now())
