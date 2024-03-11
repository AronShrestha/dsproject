def test_create_campaigns_campaigns(sales_client, login_user_data):
    _token = login_user_data["token"]
    create_campaign_payload = {
        "query": """
          mutation createCampaigns($data: CreateCampaignsInputData! ) {
            createCampaigns(data: $data){
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
                "assigneeId": "F2iNMnNw44K4Mkrffzh2gX",
                "assigneeName": "new number",
                "skipCsvUpload": True,
                "isContactListHidden": False,
                "campaignName": "test campaign 001",
                "senderNumber": "+9779849810891",
                "smsTemplateId": "CZCUoAuZHqwuDi7WZQwGt4",
                "contactListId": "YFeWf6CVLpmG9TJjLT5L7d",
                "message": "bsdjbasjkbdnask",
                "createdByName": "bishwas asdfs",
            }
        },
        "operationName": "createCampaigns",
    }
    response = sales_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=create_campaign_payload,
    )
    assert response.json()["data"]["createCampaigns"]["status"] == 200
    assert (
        response.json()["data"]["createCampaigns"]["data"]["success"] is True
    )
