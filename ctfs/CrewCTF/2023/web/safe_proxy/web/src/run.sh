#!/bin/sh

deno run --no-prompt --allow-net="0.0.0.0:8080,$PROVIDER_HOST" --allow-read=. --allow-env ./main.js
