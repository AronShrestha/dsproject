def test_delete_campaigns_contact_detail(sales_client, login_user_data):
    _token = login_user_data["token"]
    delete_contact_payload = {
        "query": """
            mutation deleteCampaignContactDetails($data: DeleteCampaignContactDetailInputData! ) {
                deleteCampaignContactDetails(data: $data){
                    status,
                    data{
                            success
                    }
                    error{
                    message
                    code
                    }

                }
            }

        """,
        "variables": {
            "data": {
                "contacts": ["ceUEGVdXTi5cDGEd53DhNw"],
                "contactListId": "YFeWf6CVLpmG9TJjLT5L7d",
            }
        },
        "operationName": "deleteCampaignContactDetails",
    }
    response = sales_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=delete_contact_payload,
    )
    assert (
        response.json()["data"]["deleteCampaignContactDetails"]["status"]
        == 200
    )
    assert (
        response.json()["data"]["deleteCampaignContactDetails"]["data"][
            "success"
        ]
        is True
    )
