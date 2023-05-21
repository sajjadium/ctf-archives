FROM php:8.1-apache

RUN sed -i 's/80/8080/g' /etc/apache2/ports.conf /etc/apache2/sites-available/*.conf

RUN apt-get update && apt-get install -y gcc

COPY src/ /var/www/html/
COPY flag /flag
COPY readflag.c /readflag.c

RUN gcc -o /readflag /readflag.c
RUN rm /readflag.c

RUN chown root:root /flag
RUN chmod 400 /flag
RUN chown root:root /readflag
RUN chmod 4755 /readflag

RUN chown -R root:root /var/www/html
RUN chmod -R 555 /var/www/html