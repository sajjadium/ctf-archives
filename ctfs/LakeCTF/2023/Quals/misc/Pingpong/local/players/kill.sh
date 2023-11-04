#!/bin/bash
set -e
rm -rf /tmp/ping
rm -rf /tmp/pong
kill -- -$( cat /tmp/pids )