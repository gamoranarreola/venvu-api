from flask import Response, request
import json

from app.model import (
    CreateCompanyProfileRequest,
    CreateCompanyProfileResponse,
)
from app.repositories import (
    AccountRepository,
    CompanyProfileRepository,
)
from app.data.schemas import company_profile_schema
from app.data.database import db_session, CompanyProfile
from app.services.common import error_400_response, error_404_response


def create_company_profile() -> Response:

    try:
        body = request.get_json()
        req = CreateCompanyProfileRequest.from_dict(body)
        req.validate()
    except ValueError as exc:
        return error_400_response(str(exc), exc)

    account = AccountRepository(db_session).find_by_email(req.email)

    if account is None:
        return error_404_response(
            f"An account for email {req.email} was not found"
        )
    else:
        company_profile = CompanyProfileRepository(db_session).find_by_name(req.company_profile['name'])  # noqa: E501

        if company_profile is None:
            company_profile = CompanyProfile(**req.company_profile)
            company_profile.accounts.append(account)
            CompanyProfileRepository(db_session).save(company_profile)
            account = AccountRepository(db_session).assign_roles(account, req.roles)  # noqa: E501
            AccountRepository(db_session).save(account)

        return CreateCompanyProfileResponse(
            company_profile=json.loads(company_profile_schema.dumps(company_profile))  # noqa: E501
        )
