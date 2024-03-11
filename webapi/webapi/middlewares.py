from __future__ import annotations
import typing
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseSettings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from functools import partial
import pendulum

utc_now = partial(pendulum.now, "UTC")

class ResponseMiddleware(BaseHTTPMiddleware):
    """attach date to response header"""

    async def dispatch(self, request, call_next):
        """ """
        response = await call_next(request)
        response.headers["Response-Time"] = utc_now().isoformat()
        return response

def load_middlewares(settings: BaseSettings) -> typing.List[Middleware]:
    return [
        Middleware(ResponseMiddleware),
        Middleware(
            CORSMiddleware,
            allow_origins=settings.cors_allow_origins,
            allow_methods=settings.cors_allow_methods,
            allow_headers=settings.cors_allow_headers,
            allow_credentials=settings.cors_allow_credentials,
            expose_headers=settings.cors_expose_headers,
            max_age=settings.cors_max_age,
        ),
        # Load session middleware
        Middleware(
            SessionMiddleware,
            secret_key=settings.secret_key.get_secret_value(),
            max_age=settings.session_lifetime,
        ),
    ]
