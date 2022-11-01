#!/bin/sh
docker run --rm -ti -p 1337:1337 -e FLAG="${1}" riot-challenge
