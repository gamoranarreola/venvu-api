from enum import Enum
from datetime import datetime

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
