# based on judo0179.tistory.com/77
FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /var/www/html

RUN apt-get update
RUN apt-get install -yq --no-install-recommends apt-utils build-essential
RUN apt-get install -yq evince

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get upgrade -yq
RUN apt-get install git wget curl unzip apache2 php7.2 php7.2-fpm \
    php7.2-mysql libapache2-mod-php7.2 php7.2-curl php7.2-gd php7.2-json php7.2-xml php7.2-mbstring php7.2-zip -yq

RUN wget http://start.xpressengine.io/download/latest.zip
RUN unzip latest.zip && chmod -R 707 storage/ bootstrap/ config/ vendor/ plugins/ index.php composer.phar

RUN rm -rf /var/www/html/latest.zip /var/www/html/index.html
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
RUN sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/apache2.conf
RUN a2enmod rewrite
RUN service apache2 restart

ADD entrypoint.sh /
CMD /entrypoint.sh
