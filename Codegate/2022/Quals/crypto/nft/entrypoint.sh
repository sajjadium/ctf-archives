#!/bin/bash

export WEB3_PROVIDER_URI=http://ip:8545

python manage.py sqlmigrate account 0001
python manage.py migrate
python manage.py runserver 0.0.0.0:1234
