from datetime import datetime
from enum import Enum
from sqlalchemy import null
from sqlalchemy.dialects import postgresql

from app.db import db


class AccountType(Enum):
    _CNS = "Consumer"
    _VND = "Vendor"


class Role(Enum):
    _VND_ADM = "Vendor Admin"
    _VND_REP = "Vendor Rep"
    _VND_PUB = "Vendor Publisher"
    _CNS_ADM = "Consumer Admin"
    _CNS_REP = "Consumer Rep"
    _CNS_PUB = "Consumer Publisher"


class EmployeeCountRange(Enum):
    _1_TO_4 = "1 to 4"
    _5_TO_9 = "5 to 9"
    _10_TO_19 = "10 to 19"
    _20_TO_49 = "20 to 49"
    _50_TO_99 = "50 to 99"
    _100_TO_249 = "100 to 249"
    _250_TO_499 = "250 to 499"
    _500_TO_999 = "500 to 999"
    _1000PLUS = "1000 or more"


class YearlyRevenueRange(Enum):
    _U500K = "Under $500K"
    _500K_TO_999K = "$500K to $999K"
    _1M_TO_U2P5M = "$1M to under $2.5M"
    _2P5M_TO_U5M = "$2.5M to under $5M"
    _5M_TO_U10M = "$5M to under $10M"
    _10M_TO_U100M = "$10M to under $100M"
    _100M_TO_U500M = "$100M to under $500M"
    _500M_TO_U1B = "$500M to under $1B"
    _1BPLUS = "$1B or more"


class CompanyType(Enum):
    _PUB = "Public Company"
    _PRV = "Privately Held"
    _PRT = "Partnership"
    _SLF = "Self Employed"
    _GOV = "Government Agency"
    _NPR = "Non-Profit"
    _SLP = "Sole Proprietorship"


class Industry(db.Model):
    __tablename__ = "industry"

    created_at = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    updated_at = db.Column(db.DateTime)

    def __init__(self, name):
        self.created_at = datetime.utcnow()
        self.name = name
        self.updated_at = datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_all():
        return Industry.query.all()

    def get_by_id(id):
        return Industry.query.get(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return super().__repr__()


class CompanyProfile(db.Model):
    """
    Represents a company or organization.
    """

    __tablename__ = "company_profile"

    __table_args__ = (
        db.UniqueConstraint("state_tax_id", "tax_id_state", name="unique_state_tax_id"),
    )

    accounts = db.relationship("Account", back_populates="company_profile")
    address_line_1 = db.Column(db.String(64))
    address_line_2 = db.Column(db.String(32))
    address_line_3 = db.Column(db.String(32))
    city = db.Column(db.String(32))
    company_type = db.Column(db.Enum(CompanyType), nullable=True)
    country = db.Column(db.String(32))
    created_at = db.Column(db.DateTime)
    description = db.Column(db.String(2048))
    employee_count_range = db.Column(db.Enum(EmployeeCountRange), nullable=True)
    founded = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    industry = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=False)
    is_tax_id_verified = db.Column(db.Boolean, default=False)
    key_products = db.Column(postgresql.ARRAY(db.String(32)))
    key_services = db.Column(postgresql.ARRAY(db.String(32)))
    name = db.Column(db.String(64), unique=True)
    parent_company = db.Column(db.String(64))
    postal_code = db.Column(db.String(8))
    state_province = db.Column(db.String(32))
    state_tax_id = db.Column(db.String(16))
    tax_id_state = db.Column(db.String(2))
    updated_at = db.Column(db.DateTime)
    website = db.Column(db.String(64), unique=True)
    yearly_revenue_range = db.Column(db.Enum(YearlyRevenueRange), nullable=True)

    def __init__(
        self,
        name,
        state_tax_id,
        tax_id_state,
        address_line_1='',
        address_line_2='',
        address_line_3='',
        city='',
        company_type=None,
        country='',
        description='',
        employee_count_range=None,
        founded=None,
        industry=None,
        is_active=False,
        is_tax_id_verified=False,
        key_products=[],
        key_services=[],
        parent_company='',
        postal_code='',
        state_province='',
        website='',
        yearly_revenue_range=None,
    ):
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.address_line_3 = address_line_3
        self.city = city
        self.company_type = company_type
        self.country = country
        self.created_at = datetime.utcnow()
        self.description = description
        self.employee_count_range = employee_count_range
        self.founded = founded
        self.industry = industry
        self.state_tax_id = state_tax_id
        self.tax_id_state = tax_id_state
        self.is_active = is_active
        self.is_tax_id_verified = is_tax_id_verified
        self.key_products = key_products
        self.key_services = key_services
        self.name = name
        self.parent_company = parent_company
        self.postal_code = postal_code
        self.state_province = state_province
        self.updated_at = datetime.utcnow()
        self.website = website
        self.yearly_revenue_range = yearly_revenue_range

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def get_all():
        return CompanyProfile.query.all()

    def get_by_id(id):
        return CompanyProfile.query.get(id)

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

    __tablename__ = "account"
    account_type = db.Column(db.Enum(AccountType))
    company_profile = db.relationship("CompanyProfile", back_populates="accounts")
    company_profile_id = db.Column(
        db.Integer,
        db.ForeignKey("company_profile.id", ondelete="CASCADE"),
        nullable=True,
    )
    department = db.Column(db.String(32))
    email = db.Column(db.String(64), unique=True)
    given_names = db.Column(db.String(32))
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(32))
    phone = db.Column(db.String(13))
    sub = db.Column(db.String(64), unique=True)
    roles = db.Column(postgresql.ARRAY(db.Enum(Role)))
    surnames = db.Column(db.String(32))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(
        self,
        email,
        sub,
        account_type=None,
        company_profile_id=None,
        department=None,
        given_names=None,
        job_title=None,
        phone=None,
        surnames=None,
        roles=[],
    ):
        self.account_type = account_type
        self.company_profile = company_profile_id
        self.created_at = datetime.utcnow()
        self.department = department
        self.email = email
        self.given_names = given_names
        self.job_title = job_title
        self.phone = phone
        self.sub = sub
        self.surnames = surnames
        self.roles = roles
        self.updated_at = datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Account.query.all()

    def get_by_id(id):
        return Account.query.get(id)

    def __repr__(self) -> str:
        return super().__repr__()
