def test_delete_bulksms_contact_detail(app_client, login_user_data):
    _token = login_user_data["token"]
    delete_contact_payload = {
        "query": """
            mutation deleteBulkSmsContactDetails($data: DeleteBulkSmsContactDetailInputData! ) {
                deleteBulkSmsContactDetails(data: $data){
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
        "operationName": "deleteBulkSmsContactDetails",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=delete_contact_payload,
    )
    assert (
        response.json()["data"]["deleteBulkSmsContactDetails"]["status"] == 200
    )
    assert (
        response.json()["data"]["deleteBulkSmsContactDetails"]["data"][
            "success"
        ]
        is True
    )
