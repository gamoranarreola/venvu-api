web: gunicorn --pythonpath=src run:application
worker: celery worker -A --pythonpath=src app.celery_worker.celery worker --pool=solo --loglevel=info
