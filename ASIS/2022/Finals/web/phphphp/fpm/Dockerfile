FROM php@sha256:aa78e0c062145185306034921fdb89cd71eea19c8b893ef28727fba4093b961b

RUN head -c 2387224 /usr/local/sbin/php-fpm  > /tmp/t
RUN /usr/bin/printf "\x90\x90\x90\x90\x90" >> /tmp/t
RUN tail -c +2387230 /usr/local/sbin/php-fpm >> /tmp/t
RUN cp /tmp/t /usr/local/sbin/php-fpm

RUN head -c 2387342 /usr/local/sbin/php-fpm  > /tmp/t
RUN /usr/bin/printf "\x90\x90\x90\x90\x90" >> /tmp/t
RUN tail -c +2387348 /usr/local/sbin/php-fpm >> /tmp/t
RUN cp /tmp/t /usr/local/sbin/php-fpm

COPY ./www.conf /usr/local/etc/php-fpm.d/www.conf
COPY ./flag.txt /flag.txt
COPY ./web /web
RUN chmod -R 555 /web/
RUN chmod 500 /flag.txt

CMD ["php-fpm","-R"]