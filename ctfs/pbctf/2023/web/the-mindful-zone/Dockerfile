FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -y --no-install-recommends install software-properties-common mysql-server apache2 php libapache2-mod-php php-mysql && \
    add-apt-repository ppa:iconnor/zoneminder-1.36 && \
    service mysql start && \
    apt-get install -y --no-install-recommends zoneminder=1.36.32-bionic1 && \
    apt-get clean

RUN sed -i 's/\[mysqld\]/[mysqld\]\nsql_mode = NO_ENGINE_SUBSTITUTION\n/' /etc/mysql/mysql.conf.d/mysqld.cnf

COPY flag.txt /flag.txt
COPY entrypoint.sh /entrypoint.sh
COPY readflag /readflag
RUN chmod 700 /flag.txt && chmod +sx /readflag

CMD bash -C '/entrypoint.sh';'bash'

# docker build -t mind .
# docker run --rm -it -p 8080:80 mind
# visit 127.0.0.1:8080/zm/