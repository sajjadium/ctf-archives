#!/bin/sh
docker build . -t profile-page
docker container rm -f profile-page
docker run --rm -p 2727:2727 --name profile-page profile-page