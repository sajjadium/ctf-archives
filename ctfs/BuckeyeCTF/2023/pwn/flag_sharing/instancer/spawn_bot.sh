#!/bin/bash

docker run --rm -d --network $1 flag-sharing-bot "$2"
