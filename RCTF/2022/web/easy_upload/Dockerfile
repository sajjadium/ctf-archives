FROM php:8.1.9-apache
RUN rm -rf /var/www/html
COPY ./src /var/www/html
COPY ./flag /flag
COPY ./site.conf /etc/apache2/sites-enabled/000-default.conf
RUN chmod -R 755 /var/www/html && chown www-data:www-data /var/www/html/public/upload && chmod 444 /flag && mkdir /var/www/html/var && chown www-data:www-data /var/www/html/var
