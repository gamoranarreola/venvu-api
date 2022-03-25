from . import celery
from app.api.auth0 import Auth0


@celery.task(name="app.tasks.delete_user_from_auth0")
def delete_user_from_auth0(email):
    user = Auth0.auth0_get_user_by_email(email)
    Auth0.auth0_delete_user(user[0].get("user_id"))
