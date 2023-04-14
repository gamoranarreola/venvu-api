from typing import Dict
import sqlalchemy.orm as orm

from app.data.database import CompanyProfile


class CompanyProfileRepository:

    def __init__(self, db_session: orm.Session) -> None:
        self.db_session = db_session

    def find_by_id(self, id: int) -> CompanyProfile | None:
        return self.db_session.query(CompanyProfile).get(id)

    def find_by_name(self, name: str) -> CompanyProfile | None:

        return (
            self.db_session.query(CompanyProfile)
            .filter(CompanyProfile.name == name)
            .first()
        )

    def update(self, company_profile: CompanyProfile, data: Dict) -> CompanyProfile:  # noqa: E501
        for key in data:
            setattr(company_profile, key, data[key])

        return company_profile

    def save(self, company_profile: CompanyProfile):
        self.db_session.add(company_profile)
        self.db_session.commit()
