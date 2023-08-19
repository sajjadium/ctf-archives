FROM ubuntu:22.10
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN apt-get update
RUN apt-get install -y nginx php-fpm php-curl

COPY html /var/www/html
COPY default /etc/nginx/sites-available/default

CMD /etc/init.d/php8.1-fpm start && nginx -g 'daemon off;'
