#!/bin/sh
cd /ctf
export LD_LIBRARY_PATH=/ctf:$LD_LIBRARY_PATH
exec ./notification
