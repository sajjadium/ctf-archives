#!/bin/bash
docker build -t library .
docker run -p 1337:1337 --rm -it library
