#!/usr/bin/env bash

# Wait for rabbitMQ server to start
sleep 5

cd src
exec su -m myuser -c "celery -A config worker -l info"
