from enum import Enum


class Role(Enum):
    _VEND_ADM = 'vendor_admin'
    _VEND_PUB = 'vendor_pubisher'
    _VEND_REP = 'vendor_representative'
    _CONS_ADM = 'consumer_admin'
    _CONS_PUB = 'consumer_publisher'
    _CONS_REP = 'consumer_representative'
