#!/bin/sh

# Port to which the task will be exposed
PORT=${1-1337}

# No spaces here
NAME="pwn-tic-tac"

# Build task docker image
cd private
docker build -t ${NAME} -f Dockerfile .

docker rm -f ${NAME}
docker run -d \
    --restart=always \
    --name=${NAME} \
    --privileged \
    -p $PORT:1337 \
    ${NAME} 
