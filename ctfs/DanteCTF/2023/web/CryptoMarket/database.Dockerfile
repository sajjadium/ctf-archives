FROM mariadb

COPY challenge/database/createDb.sql /docker-entrypoint-initdb.d/createDb.sql
