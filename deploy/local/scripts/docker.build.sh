#!/bin/sh

export build_type="local"
cd fastapi && sh scripts/docker.build.sh && cd - || exit
# cd main && sh scripts/docker.build.sh && cd - || exit
