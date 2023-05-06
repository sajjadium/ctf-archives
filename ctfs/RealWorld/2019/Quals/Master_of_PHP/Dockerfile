FROM ubuntu:18.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y autoconf gcc pkg-config libxml2-dev sqlite3 libsqlite3-dev libzip-dev libssl-dev libcurl4-openssl-dev
RUN apt-get install -y apache2-dev apache2
RUN apt-get install -y bison re2c
RUN apt-get install -y vim
COPY no_realworld_php /root/php/
WORKDIR /root/php/

RUN ./buildconf --force
RUN mkdir /etc/php/
RUN mkdir /etc/php/conf.d/
RUN ./configure --with-apxs2=/usr/bin/apxs  --with-config-file-path=/etc/php/ --with-config-file-scan-dir=/etc/php/conf.d/ --with-openssl --with-zlib --with-zip --with-iconv --without-sqlite3 --enable-xml --enable-mbregex --enable-sockets --enable-session --with-gettext --with-curl
RUN make
RUN make install
RUN a2dismod mpm_event
RUN a2enmod mpm_prefork
COPY php.conf /etc/apache2/mods-enabled/

RUN cp /root/php/php.ini-production /etc/php/php.ini
COPY disable.ini /etc/php/conf.d/
RUN rm /var/www/html/index.html
COPY index.php /var/www/html/index.php
RUN chmod 755 -R /var/www/html/

COPY flag /flag
COPY readflag /readflag
RUN chmod 555 /readflag
RUN chmod u+s /readflag
RUN chmod 500 /flag

CMD service apache2 restart & tail -f /var/log/apache2/access.log