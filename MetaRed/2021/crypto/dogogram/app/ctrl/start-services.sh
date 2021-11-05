#!/bin/sh

#launch nginx
nginx

#launch uwsgi
cd /app/web/
uwsgi --ini /app/web/uwsgi.ini &

#cleanup files older than 15 minutes, every minute
while sleep 60; do
	find /app/web/static/uploads -maxdepth 1 -mmin +5 -type f -exec rm -f {} +
	cp /app/web/dog.jpg /app/web/static/uploads/00795a8b-fb58-47c0-91be-af068ddc71b4.jpg
done

exit 0
