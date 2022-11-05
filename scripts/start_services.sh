brew services start redis
brew services start rabbitmq
cd src/app
pipenv run celery -A celery worker --pool=solo --loglevel=info
