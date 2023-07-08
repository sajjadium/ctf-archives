FROM php:7.4.33-apache

COPY flag.txt /

ADD app/ /var/www/html
ADD files/ /files

RUN chown -R root:root /files
RUN chmod -R 775 /files
