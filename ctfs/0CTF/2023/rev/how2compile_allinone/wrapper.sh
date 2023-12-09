#!/bin/bash
timeout 180 python3 -u ./pow.py
if [ $? -ne 0 ]; then
    echo 'pow failed!'
    exit 1
fi

timeout 5 rustup run nightly-2023-11-03 ./task 2>/dev/null

