#!/bin/bash
mkdir stuff 2>/dev/null
rm ./stuff/*
gcc ./sources/readme.c -o ./stuff/readme;
gcc ./sources/run.c -o ./stuff/run;

docker build --no-cache . -t readable_v2
