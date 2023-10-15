FROM php:8.1-apache

COPY index.php /var/www/html/
COPY flag.txt /flag.txt
RUN mv /flag.txt /flag_$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 8 | head -n 1).txt

USER www-data