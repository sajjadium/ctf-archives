#!/bin/bash

# To make sure database is initialised first
until nc -z $DB_HOST 3306
do
  echo Waiting for mysql to start
  sleep 5
done


python3 /djangoapp/manage.py makemigrations
python3 /djangoapp/manage.py migrate
python3 /djangoapp/manage.py runserver 0.0.0.0:8000