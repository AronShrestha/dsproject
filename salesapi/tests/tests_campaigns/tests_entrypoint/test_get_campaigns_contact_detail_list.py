def test_get_campaigns_contact_detail_list(sales_client, member_data):
    _token = member_data["accessToken"]
    get_campaigns_contact_detail_list = {
        "query": """
            query getCampaignContactDetailList($id:ShortId!) {
                getCampaignContactDetailList(id: $id) {
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
        "operationName": "getCampaignContactDetailList",
    }
    response = sales_client.post(
        "/api/v1/graphql/",
        headers={"Authorization": f"JWT {_token}"},
        json=get_campaigns_contact_detail_list,
    )
    assert response.json()
    assert (
        response.json()["data"]["getCampaignContactDetailList"]["status"]
        == 200
    )
