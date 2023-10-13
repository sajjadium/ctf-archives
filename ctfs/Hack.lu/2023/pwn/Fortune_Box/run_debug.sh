#!/bin/sh

PORT=${1:-1337}
socat -t5 tcp-listen:$PORT,max-children=50,reuseaddr,fork exec:"./run_chall_debug.sh"
