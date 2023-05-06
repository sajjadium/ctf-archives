FROM php:8.1-fpm-alpine

RUN apk add --no-cache nginx && \
    apk add --no-cache --repository=https://dl-cdn.alpinelinux.org/alpine/edge/testing goreman

RUN ln -s /dev/stderr /var/log/nginx/error.log # nginx would not accept my customer error_log location
RUN sed -i 's|/var/log/nginx/access.log|/dev/stdout|g' /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/http.d/default.conf
COPY Procfile /

COPY html /var/www/html

EXPOSE 80
WORKDIR /

ENTRYPOINT ["goreman", "start"]
