#!/usr/bin/env bash
cd src

python wait_redis_postgres.py
python manage.py migrate

touch /tmp/.done.info

{%- if cookiecutter.channels == 'yes' %}
    daphne -b 0.0.0.0 -p 8001 config.asgi:application
{%- else %}
    python manage.py runserver 0.0.0.0:8001
{%- endif %}
