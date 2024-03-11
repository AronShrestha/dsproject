def test_get_campaigns_campaigns(sales_client, member_data):
    _token = member_data["accessToken"]
    get_campaigns = {
        "query": """
            query getCampaignsList($fetchArchived:Boolean!){
                getCampaignsList(fetchArchived: $fetchArchived) {
                    data {
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
                        isArchived
                        isContactListHidden
                        callScriptId
                        contactListId
                        nextNumberToDial
                        campaignStatus
                        contactCount
                        createdOn
                        createdBy
                        contactListName
                    }
                    error {
                    message
                    errorKey
                    code
                    }
                    status
                }
                }

            """,
        "variables": {"fetchArchived": True},
        "operationName": "getCampaignsList",
    }
    response = sales_client.post(
        "/api/v1/graphql/",
        headers={"Authorization": f"JWT {_token}"},
        json=get_campaigns,
    )
    assert response.json()
    assert response.json()["data"]["getCampaignsList"]["status"] == 200
