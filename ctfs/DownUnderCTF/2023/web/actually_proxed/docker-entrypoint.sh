#!/bin/sh

# https://docs.docker.com/config/containers/multi-service_container/

cd /app/out

# Start the proxy
./proxy &

# Start the web server
./secret_server &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
