#!/bin/sh

deno run --no-prompt --allow-read=flag.txt --allow-net=0.0.0.0:8080 --allow-env ./main.js
