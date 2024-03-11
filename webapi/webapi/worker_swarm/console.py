from __future__ import annotations

from krispcall.core.log_config import configure_logging
from worker_swarm import settings


class CliCommand:
    def __init__(self):
        _settings = settings.get_application_settings()
        configure_logging(_settings)
