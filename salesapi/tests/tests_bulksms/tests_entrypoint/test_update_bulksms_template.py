def test_update_bulksms_template(app_client, login_user_data):
    _token = login_user_data["token"]
    update_template_payload = {
        "query": """
        mutation updateBulkSmsTemplate($data: UpdateBulkSmsTemplateInputData! ) {
          updateBulkSmsTemplate(data: $data){
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
        "variables": {
            "data": {
                "id": "CZCUoAuZHqwuDi7WZQwGt4",
                "title": "Delete",
                "message": "changetext",
            }
        },
        "operationName": "updateBulkSmsTemplate",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=update_template_payload,
    )
    assert response.json()["data"]["updateBulkSmsTemplate"]["status"] == 200
    assert (
        response.json()["data"]["updateBulkSmsTemplate"]["data"]["success"]
        is True
    )
