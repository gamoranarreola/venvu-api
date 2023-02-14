from app.api.auth0 import Auth0
from app.db.models import (
    AccountType,
    EmployeeCountRange,
    Role,
    YearlyRevenueRange
)

new_user = {
    "email": "gmoran@bcdev.works",
    "sub": "auth0|61cdcdafe09c83006f1aba14"
}

company_profile = {
    "address_line_1": "1000 Corellian Way",
    "city": "Corelliopolis",
    "country": "Corellia",
    "description": "We build ships",
    "employee_count_range": EmployeeCountRange._1000PLUS,
    "state_tax_id": "12-345",
    "tax_id_state": "CO",
    "name": "Corellian Industries",
    "postal_code": "99999",
    "state_province": "CO",
    "website": "corellianindustries.com",
    "yearly_revenue_range": YearlyRevenueRange._1BPLUS,
}


"""
In this case, a preexisting user has logged in.

For this test, a regular, non-admin user is created in Auth0 before the test is
run.
"""


def test_account_user_exists(app, get_vms_api_auth_token):

    with app.test_client() as client:

        response = client.post(
            "/api/accounts",
            json={
                "email": "vms_admnin@bcdev.works",
                "sub": Auth0.last_vms_admin_user_id,
            },
            headers={"authorization": get_vms_api_auth_token()},
        )

        print("\n\nTEST OUTPUT:\nlogged in with account: {}".format(response.data))  # noqa: E501
        assert response.status_code == 200


"""
In this case, a new user is attempting signup and his or her organization
already has an admin user.

In this case, an admin user is created in Auth0 before the test is run.
"""


def test_create_new_account_has_admin(app, get_vms_api_auth_token, add_admin):
    with app.test_client() as client:

        response = client.post(
            "/api/accounts",
            json={
                "email": "gmoran@bcdev.works",
                "sub": "auth0|61cdcdafe09c83006f1aba14",
            },
            headers={"authorization": get_vms_api_auth_token()},
        )

        print("\n\nTEST OUTPUT:\n {}".format(response.json))
        assert response.status_code == 409


"""
In this case, a new user is attempting signup and his or her organization
does not yet have an admin user.
"""


def test_create_new_account_has_no_admin(
    app, auth0_api_create_user, get_vms_api_auth_token
):
    with app.test_client() as client:

        response = client.post(
            "/api/accounts",
            json={
                "email": "gmoran@bcdev.works",
                "sub": "auth0|61cdcdafe09c83006f1aba14",
            },
            headers={"authorization": get_vms_api_auth_token()},
        )

        print("\n\nTEST OUTPUT:\n {}".format(response.json))
        assert response.status_code == 200


"""
In this case, an admin user exists and is completing signup
(account type and admin info)
"""


def test_update_account(app, add_admin_no_company_profile, get_vms_api_auth_token):  # noqa: E501
    with app.test_client() as client:

        response = client.put(
            "/api/accounts/1",
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

        print("\n\nTEST OUTPUT:\n {}".format(response.json))
        assert response.status_code == 200
