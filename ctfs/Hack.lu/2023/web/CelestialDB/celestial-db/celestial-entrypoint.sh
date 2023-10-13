#!/bin/sh

/templates/create-tenants.sh

exec /usr/local/bin/docker-entrypoint.sh "$@"
