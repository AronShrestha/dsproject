from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware import Middleware
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
import os

from bootstrap import init_database
import bootstrap
from salesapi.salesapi import settings
from salesapi.salesapi.middlewares import load_middlewares

# load environment variables.
load_dotenv()
from starlette.middleware.cors import CORSMiddleware
# from admin.admin import admin as app_admin
# Init application.
routes = [
    # Mount("/user", routes=UserRoutes.routes),
    # Mount("/product", routes=ProductRoutes.routes),
    # Route("/cart", endpoint=add_product_to_cart, methods=["POST"]),
    # Route("/cart", endpoint=get_user_cart, methods=["GET"])
    
]

# Define middleware

# Middlewares.
middlewares = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
]


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


app = create_app(settings.get_application_settings())


app = Starlette(
    routes=routes,
    middleware=middlewares,
)
