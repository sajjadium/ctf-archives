#!/bin/sh

./build.sh && docker run -p 5000:5000 --privileged $(docker build -f Dockerfile.Run . -q)
