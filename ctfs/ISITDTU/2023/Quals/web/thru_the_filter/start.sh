#!/bin/sh
docker build -t thruthefilter .
docker run -p 1338:8080 thruthefilter