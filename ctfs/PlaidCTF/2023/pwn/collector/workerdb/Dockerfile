FROM postgres:15.2-bullseye

COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY pre-docker-entrypoint.sh /usr/local/bin/pre-docker-entrypoint.sh

ENTRYPOINT [ "pre-docker-entrypoint.sh" ]
CMD [ "postgres", "-c", "config_file=/etc/postgresql/postgresql.conf" ]