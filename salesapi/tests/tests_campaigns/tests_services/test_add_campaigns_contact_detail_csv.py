import pytest
from krispcall.core.abstracts.shortid import ShortId
from krispcall.campaigns.service_layer import abstracts
from krispcall.campaigns import services


@pytest.mark.asyncio
async def test_add_campaigns_contact_detail_csv(
    sales_client, contact_list_id, user_auth_id, contact_ids
):
    contact_list_id = ShortId(contact_list_id).uuid()
    member_id = sales_client.user.get_claim("member_id", ShortId).uuid()
    user = ShortId(user_auth_id).uuid()
    contact_detail = await services.upload_contact_detail_csv(
        member=member_id,
        user=user,
        contact_data=[],
        total_records=0,
        contact_list_id=contact_list_id,
        db_conn=sales_client.app.state.db,
    )
    assert contact_detail
