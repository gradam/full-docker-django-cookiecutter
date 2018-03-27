#!/usr/bin/env bash

status=1
while [ ${status} != 0 ]; do
    docker exec {{cookiecutter.project_name}}-django cat /tmp/.done.info 2> /dev/null
    status=$?
    if [ ${status} != 0 ]; then
        sleep 0.5
    fi
done
