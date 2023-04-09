from flask_restx import Namespace

NSP = Namespace("venvu client")

from . import sign_in  # noqa: E402, F401
from . import accounts  # noqa: E402, F401
from . import company_profiles  # noqa: E402, F401
