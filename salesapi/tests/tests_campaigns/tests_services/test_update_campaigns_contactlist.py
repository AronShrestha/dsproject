import pytest
from krispcall.core.abstracts.shortid import ShortId
from krispcall.campaigns.service_layer import abstracts
from krispcall.campaigns import services


@pytest.mark.asyncio
async def test_update_campaigns_contact_list(
    sales_client, contact_list_id, user_auth_id
):
    contact_list_id = ShortId(contact_list_id).uuid()
    user = ShortId(user_auth_id).uuid()
    validated_data = abstracts.UpdateCampaignContactList(
        action="Archive",
        name="bishwas test contact",
        archive_contact_list=[contact_list_id],
    )
    update_contact_list = await services.update_campaign_contact_list(
        user_id=user,
        validated_data=validated_data,
        db_conn=sales_client.app.state.db,
    )
    assert update_contact_list
