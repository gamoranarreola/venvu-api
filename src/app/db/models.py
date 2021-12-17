from enum import Enum
from datetime import datetime
from mongoengine import DO_NOTHING

from app.db import db


class AccountType(Enum):
    _CONSUMER = 'CONS'
    _VENDOR = 'VEND'


class EmployeeCountRange(Enum):
    _1_TO_4 = '1TO4'
    _5_TO_9 = '5TO9'
    _10_TO_19 = '10TO19'
    _20_TO_49 = '20TO49'
    _50_TO_99 = '50TO99'
    _100_TO_249 = '100TO249'
    _250_TO_499 = '250TO499'
    _500_TO_999 = '500TO999'
    _1000PLUS = '1000PLUS'


class YearlyRevenueRange(Enum):
    _U500K = 'U500K'
    _500K_TO_999K = '500KTO999K'
    _1MTOU2P5M = '1MTOU2P5M'
    _2P5MTOU5M = '2P5MTOU5M'
    _5MTOU10M = '5MTOU10M'
    _10MTOU100M = '10MTOU100M'
    _100MTOU500M = '100MTOU500M'
    _500MTOU1B = '500MTOU1B'
    _1BPLUS = '1BPLUS'


class CompanyProfile(db.Document):
    name = db.StringField(max_length=64, unique=True)
    parent_company = db.StringField(max_length=64)
    address_line_1 = db.StringField(max_length=64)
    address_line_2 = db.StringField(max_length=32)
    address_line_3 = db.StringField(max_length=32)
    city = db.StringField(max_length=32)
    state_province = db.StringField(max_length=32)
    postal_code = db.StringField(max_length=8)
    country = db.StringField(max_length=32)
    federal_tax_id = db.StringField(max_length=16, unique=True)
    website = db.StringField(max_length=64, unique=True)
    description = db.StringField(max_length=512)
    key_products = db.ListField(db.StringField(max_length=32), default=[])
    key_services = db.ListField(db.StringField(max_length=32), default=[])
    employee_count_range = db.StringField(max_length=8, choices=EmployeeCountRange)
    yearly_revenue_range = db.StringField(max_length=11, choices=YearlyRevenueRange)
    is_tax_id_verified = db.BooleanField(default=False)
    is_active = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField()


class Account(db.Document):
    """
    Represents an individual's user account. The roles will
    be as set in the corresponding Auth0 account which is
    uniquely identified with the "sub" field.
    """
    given_names = db.StringField(max_length=32, required=True)
    surnames = db.StringField(max_length=32, required=True)
    company_profile = db.LazyReferenceField(CompanyProfile, reverse_delete_rule=DO_NOTHING)
    type = db.EnumField(AccountType)
    email = db.StringField(max_length=64, required=True, unique=True)
    job_title = db.StringField(max_length=32, required=True)
    department = db.StringField(max_length=32, required=True)
    phone = db.StringField(max_length=13, required=True)
    sub = db.StringField(max_length=64, unique=True)
