#!/bin/sh

nohup python3 /app/app.py > /dev/null;
nohup python3 /tmp/file_remover.py > /dev/null;
