#!/bin/sh

nginx -c nginx.conf -p $PWD
uwsgi --ini app/app.ini
