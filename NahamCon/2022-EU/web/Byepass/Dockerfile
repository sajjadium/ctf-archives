FROM php:7.2.12-apache

COPY www/ /var/www/html/
RUN mkdir -p /var/www/html/uploads

COPY php.ini /usr/local/etc/php/

COPY flag.txt /
RUN chmod a+r /flag.txt

RUN chown -R www-data:www-data /var/www/html/
EXPOSE 80