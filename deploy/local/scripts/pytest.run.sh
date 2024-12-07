#!/bin/bash

cd ./deploy/local

docker compose -f test.docker-compose.yml up \
    --remove-orphans
