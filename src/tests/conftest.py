from flask_migrate import init
import pytest
import json
import requests
from app import create_app
from app.db import db

from app.db.models import (
    Account,
    AccountType,
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
    flask_app = create_app('flask_test.cfg')
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def get_auth_token():
    url = 'https://dev-dh8aqmc6.us.auth0.com/oauth/token'
    headers = {'Content-Type': 'application/json'}

    params = {
        'client_id': 'nl7qE0EZL2d0mBc7NAsnwhqarhEsTnTA',
        'client_secret': 'p2H_Z4w5LAJDcxH4CzEe0ewvt6COHCRf6WbJsyVN5PVvRttUnMo2coa_ElCVgUj8',
        'audience': 'https://vms-b2b.app',
        'grant_type': 'client_credentials'
    }

    response = json.loads(requests.post(url=url, json=params, headers=headers).text)

    return 'Bearer {}'.format(response['access_token'])
