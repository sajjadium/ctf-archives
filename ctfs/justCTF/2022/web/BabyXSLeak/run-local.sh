#!/usr/bin/env bash

export DOCKER_BUILDKIT=1
export FLAG=justCTF{fake_flag}

docker-compose -p web_baby-xsleak -f docker-compose.yml rm --force --stop
docker-compose -p web_baby-xsleak -f docker-compose.yml build
docker-compose -p web_baby-xsleak -f docker-compose.yml up -d
