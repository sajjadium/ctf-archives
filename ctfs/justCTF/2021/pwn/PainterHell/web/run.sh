#!/bin/bash

if [ ${DEBUG} = "1" ];
then
  python3 manage.py runserver 0.0.0.0:8080
else
  # start nginx
  nginx -g "daemon off;" &
  echo "$!" > /tmp/nginx.pid
  NGINX_PID=$(cat /tmp/nginx.pid)

  # start app
  python3 manage.py collectstatic --noinput
  gunicorn icypis.wsgi:application \
    --name icypis \
    --bind 0.0.0.0:8081 \
    --workers ${GUNICORN_WORKERS} \
    --timeout ${GUNICORN_TIMEOUT} \
    --log-level=info \
    --limit-request-line=0 \
    --limit-request-field_size 32380 \
    --limit-request-fields 300 \
    --log-file=- &
  echo "$!" > /tmp/app.pid
  APP_PID=$(cat /tmp/app.pid)

  # wait for processes
  wait $NGINX_PID
  wait $APP_PID
fi
