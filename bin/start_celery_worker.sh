cd src
python3 -m pipenv run celery -A app.celery worker --pool=solo --loglevel=info
