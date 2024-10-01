#!/bin/bash

cd ./deploy/local

docker compose -f docker-compose.yml up \
    --remove-orphans
