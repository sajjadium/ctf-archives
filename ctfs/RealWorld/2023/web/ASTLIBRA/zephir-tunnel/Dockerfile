FROM ubuntu:20.04

RUN apt-get update
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -y install tzdata git gcc make re2c php php-json php-dev libpcre3-dev build-essential
RUN apt-get -y install php-gmp php-pdo-sqlite php-zip php-mbstring php-curl php-mysql git

WORKDIR /root/
RUN git clone https://github.com/zephir-lang/php-zephir-parser.git -b v1.5.1
RUN git clone https://github.com/zephir-lang/zephir.git -b 0.16.3
COPY secure.patch /root/
COPY fix_warning.patch /root/
WORKDIR /root/zephir/
RUN patch -p1 < ../secure.patch
RUN patch -p1 < ../fix_warning.patch
WORKDIR /
COPY ./installer /tmp/i
RUN php /tmp/i --install-dir=/usr/bin --filename=composer
WORKDIR /root/zephir
RUN composer install
RUN rm /tmp/i
WORKDIR /root/php-zephir-parser 
RUN /usr/bin/phpize
RUN ./configure; make ; make install
RUN echo "extension=zephir_parser.so" >> /etc/php/7.4/cli/php.ini

RUN rm /var/www/html/index.html
COPY src /var/www/html/
RUN chmod -R 555 /var/www/html/

COPY run.sh /root/run.sh
RUN chmod +x /root/run.sh

COPY bot.php /root/bot.php
RUN chmod +x /root/bot.php

CMD ["/root/run.sh"]