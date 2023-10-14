FROM php:8.2-cli
RUN apt-get update && apt-get install -y libmemcached-dev libssl-dev zlib1g-dev \
	&& pecl install memcached-3.2.0 \
	&& docker-php-ext-enable memcached

COPY php.ini /usr/local/etc/php/

WORKDIR /var/www/html

COPY src /var/www/html/

COPY /flag.txt /

COPY /keke.sh /

RUN chmod +x /keke.sh && /keke.sh && rm -f /keke.sh

RUN groupadd -r onsra -g 433 && \
    useradd -u 431 -r -g onsra -s /sbin/nologin -c "Docker image user" onsra
USER onsra

EXPOSE 1337

CMD ["php", "-S", "0.0.0.0:1337"]