#!/bin/bash

docker rm -f smileymaze
docker build -t smileymaze .
docker run --name=smileymaze --net=host -e DISPLAY -v /tmp/.X11-unix --rm -it smileymaze /bin/bash