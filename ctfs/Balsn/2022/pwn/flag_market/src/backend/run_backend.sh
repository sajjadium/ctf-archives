#!/bin/bash

cd /backend
gunicorn -w 4 "backend:create_app()" -b 0.0.0.0:29092
