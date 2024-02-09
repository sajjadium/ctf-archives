#!/bin/bash
docker build -t l4ugh .
docker run -dp 1337:1337 --rm -it l4ugh
