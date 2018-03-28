#!/usr/bin/env bash

cd src

echo "Waiting for redis and postgres to start"
python wait_redis_postgres.py
python manage.py migrate
python manage.py collectstatic --noinput

python manage.py createsu
touch /tmp/.done.info

{%- if cookiecutter.channels == 'yes' %}
    daphne -b 0.0.0.0 -p 8001 config.asgi:application
{%- else %}
    python manage.py runserver 0.0.0.0:8001
{%- endif %}
