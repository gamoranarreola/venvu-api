import pytest
import json
import requests
from app import create_app
from app.db import db
from app.db.models import Account


@pytest.fixture(scope='module')
def new_account():
    return Account(email='gmoran@bcdev.works', sub='auth0|61cdcdafe09c83006f1aba14')


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_db(test_client):
    db.create_all()
    yield
    db.drop_all()


@pytest.fixture(scope='module')
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
