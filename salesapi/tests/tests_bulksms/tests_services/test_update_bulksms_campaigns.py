import pytest
from krispcall.core.abstracts.shortid import ShortId
from krispcall.bulksms.service_layer import abstracts
from krispcall.bulksms import services


@pytest.mark.asyncio
async def test_update_bulksms_campaigns(
    app_client,
    contact_list_id,
    bulksms_id,
    sms_template_id,
    assignee_id,
    user_auth_id,
    workspace_id,
):
    workspace_id = ShortId(workspace_id).uuid()
    contact_list_id = ShortId(contact_list_id).uuid()
    sms_template_id = ShortId(sms_template_id).uuid()
    assignee_id = ShortId(assignee_id).uuid()
    user = ShortId(user_auth_id).uuid()
    bulksms_id = ShortId(bulksms_id).uuid()
    validated_data = abstracts.UpdateBulkSmsCampaign(
        id=bulksms_id,
        campaign_name="Test Bulk SMS",
        message="message sms template",
        created_by="bishwas wagle",
        skip_csv_upload=True,
        is_contact_list_hidden=True,
        contact_list_id=contact_list_id,
        assignee_id=assignee_id,
        assignee_name="Bishwas",
        sender_number="+98974237498",
        sms_template_id=sms_template_id,
    )
    campaigns = await services.add_bulksms_campaign(
        member=user,
        contact_list_id=contact_list_id,
        validated_data=validated_data,
    )
    assert campaigns
