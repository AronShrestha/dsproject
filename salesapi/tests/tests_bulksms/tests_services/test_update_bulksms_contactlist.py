import pytest
from krispcall.core.abstracts.shortid import ShortId
from krispcall.bulksms.service_layer import abstracts
from krispcall.bulksms import services


@pytest.mark.asyncio
async def test_update_bulksms_contact_list(
    app_client, contact_list_id, user_auth_id
):
    contact_list_id = ShortId(contact_list_id).uuid()
    user = ShortId(user_auth_id).uuid()
    validated_data = abstracts.UpdateBulkSmsContactList(
        action="Archive",
        name="bishwas test contact",
        archive_contact_list=[contact_list_id],
    )
    update_contact_list = await services.update_bulksms_contact_list(
        user_id=user,
        validated_data=validated_data,
        db_conn=app_client.app.state.db,
    )
    assert update_contact_list
