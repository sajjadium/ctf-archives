#!/bin/bash

docker build -t flag-sharing-chal chal/
docker build -t flag-sharing-bot bot/
cd instancer && docker-compose up --build

