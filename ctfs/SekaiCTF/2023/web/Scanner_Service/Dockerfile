FROM ruby:2.7.5-alpine3.15

RUN apk add --update --no-cache supervisor

RUN adduser -D -u 1000 -g 1000 -s /bin/sh www

RUN mkdir /app
COPY src/ /app
COPY config/supervisord.conf /etc/supervisord.conf

COPY flag.txt /flag.txt

RUN mv /flag.txt /flag-$(head -n 1000 /dev/random | md5sum | head -c 32).txt

WORKDIR /app
RUN bundle install

RUN apk add nmap nmap-scripts --no-cache && rm -f /var/cache/apk/*

EXPOSE 1337

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
