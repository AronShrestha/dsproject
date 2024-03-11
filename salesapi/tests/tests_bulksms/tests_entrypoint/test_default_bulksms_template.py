def test_update_default_bulksms_template(app_client, login_user_data):
    _token = login_user_data["token"]
    default_template_payload = {
        "query": """
        mutation updateDefaultBulkSmsTemplate($data: UpdateDefaultBulkSmsTemplateInputData! ) {
            updateDefaultBulkSmsTemplate(data: $data){
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
        "operationName": "updateDefaultBulkSmsTemplate",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=default_template_payload,
    )
    assert (
        response.json()["data"]["updateDefaultBulkSmsTemplate"]["status"]
        == 200
    )
    assert (
        response.json()["data"]["updateDefaultBulkSmsTemplate"]["data"][
            "success"
        ]
        is True
    )
