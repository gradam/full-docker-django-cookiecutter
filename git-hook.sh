#!/usr/bin/env bash
set -ex

make prepare-tests
make wait-for-all
make test

make lint-in-docker
