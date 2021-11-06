#! /bin/bash

docker-compose build
docker-compose up -d --scale bot=4
