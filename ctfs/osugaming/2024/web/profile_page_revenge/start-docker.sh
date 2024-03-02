#!/bin/sh
docker build . -t profile-page-revenge
docker container rm -f profile-page-revenge
docker run --rm -p 3727:3727 --name profile-page-revenge profile-page-revenge