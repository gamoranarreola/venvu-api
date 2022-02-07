from marshmallow_enum import EnumField
from marshmallow import fields

from app.db import ma
from .models import AccountType, EmployeeCountRange, YearlyRevenueRange


class AccountSchema(ma.Schema):
    account_type = EnumField(AccountType, by_value=True)
    company_profile = fields.Nested('CompanyProfileSchema')
    department = fields.Str()
    email = fields.Str()
    given_names = fields.Str()
    id = fields.Int(dump_only=True)
    job_title = fields.Str()
    phone = fields.Str()
    roles = fields.List(fields.Str)
    sub = fields.Str()
    surnames = fields.Str()


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)


class CompanyProfileSchema(ma.Schema):
    accounts = fields.Nested('AccountSchema')
    address_line_1 = fields.Str()
    address_line_2 = fields.Str()
    address_line_3 = fields.Str()
    city = fields.Str()
    country = fields.Str()
    description = fields.Str()
    employee_count_range = EnumField(EmployeeCountRange, by_value=True)
    federal_tax_id = fields.Str()
    id = fields.Int(dump_only=True)
    is_active = fields.Boolean()
    is_tax_id_verified = fields.Boolean()
    key_products = fields.List(fields.Str())
    key_services = fields.List(fields.Str())
    name = fields.Str()
    parent_company = fields.Str()
    postal_code = fields.Str()
    state_province = fields.Str()
    website = fields.Str()
    yearly_revenue_range = EnumField(YearlyRevenueRange, by_value=True)


company_profile_schema = CompanyProfileSchema()
company_profiles_schema = CompanyProfileSchema(many=True)
