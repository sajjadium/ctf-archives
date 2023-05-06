#!/bin/bash

timeout 30 ./chrome --headless --disable-gpu --remote-debugging-port=1338 --enable-blink-features=MojoJS "$1"
