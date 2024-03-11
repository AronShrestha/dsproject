"""
application cli
"""
from __future__ import annotations

import fire  # type: ignore

# from analyticsapi.console import CliCommand as AnalyticsapiCommand
# from automationapi.console import CliCommand as AutomationapiCommand
from rpc.rpc.console import CliCommand as RPCApiCommand
from salesapi.salesapi.console import CliCommand as SalesApiCommand
from webapi.webapi.console import CliCommand as WebapiCommand


class Command:
    def __init__(self):
        self.webapi = WebapiCommand()
        # self.analyticsapi = AnalyticsapiCommand()
        self.salesapi = SalesApiCommand()
        # self.automationapi = AutomationapiCommand()
        self.rpc = RPCApiCommand()


if __name__ == "__main__":
    fire.Fire(Command)