#!/usr/bin/env bash

PROJECT_NAME="main"
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
