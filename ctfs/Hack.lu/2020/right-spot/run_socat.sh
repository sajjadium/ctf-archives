#!/bin/bash
socat tcp-listen:4444,reuseaddr,fork exec:./run.py,rawer,pty,echo=0,su=ctf