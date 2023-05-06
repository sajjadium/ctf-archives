#!/bin/sh

sudo docker build -t teen-sum .
sudo docker run -d -p 14141:1024 --rm -it teen-sum