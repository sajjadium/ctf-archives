#!/bin/bash
while true
do
    docker-compose down -v
    docker-compose up -d
    sleep 5m
done
