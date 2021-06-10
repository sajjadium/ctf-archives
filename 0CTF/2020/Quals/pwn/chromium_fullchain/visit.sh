#!/bin/bash

timeout 60 ./chrome --headless --disable-gpu --remote-debugging-port=2338 "$1"
