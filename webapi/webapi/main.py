from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware import Middleware
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
import os

# load environment variables.
load_dotenv()
from starlette.middleware.cors import CORSMiddleware



from bootstrap import (
    init_database,
)

from starlette.applications import Starlette
from starlette.routing import Mount

from webapi.webapi import config
from webapi.webapi.middlewares import load_middlewares
import bootstrap

# ROUTES = (
#     [
#         Mount(
#             "/api/" + config.API_BASE_VERSION,
#             routes=[
#                 Mount("/graphql/", graphql),
#             ]
#             + common_routes
#             + billing_routes
#             + integration_routes
#             + krispcall_integration_routes,
#         ),
#     ]
#     + routes
#     + callroutes
#     + webmaster_routes
# )
ROUTES = []


def create_app(settings) -> Starlette:
    db = init_database(settings)
    queue = bootstrap.init_queue(settings)
    broadcast = bootstrap.init_broadcaster(settings)
    _middlewares = load_middlewares(settings)
    app = Starlette(
        debug=settings.debug,
        routes=ROUTES,
        middleware=_middlewares,
        on_startup=[
            db.connect,
            queue.connect,
            broadcast.connect,
        ],
        on_shutdown=[db.disconnect, broadcast.disconnect],
    )
    app.state.settings = settings
    app.state.db = db
    app.state.queue = queue
    app.state.broadcast = broadcast
    return app


app = create_app(config.get_application_settings())


# key = bytes(os.getenv("FERNET_PRIVATE_KEY").encode('utf-8'))
# cryptographer = Fernet(key=key)


# Application states.
# app.state.cryptographer = cryptographer

