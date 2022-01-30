from flask_restful import Api

from ...app.api.accounts import AccountApi, AccountListApi
from ...app.api.company_profiles import CompanyProfileApi, CompanyProfileListApi


def create_routes(api: Api):
    api.add_resource(CompanyProfileApi, '/api/company-profiles/<int:company_profile_id>')
    api.add_resource(CompanyProfileListApi, '/api/company-profiles')
    api.add_resource(AccountApi, '/api/accounts/<int:account_id>')
    api.add_resource(AccountListApi, '/api/accounts')
