#!/bin/bash
mkdir stuff 2>/dev/null
gcc ./sources/readme.c -o ./stuff/readme;
gcc ./sources/run.c -o ./stuff/run;

docker build . -t readable
