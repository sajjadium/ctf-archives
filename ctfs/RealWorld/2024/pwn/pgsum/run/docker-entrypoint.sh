#!/usr/bin/env bash

export PGDATA=/var/lib/postgresql/data
export PATH=/opt/postgres/bin/:$PATH

docker_init_database_dir() {
    mkdir $PGDATA
    if [[ -z $POSTGRES_PASSWORD ]]; then
        POSTGRES_PASSWORD=`head /dev/urandom | tr -dc A-Za-z0-9 | head -c32`
    fi
    echo $POSTGRES_PASSWORD
    initdb -D "$PGDATA" --username="postgres" --pwfile=<(echo "$POSTGRES_PASSWORD")
    AUTH_METHOD=$(postgres -D "$PGDATA" -C password_encryption)
    echo "listen_addresses = '*'" >> "$PGDATA/postgresql.conf"
    echo "unix_socket_directories = '/var/run/postgresql'" >> "$PGDATA/postgresql.conf"
    echo "shared_preload_libraries = 'pg_backtrace'" >> "$PGDATA/postgresql.conf"
    printf "local all all $AUTH_METHOD\nhost all ctf all $AUTH_METHOD" > "$PGDATA/pg_hba.conf"
    # start server
    pg_ctl -D "$PGDATA" -w start
    # run init.sql
    psql "host=/var/run/postgresql/ user=postgres dbname=postgres password=$POSTGRES_PASSWORD" -f /init.sql
    pg_ctl -D "$PGDATA" -m fast -w stop
}

if [[ ! -d $PGDATA ]]; then
    docker_init_database_dir
fi

exec "$@"
