#!/bin/bash

python gen.py
openssl req -x509 -newkey rsa:2048 -nodes -sha256 -subj '/CN=babyweb_internal' -keyout key.pem -out cert.pem
cp cert.pem key.pem internal/
cp cert.pem public/

sudo docker-compose up -d
