import os

import http.client
import pytest
import json

from app.api.auth0 import Auth0
from app import create_app
from app.db import db
from app.db.models import (
    Account,
    CompanyProfile,
    EmployeeCountRange,
    Roles,
    YearlyRevenueRange
)


@pytest.fixture
def create_account():

    return Account(
        email='gmoran@bcdev.works',
        sub='auth0|61cdcdafe09c83006f1aba14',
        roles=[Roles._CONS_ADM.name]
    )


@pytest.fixture
def create_company_profile():

    return CompanyProfile(
        address_line_1='1000 Corellian Way',
        city='Corelliopolis',
        country='Corellia',
        description='We build ships',
        employee_count_range=EmployeeCountRange._1000PLUS,
        state_tax_id='12-345',
        tax_id_state='CO',
        name='Corellian Industries',
        postal_code='99999',
        state_province='CO',
        website='corellianindustries.com',
        yearly_revenue_range=YearlyRevenueRange._1BPLUS
    )


@pytest.fixture
def add_admin(create_account, create_company_profile):
    account = create_account
    company_profile = create_company_profile
    account.company_profile = company_profile
    db.session.add(account)
    db.session.add(company_profile)
    db.session.commit()


@pytest.fixture
def app():
    flask_app = create_app()
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def get_vms_api_auth_token():
    conn = http.client.HTTPSConnection(os.environ.get('AUTH0_DOMAIN'))

    data = {
        'client_id': Auth0.vms_api_app.get('client_id'),
        'client_secret': Auth0.vms_api_app.get('client_secret'),
        'audience': os.environ.get('API_AUDIENCE'),
        'grant_type': 'client_credentials'
    }

    conn.request(
        'POST',
        '/oauth/token',
        json.dumps(data),
        { 'content-type': 'application/json' }
    )

    return 'Bearer ' + json.loads(conn.getresponse().read()).get('access_token')


@pytest.fixture
def auth0_api_create_user():
    conn = http.client.HTTPSConnection(os.environ.get('AUTH0_DOMAIN'))

    data = {
        'email': 'sbassett@bcdev.works',
        'connection': 'Username-Password-Authentication',
        'password': 'D$s8dKU7Sp9o'
    }

    conn.request(
        'POST',
        '/api/v2/users',
        json.dumps(data),
        { 'content-type': 'application/json' }
    )

    return json.loads(conn.getresponse().read())
