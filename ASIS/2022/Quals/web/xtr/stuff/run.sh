#!/bin/bash
for var in "$@"
do
    ./index.js "$var"
done
