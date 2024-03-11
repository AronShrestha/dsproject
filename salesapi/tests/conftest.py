import asyncio
import pytest
import os
from salesapi.main import new_app
from tests.tests_billing.utils.constant import (
    MEMBER_LOGIN_EMAIL,
    MEMBER_LOGIN_PASSWORD,
)
from webapi.config import get_application_settings
from salesapi.settings import get_application_settings as get_sales_settings
from webapi.main import create_app
from starlette.testclient import TestClient

from krispcall.core.abstracts.shortid import ShortId
from krispcall.core.adapters.user import PrincipalUser


@pytest.fixture(scope="session")
def event_loop(request):
    """Loop"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app_client(event_loop):
    """Creates webapi client to do the test requests"""
    # Todo remove this line
    os.environ["app_env"] = "development"
    settings = get_application_settings()
    settings.is_testing = True
    app = create_app(settings)
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def sales_client(event_loop):
    """Creates salesapi client to do the test requests"""
    settings = get_sales_settings()
    settings.is_testing = True
    app = new_app(settings)
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def app_user(app_client):
    register_paylod = {
        "query": """
            mutation register($data: RegisterInputData!) {
              register(data: $data){
                status,
                data{
                  id,
                  organizationId,
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
                "organization": "764cba4d8fff",
                "firstName": "test1",
                "lastName": "user",
                "email": "test1@gmail.com",
                "password": "Test@123",
                "passwordConfirm": "Test@123",
                "defaultTimezone": "UTC 5.45+ Kathmandu",
                "phoneNumber": "9849810891",
            }
        },
        "operationName": "register",
    }
    assert (
        app_client.post(
            "/api/v1/graphql/",
            headers={"Content-Type": "application/json"},
            json=register_paylod,
        ).status_code
        == 200
    )
    login_paylod = {
        "query": """
        mutation login($data:LoginInputData!) {
              login(data: $data){
                status,
                data{
                  token,
                  details {
                    id,
                    workspaces{
                      id,
                      memberId,
                      title,
                      role
                    }
                  }
                }
                error{
                  code
                  message
                }
              }
            }
            """,
        "variables": {
            "data": {
                "details": {
                    "kind": "classic",
                    "login": "test1@gmail.com",
                    "password": "Test@123",
                },
                "client": "web",
                "device": "Acer",
            }
        },
        "operationName": "login",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={"Content-Type": "application/json"},
        json=login_paylod,
    )
    assert response.json()["data"]["login"]["status"] == 200
    yield response.json()["data"]["login"]["data"]["token"]


@pytest.fixture(scope="session")
def workspace_id(app_client, app_user):
    _token = app_user
    add_workspace_paylod = {
        "query": """
                mutation addWorkspace($data: WorkspaceInputData!) {
                  addWorkspace(data: $data){
                    status,
                    data{
                      id,
                    }
                    error{
                      message
                      code
                    }
                  }
                }
            """,
        "variables": {"data": {"title": "Test8"}},
        "operationName": "addWorkspace",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={"Authorization": f"JWT {_token}"},
        json=add_workspace_paylod,
    )
    assert response.json()["data"]["addWorkspace"]["status"] == 201
    yield response.json()["data"]["addWorkspace"]["data"]["id"]


@pytest.fixture(scope="session")
def login_user_data(app_client):
    login_paylod = {
        "query": """
         mutation login($data:LoginInputData!) {
               login(data: $data){
                 status,
                 data{
                   token,
                   details {
                     id,
                     workspaces{
                       id,
                       memberId,
                       title,
                       role
                     }
                   }
                 }
                 error{
                   code
                   message
                 }
               }
             }
             """,
        "variables": {
            "data": {
                "details": {
                    "kind": "classic",
                    "login": MEMBER_LOGIN_EMAIL,
                    "password": MEMBER_LOGIN_PASSWORD,
                },
                "client": "web",
                "device": "Acer",
            }
        },
        "operationName": "login",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={"Content-Type": "application/json"},
        json=login_paylod,
    )
    assert response.json()["data"]["login"]["status"] == 200
    yield response.json()["data"]["login"]["data"]


@pytest.fixture(scope="session")
def workspace_user(login_user_data):
    return login_user_data["details"]["workspaces"][0]


@pytest.fixture(scope="session")
def user_workspace(login_user_data):
    return login_user_data["details"]["workspaces"][0]


@pytest.fixture(scope="session")
def user_auth_id(login_user_data):
    return login_user_data["details"]["id"]


@pytest.fixture(scope="session")
def principal_user(login_user_data):
    auth_id = login_user_data["details"]["id"]
    user_id = ShortId(auth_id).uuid()
    user = PrincipalUser.construct(id_=user_id, authenticated_=True)
    return user


@pytest.fixture(scope="session")
def member_data(app_client, login_user_data, workspace_user):
    _token = login_user_data["token"]
    workspace_id = workspace_user["id"]
    member_id = workspace_user["memberId"]
    login_paylod = {
        "query": """
            mutation memberLogin($data:MemberLoginInputData!) {
              memberLogin(data: $data){
                status,
                data {
                  accessToken,
                  refreshToken
                }
                error {
                  code
                  message
                }
              }
        }
                """,
        "variables": {
            "data": {
                "authToken": f"{_token}",
                "workspaceId": f"{workspace_id}",
                "memberId": f"{member_id}",
            }
        },
        "operationName": "memberLogin",
    }
    response = app_client.post(
        "/api/v1/graphql/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"JWT {_token}",
        },
        json=login_paylod,
    )
    assert response.json()["data"]["memberLogin"]["status"] == 200
    yield response.json()["data"]["memberLogin"]["data"]
