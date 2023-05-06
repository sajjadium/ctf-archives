#!/bin/bash

timeout 20 ./chrome --headless --disable-gpu --remote-debugging-port=1338 --no-sandbox "$1"
