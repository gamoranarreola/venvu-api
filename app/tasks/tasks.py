"""
from celery import Celery

from app.auth0.auth0 import Auth0
from app.main import app

celery = Celery(
    __name__,
    app.config["CELERY_BROKER_URL"],
    app.config["RESULT_BACKEND"]
)

@celery.task(name="app.tasks.delete_user_from_auth0")
def delete_user_from_auth0(email):
    user = Auth0.auth0_get_user_by_email(email)
    Auth0.auth0_delete_user(user[0].get("user_id"))


@celery.task(name="app.tasks.assign_user_roles")
def assign_user_roles(user_id, roles):
    Auth0.auth0_assign_user_roles(user_id=user_id, roles=roles)
"""
