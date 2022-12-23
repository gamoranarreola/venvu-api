from flask_restful import Api

from app.api.accounts import AccountApi, AccountListApi
from app.api.company_profiles import (
    CompanyProfileApi,
    CompanyProfileListApi,
    CompanyTypeListApi,
    CompanyTypeApi,
    EmployeeCountRangeListApi,
    EmployeeCountRangeApi,
    IndustryApi,
    YearlyRevenueRangeListApi,
    YearlyRevenueRangeApi,
    CountriesListApi,
    ProvincesListApi,
    IndustryListApi
)

from app.api.roles import RolesListApi


def create_routes(api: Api):
    api.add_resource(CompanyProfileApi, "/api/company-profiles/<int:company_profile_id>")  # noqa: E501
    api.add_resource(CompanyProfileListApi, "/api/company-profiles")
    api.add_resource(AccountApi, "/api/accounts/<int:account_id>")
    api.add_resource(AccountListApi, "/api/accounts")
    api.add_resource(CompanyTypeListApi, "/api/company-profiles/company-types")
    api.add_resource(CompanyTypeApi, "/api/company-profiles/company-types/<string:company_type_name>")  # noqa: E501
    api.add_resource(EmployeeCountRangeListApi, "/api/company-profiles/employee-count-ranges")  # noqa: E501
    api.add_resource(EmployeeCountRangeApi, "/api/company-profiles/employee-count-ranges/<string:employee_count_range_name>")  # noqa: E501
    api.add_resource(YearlyRevenueRangeListApi, "/api/company-profiles/yearly-revenue-ranges")  # noqa: E501
    api.add_resource(YearlyRevenueRangeApi, "/api/company-profiles/yearly-revenue-ranges/<string:yearly_revenue_range_name>")  # noqa: E501
    api.add_resource(CountriesListApi, "/api/company-profiles/countries")
    api.add_resource(ProvincesListApi, "/api/company-profiles/provinces")
    api.add_resource(IndustryListApi, "/api/company-profiles/industries")
    api.add_resource(IndustryApi, "/api/company-profiles/industries/<int:industry_id>")  # noqa: E501
    api.add_resource(RolesListApi, "/api/user-management/roles")
