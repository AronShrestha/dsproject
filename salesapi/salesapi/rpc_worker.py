from salesapi import settings as config
from krispcall.addon.databases.bootstrap import init_database
from arq.connections import RedisSettings
from krispcall.common.core import bootstrap
from krispcall.bulksms.entrypoints.queue_handlers import (
    save_bulksms_campaign_info,
    task_update_bulksms_estimated_cost,
    task_update_bulksms_campaign,
    task_update_bulksms_create_by_name,
    task_update_bulksms_total_cost,
    task_get_intermediate_state_sms,
)


async def startup(ctx):
    settings = config.get_application_settings()
    ctx["settings"] = settings
    ctx["db"] = init_database(ctx["settings"])
    ctx["broadcaster"] = bootstrap.init_broadcaster(ctx["settings"])
    ctx["queue"] = bootstrap.init_queue(ctx["settings"])
    await ctx["db"].connect()
    await ctx["queue"].connect()
    await ctx["broadcaster"].connect()


async def shutdown(ctx):
    await ctx["db"].disconnect()


class RpcWorker:
    settings = config.get_application_settings()

    functions = [
        save_bulksms_campaign_info,
        task_update_bulksms_estimated_cost,
        task_update_bulksms_campaign,
        task_update_bulksms_create_by_name,
        task_update_bulksms_total_cost,
        task_get_intermediate_state_sms,
    ]
    queue_name = "arq:sales_queue"
    on_startup = startup
    on_shutdown = shutdown

    redis_settings = RedisSettings.from_dsn(settings.redis_settings)
    # if os.environ.get("REDIS_HOST"):
    #     redis_settings = RedisSettings(host=os.environ.get("REDIS_HOST"))
