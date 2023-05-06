#!/bin/sh

echo 'host replication replicator all scram-sha-256' >> "${PGDATA}/pg_hba.conf"
echo 'host replication replicator all password' >> "${PGDATA}/pg_hba.conf"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER replicator WITH REPLICATION LOGIN PASSWORD '${DBUSER_REPLICATOR_PASSWORD}';
    SELECT * FROM pg_create_physical_replication_slot('workerdb'); 
EOSQL