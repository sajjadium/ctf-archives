#!/bin/bash
socat -t 5 tcp-listen:1337,reuseaddr,fork exec:./run.sh,pty,raw,stderr,echo=0