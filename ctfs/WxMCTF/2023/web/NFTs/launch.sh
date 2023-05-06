#!/bin/sh
gunicorn -w 1 -b 0.0.0.0:5000 --reload app:app
python -m http.server 5000