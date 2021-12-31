def test_create_new_account(test_client, get_auth_token):

    response = test_client.post(
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
