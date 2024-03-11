import pytest
from krispcall.core.abstracts.shortid import ShortId
from krispcall.bulksms.service_layer import abstracts
from krispcall.bulksms import services


@pytest.mark.asyncio
async def test_drop_bulksms_template(app_client, workspace_id, template_id):
    template_id = ShortId(template_id).uuid()
    workspace_id = ShortId(workspace_id).uuid()
    validated_data = abstracts.BulkSmsTemplate(id=template_id)
    default_template = await services.drop_bulksms_template(
        workspace_id=workspace_id,
        validated_data=validated_data,
        db_conn=app_client.app.state.db,
    )
    assert default_template
