import pytest
from krispcall.core.abstracts.shortid import ShortId
from krispcall.campaigns.service_layer import abstracts
from krispcall.campaigns import services


@pytest.mark.asyncio
async def test_update_campaigns_campaigns(
    app_client,
    contact_list_id,
    campaigns_id,
    sms_template_id,
    assignee_id,
    user_auth_id,
):
    workspace_id = ShortId(workspace_id).uuid()
    contact_list_id = ShortId(contact_list_id).uuid()
    sms_template_id = ShortId(sms_template_id).uuid()
    assignee_id = ShortId(assignee_id).uuid()
    user = ShortId(user_auth_id).uuid()
    campaigns_id = ShortId(campaigns_id).uuid()
    validated_data = abstracts.UpdateCampaign(
        id=campaigns_id,
        campaign_name="Test Bulk SMS",
        message="message sms template",
        created_by="Abinn Khatiwada",
        skip_csv_upload=True,
        is_contact_list_hidden=True,
        contact_list_id=contact_list_id,
        assignee_id=assignee_id,
        assignee_name="Abin",
        sender_number="+98974237498",
        sms_template_id=sms_template_id,
    )
    campaigns = await services.create_campaign(
        member=user,
        contact_list_id=contact_list_id,
        validated_data=validated_data,
    )
    assert campaigns
