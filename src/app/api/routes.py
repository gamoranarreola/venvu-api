from flask_restful import Api

from app.api.accounts import AccountApi, AccountListApi
from app.api.company_profiles import (
    CompanyProfileApi,
    CompanyProfileListApi,
    CompanyTypeListApi,
    EmployeeCountRangeListApi,
    YearlyRevenueRangeListApi,
    CountriesListApi,
    ProvincesListApi,
    IndustryListApi
)


def create_routes(api: Api):
    api.add_resource(CompanyProfileApi, "/api/company-profiles/<int:company_profile_id>")
    api.add_resource(CompanyProfileListApi, "/api/company-profiles")
    api.add_resource(AccountApi, "/api/accounts/<int:account_id>")
    api.add_resource(AccountListApi, "/api/accounts")
    api.add_resource(CompanyTypeListApi, "/api/company-profiles/company-type")
    api.add_resource(EmployeeCountRangeListApi, "/api/company-profiles/employee-count-range")
    api.add_resource(YearlyRevenueRangeListApi, "/api/company-profiles/yearly-revenue-range")
    api.add_resource(CountriesListApi, "/api/company-profiles/countries")
    api.add_resource(ProvincesListApi, "/api/company-profiles/provinces")
    api.add_resource(IndustryListApi, "/api/company-profiles/industries")
