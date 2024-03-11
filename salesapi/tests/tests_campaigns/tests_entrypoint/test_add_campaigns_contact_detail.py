def test_add_campaigns_contact_detail(sales_client, login_user_data):
    _token = login_user_data["token"]
    add_contact_payload = {
        "query": """
            mutation addCampaignContactDetail($data: AddCampaignContactDetailInputData! ) {
                addCampaignContactDetail(data: $data){
                    status,
                    data{
                            id
                    name

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
                "id": "YFeWf6CVLpmG9TJjLT5L7d",
                "name": "Check test okay",
                "number": "98411123112232",
            }
        },
        "operationName": "addCampaignContactDetail",
    }
    response = sales_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=add_contact_payload,
    )
    assert response.json()["data"]["addCampaignContactDetail"]["status"] == 200
    assert (
        response.json()["data"]["addCampaignContactDetail"]["data"]["success"]
        is True
    )
