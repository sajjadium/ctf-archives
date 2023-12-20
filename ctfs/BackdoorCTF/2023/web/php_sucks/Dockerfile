FROM php:7.0-apache

RUN mkdir /var/www/html/chal

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

WORKDIR /var/www/html/chal

RUN useradd ctf-player
COPY ./upload.php /var/www/html/chal
COPY ./REDACTED.txt /var/www/html/chal

RUN mkdir /var/www/html/chal/uploaded && chmod 777 /var/www/html/chal/uploaded/

RUN chown -R root:ctf-player /var/www/html/chal && chmod 750 /var/www/html/chal

RUN chmod 750 /var/www/html/chal/upload.php /var/www/html/chal/REDACTED.txt
RUN chmod 777 /var/www/html/chal/uploaded

EXPOSE 4052

USER ctf-player

CMD ["apache2-foreground"]

