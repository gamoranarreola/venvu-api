from flask_restful import Api

from app.api.accounts import AccountApi, AccountListApi
from app.api.company_profiles import (
    CompanyProfileApi,
    CompanyProfileListApi,
    CompanyTypeApi,
    CompanyTypeListApi,
    CountriesListApi,
    EmployeeCountRangeApi,
    EmployeeCountRangeListApi,
    IndustryApi,
    IndustryListApi,
    ProvincesListApi,
    YearlyRevenueRangeApi,
    YearlyRevenueRangeListApi
)
from app.api.roles import RolesListApi


def create_routes(api: Api):

    api.add_resource(
        CompanyProfileApi,
        "/api/company-profiles/<int:company_profile_id>"
    )

    api.add_resource(
        CompanyProfileListApi,
        "/api/company-profiles"
    )

    api.add_resource(
        AccountApi,
        "/api/accounts/<int:account_id>"
    )

    api.add_resource(
        AccountListApi,
        "/api/accounts"
    )

    api.add_resource(
        CompanyTypeListApi,
        "/api/company-profiles/company-types"
    )

    api.add_resource(
        CompanyTypeApi,
        "/api/company-profiles/company-types/<string:company_type_name>"
    )

    api.add_resource(
        EmployeeCountRangeListApi,
        "/api/company-profiles/employee-count-ranges"
    )

    api.add_resource(
        EmployeeCountRangeApi,
        "/api/company-profiles/employee-count-ranges/<string:employee_count_range_name>",  # noqa: E501
    )

    api.add_resource(
        YearlyRevenueRangeListApi,
        "/api/company-profiles/yearly-revenue-ranges"
    )

    api.add_resource(
        YearlyRevenueRangeApi,
        "/api/company-profiles/yearly-revenue-ranges/<string:yearly_revenue_range_name>",  # noqa: E501
    )

    api.add_resource(
        CountriesListApi,
        "/api/company-profiles/countries"
    )

    api.add_resource(
        ProvincesListApi,
        "/api/company-profiles/provinces"
    )

    api.add_resource(
        IndustryListApi,
        "/api/company-profiles/industries"
    )

    api.add_resource(
        IndustryApi,
        "/api/company-profiles/industries/<int:industry_id>"
    )

    api.add_resource(
        RolesListApi,
        "/api/user-management/roles"
    )
