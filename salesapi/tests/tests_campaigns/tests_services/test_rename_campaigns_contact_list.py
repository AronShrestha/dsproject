import pytest
from krispcall.core.abstracts.shortid import ShortId
from krispcall.campaigns.service_layer import abstracts
from krispcall.campaigns import services


@pytest.mark.asyncio
async def test_rename_campaigns_contact_list(
    sales_client, workspace_id, user_auth_id
):
    workspace_id = ShortId(workspace_id).uuid()
    user = ShortId(user_auth_id).uuid()
    upload_contacts = await services.upload_campaign_contact_list(
        workspace_id=workspace_id,
        contact_list_name="Abin Khatiwada",
        is_list_hidden=True,
        skip_csv_upload=True,
        user=user,
        contact_data=[],
        contact_count=0,
        created_by_name="Abinn Khatiwada",
        db_conn=sales_client.app.state.db,
    )

    assert upload_contacts
