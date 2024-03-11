import pytest
from krispcall.core.abstracts.shortid import ShortId
from krispcall.bulksms.service_layer import abstracts
from krispcall.bulksms import services


@pytest.mark.asyncio
async def test_create_bulksms_template(app_client, workspace_id, user_auth_id):
    workspace_id = ShortId(workspace_id).uuid()
    member = ShortId(user_auth_id).uuid()
    validated_data = abstracts.UpdateBulkSmsTemplate(
        title="Test Bulk SMS update",
        message="message updated sms template",
        created_by="bishwas wagle",
    )
    update_template = await services.add_bulksms_template(
        workspace_id=workspace_id,
        validated_data=validated_data,
        db_conn=app_client.app.state.db,
    )
    assert update_template
