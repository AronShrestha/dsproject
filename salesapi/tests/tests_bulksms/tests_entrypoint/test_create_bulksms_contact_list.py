def test_create_bulksms_campaigns(app_client, login_user_data):
    _token = login_user_data["token"]
    create_contact_list_payload = {
        "query": """
         mutation createBulkSmsContactList($data: BulkSmsContactCSVInputData! ) {
            createBulkSmsContactList(data: $data){
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
        "operationName": "createBulkSmsContactList",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=create_contact_list_payload,
    )
    assert response.json()["data"]["createBulkSmsContactList"]["status"] == 200
    assert (
        response.json()["data"]["createBulkSmsContactList"]["data"]["success"]
        is True
    )
