#!/usr/bin/env sh

docker build -t smuggling_mail .
docker run -it -p 8080:8080 --rm smuggling_mail
