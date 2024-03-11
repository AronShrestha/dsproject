def test_rename_bulksms_campaigns(app_client, login_user_data):
    _token = login_user_data["token"]
    rename_contact_list_payload = {
        "query": """
            mutation updateBulkSmsContactList($data: UpdateBulkSmsContactListInputData! ) {
            updateBulkSmsContactList(data: $data){
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
                "contactListId": "YFeWf6CVLpmG9TJjLT5L7d",
                "name": "Check kere okay yyy ttt",
                "action": "Rename",
                "archiveContactList": False,
            }
        },
        "operationName": "updateBulkSmsContactList",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=rename_contact_list_payload,
    )
    assert response.json()["data"]["updateBulkSmsContactList"]["status"] == 200
    assert (
        response.json()["data"]["updateBulkSmsContactList"]["data"]["success"]
        is True
    )
