#!/bin/sh

docker build -t ignition . > /dev/null 2>&1
docker run --rm ignition $@
