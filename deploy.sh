#!/bin/sh
set -e
set -x

docker build --tag darkwind8/github_runner:$1 .
docker tag darkwind8/github_runner:$1 darkwind8/github_runner:latest
docker push darkwind8/github_runner:$1
docker push darkwind8/github_runner:latest