from enum import Enum
from marshmallow_enum import EnumField

from app.db import db, ma


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


class CompanyProfile(db.Model):
    """
    Represents a company or organization.
    """
    __tablename__ = 'company_profile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    parent_company = db.Column(db.String(64))
    address_line_1 = db.Column(db.String(64))
    address_line_2 = db.Column(db.String(32))
    address_line_3 = db.Column(db.String(32))
    city = db.Column(db.String(32))
    state_province = db.Column(db.String(32))
    postal_code = db.Column(db.String(8))
    country = db.Column(db.String(32))
    federal_tax_id = db.Column(db.String(16), unique=True)
    website = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(512))
    key_products = db.Column(db.String(32), default=[])
    key_services = db.Column(db.String(32), default=[])
    employee_count_range = db.Column(db.Enum(EmployeeCountRange))
    yearly_revenue_range = db.Column(db.Enum(YearlyRevenueRange))
    is_tax_id_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    accounts = db.relationship('Account', back_populates='company_profile')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self) -> None:
        super().__init__()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return CompanyProfile.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return super().__repr__()


class Account(db.Model):
    """
    Represents an individual's user account. The roles will
    be as set in the corresponding Auth0 account which is
    uniquely identified with the "sub" field.
    """
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    given_names = db.Column(db.String(32))
    surnames = db.Column(db.String(32))
    company_profile_id = db.Column(db.Integer, db.ForeignKey('company_profile.id', ondelete='CASCADE'), nullable=True)
    company_profile = db.relationship('CompanyProfile', back_populates='accounts')
    account_type = db.Column(db.Enum(AccountType))
    email = db.Column(db.String(64), unique=True)
    job_title = db.Column(db.String(32))
    department = db.Column(db.String(32))
    phone = db.Column(db.String(13))
    sub = db.Column(db.String(64), unique=True)

    def __init__(
        self,
        email,
        sub,
        account_type = None,
        given_names = None,
        surnames = None,
        job_title = None,
        department = None,
        phone = None,
        company_profile_id = None,
    ) -> None:
        self.given_names = given_names
        self.surnames = surnames
        self.account_type
        self.email = email
        self.job_title = job_title
        self.department = department
        self.phone = phone
        self.sub = sub
        self.company_profile = company_profile_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Account.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return super().__repr__()


class AccountSchema(ma.Schema):
    account_type = EnumField(AccountType, by_value=True)

    class Meta:
        fields = (
            'given_names',
            'surnames',
            'account_type',
            'email',
            'job_title',
            'department',
            'phone',
            'sub',
            'company_profile',
            '_links',
        )

    _links = ma.Hyperlinks(
        {
            'self': ma.URLFor('accountlistapi', values=dict(id='<id>')),
            'collections': ma.URLFor('accountlistapi')
        }
    )

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
