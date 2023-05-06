#!/bin/bash


docker-compose -f ./docker-compose-backend.yml build
CHAL_PORT=13337 docker-compose -f ./docker-compose-chal.yml build

docker-compose -f ./docker-compose-backend.yml up -d
CHAL_PORT=13337 docker-compose -f ./docker-compose-chal.yml up -d
