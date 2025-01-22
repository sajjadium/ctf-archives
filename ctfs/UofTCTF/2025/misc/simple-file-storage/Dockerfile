FROM php:7.4-apache

RUN apt-get update && apt-get install -y \
    p7zip-full \
    libzip-dev \
    gcc make \
    && docker-php-ext-install zip

RUN echo "uoftctf{fake_flag}" > /flag.txt && \
    chmod 400 /flag.txt && \
    chown root:root /flag.txt

COPY ./src/readflag.c /readflag.c

RUN gcc /readflag.c -o /readflag

RUN rm /readflag.c

RUN chmod 4755 /readflag

RUN mkdir -p /var/www/html/uploads \
    && mkdir -p /var/www/html/extracted \
    && mkdir -p /tmp/sessions

COPY ./src/index.php /var/www/html/
COPY ./src/style.css /var/www/html/
COPY ./src/upload.php /var/www/html/
COPY ./src/view.php /var/www/html/
COPY ./src/download.php /var/www/html/

RUN chown -R www-data:www-data /var/www/html \
    && chmod 555 /var/www/html \
    && chmod -R 777 /var/www/html/uploads \
    && chmod -R 777 /var/www/html/extracted \
    && chmod -R 777 /tmp/sessions

RUN echo "session.save_path = '/tmp/sessions'" >> /usr/local/etc/php/php.ini

EXPOSE 80

CMD ["apache2-foreground"]