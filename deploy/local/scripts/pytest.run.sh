#!/bin/bash

cd ./deploy/local

docker compose -f test.compose.yml up \
    --remove-orphans
