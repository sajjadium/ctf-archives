#!/bin/bash
exec 2>/dev/null
timeout -k 5 20 ./chromium/chrome --headless --disable-gpu --remote-debugging-port=9222 --enable-blink-features=MojoJS --enable-logging=stderr "$1"
