# extra step in another container to have the smallest thing running later
FROM alpine:3.18.3 as compiler

RUN apk update && apk add gcc musl-dev php81-phar php81-iconv php81-openssl curl
RUN curl -s https://getcomposer.org/installer | php -- --install-dir=/usr/bin/ --filename=composer

COPY trashbin /app/trashbin
WORKDIR /app/trashbin
RUN composer install
WORKDIR /

COPY readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag

# actually running image
FROM alpine:3.18.3

RUN apk update && apk add php81 php81-fpm php81-curl php81-session php81-common php81-zip php81-pdo php81-pdo_sqlite nginx supervisor

RUN addgroup -S web && adduser -H -S --shell /sbin/nologin -g web web

COPY trashbin /app/trashbin

COPY --from=compiler /app/trashbin/vendor /app/trashbin/vendor

COPY supervisord/supervisord.conf /supervisord.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf

COPY flag.txt /flag.txt
RUN chmod 400 /flag.txt
RUN chown root:root /flag.txt

COPY --from=compiler readflag /readflag
RUN chown root:root /readflag
RUN chmod 4555 /readflag

# I guess there are better ways to fix this, but who cares
RUN chown -R web:web /var/log/

RUN chmod -R 755 /app
RUN chown -R web:web /app/trashbin/src/data

CMD ["supervisord", "-c", "/supervisord.conf"]