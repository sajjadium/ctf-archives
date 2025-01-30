FROM php:8.4-apache

COPY src/ /var/www/html/
RUN chown www-data:www-data -R /var/www/html/uploads/
RUN chmod 000 /var/www/html/uploads/flag.txt
