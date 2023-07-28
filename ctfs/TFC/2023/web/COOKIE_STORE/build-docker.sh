#!/bin/bash
docker rm -f web_cookiestore
docker build --tag=web_cookiestore .
docker run -p 1337:1337 --rm --name=web_cookiestore web_cookiestore