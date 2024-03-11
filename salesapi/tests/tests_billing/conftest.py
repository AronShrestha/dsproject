import json
from uuid import uuid4
from krispcall.common.core.bootstrap import JobQueue
import pytest
from unittest.mock import patch

from tests.tests_billing.utils.constant import CONTACT_CSV_FILE_PATH
from salesapi.settings import get_application_settings

scope = "function"


@pytest.fixture(scope=scope)
def get_campaign_name():
    return _get_campaign_name()


@pytest.fixture(scope=scope)
def test_create_campaigns_campaigns_with_csv(
    sales_client, member_data, get_campaign_name
):
    return _create_campaigns_campaign_with_csv(
        sales_client, member_data, get_campaign_name
    )


@pytest.fixture(scope=scope)
def test_get_campaign(
    sales_client,
    member_data,
    get_campaign_name,
    test_create_campaigns_campaigns_with_csv,
):
    return _test_get_campaign(
        sales_client,
        member_data,
        get_campaign_name,
    )


@pytest.fixture(scope=scope)
def contact_list_id(test_get_campaign):
    return test_get_campaign["contactListId"]


@pytest.fixture(scope=scope)
def mock_get_workspace_credit():
    with patch(
        "krispcall.konference.adapters.provider.get_workspace_credit"
    ) as mock:
        yield mock


@pytest.fixture(scope=scope)
def mock_call_charge_transaction():
    with patch(
        "krispcall.konference.adapters.provider.call_charge_transaction"
    ) as mock:
        yield mock


@pytest.fixture(scope="session")
async def connect_queue(request):
    """Queue"""
    settings = get_application_settings()
    redis_settings = settings.redis_settings
    queue = JobQueue(redis_settings)
    await queue.connect()
    yield queue


def _get_campaign_name():
    return f"test campaign {uuid4()}"


def _test_create_campaigns_campaigns(
    sales_client, member_data, get_campaign_name
):
    _token = member_data["accessToken"]
    create_campaign_payload = {
        "query": """
        mutation createCampaigns($data: CreateCampaignsInputData! ) {
            createCampaigns(data: $data) {
            status
            error {
                message
                code
            }
            data {
                success
            }
            }
        }
        """,
        "variables": {
            "data": {
                "assigneeId": "7Nwrk6YY5Vn7CYEXV9S47Q",
                "assigneeName": "Nawaraj Subedi",
                "callAttemptCount": 0,
                "callAttemptGap": 0,
                "callScriptId": "",
                "campaignName": f"{get_campaign_name}",
                "contactListId": "KVKUHLoDHYVoJTCxM7gGXP",
                "coolOffPeriod": 10,
                "createdByName": "Nawaraj Subedi",
                "dataCenter": "USA",
                "dialingNumber": "+12052363970",
                "dialingNumberId": "VWKH2tQgo8QGNZW2ao2x5J",
                "file": "",
                "isAttemptsPerCallEnabled": False,
                "isCallRecordingEnabled": False,
                "isCallScriptEnabled": False,
                "isContactListHidden": True,
                "isCoolOffPeriodEnabled": True,
                "isVoicemailEnabled": True,
                "skipCsvUpload": True,
                "voiceMailId": "4TgwMgpid26MnUrQLcwmpW",
            }
        },
        "operationName": "createCampaigns",
    }
    response = sales_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=create_campaign_payload,
    )
    return response.json()["data"]


def _create_campaigns_campaign_with_csv(
    sales_client, member_data, get_campaign_name
):
    token = member_data["accessToken"]
    api_uri = "/api/v1/graphql/"

    query = """
        mutation createCampaigns($data: CreateCampaignsInputData! ) {
                createCampaigns(data: $data) {
                status
                error {
                    message
                    code
                }
                data {
                    success
                }
                }
            }
    """

    variables = {
        "data": {
            "assigneeId": "7Nwrk6YY5Vn7CYEXV9S47Q",
            "assigneeName": "Nawaraj Subedi",
            "callAttemptCount": 0,
            "callAttemptGap": 0,
            "callScriptId": None,
            "campaignName": f"{get_campaign_name}",
            "contactListId": "KVKUHLoDHYVoJTCxM7gGXP",
            "coolOffPeriod": 10,
            "createdByName": "Nawaraj Subedi",
            "dataCenter": "USA",
            "dialingNumber": "+12052363970",
            "dialingNumberId": "VWKH2tQgo8QGNZW2ao2x5J",
            "file": None,
            "isAttemptsPerCallEnabled": False,
            "isCallRecordingEnabled": False,
            "isCallScriptEnabled": False,
            "isContactListHidden": True,
            "isCoolOffPeriodEnabled": True,
            "isVoicemailEnabled": True,
            "skipCsvUpload": False,
            "voiceMailId": "4TgwMgpid26MnUrQLcwmpW",
        }
    }

    operations = json.dumps({"query": query, "variables": variables})
    map = json.dumps({"file": ["variables.data.file"]})
    file = open(CONTACT_CSV_FILE_PATH, "rb")

    response = sales_client.post(
        api_uri,
        data={"operations": operations, "map": map},
        files={"file": file},
        headers={"Authorization": f"JWT {token}"},
    )

    return response.json()["data"]


def build_auth_headers(_token, content_type="application/json"):
    return {"Content-Type": content_type, "Authorization": f"JWT {_token}"}


def _test_get_campaign(
    sales_client,
    member_data,
    get_campaign_name,
):
    campaign_name = get_campaign_name
    _token = member_data["accessToken"]

    get_campaign_payload = {
        "query": """
            query getCampaignsList($fetchArchived: Boolean!, $params: CampaignListCursor) {
                    getCampaignsList(fetchArchived: $fetchArchived, params: $params) {
                        data {
                        edges {
                            cursor
                                node {
                                id
                                workspaceId
                                campaignName
                                assigneName
                                assigneId
                                dialingNumber
                                dialingNumberId
                                callingDatacenter
                                callRecordingEnabled
                                voicemailEnabled
                                voicemailId
                                cooloffPeriodEnabled
                                coolOffPeriod
                                callAttemptsEnabled
                                callAttemptsCount
                                callAttemptsGap
                                callScriptEnabled
                                callScriptId
                                contactListId
                                nextNumberToDial
                                campaignStatus
                                contactCount
                                contactListName
                            }
                        }
                    }
                status
            }
            }""",
        "operationName": "getCampaignsList",
        "variables": {
            "fetchArchived": False,
            "params": {
                "after": None,
                "first": 1,
                "search": {
                    "columns": ["campaignName"],
                    "value": f"{campaign_name}",
                },
            },
        },
    }

    response = sales_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=get_campaign_payload,
    )
    campaign_list = response.json()["data"]["getCampaignsList"]

    return campaign_list["data"]["edges"][0]["node"]
