from flask_restful import Api

from app.api.company_profiles import CompanyProfileListApi


def create_routes(api: Api):
    api.add_resource(CompanyProfileListApi, '/api/company-profiles')
