FROM php:8.0-apache
COPY framework /var/www/html/framework
RUN mkdir /var/www/html/tmp
RUN chmod -R 777 /var/www/html/tmp
COPY index.php /var/www/html/
COPY *.js /var/www/html/

