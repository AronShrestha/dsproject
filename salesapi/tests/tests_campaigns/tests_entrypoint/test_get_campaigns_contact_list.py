def test_get_campaigns_contact_list(sales_client, member_data):
    _token = member_data["accessToken"]
    get_sms_contact_list = {
        "query": """
            query getCampaignContactList($id:ShortId!) {
                getCampaignContactList(id: $id) {
                    data {
                            id
                                createdOn
                                name
                            number
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
        "variables": {"id": "ceUEGVdXTi5cDGEd53DhNw"},
        "operationName": "getCampaignContactList",
    }
    response = sales_client.post(
        "/api/v1/graphql/",
        headers={"Authorization": f"JWT {_token}"},
        json=get_sms_contact_list,
    )
    assert response.json()
    assert response.json()["data"]["getCampaignContactList"]["status"] == 200
