from __future__ import annotations
import uvicorn
from salesapi.salesapi import settings


class CliCommand:
    """Sales dialer cli command"""

    # def __init__(self) -> None:
    #     _settings = settings.get_application_settings()
    #     self.alembic = AlembicCommand(_settings)

    def serve(self, host: str = "127.0.0.1", port: int = 8002):
        """Serves the sales dialer api"""
        uvicorn.run(
            "salesapi.salesapi.main:app",
            host=host,
            port=port,
            log_level="info",
            reload=True,
        )
