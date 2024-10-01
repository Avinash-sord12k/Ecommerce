#!/usr/bin/env bash

PROJECT_NAME="fastapi"
DOCKER_IMAGE_NAME="$PROJECT_NAME"

echo "Running: docker build \
    -t $DOCKER_IMAGE_NAME \
    . \
    || exit
    "

docker buildx build  \
    -t "$DOCKER_IMAGE_NAME" \
    . \
    || exit
