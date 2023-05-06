#!/bin/bash

CONTAINER=$1
PORT=$2
IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CONTAINER)
# add rule
iptables -A DOCKER -p tcp -d $IP --dport $PORT -j DROP
