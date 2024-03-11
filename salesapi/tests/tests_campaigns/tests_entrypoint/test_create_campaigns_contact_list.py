def test_create_campaigns_campaigns(sales_client, login_user_data):
    _token = login_user_data["token"]
    create_contact_list_payload = {
        "query": """
         mutation createCampaignContactList($data: CampaignContactCSVInputData! ) {
            createCampaignContactList(data: $data){
                status
                error{
                message
                code
                }
                    data{
                        totalContactCount
                    }
                }
            }
        """,
        "variables": {
            "data": {
                "contactListName": "bishwas empty",
                "skipCsvUpload": True,
                "isContactListHidden": True,
                "createdBy": "bhishwas wagle",
            }
        },
        "operationName": "createCampaignContactList",
    }
    response = sales_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=create_contact_list_payload,
    )
    assert (
        response.json()["data"]["createCampaignContactList"]["status"] == 200
    )
    assert (
        response.json()["data"]["createCampaignContactList"]["data"]["success"]
        is True
    )
