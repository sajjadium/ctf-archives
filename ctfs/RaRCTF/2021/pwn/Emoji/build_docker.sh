#!/bin/sh

docker rm -f emoji
docker build . -t emoji
docker run -it --name emoji -p 1337:1337 emoji
