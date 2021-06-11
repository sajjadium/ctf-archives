FROM php:7.3-apache

RUN chmod 1733 /tmp /var/tmp /dev/shm

ADD challenge/flag.txt /flag
RUN chmod 0444 /flag

ADD challenge/index.php /var/www/html/
ADD challenge/fs.php    /var/www/html/

RUN mkdir /var/www/root

RUN chown -R root:www-data /var/www/

RUN chmod 0755 /var/www/html
RUN chmod 0755 /var/www/html/index.php
RUN chmod 0755 /var/www/html/fs.php

RUN chmod 0733 /var/www/root/
