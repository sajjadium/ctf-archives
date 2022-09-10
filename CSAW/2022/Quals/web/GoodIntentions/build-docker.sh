#!/bin/bash
docker rm -f web_good_intentions
docker build --tag=web_good_intentions .
docker run -p 1337:1337 --rm --name=web_good_intentions web_good_intentions
