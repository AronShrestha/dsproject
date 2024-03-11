def test_add_bulksms_template(app_client, login_user_data):
    _token = login_user_data["token"]
    add_template_payload = {
        "query": """
        mutation addBulkSmsTemplate($data: BulkSmsTemplateInputData! ) {
            addBulkSmsTemplate(data: $data){
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
                "message": "addCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScriptsaddCampaignCallScripts",
                "title": "Test",
                "createdBy": "Bishwas wagle",
            }
        },
        "operationName": "addBulkSmsTemplate",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=add_template_payload,
    )
    assert response.json()["data"]["addBulkSmsTemplate"]["status"] == 200
    assert (
        response.json()["data"]["addBulkSmsTemplate"]["data"]["success"]
        is True
    )
