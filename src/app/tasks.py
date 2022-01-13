from flask_mail import Message
from flask import current_app

from . import mail, celery


@celery.task(name='app.tasks.delete_auth0_user')
def delete_auth0_user(email):
    print(email)
