FROM ubuntu

RUN apt-get -y update && DEBIAN_FRONTEND="noninteractive" TZ="Asia/Kolkata" apt-get -y -q install nginx apache2-utils spawn-fcgi fcgiwrap python3 python3-pip

EXPOSE 80/tcp

RUN ["pip3", "install", "pandas"]

COPY docker-entrypoint.sh /

RUN ["chmod", "+x", "/docker-entrypoint.sh"]

COPY flag.txt /

COPY static /static/

COPY config/nginx.conf /etc/nginx/

COPY src/ /panda

ENTRYPOINT ["/docker-entrypoint.sh"]   
