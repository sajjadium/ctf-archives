#!/bin/sh
#

sudo docker build -t "mailservice" . && sudo docker run -d -p "0.0.0.0:1337:1337" mailservice