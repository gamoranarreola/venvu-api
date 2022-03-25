brew services start postgres
brew services start redis
brew services start rabbitmq
cd src/
python3.9 -m pipenv run celery -A app.celery_worker.celery worker --pool=solo --loglevel=info
