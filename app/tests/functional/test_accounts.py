from colorama import Fore

from app.auth0 import Auth0
from app.tests.conftest import log_test_end, log_test_start
from app.data.database import AccountType, Role


"""
In this case, a preexisting user has logged in.
For this test, a regular, non-admin user is created in Auth0 before the test is
run.
"""


def test_account_user_exists(create_app, get_vms_api_auth_token, create_user):
    log_test_start()

    with create_app.test_client() as client:

        print(Fore.BLUE + "In test function")
        print(Fore.BLUE + f"VMS last user id: {Auth0.last_vms_user_id}")

        response = client.post(
            "/api/v1/sign-in",
            json={
                "email": "vms_user@venvu.com",
                "sub": Auth0.last_vms_user_id,
            },
            headers={"authorization": get_vms_api_auth_token()},
        )

        print(Fore.BLUE + "\n\nTEST OUTPUT:\nlogged in with account: {}".format(response.data))  # noqa: E501
        assert response.status_code == 200
        log_test_end()


"""
In this case, a new user is attempting signup and his or her organization
already has an admin user.
For this test, an admin user is created in Auth0 before the test is run.
"""


def test_create_new_account_has_admin(create_app, get_vms_api_auth_token, create_admin):  # noqa: E501
    log_test_start()

    with create_app.test_client() as client:

        print(Fore.BLUE + f"VMS last admin user id: {Auth0.last_vms_admin_user_id}")  # noqa: E501

        response = client.post(
            "/api/v1/sign-in",
            json={
                "email": "vms_user@venvu.com",
                "sub": "auth0|61cdcdafe09c83006f1aba14",
            },
            headers={"authorization": get_vms_api_auth_token()},
        )

        print(Fore.BLUE + "\n\nTEST OUTPUT:\n {}".format(response.json))
        assert response.status_code == 409
        log_test_end()


"""
In this case, a new user is attempting signup and his or her organization
does not yet have an admin user.
"""


def test_create_new_account_has_no_admin(
    create_app,
    get_vms_api_auth_token
):
    log_test_start()

    with create_app.test_client() as client:

        response = client.post(
            "/api/v1/sign-in",
            json={
                "email": "vms_user@venvu.com",
                "sub": "auth0|61cdcdafe09c83006f1aba14",
            },
            headers={"authorization": get_vms_api_auth_token()},
        )

        print(Fore.BLUE + "\n\nTEST OUTPUT:\n {}".format(response.json))
        assert response.status_code == 200
        log_test_end()


"""
In this case, an admin user exists and is completing signup
(account type and admin info)
"""


def test_update_account(create_app, create_admin_no_company_profile, get_vms_api_auth_token):  # noqa: E501
    log_test_start()

    with create_app.test_client() as client:

        response = client.put(
            "/api/v1/accounts/1",
            json={
                "account_type": AccountType._CNS.name,
                "given_names": "Guillermo Alberto",
                "surnames": "Moran-Arreola",
                "department": "IT",
                "job_title": "Manager",
                "roles": [Role._CNS_ADM.name],
            },
            headers={"authorization": get_vms_api_auth_token()},
        )

        print(Fore.BLUE + "\n\nTEST OUTPUT:\n {}".format(response.json))
        assert response.status_code == 200
        log_test_end()
