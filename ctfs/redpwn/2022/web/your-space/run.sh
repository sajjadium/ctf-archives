#!/bin/bash

export SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(64))')
exec gunicorn -w 4 -b '0.0.0.0:8000' --preload 'app:create_app()'
