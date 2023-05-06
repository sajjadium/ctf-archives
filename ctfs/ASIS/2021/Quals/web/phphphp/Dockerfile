FROM php:7.4.25-fpm

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade -y 
RUN apt install -y python3 xinetd

COPY ./app /app
COPY ./app/xinetd.conf /etc/xinetd.d/service
COPY ./flag /flag
RUN find /usr/local/lib/ -name "*.php" -type f -delete

RUN chmod +x /app/app.py /app/run.py
RUN chmod 777 /app/request
RUN useradd -m www
CMD ["/usr/sbin/xinetd","-dontfork"]