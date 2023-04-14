import json
from flask import Response, request

from app.data.database import CompanyProfile, db_session
from app.repositories.company_profile_repository import CompanyProfileRepository  # noqa: E501
from app.model import EditCompanyProfileRequest, EditCompanyProfileResponse
from app.data.schemas import company_profile_schema
from app.services.common import api_edit_company_profile, error_400_response


@api_edit_company_profile("Edit Company Profile API")
def edit_company_profile(company_profile: CompanyProfile) -> Response:
    try:
        body = request.get_json()
        req = EditCompanyProfileRequest.from_dict(body)
        req.validate()
    except ValueError as exc:
        return error_400_response(str(exc), exc)

    company_profile = CompanyProfileRepository(db_session).update(company_profile, body)  # noqa: E501
    CompanyProfileRepository(db_session).save(company_profile)

    return EditCompanyProfileResponse(
        company_profile=json.loads(company_profile_schema.dumps(company_profile))  # noqa: E501
    )
