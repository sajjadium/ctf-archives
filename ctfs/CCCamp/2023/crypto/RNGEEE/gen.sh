#!/usr/bin/env bash
BITS=32 FLAG="ALLES!{TESTFLAG}" python3 main.py > msg32.txt
BITS=56 FLAG=$(cat flag.txt) python3 main.py > msg56.txt
