#!/bin/bash

docker build -t dogogram .

docker run -d -it --init --name=dogogram-c -p 13374:80 dogogram
