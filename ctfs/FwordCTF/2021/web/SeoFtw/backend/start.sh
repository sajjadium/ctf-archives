#!/bin/sh
echo "waiting for neo4j to be up"
sleep 30
python init.py
gunicorn main:app -w 4 --threads 3 -b 0.0.0.0:5000
