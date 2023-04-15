from operator import itemgetter
import pycountry

from app.data.database import (
    EmployeeCountRange,
    YearlyRevenueRange,
)


def get_employee_count_ranges():
    return [{"code": d.name, "name": d.value} for d in EmployeeCountRange]


def get_employee_count_range_by_name(name: str):
    return EmployeeCountRange[name].value


def get_yearly_revenue_ranges():
    return [{"code": d.name, "name": d.value} for d in YearlyRevenueRange]


def get_yearly_revenue_range_by_name(name: str):
    return YearlyRevenueRange[name].value


def get_countries():
    return sorted(
        [
            {
                "code": d.alpha_3,
                "country_code": d.alpha_2,
                "name": d.name
            }
            for d in pycountry.countries
        ],
        key=itemgetter("name")
    )


def get_provinces(country_code: str):
    return sorted(
        [
            {
                "code": d.code,
                "name": d.name
            }
            for d in pycountry.subdivisions.get(
                country_code=country_code
            )
        ],
        key=itemgetter("name")

    )
