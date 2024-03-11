def test_delete_bulksms_template(app_client, login_user_data):
    _token = login_user_data["token"]
    delete_template_payload = {
        "query": """
        mutation deleteBulkSmsTemplate($data: UpdateDefaultBulkSmsTemplateInputData! ) {
            deleteBulkSmsTemplate(data: $data){
                status
                error{
                message
                code
                }
                    data{
                        success
                    }

                }
            }
        """,
        "variables": {"data": {"id": "CZCUoAuZHqwuDi7WZQwGt4"}},
        "operationName": "deleteBulkSmsTemplate",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=delete_template_payload,
    )
    assert response.json()["data"]["deleteBulkSmsTemplate"]["status"] == 200
    assert (
        response.json()["data"]["deleteBulkSmsTemplate"]["data"]["success"]
        is True
    )
