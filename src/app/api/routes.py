from flask_restful import Api
from app.api.accounts import AccountListApi

from app.api.company_profiles import CompanyProfileListApi


def create_routes(api: Api):
    api.add_resource(CompanyProfileListApi, '/api/company-profiles')
    api.add_resource(AccountListApi, '/api/accounts')
