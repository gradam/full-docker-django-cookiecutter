#!/usr/bin/env bash
cd src

python wait_redis_postgres.py
python manage.py migrate

touch /tmp/.done.info

daphne -p 8001 config.asgi:application
