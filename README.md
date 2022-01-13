# Startup Commands for Services
PostgreSQL
```
/usr/local/opt/postgresql/bin/postgres -D /usr/local/var/postgres
```
REDIS
```
/usr/local/opt/redis/bin/redis-server /usr/local/etc/redis.conf
```
RabbitMQ
```
rabbitmq-server
```
Celery (must run ```pipenv shell``` from project root first)
```
celery -A celery_worker.celery worker --loglevel=info
```
