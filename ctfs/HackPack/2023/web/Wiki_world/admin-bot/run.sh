#!/bin/bash
export DISPLAY=:99
xvfb-run --auto-servernum --server-num=1 node admin.js