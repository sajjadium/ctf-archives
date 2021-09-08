FROM wordpress:5.8.0-apache

# These are identical on remote
ARG SHOPUSER=productmanager
ARG SHOPPW=productmanager

# These are different on remote
ARG FLAG=ALLES!{fakeflag}
ARG ADMINUSER=fakeadmin
ARG ADMINPW=fakeadmin
ARG DAVUSER=fakedav
ARG DAVPW=&-mS6

RUN apt update
RUN apt install sudo less

# install WP_CLI
RUN cd /tmp && curl -LO https://github.com/wp-cli/wp-cli/releases/download/v2.5.0/wp-cli-2.5.0.phar

# create webdav folder
RUN mkdir /var/www/webdav
RUN touch /var/www/DavLock
RUN chown www-data:www-data /var/www/webdav
RUN chown www-data:www-data /var/www/DavLock

# configure apache for webdav
RUN a2enmod dav
RUN a2enmod dav_fs

COPY dav.conf dav.conf
RUN sed -i '/<VirtualHost/r dav.conf'      /etc/apache2/sites-available/000-default.conf
RUN sed -i "1i DavLockDB /var/www/DavLock" /etc/apache2/sites-available/000-default.conf

# configure webdav user
RUN htpasswd -nbs $DAVUSER $DAVPW > /etc/apache2/dav-passwords

# configure flag
RUN echo "Flag: <? // $FLAG ?>" > /flag.php

# copy init script wrapper
COPY apache2_init_wp.sh /usr/local/bin/
RUN sed -i "s/ADMINUSER/$ADMINUSER/g" /usr/local/bin/apache2_init_wp.sh
RUN sed -i "s/ADMINPW/$ADMINPW/g" /usr/local/bin/apache2_init_wp.sh
RUN sed -i "s/SHOPUSER/$SHOPUSER/g" /usr/local/bin/apache2_init_wp.sh
RUN sed -i "s/SHOPPW/$SHOPPW/g" /usr/local/bin/apache2_init_wp.sh

# Set new cmd, so user-creation runs before apache start.
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["apache2_init_wp.sh"]