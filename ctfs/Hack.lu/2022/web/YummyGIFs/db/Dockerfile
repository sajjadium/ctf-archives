FROM mysql:8

ARG RANDOM_ID
ENV RANDOM_ID $RANDOM_ID

COPY init.sql /docker-entrypoint-initdb.d/
RUN sed -i "s/RANDOM_ID/$RANDOM_ID/" /docker-entrypoint-initdb.d/init.sql
