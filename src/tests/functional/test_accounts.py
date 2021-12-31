from app import create_app
from app.db.models import CompanyProfile

def test_create_new_account(app, get_auth_token):

    with app.test_client() as client:
        response = client.post(
            '/api/accounts',
            json={
                'email': 'gmoran@bcdev.works',
                'sub': 'auth0|61cdcdafe09c83006f1aba14'
            },
            headers={
                'Authorization': get_auth_token
            }
        )

        assert response.status_code == 200


def test_create_new_account_verify_no_prior_admin(
    app,
    get_auth_token,
    add_admin
):
    with app.test_client() as client:
        print(add_admin)
