import pytest
from krispcall.core.abstracts.shortid import ShortId
from krispcall.bulksms.service_layer import abstracts
from krispcall.bulksms import services


@pytest.mark.asyncio
async def test_rename_bulksms_contact_list(
    app_client, workspace_id, user_auth_id
):
    workspace_id = ShortId(workspace_id).uuid()
    user = ShortId(user_auth_id).uuid()
    upload_contacts = await services.upload_bulksms_contact_list(
        workspace_id=workspace_id,
        contact_list_name="bishwas empty",
        is_list_hidden=True,
        skip_csv_upload=True,
        user=user,
        contact_data=[],
        contact_count=0,
        created_by_name="Bishwas Wagle",
        db_conn=app_client.app.state.db,
    )

    assert upload_contacts
