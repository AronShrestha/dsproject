import pytest
from krispcall.core.abstracts.shortid import ShortId
from krispcall.bulksms.service_layer import abstracts
from krispcall.bulksms import services


@pytest.mark.asyncio
async def test_add_bulksms_contact_detail(
    app_client, contact_list_id, user_auth_id, contact_ids
):
    contact_list_id = ShortId(contact_list_id).uuid()
    user = ShortId(user_auth_id).uuid()
    validated_data = abstracts.AddBulkSmsContactDetail(
        contacts=contact_ids, contact_list_id=contact_list_id
    )
    contact_detail = await services.add_bulksms_contact_detail(
        validated_data=validated_data,
        user=user,
        db_conn=app_client.app.state.db,
    )
    assert contact_detail
