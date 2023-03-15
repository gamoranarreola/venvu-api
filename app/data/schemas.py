from marshmallow import fields
from marshmallow_enum import EnumField

from app.data import ma

from app.data.database import (
    AccountType,
    CompanyType,
    EmployeeCountRange,
    Role,
    YearlyRevenueRange
)


class AccountSchema(ma.Schema):
    account_type = EnumField(AccountType)
    company_profile = fields.Nested("CompanyProfileSchema")
    department = fields.Str()
    email = fields.Str()
    given_names = fields.Str()
    id = fields.Int(dump_only=True)
    is_tax_id_verified = fields.Boolean()
    job_title = fields.Str()
    phone = fields.Str()
    roles = fields.List(EnumField(
        Role,
        load_by=EnumField.NAME,
        dump_by=EnumField.NAME
    ))
    state_tax_id = fields.Str()
    sub = fields.Str()
    surnames = fields.Str()
    tax_id_state = fields.Str()


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)


class CompanyProfileSchema(ma.Schema):
    accounts = fields.Nested("AccountSchema")
    address_line_1 = fields.Str()
    address_line_2 = fields.Str()
    address_line_3 = fields.Str()
    city = fields.Str()
    company_type = EnumField(CompanyType)
    country = fields.Str()
    description = fields.Str()
    employee_count_range = EnumField(EmployeeCountRange)
    founded = fields.Integer()
    id = fields.Int(dump_only=True)
    industry = fields.Int()
    key_products = fields.List(fields.Str())
    key_services = fields.List(fields.Str())
    name = fields.Str()
    parent_company = fields.Str()
    postal_code = fields.Str()
    state_province = fields.Str()
    website = fields.Str()
    yearly_revenue_range = EnumField(YearlyRevenueRange)


company_profile_schema = CompanyProfileSchema()
company_profiles_schema = CompanyProfileSchema(many=True)


class IndustrySchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


industry_schema = IndustrySchema()
industries_schema = IndustrySchema(many=True)
