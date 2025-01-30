FROM php:8.3-apache-bookworm

WORKDIR /var/www/html

COPY flag.txt /flag.txt

COPY src/ .

RUN useradd --user-group --system --create-home --no-log-init app

RUN chown app magicians

USER app
