#!/usr/bin/env bash
Xvfb :99 &
./node_modules/.bin/electron . --no-sandbox
