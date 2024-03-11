"""
"""
from __future__ import annotations

import logging

import msgpack  # type: ignore
from arq import cron
from arq.connections import RedisSettings
import bootstrap


# from krispcall.webmaster.entrypoints.queue_handlers import send_webmaster_email

from webapi.webapi import config

# from arq import cron


def deserializer(b):
    return msgpack.unpackb(b, raw=False)


async def startup(ctx):
    settings = config.get_application_settings()
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(message)s",
        handlers=[logging.StreamHandler()],
    )

    ctx["settings"] = settings
    ctx["db"] = bootstrap.init_worker_database(ctx["settings"])
    ctx["broadcaster"] = bootstrap.init_broadcaster(ctx["settings"])
    ctx["queue"] = bootstrap.init_queue(ctx["settings"])
    await ctx["broadcaster"].connect()
    # await ctx["db"].connect()
    await ctx["queue"].connect()


async def shutdown(ctx):
    await ctx["db"].disconnect()
    await ctx["broadcaster"].disconnect()

async def test_job(ctx):
    pass


class WorkerSettings:
    settings = config.get_application_settings()


    functions = [
        # send_webmaster_email
        test_job
    ]

    queue_name = "arq:general_queue"
    on_startup = startup
    on_shutdown = shutdown

    redis_settings = RedisSettings.from_dsn(settings.redis_settings)
    # if os.environ.get("REDIS_HOST"):
    #     redis_settings = RedisSettings(host=os.environ.get("REDIS_HOST"))
