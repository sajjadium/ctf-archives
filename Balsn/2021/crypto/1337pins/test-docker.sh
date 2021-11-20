#!/bin/bash

docker build -t balsn-1337pins .
docker run --rm -it --name test -p 127.0.0.1:27491:27491/tcp balsn-1337pins
