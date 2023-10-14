#!/bin/sh
sudo apt-get install docker-compose -y
# sudo docker-compose up --force-recreate --remove-orphans
sudo docker-compose down
sudo docker-compose up --build
