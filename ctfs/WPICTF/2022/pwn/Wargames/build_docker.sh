#!/bin/sh

docker build --tag=wargames .
docker run -it -p 7777:7777 --rm --name=wargames wargames 
