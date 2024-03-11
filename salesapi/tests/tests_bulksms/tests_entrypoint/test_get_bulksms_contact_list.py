def test_get_bulksms_contact_list(app_client, member_data):
    _token = member_data["accessToken"]
    get_sms_contact_list = {
        "query": """
            query getBulkSmsContactDetailList($id:ShortId!) {
                getBulkSmsContactDetailList(id: $id) {
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
        "operationName": "getBulkSmsContactDetailList",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={"Authorization": f"JWT {_token}"},
        json=get_sms_contact_list,
    )
    assert response.json()
    assert (
        response.json()["data"]["getBulkSmsContactDetailList"]["status"] == 200
    )
