FROM php:apache

RUN apt update
RUN apt -y install zlib1g-dev libpng-dev libfreetype6-dev
RUN docker-php-ext-configure gd --with-freetype && docker-php-ext-install -j$(nproc) gd
RUN a2enmod rewrite

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y install postfix
RUN sed -i 's/myhostname.\+/myhostname = mail.alpha/' /etc/postfix/main.cf
RUN sed -i 's/mydestination.\+/mydestination = $myhostname/' /etc/postfix/main.cf
RUN sed -i 's/inet_interfaces.\+/inet_interfaces = loopback-only/' /etc/postfix/main.cf
RUN echo 'default_transport = error\nrelay_transport = error' >> /etc/postfix/main.cf
RUN chmod u+s /usr/sbin/useradd

COPY www/ /var/www/html/

RUN chmod 0777 /var/www/html/db /var/www/html/db/db.db

CMD service postfix start ; exec apache2-foreground
