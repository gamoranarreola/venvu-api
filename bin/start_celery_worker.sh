cd src
pipenv run celery -A app.celery worker --pool=solo --loglevel=info
