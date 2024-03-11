from __future__ import annotations

import asyncio

from rpc.rpc.settings import get_application_settings
from rpc.rpc.main import server


class CliCommand:
    """Rpc api cli command"""

    def __init__(self):
        _settings = get_application_settings()
        self.settings = _settings

    def serve(self):
        asyncio.run(server(self.settings))
