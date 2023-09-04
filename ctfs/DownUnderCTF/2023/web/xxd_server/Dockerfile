FROM php:8.1-apache

COPY index.php .htaccess /var/www/html/
COPY flag /
RUN sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/apache2.conf
RUN mkdir -p /var/www/html/uploads && chmod 1333 /var/www/html/uploads
