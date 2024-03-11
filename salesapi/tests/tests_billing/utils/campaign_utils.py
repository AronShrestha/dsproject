import uuid
from krispcall.billing.service_layer.helpers import business_rules
import asyncio
from krispcall.konference.billing.models import (
    BillingResponse,
    CampaignOutboundCallRequest,
)
from krispcall.konference.billing.enums import BillingTypeEnum
from krispcall.twilio.enums import ActiveStatusEnum, NotActiveStatusEnum
from krispcall.konference.billing.billing_service import BillingService
from tests.tests_billing.utils.models import (
    CampaignCall,
    CampaignCallDataStore,
)
from krispcall.core.abstracts.shortid import ShortId


def get_campaigns_contact_list(contact_list_id, sales_client, member_data):
    _token = member_data["accessToken"]
    get_sms_contact_list = {
        "query": """
            query getCampaignContactDetailList($id: ShortId!) {
                getCampaignContactDetailList(id: $id) {
                    data {
                    id
                    createdOn
                    name
                    number
                    }
                    error {
                    message
                    errorKey
                    code
                    }
                    status
                }
            }
            """,
        "variables": {"id": contact_list_id},
        "operationName": "getCampaignContactDetailList",
    }
    response = sales_client.post(
        "/api/v1/graphql/",
        headers={"Authorization": f"JWT {_token}"},
        json=get_sms_contact_list,
    )
    contacts = response.json()["data"]["getCampaignContactDetailList"]["data"]
    return contacts


async def run_task_call_charge(
    campaign_call_params: CampaignOutboundCallRequest,
    contact: CampaignCall,
    data_store: CampaignCallDataStore,
):

    try:
        call_status = contact.status
        not_active_statuses = {status for status in NotActiveStatusEnum}
        active_statuses = {status for status in ActiveStatusEnum}

        if (
            call_status in not_active_statuses
            or not campaign_call_params.call_sid
        ):
            campaign_call_params.total_participants = 1

        if call_status in active_statuses:
            campaign_call_params.billing_types.append(
                BillingTypeEnum.CALL_CHARGE
            )

            # Running the function and checking assertions
        if contact.elapsed_time <= contact.call_duration:
            result: BillingResponse = (
                await BillingService.execute_campaign_call_transaction(
                    campaign_call_params
                )
            )
            contact.running_total_charge = (
                contact.running_total_charge + result.charge_amount
            )
            contact.charge_amount = (
                contact.charge_amount + result.charge_amount
            )
            contact.elapsed_time = contact.elapsed_time + 1
            contact.status = call_status

            print(f"Charged {contact.elapsed_time} time")

            if contact.elapsed_time == contact.call_duration:
                contact.charge_amount = float(
                    "{0:.4f}".format(contact.charge_amount)
                )
                data_store.update(contact)
            else:
                await asyncio.sleep(1)
                await run_task_call_charge(
                    campaign_call_params, contact, data_store
                )

    except Exception as e:
        print("Error:", e)


async def execute_campaign_call(
    campaign, contact: CampaignCall, data_store: CampaignCallDataStore
):
    conference_id = str(uuid.uuid4())
    call_sid = str(uuid.uuid4())
    contact.call_sid = call_sid
    contact.conference_sid = conference_id
    contact.conference_friendly_name = conference_id

    # Creating a CampaignOutboundCallRequest
    campaign_call_params = CampaignOutboundCallRequest(
        conversation_id=str(uuid.uuid4()),
        conference_friendly_name=str(uuid.uuid4()),
        campaign_id=contact.campaign_id,
        total_participants=business_rules.DEFAULT_TOTAL_PARTICIPANTS,
        billing_types=[
            BillingTypeEnum.SIP_CHARGE,
            BillingTypeEnum.CONFERENCE_CHARGE,
        ],
        call_sid=call_sid,
        child_call_sid=call_sid,
        conference_sid=conference_id,
        to=contact.to,
        from_=contact.from_,
        parent_call_sid=call_sid,
        remarks="",
        workspace_id=ShortId(contact.workspace_id).uuid(),
    )
    await run_task_call_charge(campaign_call_params, contact, data_store)
