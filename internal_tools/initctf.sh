#!/bin/bash

CTF_NAME=$(`dirname $0`/initctf.py "$@")

if [ -n "$CTF_NAME" ]; then
  cd ctfs/$CTF_NAME
  git --no-pager diff
fi
