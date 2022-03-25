from datetime import datetime
from enum import Enum
from sqlalchemy.dialects import postgresql

from app.db import db


class AccountType(Enum):
    _CNS = "CNS"
    _VND = "VND"


class Role(Enum):
    _VND_ADM = "VND_ADM"
    _VND_REP = "VND_REP"
    _VND_PUB = "VND_PUB"
    _CNS_ADM = "CNS_ADM"
    _CNS_REP = "CNS_REP"
    _CNS_PUB = "CNS_PUB"


class EmployeeCountRange(Enum):
    _1_TO_4 = "1_TO_4"
    _5_TO_9 = "5_TO_9"
    _10_TO_19 = "10_TO_19"
    _20_TO_49 = "20_TO_49"
    _50_TO_99 = "50_TO_99"
    _100_TO_249 = "100_TO_249"
    _250_TO_499 = "250_TO_499"
    _500_TO_999 = "500_TO_999"
    _1000PLUS = "1000PLUS"


class YearlyRevenueRange(Enum):
    _U500K = "U500K"
    _500K_TO_999K = "500K_TO_999K"
    _1M_TO_U2P5M = "1M_TO_U2P5M"
    _2P5M_TO_U5M = "2P5M_TO_U5M"
    _5M_TO_U10M = "5M_TO_U10M"
    _10M_TO_U100M = "10M_TO_U100M"
    _100M_TO_U500M = "100M_TO_U500M"
    _500M_TO_U1B = "500M_TO_U1B"
    _1BPLUS = "1BPLUS"


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
    country = db.Column(db.String(32))
    created_at = db.Column(db.DateTime)
    description = db.Column(db.String(512))
    employee_count_range = db.Column(db.Enum(EmployeeCountRange))
    id = db.Column(db.Integer, primary_key=True)
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
    yearly_revenue_range = db.Column(db.Enum(YearlyRevenueRange))

    def __init__(
        self,
        name,
        state_tax_id,
        tax_id_state,
        address_line_1=None,
        city=None,
        country=None,
        description=None,
        employee_count_range=None,
        postal_code=None,
        state_province=None,
        website=None,
        yearly_revenue_range=None,
        address_line_2=None,
        address_line_3=None,
        is_active=False,
        is_tax_id_verified=False,
        key_products=[],
        key_services=[],
        parent_company=None,
    ):
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.address_line_3 = address_line_3
        self.city = city
        self.country = country
        self.created_at = datetime.utcnow()
        self.description = description
        self.employee_count_range = employee_count_range
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
        return Account.query.get(id)

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
