#!/bin/sh

# Create the uploads folder and run the server.

export uploads=/tmp/uploads_$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 8)
mkdir -p $uploads
gunicorn server.serve:application --bind 0.0.0.0:80 --worker-class aiohttp.worker.GunicornWebWorker --workers=$(expr $(nproc) \* 2 + 1)
rm -rf $uploads