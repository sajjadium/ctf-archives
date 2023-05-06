FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y gcc make openssl wget curl vim libbz2-dev libxml2-dev libjpeg-dev libpng-dev libfreetype6-dev libzip-dev libssl-dev libsqlite3-dev libcurl4-openssl-dev libgmp3-dev libonig-dev libreadline-dev libxslt1-dev libffi-dev libmysqlclient-dev pkg-config apache2-dev apache2 mysql-server

RUN wget https://www.php.net/distributions/php-7.4.28.tar.gz -O /tmp/php-7.4.28.tar.gz
RUN cd /tmp && tar zxvf php-7.4.28.tar.gz
RUN cd /tmp/php-7.4.28 && ./configure --with-apxs2 --with-mysqli=/usr/bin/mysql_config --with-pdo-mysql=/usr/bin/mysql_config && make -j8 && make install

RUN echo "\nSetHandler application/x-httpd-php\n" >> /etc/apache2/apache2.conf
RUN echo "\nLoadModule php7_module modules/libphp7.so\n" >> /etc/apache2/apache2.conf
RUN a2dismod mpm_event
RUN a2enmod mpm_prefork
COPY ./files/readflag.c /
COPY ./flag /
COPY ./files/start.sh /start.sh
COPY ./files/my.cnf /etc/my.cnf
COPY ./files/index.php /var/www/html/

RUN \
        chown root:root /flag && \
        chmod 600 /flag && \
        gcc /readflag.c -o /readflag && \
        chmod +s /readflag && \
        rm /readflag.c
RUN groupmod -g 1337 www-data -o
RUN groupmod -g 1337 mysql -o
EXPOSE 80
ENTRYPOINT ["bash","/start.sh"]





