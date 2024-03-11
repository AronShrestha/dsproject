def test_get_bulksms_campaigns(app_client, member_data):
    _token = member_data["accessToken"]
    get_sms_campaigns = {
        "query": """
            query getBulkSmsCampaignList($fetchArchived:Boolean!){
                getBulkSmsCampaignList(fetchArchived: $fetchArchived) {
                    data {
                        id
                        campaignName
                        createdOn
                        createdBy
                        totalContacts
                        campaignStatus
                        message
                        assigneeId
                        assigneeName
                        contactListId
                        smsTemplateId
                        createdBy
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
        "variables": {"params": {"first": 100}},
        "operationName": "getBulkSmsCampaignList",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={"Authorization": f"JWT {_token}"},
        json=get_sms_campaigns,
    )
    assert response.json()
    assert response.json()["data"]["getBulkSmsCampaignList"]["status"] == 200
