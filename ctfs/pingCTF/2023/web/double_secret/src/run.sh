#!/bin/sh

sleep 15

python setup_db.py

export SECRET=$(openssl rand -hex 12)

gunicorn app:app -b 0.0.0.0:3000