import pytest
import http.client
import os
import json
from colorama import Fore

from app.main import app
from app.data.database import (
    Role,
    Account,
    CompanyProfile,
    YearlyRevenueRange,
    EmployeeCountRange,
    db_session,
    Base,
    engine,
)
from app.auth0 import Auth0


@pytest.fixture
def create_app():

    with app.app_context():
        Base.metadata.create_all(bind=engine)
        yield app
        db_session.remove()
        Base.metadata.drop_all(bind=engine)

        if Auth0.last_vms_admin_user_id is not None:
            print(Fore.BLUE + f"Deleting admin user {Auth0.last_vms_admin_user_id}")  # noqa: E501
            Auth0.auth0_delete_user(Auth0.last_vms_admin_user_id)

        if Auth0.last_vms_user_id is not None:
            print(Fore.BLUE + f"Deleting user {Auth0.last_vms_user_id}")  # noqa: E501
            Auth0.auth0_delete_user(Auth0.last_vms_user_id)


@pytest.fixture
def create_account():
    def _create_account(data):
        return Account(**data)
    return _create_account


@pytest.fixture
def create_company_profile():

    return CompanyProfile(
        address_line_1="1000 Corellian Way",
        city="Corelliopolis",
        country="Corellia",
        description="We build ships",
        employee_count_range=EmployeeCountRange._1000PLUS,
        name="Corellian Industries",
        postal_code="99999",
        state_province="CO",
        website="corellianindustries.com",
        yearly_revenue_range=YearlyRevenueRange._1BPLUS,
    )


@pytest.fixture
def create_user(create_account, create_company_profile):
    email = "vms_user@venvu.com"
    auth0_user = Auth0.auth0_create_user(email, "s8dKU7Sp9o")

    Auth0.auth0_assign_user_roles(
        auth0_user.get("user_id"),
        "rol_mOHJ7dARVN420281"
    )

    account = create_account(
        {
            "email": email,
            "sub": auth0_user.get("user_id"),
            "roles": [Role["_VND_ADM"]],
        }
    )

    company_profile = create_company_profile
    account.company_profile = company_profile
    db_session.add(account)
    db_session.add(company_profile)
    db_session.commit()
    print(Fore.BLUE + f"Created user {auth0_user.get('user_id')}")


@pytest.fixture
def create_admin(create_account, create_company_profile):
    email = "vms_admin@venvu.com"
    auth0_admin_user = Auth0.auth0_create_user(email, "s8dKU7Sp9o", True)

    Auth0.auth0_assign_user_roles(
        auth0_admin_user.get("user_id"),
        "rol_mOHJ7dARVN420281"
    )

    account = create_account(
        {
            "email": email,
            "sub": auth0_admin_user.get("user_id"),
            "roles": [Role["_VND_ADM"]],
        }
    )

    company_profile = create_company_profile
    account.company_profile = company_profile
    db_session.add(account)
    db_session.add(company_profile)
    db_session.commit()
    print(Fore.BLUE + f"Created admin user {auth0_admin_user.get('user_id')}")


@pytest.fixture
def create_admin_no_company_profile(create_account):
    email = "vms_admin@venvu.com"
    auth0_admin_user = Auth0.auth0_create_user(email, "s8dKU7Sp9o", True)

    Auth0.auth0_assign_user_roles(
        auth0_admin_user.get("user_id"), "rol_mOHJ7dARVN420281"
    )

    account = create_account(
        {
            "email": email,
            "sub": auth0_admin_user.get("user_id"),
            "roles": [Role["_VND_ADM"]],
        }
    )

    db_session.add(account)
    db_session.commit()


@pytest.fixture
def get_vms_api_auth_token():
    def _get_vms_api_auth_token():
        conn = http.client.HTTPSConnection(os.environ.get("AUTH0_DOMAIN"))

        data = {
            "client_id": Auth0.vms_api_app.get("client_id"),
            "client_secret": Auth0.vms_api_app.get("client_secret"),
            "audience": os.environ.get("API_AUDIENCE"),
            "grant_type": "client_credentials",
        }

        conn.request(
            "POST",
            "/oauth/token",
            json.dumps(data),
            {"content-type": "application/json"},
        )

        return "Bearer " + json.loads(conn.getresponse().read()).get("access_token")  # noqa: E501

    return _get_vms_api_auth_token


@pytest.fixture
def auth0_api_create_user():
    return Auth0.auth0_create_user("vms_user@venvu.com", "D$s8dKU7Sp9o")


def log_test_start():
    print(Fore.GREEN + "BEGIN TEST")


def log_test_end():
    print(Fore.RED + "END TEST")
