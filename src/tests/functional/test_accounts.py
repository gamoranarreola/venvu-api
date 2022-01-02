from app import create_app
from app.db.models import EmployeeCountRange, YearlyRevenueRange


new_user = {
    'email' :'gmoran@bcdev.works',
    'sub': 'auth0|61cdcdafe09c83006f1aba14'
}

company_profile = {
    'address_line_1': '1000 Corellian Way',
    'city': 'Corelliopolis',
    'country': 'Corellia',
    'description': 'We build ships',
    'employee_count_range': EmployeeCountRange._1000PLUS,
    'state_tax_id': '12-345',
    'tax_id_state': 'CO',
    'name': 'Corellian Industries',
    'postal_code': '99999',
    'state_province': 'CO',
    'website': 'corellianindustries.com',
    'yearly_revenue_range': YearlyRevenueRange._1BPLUS
}


"""
In this case, a preexisting user has logged in.
"""
def test_account_user_exists(app, get_auth_token, add_admin):

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

        print('\n\nTEST OUTPUT:\nlogged in with account: {}'.format(response.data))
        assert response.status_code == 200


"""
In this case, a new user is attempting signup and his or her organization already
has an admin user.
"""
def test_create_new_account_has_admin(app, get_auth_token, add_admin):
    with app.test_client() as client:

        response = client.post(
            '/api/accounts',
            json={
                'email': 'sbassett@bcdev.works',
                'sub': 'auth0|61cdcdafe09c83006f1aba14'
            },
            headers={
                'Authorization': get_auth_token
            }
        )

        print('\n\nTEST OUTPUT:\n {}'.format(response.json))
        assert response.status_code == 409


"""
In this case, a new user is attempting signup and his or her organization
does not yet have an admin user.
"""
def test_create_new_account_has_no_admin(app, get_auth_token):
    with app.test_client() as client:

        response = client.post(
            '/api/accounts',
            json={
                'email': 'sbassett@bcdev.works',
                'sub': 'auth0|61cdcdafe09c83006f1aba14'
            },
            headers={
                'Authorization': get_auth_token
            }
        )

        print('\n\nTEST OUTPUT:\n {}'.format(response.json))
        assert response.status_code == 200
