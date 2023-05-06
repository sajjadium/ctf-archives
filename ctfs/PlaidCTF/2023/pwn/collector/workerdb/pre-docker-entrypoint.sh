#!/bin/bash

REPLICATOR_USER=replicator

echo "Writing passwords into $HOME/.pgpass" >&2
echo "*:*:replication:${REPLICATOR_USER}:${DBUSER_REPLICATOR_PASSWORD}" \
    | su postgres -c 'tee "/var/lib/postgresql/.pgpass"' \
    | tee "$HOME/.pgpass" >/dev/null
chmod 0600 "/var/lib/postgresql/.pgpass" "$HOME/.pgpass"

if [[ ! -s "${PGDATA}/PG_VERSION" ]]; then
    until
        pg_basebackup \
            -h maindb \
            -U "${REPLICATOR_USER}" \
            -D "${PGDATA}" \
            -X stream \
            -S workerdb \
            --no-password
    do
        echo 'Waiting for maindb to come up' >&2
        sleep 1
    done

    echo 'Finished backup' >&2

    # start the standby
    touch "${PGDATA}/standby.signal"

    chown -R postgres: "${PGDATA}"
fi

echo 'Starting postgres' >&2
exec docker-entrypoint.sh "$@"
