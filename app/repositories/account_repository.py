import sqlalchemy.orm as orm
from sqlalchemy.sql.expression import and_

from app.data.database import Account, Role


class AccountRepository:

    def __init__(self, db_session: orm.Session) -> None:
        self.db_session = db_session

    def find_by_email(self, email: str) -> Account | None:

        return (
            self.db_session.query(Account)
            .filter(Account.email == email)
            .first()
        )

    def find_by_account_admin(self, email: str) -> Account | None:

        return (
            self.db_session.query(Account)
            .filter(
                and_(
                    Account.email.contains(email.split("@")[1]),
                    Account.roles.overlap([Role._VND_ADM, Role._CNS_ADM]),
                )
            ).first()
        )

    def save(self, account: Account) -> Account:
        self.db_session.add(account)
        self.db_session.commit()
        return account
