#!/bin/sh
docker build . -t pp-ranking
docker container rm -f pp-ranking
docker run --rm -p 4727:4727 --name pp-ranking pp-ranking