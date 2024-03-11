"""
payment worker
"""

from __future__ import annotations

import logging

from arq.connections import RedisSettings
from krispcall.billing.entrypoints.queue_handlers import (
    task_add_free_number,
    task_add_voice_mail_duration,
    task_adjust_price,
    task_charge_caller_id_verification,
    task_charge_credit,
    task_charge_credit_for_bulksms,
    task_charge_inbound_call,
    task_charge_inbound_call_callback,
    task_charge_inbound_call_in_voice_mail,
    task_charge_live_call_listening,
    task_charge_call_whispering,
    task_charge_call_barging,
    task_charge_live_call_listening_callback,
    task_charge_call_whispering_callback,
    task_charge_call_barging_callback,
    task_charge_outbound_call,
    task_charge_outbound_call_callback,
    task_charge_transcription,
    task_charge_transfer_call,
    task_charge_transfer_call_callback,
    task_charge_voice_mail,
    task_email_and_autorecharge,
    task_number_subscription_expired,
    task_autorenewal_of_workspace,
    task_auto_renewal_of_workspace_subscription,
    task_autorenewal_of_number,
    task_auto_renewal_of_number_subscription,
    task_partnerstack_create_customer,
    task_partnerstack_update_customer,
    task_partnerstack_delete_customer,
    task_partnerstack_delete_customer_by_customer_key,
    task_partnerstack_create_transaction,
    task_partnerstack_delete_transaction,
    task_reminder_email_after_expire_subscription,
    task_send_account_suspension_email,
    task_send_data_to_make_webook_on_subscription_status_change,
    task_send_data_to_sendgrid_on_subscription_status_change,
    task_send_email_in_interval,
    task_send_workspace_auto_renewal_status_to_sendgrid,
    task_subscription_cancelled_permanently,
    task_sync_agent_to_analytics,
    update_chargebee_customer_email,
    task_charge_refund_credit_for_bulksms,
)
from krispcall.common.core import bootstrap

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
    ctx["chargebee"] = bootstrap.init_chargebee(ctx["settings"])
    ctx["partnerstack"] = bootstrap.init_partnerstack(ctx["settings"])
    ctx["twilio"] = bootstrap.init_twillo(ctx["settings"])
    ctx["db"] = bootstrap.init_worker_database(ctx["settings"])
    bootstrap.init_rollbar(settings)
    ctx["queue"] = bootstrap.init_queue(ctx["settings"])
    await ctx["db"].connect()
    await ctx["queue"].connect()


async def shutdown(ctx):
    await ctx["db"].disconnect()


class WorkerSettings:
    settings = get_application_settings()

    functions = [
        task_email_and_autorecharge,
        task_subscription_cancelled_permanently,
        task_add_free_number,
        task_send_email_in_interval,
        task_charge_inbound_call,
        task_charge_inbound_call_callback,
        task_charge_transfer_call,
        task_charge_transfer_call_callback,
        task_add_voice_mail_duration,
        task_charge_outbound_call,
        task_charge_outbound_call_callback,
        task_charge_credit,
        task_charge_live_call_listening,
        task_charge_live_call_listening_callback,
        task_charge_call_whispering,
        task_charge_call_whispering_callback,
        task_charge_call_barging,
        task_charge_call_barging_callback,
        task_charge_caller_id_verification,
        task_charge_transcription,
        task_charge_voice_mail,
        task_sync_agent_to_analytics,
        task_charge_inbound_call_in_voice_mail,
        task_adjust_price,
        task_autorenewal_of_workspace,
        task_auto_renewal_of_workspace_subscription,
        task_autorenewal_of_number,
        task_auto_renewal_of_number_subscription,
        task_number_subscription_expired,
        update_chargebee_customer_email,
        task_charge_credit_for_bulksms,
        task_send_account_suspension_email,
        task_partnerstack_create_customer,
        task_partnerstack_update_customer,
        task_partnerstack_delete_customer,
        task_partnerstack_delete_customer_by_customer_key,
        task_partnerstack_create_transaction,
        task_partnerstack_delete_transaction,
        task_reminder_email_after_expire_subscription,
        task_send_workspace_auto_renewal_status_to_sendgrid,
        task_send_data_to_make_webook_on_subscription_status_change,
        task_send_data_to_sendgrid_on_subscription_status_change,
        task_charge_refund_credit_for_bulksms,
    ]
    queue_name = "arq:payment_queue"
    on_startup = startup
    on_shutdown = shutdown

    redis_settings = RedisSettings.from_dsn(settings.redis_settings)
