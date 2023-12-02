#!/bin/sh
python3 -m flask --app flag.py run --host=0.0.0.0 --port=1337&
python3 -m flask --app main.py run --host=0.0.0.0
