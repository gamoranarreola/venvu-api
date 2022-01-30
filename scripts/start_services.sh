brew services start postgres
brew services start redis
brew services start rabbitmq
cd src/
pipenv run python3.9 -m celery -A celery_worker.celery worker --pool=solo --loglevel=info
