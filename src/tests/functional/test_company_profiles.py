from app.db.models import AccountType, Role


def test_create_company_profile(
    app, add_admin_no_company_profile, get_vms_api_auth_token
):

    with app.test_client() as client:

        response = client.post(
            "/api/company-profiles",
            json={
                "email": "vms_admin@bcdev.works",
                "account": {
                    "account_type": AccountType._CNS.name,
                    "given_names": "Guillermo Alberto",
                    "surnames": "Moran-Arreola",
                    "department": "IT",
                    "job_title": "Manager",
                    "roles": [Role._CNS_REP.name, Role._CNS_PUB.name]
                },
                "company_profile": {
                    "name": "TestCompany One",
                    "parent_company": "Parent One",
                    "state_tax_id": "12-3456",
                    "tax_id_state": "CA",
                    "website": "testcompanyone.com",
                },
            },
            headers={"authorization": get_vms_api_auth_token()},
        )

        print("\n\nTEST OUTPUT:\n {}".format(response.json))
        assert response.status_code == 200
