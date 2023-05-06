#!/bin/sh

set -e 

export PGHOST=maindb
export PGUSER=web
export PGDATABASE=postgres

exec "$@"