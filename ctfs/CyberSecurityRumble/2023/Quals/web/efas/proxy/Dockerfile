FROM debian:bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    nginx

COPY nginx-host.conf /etc/nginx/sites-enabled/default

ENTRYPOINT nginx -g "daemon off;"