"""
This script serves as an entry point for running the FastAPI application.
And also provides a CLI for starting the server.


Usage:
- To run the FastAPI server, execute this script directly.
    python main.py serve --host 0.0.0.0 --port 8080
  It will start the server using Uvicorn with default or specified host and port.
- Additionally, the script provides a CLI command 'serve'
  for running the server from the command line with custom host and port settings.
"""

import fire
import uvicorn
from fastapi import FastAPI
# from app.calculator import router

# app = FastAPI()
# app.include_router(router)


class CliCommand:

    def serve(self, host: str = "127.0.0.1", port: int = 8000):
        uvicorn.run(
            "webapi.webapi.main:app",
            host=host,
            port=port,
            log_level="info",
            reload=True,
        )


if __name__ == "__main__":
    fire.Fire(CliCommand)
