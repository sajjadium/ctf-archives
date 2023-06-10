FROM php:8.1-apache

COPY index.php /var/www/html/

RUN chown -R root:root /var/www/
RUN chmod -R 755 /var/www/

RUN sed -i "s/Listen 80/Listen 8080/" /etc/apache2/ports.conf 

USER www-data