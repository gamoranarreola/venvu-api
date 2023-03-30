import enum
import os

from sqlalchemy import (
    create_engine,
    Column,
    DateTime,
    Integer,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Enum,
    text,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
import sqlalchemy.orm

engine = create_engine(os.environ.get("DATABASE_URL", None))

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = sqlalchemy.orm.declarative_base()
Base.query = db_session.query_property()


class AccountType(enum.Enum):
    _CNS = "Consumer"
    _VND = "Vendor"


class Role(enum.Enum):
    _VND_ADM = "Vendor Admin"
    _VND_REP = "Vendor Rep"
    _VND_PUB = "Vendor Publisher"
    _CNS_ADM = "Consumer Admin"
    _CNS_REP = "Consumer Rep"
    _CNS_PUB = "Consumer Publisher"


class EmployeeCountRange(enum.Enum):
    _1_TO_4 = "1 to 4"
    _5_TO_9 = "5 to 9"
    _10_TO_19 = "10 to 19"
    _20_TO_49 = "20 to 49"
    _50_TO_99 = "50 to 99"
    _100_TO_249 = "100 to 249"
    _250_TO_499 = "250 to 499"
    _500_TO_999 = "500 to 999"
    _1000PLUS = "1000 or more"


class YearlyRevenueRange(enum.Enum):
    _U500K = "Under $500K"
    _500K_TO_999K = "$500K to $999K"
    _1M_TO_U2P5M = "$1M to under $2.5M"
    _2P5M_TO_U5M = "$2.5M to under $5M"
    _5M_TO_U10M = "$5M to under $10M"
    _10M_TO_U100M = "$10M to under $100M"
    _100M_TO_U500M = "$100M to under $500M"
    _500M_TO_U1B = "$500M to under $1B"
    _1BPLUS = "$1B or more"


class CompanyType(enum.Enum):
    _PUB = "Public Company"
    _PRV = "Privately Held"
    _PRT = "Partnership"
    _SLF = "Self Employed"
    _GOV = "Government Agency"
    _NPR = "Non-Profit"
    _SLP = "Sole Proprietorship"


class Industry(Base):
    __tablename__ = "industry"

    created_at = Column(DateTime, server_default=text("now()"))
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    updated_at = Column(DateTime, server_default=text("now()"))


class CompanyProfile(Base):
    """
    Represents a company or organization.
    """
    __tablename__ = "company_profile"

    accounts = relationship(
        "Account",
        back_populates="company_profile",
        cascade="all,delete"
    )

    address_line_1 = Column(String(64))
    address_line_2 = Column(String(32))
    address_line_3 = Column(String(32))
    city = Column(String(32))
    company_type = Column(Enum(CompanyType), nullable=True)
    country = Column(String(32))
    created_at = Column(DateTime, server_default=text("now()"))
    description = Column(String(2048))

    employee_count_range = Column(
        Enum(EmployeeCountRange),
        nullable=True
    )

    founded = Column(Integer)
    id = Column(Integer, primary_key=True)
    industry = Column(Integer)
    key_products = Column(postgresql.ARRAY(String(32)))
    key_services = Column(postgresql.ARRAY(String(32)))
    name = Column(String(64), unique=True)
    parent_company = Column(String(64))
    postal_code = Column(String(8))
    state_province = Column(String(32))
    updated_at = Column(DateTime, server_default=text("now()"))
    website = Column(String(64), unique=True)

    yearly_revenue_range = Column(
        Enum(YearlyRevenueRange),
        nullable=True
    )


class Account(Base):
    """
    Represents an individual's user account. The roles will
    be as set in the corresponding Auth0 account which is
    uniquely identified with the "sub" field.
    """
    __tablename__ = "account"

    __table_args__ = (
        UniqueConstraint(
            "state_tax_id",
            "tax_id_state",
            name="unique_state_tax_id"
        ),
    )

    account_type = Column(Enum(AccountType))

    company_profile = relationship(
        "CompanyProfile",
        back_populates="accounts"
    )

    company_profile_id = Column(
        Integer,
        ForeignKey("company_profile.id", ondelete="CASCADE"),
        nullable=True,
    )

    created_at = Column(DateTime, server_default=text("now()"))
    department = Column(String(32))
    email = Column(String(64), unique=True)
    given_names = Column(String(32))
    id = Column(Integer, primary_key=True)
    is_tax_id_verified = Column(Boolean, default=False)
    job_title = Column(String(32))
    phone = Column(String(13))
    roles = Column(postgresql.ARRAY(Enum(Role)))
    state_tax_id = Column(String(16))
    sub = Column(String(64), unique=True)
    surnames = Column(String(32))
    tax_id_state = Column(String(2))
    updated_at = Column(DateTime, server_default=text("now()"))
