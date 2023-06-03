#!/bin/sh

# Port to which the task will be exposed
PORT=${1-1337}

# No spaces here
NAME="pwn-windytooth"

# Build task docker image
cd private
docker build -t ${NAME} -f Dockerfile .

docker rm -f ${NAME}
docker run -d \
    --restart=always \
    --read-only \
    --name=${NAME} \
    -p $PORT:1337 \
    ${NAME}
