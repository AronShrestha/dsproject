"""
twilio worker
"""
from __future__ import annotations

import logging

from arq import cron
from arq.connections import RedisSettings
from krispcall.channel.entrypoints.queue_handlers import (
    add_conversations_to_db,
    handle_failed_conversation_events,
    run_bulksms_campaign,
    send_conversation,
    send_zapier_conversation,
    task_auto_reply_to_client,
    task_contact_open_state,
    task_delete_twilio_conversation,
    task_estimate_bulksms_cost,
    unarchive_contact_on_call,
    refetch_sms_service_status,
)
from krispcall.common.core import bootstrap
from krispcall.foundation.entrypoints.queue_handlers import (
    create_workspace_sub_account,
    get_sms_price_function,
    rename_workspace_sub_account,
    update_mobile_credentials,
    update_workspace_twilio_sub_account,
)
from krispcall.provider.entrypoints.queue_handlers import (
    agent_queue_service,
    agent_termination_service,
    append_new_leg,
    call_transfer_service,
    check_usage_metrics,
    complete_broken_pipe_calls,
    end_conference_call,
    fetch_and_update_recording,
    handle_terminated_calls,
    ivr_queue_service,
    limit_housekeeping,
    outgoing_queue_service,
    purchase_numbers,
    release_number,
    rename_number,
    setup_ivr,
    setup_routes,
    task_archive_and_release_numbers,
    termination_service,
    update_conference_data,
)

from webapi import config
from webapi.config import get_application_settings


async def startup(ctx):
    settings = get_application_settings()
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(message)s",
        handlers=[logging.StreamHandler()],
    )
    ctx["settings"] = settings
    ctx["payment"] = bootstrap.init_payment_service(ctx["settings"])
    ctx["twilio"] = bootstrap.init_twillo(ctx["settings"])
    ctx["db"] = bootstrap.init_worker_database(ctx["settings"])
    ctx["broadcaster"] = bootstrap.init_broadcaster(ctx["settings"])
    ctx["queue"] = bootstrap.init_queue(ctx["settings"])
    bootstrap.init_rollbar(settings)
    await ctx["broadcaster"].connect()
    await ctx["db"].connect()
    await ctx["queue"].connect()


async def shutdown(ctx):
    await ctx["db"].disconnect()


class WorkerSettings:
    settings = get_application_settings()
    cron_jobs = [
        cron(
            get_sms_price_function,
            hour={7},  # run the job every day at 7:15 AM.
            minute={15},
        )
    ]

    functions = [
        # twilio tasks
        create_workspace_sub_account,
        rename_workspace_sub_account,
        update_mobile_credentials,
        send_conversation,
        setup_routes,
        purchase_numbers,
        setup_ivr,
        release_number,
        handle_failed_conversation_events,
        complete_broken_pipe_calls,
        task_contact_open_state,
        add_conversations_to_db,
        outgoing_queue_service,
        unarchive_contact_on_call,
        call_transfer_service,
        agent_termination_service,
        termination_service,
        update_conference_data,
        append_new_leg,
        agent_queue_service,
        task_auto_reply_to_client,
        ivr_queue_service,
        rename_number,
        end_conference_call,
        check_usage_metrics,
        limit_housekeeping,
        fetch_and_update_recording,
        run_bulksms_campaign,
        task_estimate_bulksms_cost,
        update_workspace_twilio_sub_account,
        handle_terminated_calls,
        task_archive_and_release_numbers,
        send_zapier_conversation,
        task_delete_twilio_conversation,
        refetch_sms_service_status,
    ]
    queue_name = "arq:twilio_queue"
    on_startup = startup
    on_shutdown = shutdown

    redis_settings = RedisSettings.from_dsn(settings.redis_settings)

    # if os.environ.get("REDIS_HOST"):
    #     redis_settings = RedisSettings(host=os.environ.get("REDIS_HOST"))
