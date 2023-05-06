FROM debian:bullseye-20230227

RUN apt-get update \
    && apt-get install -y make libpq5 libcurl4 libssl1.1

COPY src/webhook /usr/local/bin/webhook

CMD [ "webhook" ]
