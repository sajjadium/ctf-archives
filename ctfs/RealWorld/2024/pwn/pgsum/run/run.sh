#!/bin/bash

docker build -t pgsql-sum . \
    && docker run -it -p 5432:5432 --rm --name pgsql-sum pgsql-sum
