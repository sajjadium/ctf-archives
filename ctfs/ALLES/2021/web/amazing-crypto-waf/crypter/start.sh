#/bin/sh

sleep 30 && python init.py &

gunicorn -w 8 -b "$BIND_ADDR:$PORT" --access-logfile - --error-logfile - app:app