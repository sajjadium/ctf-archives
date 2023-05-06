FROM debian:latest

RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi-py3 \
    build-essential \
    python3 \
    python3-dev\
    python3-pip

COPY ./stuff/app.conf /etc/apache2/sites-available/app.conf
COPY ./stuff/app.py /var/www/app/app.py

RUN a2ensite app
RUN a2enmod headers

RUN a2dissite 000-default.conf
RUN a2ensite app.conf

RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
    ln -sf /proc/self/fd/1 /var/log/apache2/error.log

RUN pip install flask requests

WORKDIR /var/www/app
EXPOSE 80
CMD  /usr/sbin/apache2ctl -D FOREGROUND
