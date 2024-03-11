from salesapi import settings as config
from krispcall.addon.databases.bootstrap import init_database
from arq.connections import RedisSettings
from krispcall.common.core import bootstrap
from krispcall.konference.entrypoints import queue_handlers
from krispcall.campaigns.entrypoints import queue_handlers as camp_queues
from krispcall.konference.billing import billing_task_queue as billing_queues


async def test(ctx):
    print("This is test")


async def startup(ctx):
    settings = config.get_application_settings()
    ctx["settings"] = settings
    ctx["db"] = init_database(ctx["settings"])
    ctx["twilio"] = bootstrap.init_twillo(ctx["settings"])
    ctx["broadcaster"] = bootstrap.init_broadcaster(ctx["settings"])
    ctx["queue"] = bootstrap.init_queue(ctx["settings"])
    await ctx["db"].connect()
    await ctx["queue"].connect()
    await ctx["broadcaster"].connect()


async def shutdown(ctx):
    await ctx["db"].disconnect()


class PDWorker:
    settings = config.get_application_settings()

    functions = [
        queue_handlers.handle_campaign_conversation_end,
        camp_queues.update_campaign_calls,
        camp_queues.update_campaign_duration,
        camp_queues.create_campaign_stats,
        camp_queues.update_next_number_to_dial,
        camp_queues.update_dialed_contacts,
        camp_queues.end_campaign,
        queue_handlers.queue_conversation,
        queue_handlers.add_participant_call,
        queue_handlers.add_agent_to_conversation,
        queue_handlers.hold_conversation_by_id,
        billing_queues.task_campaign_call_charge,
        queue_handlers.expire_cache,
        test,
    ]
    queue_name = "arq:pd_queue"
    on_startup = startup
    on_shutdown = shutdown

    redis_settings = RedisSettings.from_dsn(settings.redis_settings)
    # if os.environ.get("REDIS_HOST"):
    #     redis_settings = RedisSettings(host=os.environ.get("REDIS_HOST"))
