#!/bin/sh

# Make sure the shell is opened inside the current directory.

cd "${0%/*}"

# Fire up the docker image.

sudo docker-compose up