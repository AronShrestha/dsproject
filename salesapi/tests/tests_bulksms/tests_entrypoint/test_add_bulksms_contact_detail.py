def test_add_bulksms_contact_detail(app_client, login_user_data):
    _token = login_user_data["token"]
    add_contact_payload = {
        "query": """
            mutation addBulkSmsContactDetail($data: AddBulkSmsContactDetailInputData! ) {
                addBulkSmsContactDetail(data: $data){
                    status,
                    data{
                            id
                    name
                            number
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
        "operationName": "addBulkSmsContactDetail",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=add_contact_payload,
    )
    assert response.json()["data"]["addBulkSmsContactDetail"]["status"] == 200
    assert (
        response.json()["data"]["addBulkSmsContactDetail"]["data"]["success"]
        is True
    )
