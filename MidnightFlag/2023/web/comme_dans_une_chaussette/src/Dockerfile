FROM richarvey/nginx-php-fpm:latest

WORKDIR /root
RUN apk add make gcc musl-dev
RUN wget http://download.redis.io/redis-stable.tar.gz && \
    tar xvzf redis-stable.tar.gz && \
    cd redis-stable/deps/ && \
    make lua hiredis linenoise jemalloc && \
    cd .. && \
    make && \
    cp src/redis-server /usr/local/bin/

COPY ./nginx/default.conf /etc/nginx/sites-available/
COPY ./nginx/nginx.conf /etc/nginx/
COPY ./www/ /var/www/html/
COPY ./www.conf.default /usr/local/etc/php-fpm.d/
COPY ./zz-docker.conf /usr/local/etc/php-fpm.d/
COPY ./start.sh /root
COPY ./redis_logger.py /root
COPY ./flag.txt /

RUN apk add python3 && \
    pip3 install redis && \
    echo "* * * * * python3 /root/redis_logger.py '127.0.0.1'" > /var/spool/cron/crontabs/root && \
    crontab /var/spool/cron/crontabs/root


CMD ["bash","/root/start.sh"]