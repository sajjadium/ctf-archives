#!/bin/bash

socat TCP-LISTEN:2326,reuseaddr,fork EXEC:"python -u /home/ctf/program.py" 


