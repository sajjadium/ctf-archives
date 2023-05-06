#!/bin/bash
# docker build -t happy .
docker run --rm -v `pwd`/upload:/upload happy
