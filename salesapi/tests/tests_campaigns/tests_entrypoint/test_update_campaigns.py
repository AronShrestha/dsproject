def test_create_campaigns_campaigns(sales_client, login_user_data):
    _token = login_user_data["token"]
    update_campaign_payload = {
        "query": """
          mutation updateCampaign($data: UpdateCampaignsInputData! ) {
            updateCampaign(data: $data){
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
                "id": "5M6usPRjUBgcaVG4ZPFdmL",
                "assigneeId": "F2iNMnNw44K4Mkrffzh2gX",
                "assigneeName": "new number",
                "skipCsvUpload": True,
                "isContactListHidden": False,
                "campaignName": "test campaign 0012",
                "senderNumber": "+9779849810891",
                "smsTemplateId": "CZCUoAuZHqwuDi7WZQwGt4",
                "contactListId": "YFeWf6CVLpmG9TJjLT5L7d",
                "message": "bsdjbasjkbdnask",
            }
        },
        "operationName": "updateCampaign",
    }
    response = sales_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=update_campaign_payload,
    )
    assert response.json()["data"]["updateCampaign"]["status"] == 200
    assert response.json()["data"]["updateCampaign"]["data"]["success"] is True
