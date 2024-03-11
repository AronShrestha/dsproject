def test_get_bulksms_template(app_client, member_data):
    _token = member_data["accessToken"]
    get_sms_template = {
        "query": """
            query getBulkSmsTemplateList {
                getBulkSmsTemplateList {
                    data {
                        id
                        message
                            createdOn
                            createdBy
                            title
                            isDefault
                        isArchived
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
        "variables": {"params": {"first": 100}},
        "operationName": "getBulkSmsTemplateList",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={"Authorization": f"JWT {_token}"},
        json=get_sms_template,
    )
    assert response.json()
    assert response.json()["data"]["getBulkSmsTemplateList"]["status"] == 200
