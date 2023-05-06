#!/bin/bash

docker-compose up -d --build

sleep 120

docker ps

# all container up now
# additional settings

./unexpose_docker_port.sh admin 8000

./unexpose_docker_port.sh admin 8009

./unexpose_docker_port.sh admin 8080

./unexpose_docker_port.sh admin 11311
